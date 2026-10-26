"""One local MRT2 quality audition using automatically extracted note controls."""

import argparse
import json
import os
import subprocess
import time
from pathlib import Path

import numpy as np

from experiments.audio_only import analyze, write_json
from mit2009_studio import media

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / "data/runtime"
CODE_COMMIT = "694a545e4ba0b88bf1150137b129582166d3e07f"
STYLE = "instrumental funk band, expressive electric guitar, warm electric bass, dry punchy live drums, rhythmic brass"

PROFILES = {
    "benchmark": {"note_guidance": 2.0, "lead_register": False},
    "closer": {"note_guidance": 4.0, "lead_register": False},
    "lead": {"note_guidance": 4.0, "lead_register": True},
}


def lead_octave_shift(notes):
    """Choose a whole-octave placement for an exposed instrumental lead."""
    pitches = np.array([n["midi"] for n in notes])
    choices = [
        shift
        for shift in (-24, -12, 0, 12, 24)
        if pitches.min() + shift >= 0 and pitches.max() + shift <= 127
    ]

    def cost(shift):
        low, high = pitches.min() + shift, pitches.max() + shift
        return 5 * max(0, 55 - low) ** 2 + 5 * max(0, high - 86) ** 2 + abs(np.median(pitches) + shift - 70)

    return min(choices, key=cost)


