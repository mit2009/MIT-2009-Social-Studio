"""Audio-only E01/E02/E04 pilot, reusing installed instruments. No feedback input."""

import argparse
import json
import platform
import subprocess
import sys
import time
from pathlib import Path

import librosa
import numpy as np
from scipy.ndimage import median_filter

from mit2009_studio import media
from mit2009_studio.melody import extract_notes
from mit2009_studio.providers.arranged import InstrumentBank, close_pitch, harmonize, room, runtime

METHOD = "audio-only-house-band-pilot-v1"
KINDS = {"faithful": "Follow the phrase", "groove": "Find the groove", "riff": "Play with the idea"}


def write_json(path, data):
    Path(path).write_text(json.dumps(data, indent=2, allow_nan=False) + "\n")


def expression(audio, notes, rate):
    """Measured level and pitch cues, not an emotional-story classifier."""
    mono = np.asarray(audio).mean(axis=1) if np.asarray(audio).ndim == 2 else np.asarray(audio)
    levels = []
    for n in notes:
        part = mono[round(n["start"] * rate) : round((n["start"] + n["duration"]) * rate)]
        width = max(1, round(0.02 * rate))
        power = [np.mean(part[i : i + width] ** 2) for i in range(0, len(part), width)]
        levels.append(float(10 * np.log10(max(float(np.percentile(power, 75)), 1e-10))))
    levels = median_filter(np.asarray(levels), size=3, mode="nearest")
    # Fixed dB mapping retains contrast without inventing a crescendo in flat audio.
    gain = np.clip(0.8 * (levels - np.percentile(levels, 90)), -16, 2)
    pitches = np.array([n["midi"] for n in notes], dtype=float)
    pitch_span = float(np.ptp(pitches))
    register = (pitches - pitches.min()) / pitch_span if pitch_span > 2 else np.full(len(notes), 0.5)
    # This alternate cue is allowed to disagree with raw phone loudness.
    gesture = np.clip(0.7 * gain + 0.3 * (register - 0.5) * 10, -16, 2)
    return [
        {
            "source_level_dbfs": round(float(level), 4),
            "gain_db": round(float(g), 4),
            "gesture_gain_db": round(float(h), 4),
        }
        for level, g, h in zip(levels, gain, gesture, strict=True)
    ]


def analyze(source):
    info = media.probe(source)
    seconds = float(info["format"]["duration"])
    if not 0.2 <= seconds <= 60:
        raise ValueError("This bounded trial accepts recordings between 0.2 and 60 seconds.")
    score = extract_notes(source, seconds)
    audio = media.read_audio(source, seconds)
    cues = expression(audio, score["notes"], media.SAMPLE_RATE)
    notes = [
        {**n, **cue, "source_note_id": i} for i, (n, cue) in enumerate(zip(score["notes"], cues, strict=True))
    ]
    origin = notes[0]["start"]
    end = max(n["start"] + n["duration"] for n in notes)
    phrases = [0]
    for i in range(1, len(notes)):
        if notes[i]["start"] - (notes[i - 1]["start"] + notes[i - 1]["duration"]) > 0.45:
            phrases.append(i)
    peak = max(notes, key=lambda n: n["source_level_dbfs"])
    return {
        "method": METHOD,
        "source_sha256": media.digest(source),
        "source_duration_seconds": seconds,
        "notes": notes,
        "source_origin_seconds": origin,
        "source_end_seconds": end,
        "phrase_start_note_ids": phrases,
        "level_peak_source_seconds": peak["start"],
        "level_peak_trimmed_seconds": round(peak["start"] - origin, 6),
        "median_pitch_confidence": float(np.median([n["confidence"] for n in notes])),
        "limitations": [
            "Quantized monophonic pitches; octave/split errors possible.",
            "Phone loudness is not identical to musical intent.",
            "Pitch/register and level cues are hypotheses, not story comprehension.",
        ],
        "source_audio_in_output": False,
    }


