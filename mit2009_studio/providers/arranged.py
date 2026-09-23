"""Note-preserving arrangements performed with recorded CC0 instruments."""

import hashlib
import json
from fractions import Fraction
from pathlib import Path

import numpy as np
import soundfile as sf
from scipy.signal import butter, fftconvolve, resample_poly, sosfilt

from .. import media
from . import AudioResult

ROOT = Path(__file__).resolve().parents[2]
CATALOG = ROOT / "mit2009_studio/instruments.json"
SAMPLES = ROOT / "data/instruments"
PROVIDER = "local-recorded-ensembles"
MODEL = "Local instruments · phrase arranger 2"
STYLES = [
    {
        "id": "dance",
        "family": "dance",
        "mode": "ensemble",
        "name": "Club bounce",
        "feel": "upbeat",
        "color": "#1f78bb",
        "description": "Your melody becomes a wide plucked-synth hook, with offbeat bass and a punchy club beat.",
    },
    {
        "id": "chamber",
        "family": "chamber",
        "mode": "ensemble",
        "name": "Indie dance",
        "feel": "upbeat",
        "color": "#924c9e",
        "description": "Bright electric guitar, plucked-string replies and a springy dance beat carry your phrase.",
    },
    {
        "id": "jazz",
        "family": "jazz",
        "mode": "ensemble",
        "name": "Brass bounce",
        "feel": "upbeat",
        "color": "#ee3a80",
        "description": "A bold trumpet hook, short brass punches and a syncopated bass groove answer your phrase.",
    },
]


def runtime():
    ready = SAMPLES / "ready.json"
    if not ready.is_file():
        return None
    info = json.loads(ready.read_text())
    if info["catalog_sha256"] != media.digest(CATALOG):
        return None
    catalog = json.loads(CATALOG.read_text())
    if not all(
        (SAMPLES / e["file"]).is_file() and (SAMPLES / e["file"]).stat().st_size == e["bytes"]
        for e in catalog["samples"]
    ):
        return None
    return {"folder": SAMPLES, "catalog": catalog, "catalog_sha256": info["catalog_sha256"]}


def melody_notes(score):
    """Keep all accepted notes and their relative timing; only remove opening wait."""
    notes = score["notes"]
    if not notes:
        raise ValueError("Check a musical phrase before arranging it.")
    origin = notes[0]["start"]
    return [{**n, "start": round(n["start"] - origin, 6)} for n in notes]


def harmonize(notes, end, bar):
    """Fit quiet triads to each phrase window, penalizing abrupt chord movement."""
    chords = [(root, intervals) for root in range(12) for intervals in ((0, 4, 7), (0, 3, 7))]
    count = max(1, int(np.ceil(end / bar)))
    local = np.zeros((count, len(chords)))
    for k in range(count):
        for j, (root, intervals) in enumerate(chords):
            pcs = {(root + i) % 12 for i in intervals}
            for n in notes:
                overlap = max(0, min(n["start"] + n["duration"], (k + 1) * bar) - max(n["start"], k * bar))
                pc = n["midi"] % 12
                local[k, j] += overlap * (2.5 if pc in pcs else -0.4)
    transition = np.zeros((len(chords), len(chords)))
    for i, (r1, a) in enumerate(chords):
        for j, (r2, b) in enumerate(chords):
            shared = len({(r1 + x) % 12 for x in a} & {(r2 + x) % 12 for x in b})
            distance = min((r1 - r2) % 12, (r2 - r1) % 12)
            transition[i, j] = 0.16 * shared - 0.025 * distance
    best = local[0].copy()
    parents = []
    for row in local[1:]:
        candidates = best[:, None] + transition
        parents.append(candidates.argmax(axis=0))
        best = candidates.max(axis=0) + row
    chosen = [int(best.argmax())]
    for parent in reversed(parents):
        chosen.append(int(parent[chosen[-1]]))
    chosen.reverse()
    return [
        {"start": round(k * bar, 6), "root": chords[j][0], "intervals": list(chords[j][1])}
        for k, j in enumerate(chosen)
    ]


def close_pitch(pc, around, low, high):
    return min((p for p in range(low, high + 1) if p % 12 == pc % 12), key=lambda p: abs(p - around))