def note_controls(sketch, duration=15.0, profile="benchmark"):
    """Partial note control: lead register constrained, other registers available."""
    setting = PROFILES[profile]
    frames = round((duration + 1.0) * 25)
    original_notes = sketch["notes"]
    shift = lead_octave_shift(original_notes) if setting["lead_register"] else 0
    notes = [{**n, "source_midi": n["midi"], "midi": n["midi"] + shift} for n in original_notes]
    origin = sketch["source_origin_seconds"]
    span = sketch["source_end_seconds"] - origin
    fit = (duration - 1.04) / span
    low, high = min(n["midi"] for n in notes), max(n["midi"] for n in notes)
    constrained_low = max(0, low - 3) if setting["lead_register"] else low
    constrained_high = min(127, max(84, high + 12)) if setting["lead_register"] else high
    roll = np.full((frames, 128), -1, dtype=np.int32)
    roll[:, constrained_low : constrained_high + 1] = 0
    mapping = []
    previous_end = None
    for n in notes:
        start = 0.04 + (n["start"] - origin) * fit
        end = 0.04 + (n["start"] + n["duration"] - origin) * fit
        left = round(start * 25)
        right = max(left + 1, round(end * 25))
        roll[left:right, n["midi"]] = 1
        # A continuous sung pitch change is not necessarily a fresh picked attack.
        # Let the performer choose its articulation for connected notes.
        connected = previous_end is not None and n["start"] - previous_end < 0.06
        onset_state = 3 if connected else 2
        roll[left, n["midi"]] = onset_state
        previous_end = n["start"] + n["duration"]
        mapping.append(
            {
                "source_note_id": n["source_note_id"],
                "source_start": n["start"],
                "source_duration": n["duration"],
                "midi": n["midi"],
                "source_midi": n["source_midi"],
                "model_start": left / 25,
                "model_end": right / 25,
                "onset_state": onset_state,
            }
        )
    return (
        roll,
        mapping,
        {
            "source_origin": origin,
            "uniform_fit": fit,
            "profile": profile,
            "octave_shift_semitones": shift,
            "constrained_pitch_range": [constrained_low, constrained_high],
            "other_pitches": "masked / performer may add accompaniment",
            "frame_rate": 25,
            "source_dynamics": "retained in analysis but not encoded by this MIDI-only trial",
        },
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--seed", type=int, default=2009)
    parser.add_argument("--profile", choices=PROFILES, default="benchmark")
    parser.add_argument("--style", default=STYLE, help="Internal experiment preset; not a student input")
    args = parser.parse_args()
    assert args.source.is_file()
    commit = subprocess.check_output(
        ["git", "-C", str(RUNTIME / "magenta-realtime"), "rev-parse", "HEAD"], text=True
    ).strip()
    assert commit == CODE_COMMIT
    assets = json.loads((RUNTIME / "mrt2-assets/assets.json").read_text())
    for entry in assets["files"]:
        path = RUNTIME / "mrt2-assets" / entry["rfilename"]
        assert path.stat().st_size == entry["size"] and media.digest(path) == entry["lfs"]["sha256"]
    folder = args.output.resolve()
    folder.mkdir(parents=True, exist_ok=False)
    source_hash = media.digest(args.source)
    started = time.perf_counter()
    sketch = analyze(args.source)
    write_json(folder / "analysis.json", sketch)
    roll, mapping, policy = note_controls(sketch, profile=args.profile)
    np.save(folder / "note-control.npy", roll)
    write_json(folder / "source-map.json", {"notes": mapping, "policy": policy})
    job = {
        "output_folder": str(folder),
        "assets_root": str(RUNTIME / "mrt2-assets"),
        "style": args.style,
        "frames": len(roll),
        "seed": args.seed,
        "project_duration": 15.0,
        "profile": args.profile,
        "cfg_scales": {"musiccoca": 3.0, "notes": PROFILES[args.profile]["note_guidance"], "drums": 1.0},
    }
    write_json(folder / "job.json", job)
    env = {
        **os.environ,
        "HF_HUB_OFFLINE": "1",
        "HF_HUB_DISABLE_TELEMETRY": "1",
        "TOKENIZERS_PARALLELISM": "false",
    }
    print("Rendering one local note-conditioned performance", flush=True)
    with (folder / "model.log").open("wb") as log:
        subprocess.run(
            [
                str(RUNTIME / "mrt2-env/bin/python"),
                str(ROOT / "experiments/mrt2_worker.py"),
                str(folder / "job.json"),
            ],
            check=True,
            env=env,
            stdout=log,
            stderr=subprocess.STDOUT,
            timeout=600,
        )
    raw = media.read_audio(folder / "model-raw.wav", 16.0)
    assert np.isfinite(raw).all() and np.max(np.abs(raw)) > 0.0001
    opening = media.playback_start(raw)
    y = media.fit_audio(raw[opening:], 15 * 48000)
    # Transparent boundary treatment for a streaming model, not a claimed cadence.
    y[:240] *= np.linspace(0, 1, 240)[:, None]
    y[-9600:] *= np.linspace(1, 0, 9600)[:, None]
    gain = min(1.0, 0.90 / float(np.max(np.abs(y))))
    media.write_audio(folder / "prepared.wav", y * gain)
    mastering = media.master_audio(folder / "prepared.wav", folder / "audio.wav")
    check = media.verify_output(folder / "audio.wav", 15.0, audio=True)
    exported = media.read_audio(folder / "audio.wav", 15.0)
    assert exported.shape == (720000, 2) and np.isfinite(exported).all() and np.max(np.abs(exported)) < 1
    active = np.flatnonzero(np.max(np.abs(exported), axis=1) > 0.001)
    first = float(active[0] / 48000)
    assert first < 0.15, first
    meter = subprocess.run(
        [
            media.executable("ffmpeg"),
            "-hide_banner",
            "-nostdin",
            "-i",
            str(folder / "audio.wav"),
            "-af",
            "loudnorm=I=-18:TP=-1:LRA=11:print_format=json",
            "-f",
            "null",
            "-",
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    stats = json.loads(meter.stderr[meter.stderr.rfind("{") : meter.stderr.rfind("}") + 1])
    assert float(stats["input_tp"]) <= -1
    assert media.digest(args.source) == source_hash
    check.update(
        {
            "first_audible_seconds": first,
            "measured_lufs": stats["input_i"],
            "true_peak_dbfs": stats["input_tp"],
            "mastering": mastering,
            "opening_removed_seconds": opening / 48000,
            "end_fade_seconds": 0.2,
            "raw_signal_gain": gain,
            "source_unchanged": True,
            "source_sha256": source_hash,
            "output_sha256": media.digest(folder / "audio.wav"),
            "script_sha256": media.digest(__file__),
            "worker_sha256": media.digest(ROOT / "experiments/mrt2_worker.py"),
            "runtime_commit": commit,
            "weights_revision": assets["revision"],
            "elapsed_seconds": time.perf_counter() - started,
            "paid_api_calls": 0,
            "original_voice_mixed_in": False,
            "model_may_generate_vocal_like_sounds": True,
            "profile": args.profile,
            "cfg_scales": job["cfg_scales"],
            "style": job["style"],
            "note_adherence": "unverified by listening",
            "sound_quality": "awaiting listening; different renderer is not proof of improvement",
            "review": None,
        }
    )
    write_json(folder / "checks.json", check)
    write_json(
        folder / "attribution.json",
        {
            "model": "Magenta RealTime 2 base",
            "author": "Google DeepMind / Google LLC",
            "source": "https://github.com/magenta/magenta-realtime",
            "code_license": "Apache-2.0",
            "weights_license": "CC-BY-4.0 plus MODEL.md usage terms",
            "runtime_commit": commit,
            "weights_revision": assets["revision"],
            "changes": "New note-control adapter and local output trimming, constant-gain mastering and 200ms ending fade.",
        },
    )
    print(json.dumps({"audio": str(folder / "audio.wav"), "checks": check}, indent=2), flush=True)


if __name__ == "__main__":
    main()