def make_plan(sketch, kind, seed, duration=15.0):
    if kind not in KINDS or duration < 3:
        raise ValueError("Unknown musician or project duration too short.")
    rng = np.random.default_rng(seed)
    origin = sketch["source_origin_seconds"]
    span = sketch["source_end_seconds"] - origin
    end = duration - 0.55
    scale = (end - 0.02) / span
    mapped = [
        {
            **n,
            "source_start": n["start"],
            "start": 0.02 + (n["start"] - origin) * scale,
            "duration": n["duration"] * scale,
            "transform": "uniform duration fit",
        }
        for n in sketch["notes"]
    ]
    beat = 0.5
    if kind == "groove":
        previous = -0.04
        for n in mapped:
            target = round(n["start"] / (beat / 2)) * (beat / 2)
            if seed % 2 == 0 and round(target / (beat / 2)) % 2:
                target += beat * 0.1
            n["start"] = max(previous + 0.03, 0.02, 0.5 * n["start"] + 0.5 * target)
            previous = n["start"]
            n["transform"] = "halfway to eighth-note groove grid"
        for i, n in enumerate(mapped):
            next_start = mapped[i + 1]["start"] if i + 1 < len(mapped) else end
            n["duration"] = max(0.025, min(n["duration"], next_start - n["start"] - 0.012, end - n["start"]))
    elif kind == "riff":
        opening_end = duration * 0.57
        factor = (opening_end - 0.02) / (end - 0.02)
        for n in mapped:
            n["start"] = 0.02 + (n["start"] - 0.02) * factor
            n["duration"] *= factor
            n["transform"] = "literal opening, time compressed"
        reliable = [n for n in sketch["notes"] if n["confidence"] >= 0.5]
        motif = (reliable or sketch["notes"])[:3]
        motif_span = max(n["start"] + n["duration"] for n in motif) - motif[0]["start"]
        section = (end - opening_end - 0.55) / 3
        for repeat in range(3):
            for n in motif:
                interval = n["midi"] - motif[0]["midi"]
                inverted = seed % 2 == 0 and repeat == 1
                pitch = motif[0]["midi"] + (-interval if inverted else interval) + [12, 14, 17][repeat]
                while pitch > 84:
                    pitch -= 12
                start = (
                    opening_end
                    + 0.12
                    + repeat * section
                    + (n["start"] - motif[0]["start"]) / motif_span * section * 0.72
                )
                mapped.append(
                    {
                        **n,
                        "source_start": n["start"],
                        "start": start,
                        "duration": max(0.09, n["duration"] / motif_span * section * 0.6),
                        "midi": pitch,
                        "transform": "motif inversion" if inverted else "motif sequence",
                    }
                )
        n = sketch["notes"][-1]
        mapped.append(
            {
                **n,
                "source_start": n["start"],
                "start": end - 0.38,
                "duration": 0.38,
                "transform": "return to source final pitch",
            }
        )
    mapped.sort(key=lambda n: n["start"])
    events = []
    for i, n in enumerate(mapped):
        next_start = mapped[i + 1]["start"] if i + 1 < len(mapped) else end + 0.01
        length = max(0.025, min(max(n["duration"], 0.1), next_start - n["start"] - 0.008, end - n["start"]))
        events.append(
            {
                "instrument": "guitar",
                "midi": n["midi"],
                "start": round(n["start"], 6),
                "duration": round(length, 6),
                "velocity": int(85 + rng.integers(-2, 3)),
                "gain_db": n["gain_db"] if kind == "faithful" else n["gesture_gain_db"],
                "role": "melody",
                "pan": -0.06,
                "source_note_id": n["source_note_id"],
                "source_start": n["source_start"],
                "transform": n["transform"],
            }
        )
    chords = harmonize(mapped, end, beat * 4)

    def cue(at):
        return float(
            np.interp(
                at,
                [n["start"] for n in mapped],
                [n["gain_db"] if kind == "faithful" else n["gesture_gain_db"] for n in mapped],
            )
        )

    def add(instrument, midi, at, length, velocity, part, pan=0):
        if at >= end - 0.06:
            return
        events.append(
            {
                "instrument": instrument,
                "midi": int(midi),
                "start": round(max(0.02, at), 6),
                "duration": round(min(length, end - max(0.02, at)), 6),
                "velocity": velocity,
                "gain_db": round(cue(at) * 0.85, 4),
                "role": "accompaniment",
                "pan": pan,
                "transform": part,
            }
        )

    # Accompaniment is composed from the inferred notes; no audio-bed assets.
    for c in chords:
        root, at = c["root"], c["start"]
        bass = close_pitch(root, 40, 32, 48)
        for b in range(4):
            t = at + b * beat
            if kind == "faithful":
                if b in (0, 2):
                    add("bass", bass, t, beat * 0.75, 55, "sparse bass")
                if b == 3:
                    add(
                        "violin_pizz",
                        close_pitch(root + 7, 65, 55, 78),
                        t + 0.25,
                        0.14,
                        40,
                        "light answer",
                        0.3,
                    )
            else:
                add("club_kick", 36, t, 0.17, 70 if b % 2 == 0 else 58, "pulse")
                add("hat", 42, t + beat * 0.5, 0.07, 44, "offbeat", 0.25)
                if b % 2:
                    add("clap", 38, t, 0.13, 57, "backbeat", -0.1)
                bp = bass if b % 2 == 0 else close_pitch(root + 7, bass, 32, 50)
                add("bass", bp, t + beat * 0.5, beat * 0.34, 62, "syncopated bass", 0.08)
                if b in (1, 3):
                    for j, interval in enumerate(c["intervals"]):
                        add(
                            "violin_pizz",
                            close_pitch(root + interval, 59 + j * 3, 50, 77),
                            t + 0.25 + j * 0.006,
                            0.12,
                            39,
                            "short harmony",
                            -0.25,
                        )
    events.sort(key=lambda e: e["start"])
    if not all(
        0 <= e["start"] < duration and 0 < e["duration"] <= duration - e["start"] + 1e-6 for e in events
    ):
        raise ValueError("An event falls outside the project duration.")
    return {
        "method": METHOD,
        "kind": kind,
        "name": KINDS[kind],
        "seed": seed,
        "duration_seconds": duration,
        "events": events,
        "chords": chords,
        "source_time_fit": {
            "source_origin_seconds": origin,
            "source_span_seconds": span,
            "uniform_scale_before_transform": scale,
        },
        "policy": "Faithful preserves pitch/order and relative timing proportions, uniformly fitted to duration; groove shifts timing; riff develops source fragments.",
        "notes": "Pilot adaptation of E01/E02/E04, with sparse/beat accompaniment; not the original solo-renderer control.",
        "source_audio_in_output": False,
    }