def arrange(score, style, seed, duration=15, *, feel="original"):
    if feel == "upbeat":
        from .upbeat import arrange_upbeat

        return arrange_upbeat(score, style, seed, duration)
    notes = melody_notes(score)
    rng = np.random.default_rng(seed)
    end = max(n["start"] + n["duration"] for n in notes)
    # Accompaniment follows a pulse while the accepted, possibly rubato lead stays intact.
    beat = {"chamber": 0.58, "jazz": 0.54, "dance": 0.48}[style]
    bar = 4 * beat
    chords = harmonize(notes, end, bar)
    events = []

    def add(instrument, pitch, start, length, velocity, role="accompaniment", pan=0):
        if start >= duration or (role != "melody" and start >= duration - 0.4):
            return
        events.append(
            {
                "instrument": instrument,
                "midi": int(pitch),
                "start": round(max(0, start), 6),
                "duration": round(min(length, duration - max(0, start)), 6),
                "velocity": int(np.clip(velocity, 20, 110)),
                "role": role,
                "pan": pan,
            }
        )

    for i, n in enumerate(notes):
        gap = notes[i + 1]["start"] - n["start"] if i + 1 < len(notes) else 1
        strength = 76 + 7 * np.sin(i * 0.8) + (5 if gap > 0.5 else 0) + rng.normal(0, 2)
        # Acoustic key release allows each note to breathe without altering onset or pitch.
        length = min(max(n["duration"], 0.16), max(0.08, gap - 0.015))
        add("piano", n["midi"], n["start"], length, strength, "melody", -0.08)

    previous_violin = 67
    previous_voicing = [48, 55, 60]
    for k, chord in enumerate(chords):
        start, root, intervals = chord["start"], chord["root"], chord["intervals"]
        length = min(bar, end - start + 0.1)
        pcs = [(root + x) % 12 for x in intervals]
        bass = close_pitch(root, 41, 34, 48)
        voicing = sorted(close_pitch(pc, previous_voicing[i], 45, 65) for i, pc in enumerate(pcs))
        previous_voicing = voicing
        if style == "chamber":
            add("cello", bass, start + 0.02, length - 0.08, 47 + k % 3 * 3, pan=0.28)
            violin = close_pitch(pcs[1 if k % 2 == 0 else 2], previous_violin, 60, 79)
            previous_violin = violin
            add("violin", violin, start + 0.05, length * 0.87, 42 + k % 3 * 4, pan=-0.27)
            # Broken piano harmony occupies space below the melody, sparsely.
            for j, pitch in enumerate(voicing[:2]):
                at = start + beat * (0.6 + j * 1.5)
                add("piano", pitch - (12 if pitch > 54 else 0), at, beat * 1.4, 39 + j * 3, pan=-0.08)
        else:
            for b in range(4):
                at = start + b * beat
                if at >= end:
                    break
                # Root/fifth/bass approach, tied to this phrase's fitted harmony.
                bp = bass if b in (0, 2) else close_pitch(pcs[2], bass, 30, 50)
                if b == 3 and k + 1 < len(chords):
                    target = close_pitch(chords[k + 1]["root"], bp, 32, 48)
                    bp = target + (1 if bp > target else -1)
                add(
                    "bass" if style == "jazz" else "sub",
                    bp,
                    at + rng.uniform(0, 0.012),
                    beat * 0.76,
                    67 if b % 2 == 0 else 55,
                    pan=0.08,
                )
                add("kick", 36, at, 0.38, 66 if style == "dance" else 26, pan=0)
                add(
                    "hat",
                    42,
                    at + beat * (0.5 if style == "dance" else 0.64),
                    0.15,
                    42 if style == "dance" else 30,
                    pan=0.23,
                )
                if b % 2:
                    add("snare", 38, at + 0.008, 0.27, 73 if style == "dance" else 36, pan=-0.12)
            offsets = [0.5, 2.5] if style == "dance" else [0.65, 2.8]
            for off in offsets:
                at = start + off * beat
                if at >= end:
                    continue
                for j, p in enumerate(voicing):
                    add("piano", p, at + j * 0.009, beat * 0.60, 43 + rng.integers(-3, 4), pan=-0.08)
    # A quiet closing answer after the phrase; leave time for acoustic decay.
    cadence = min(end + 0.30, duration - 1.15)
    if cadence > end + 0.05:
        root = chords[-1]["root"]
        for j, interval in enumerate(chords[-1]["intervals"]):
            add(
                "piano",
                close_pitch(root + interval, 52 + j * 4, 42, 70),
                cadence + j * 0.025,
                0.45,
                48 - j * 4,
                pan=-0.08,
            )
    return {
        "version": 1,
        "style": style,
        "melody_notes": notes,
        "chords": chords,
        "events": sorted(events, key=lambda e: e["start"]),
        "accompaniment_bpm": round(60 / beat, 2),
        "note": "Lead pitch/order/onsets preserved; harmony and accompaniment are heuristic, not human-approved.",
    }


class InstrumentBank:
    def __init__(self, installed):
        self.folder = installed["folder"]
        self.entries = installed["catalog"]["samples"]
        self.cache = {}
        self.counts = {}
        self.used = {}

    def voice(self, event):
        instrument, note, velocity = event["instrument"], event["midi"], event["velocity"]
        length = event["duration"]
        from .electronic import VOICES, voice

        if instrument in VOICES:
            return voice(event)
        if instrument == "sub":
            t = np.arange(round((length + 0.08) * media.SAMPLE_RATE)) / media.SAMPLE_RATE
            phase = 2 * np.pi * (440 * 2 ** ((note - 69) / 12)) * t
            a = np.sin(phase) + 0.15 * np.sin(2 * phase)
            a *= np.minimum(1, t / 0.008) * np.minimum(1, np.maximum(0, (length + 0.08 - t) / 0.08))
            return np.column_stack((a, a)) * 0.18 * (velocity / 90)
        candidates = [e for e in self.entries if e["instrument"] == instrument]

        def distance(e):
            return (abs((e["midi"] if e["midi"] is not None else note) - note), abs(e["velocity"] - velocity))

        nearest = min(map(distance, candidates))
        candidates = [e for e in candidates if distance(e) == nearest]
        self.counts[instrument] = self.counts.get(instrument, -1) + 1
        entry = candidates[self.counts[instrument] % len(candidates)]
        key = (entry["file"], note)
        if key not in self.cache:
            path = self.folder / entry["file"]
            data = path.read_bytes()
            blob = hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()
            if blob != entry["git_blob"]:
                raise ValueError("A recorded instrument changed. Run the instrument installer again.")
            audio, rate = sf.read(path, dtype="float32", always_2d=True)
            if audio.shape[1] == 1:
                audio = np.repeat(audio, 2, axis=1)
            shift = 2 ** ((note - entry["midi"]) / 12) if entry["midi"] is not None else 1
            ratio = Fraction(media.SAMPLE_RATE / rate / shift).limit_denominator(1000)
            audio = resample_poly(audio[:, :2], ratio.numerator, ratio.denominator, axis=0)
            onset = media.playback_start(audio)
            audio = audio[onset:]
            peak = np.max(np.abs(audio))
            if not np.isfinite(audio).all() or peak < 0.0001:
                raise ValueError("An instrument sample is silent or invalid.")
            self.cache[key] = audio / peak
            self.used[entry["file"]] = entry["git_blob"]
        source = self.cache[key]
        release = {
            "piano": 0.48,
            "bass": 0.22,
            "violin": 0.30,
            "cello": 0.34,
            "violin_pizz": 0.18,
            "cello_pizz": 0.23,
            "guitar": 0.20,
            "trumpet": 0.11,
            "trombone": 0.13,
        }.get(instrument, 0.15)
        if event.get("articulation") == "detached" and instrument == "piano":
            release = 0.28
        count = min(len(source), round((length + release) * media.SAMPLE_RATE))
        audio = source[:count].copy()
        t = np.arange(count) / media.SAMPLE_RATE
        attack = 0.065 if instrument in ("violin", "cello") else 0.002
        envelope = np.minimum(1, t / attack) * np.exp(-np.maximum(t - length, 0) * 5 / release)
        envelope *= np.minimum(1, np.maximum(0, (count / media.SAMPLE_RATE - t) / 0.01))
        levels = {
            "piano": 0.40,
            "violin": 0.20,
            "cello": 0.28,
            "violin_pizz": 0.30,
            "cello_pizz": 0.35,
            "guitar": 0.42,
            "trumpet": 0.36,
            "trombone": 0.28,
            "bass": 0.36,
            "kick": 0.43,
            "snare": 0.24,
            "hat": 0.16,
        }
        audio *= (envelope * levels[instrument] * (velocity / 90) ** 1.35)[:, None]
        return audio