def render(plan, folder, installed):
    folder.mkdir()
    count = round(plan["duration_seconds"] * media.SAMPLE_RATE)
    tracks = {key: np.zeros((count, 2)) for key in ("melody", "accompaniment")}
    bank = InstrumentBank(installed)
    for e in plan["events"]:
        voice = bank.voice(e) * 10 ** (e["gain_db"] / 20)
        voice *= np.array([np.sqrt(1 - e["pan"]), np.sqrt(1 + e["pan"])])
        start = round(e["start"] * media.SAMPLE_RATE)
        length = min(len(voice), count - start)
        tracks[e["role"]][start : start + length] += voice[:length]
    lead_rms = np.sqrt(np.mean(tracks["melody"] ** 2))
    band_rms = np.sqrt(np.mean(tracks["accompaniment"] ** 2))
    tracks["accompaniment"] *= min(
        1.0, (0.4 if plan["kind"] == "faithful" else 0.7) * lead_rms / max(band_rms, 1e-9)
    )
    output = room(sum(tracks.values()), 0.30, 0.025, plan["seed"])
    scale = min(1.0, 0.90 / max(float(np.max(np.abs(output))), 1e-9))
    output *= scale
    output[-4800:] *= np.linspace(1, 0, 4800)[:, None]
    assert np.isfinite(output).all() and np.max(np.abs(output)) < 1
    raw = folder / "unmastered.wav"
    media.write_audio(raw, output)
    for name, track in tracks.items():
        media.write_audio(folder / (name + "-stem.wav"), track * scale)
    final = folder / "audio.wav"
    mastering = media.master_audio(raw, final)
    check = media.verify_output(final, plan["duration_seconds"], audio=True)
    y = media.read_audio(final, plan["duration_seconds"])
    assert y.shape == (count, 2) and np.isfinite(y).all() and np.max(np.abs(y)) < 1
    active = np.flatnonzero(np.max(np.abs(y), axis=1) > 0.001)
    first = float(active[0] / media.SAMPLE_RATE)
    assert first < 0.15
    meter = subprocess.run(
        [
            media.executable("ffmpeg"),
            "-hide_banner",
            "-nostdin",
            "-i",
            str(final),
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
    plan["samples_used"] = bank.used
    write_json(folder / "arrangement.json", plan)
    check.update(
        {
            "first_audible_seconds": first,
            "last_audible_seconds": float(active[-1] / media.SAMPLE_RATE),
            "measured_lufs": stats["input_i"],
            "true_peak_dbfs": stats["input_tp"],
            "mastering": mastering,
            "output_sha256": media.digest(final),
            "source_audio_in_output": False,
            "listening_review": None,
        }
    )
    write_json(folder / "checks.json", check)
    return check


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--seed", type=int, default=2009)
    parser.add_argument("--config", type=Path, help="Project settings, not a student control")
    args = parser.parse_args()
    config = json.loads(args.config.read_text()) if args.config else {"duration_seconds": 15.0}
    if set(config) != {"duration_seconds"}:
        raise ValueError("Only the project duration setting is accepted.")
    duration = float(config["duration_seconds"])
    if not np.isfinite(duration) or not 3 <= duration <= 60:
        raise ValueError("Project duration must be between 3 and 60 seconds.")
    installed = runtime()
    if installed is None:
        raise ValueError("The existing local instrument bank is unavailable; no automatic download.")
    args.output.mkdir(parents=True, exist_ok=False)
    before = media.digest(args.source)
    started = time.perf_counter()
    sketch = analyze(args.source)
    write_json(args.output / "analysis.json", sketch)
    print(
        json.dumps(
            {
                "analysis_ready": True,
                "notes": len(sketch["notes"]),
                "level_peak_source_seconds": sketch["level_peak_source_seconds"],
            }
        ),
        flush=True,
    )
    results = {}
    for kind in KINDS:
        results[kind] = render(make_plan(sketch, kind, args.seed, duration), args.output / kind, installed)
        print(json.dumps({"ready": kind, "seconds": round(time.perf_counter() - started, 2)}), flush=True)
    assert media.digest(args.source) == before
    assert len({r["output_sha256"] for r in results.values()}) == 3
    write_json(
        args.output / "run.json",
        {
            "method": METHOD,
            "source_sha256": before,
            "source_unchanged": True,
            "configuration": config,
            "seed": args.seed,
            "outputs": results,
            "analysis_sha256": media.digest(args.output / "analysis.json"),
            "script_sha256": media.digest(__file__),
            "instrument_catalog_sha256": installed["catalog_sha256"],
            "generation_seconds": round(time.perf_counter() - started, 3),
            "paid_api_calls": 0,
            "network_calls": 0,
            "feedback_text_or_manual_curve_input": False,
            "environment": {
                "python": sys.version,
                "platform": platform.platform(),
                "librosa": librosa.__version__,
                "numpy": np.__version__,
            },
            "listening_review": None,
            "limitation": "Seen development recording. Input independence does not establish generalization or perceptual quality.",
        },
    )


if __name__ == "__main__":
    main()