def room(audio, seconds, amount, seed):
    rng = np.random.default_rng(seed)
    count = round(seconds * media.SAMPLE_RATE)
    t = np.arange(count) / media.SAMPLE_RATE
    impulse = rng.normal(0, 1, (count, 2)) * np.exp(-6.9 * t / seconds)[:, None]
    impulse = sosfilt(
        butter(2, [250, 6500], btype="bandpass", fs=media.SAMPLE_RATE, output="sos"), impulse, axis=0
    )
    impulse[: round(0.019 * media.SAMPLE_RATE)] = 0
    impulse /= np.sqrt(np.sum(impulse**2, axis=0))[None, :]
    wet = np.column_stack([fftconvolve(audio[:, c], impulse[:, c])[: len(audio)] for c in range(2)])
    return audio + wet * amount


class RecordedEnsembleProvider:
    name = PROVIDER

    def generate(self, request, folder):
        installed = runtime()
        if not installed:
            raise ValueError("The free recorded instruments need their one-time setup.")
        if request.score is None:
            raise ValueError("The accepted melody score is required.")
        score = json.loads(Path(request.score).read_text())
        upbeat = request.style.get("feel") == "upbeat"
        arrangement = arrange(
            score,
            request.style["id"],
            request.seed,
            request.duration,
            feel="upbeat" if upbeat else "original",
        )
        folder = Path(folder)
        bank = InstrumentBank(installed)
        tracks = {
            "melody": np.zeros((round(request.duration * media.SAMPLE_RATE), 2)),
            "accompaniment": np.zeros((round(request.duration * media.SAMPLE_RATE), 2)),
        }
        for event in arrangement["events"]:
            audio = bank.voice(event)
            pan = event["pan"]
            audio *= np.array([np.sqrt(1 - pan), np.sqrt(1 + pan)])
            start = round(event["start"] * media.SAMPLE_RATE)
            count = min(len(audio), len(tracks["melody"]) - start)
            tracks[event["role"]][start : start + count] += audio[:count]
        # Melody stays forward; accompaniment supports it instead of masking it.
        lead_rms = np.sqrt(np.mean(tracks["melody"] ** 2))
        support_rms = np.sqrt(np.mean(tracks["accompaniment"] ** 2))
        target = (
            {"dance": 1.05, "chamber": 0.76, "jazz": 0.85}[request.style["id"]]
            if upbeat
            else 0.70
            if request.style["id"] == "dance"
            else 0.48
        )
        support_gain = min(1.0, target * lead_rms / max(support_rms, 1e-8))
        tracks["accompaniment"] *= support_gain
        combined = sum(tracks.values())
        combined = room(
            combined,
            0.60 if upbeat else 1.3 if request.style["id"] == "chamber" else 0.75,
            0.045 if upbeat else 0.13 if request.style["id"] == "chamber" else 0.065,
            request.seed,
        )
        peak = float(np.abs(combined).max())
        gain = min(1, 0.90 / max(peak, 1e-8))
        combined *= gain
        # A short end safety fade follows a deliberately reserved acoustic tail.
        combined[-4800:] *= np.linspace(1, 0, 4800)[:, None]
        prepared = folder / "performed.wav"
        media.write_audio(prepared, combined)
        for name, audio in tracks.items():
            media.write_audio(folder / f"{name}-stem.wav", audio * gain)
        output = folder / "audio.wav"
        mastering = media.master_audio(prepared, output)
        arrangement["samples_used"] = bank.used
        (folder / "arrangement.json").write_text(json.dumps(arrangement, indent=2))
        return AudioResult(
            output,
            {
                "provider": PROVIDER,
                "model": MODEL,
                "generation_cost_usd": 0,
                "execution": "local recorded-instrument arrangement; no network requests",
                "source_recording_in_model_input": False,
                "source_audio_in_output": False,
                "guide_sha256": media.digest(request.reference),
                "score_sha256": media.digest(request.score),
                "catalog_sha256": installed["catalog_sha256"],
                "license": "CC0-1.0",
                "lead_notes": len(arrangement["melody_notes"]),
                "lead_pitch_and_onsets_preserved": True,
                "arranger_version": arrangement["version"],
                "feel": arrangement.get("feel", "original"),
                "accompaniment_bpm": arrangement["accompaniment_bpm"],
                "support_gain": round(float(support_gain), 4),
                "mastering": mastering,
                "seed": request.seed,
                "listening_review": "Needed: naturalness, melody recognition and musical fit.",
            },
        )
