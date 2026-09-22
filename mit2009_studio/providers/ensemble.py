"""Free local ensemble drafts conditioned only on a wordless melody guide."""

import json
import os
import subprocess
from pathlib import Path

import numpy as np

from .. import media
from . import AudioResult

ROOT = Path(__file__).resolve().parents[2]
PROVIDER = "local-stable-audio-3"
MODEL = "Stable Audio 3 Medium"
STYLES = [
    {
        "id": "dance",
        "family": "dance",
        "mode": "ensemble",
        "name": "Bass-heavy dance",
        "color": "#1f78bb",
        "description": "Your melody as a synth hook, with deep bass and a tight dance groove.",
        "prompt": "TrackType: Music, instrumental bass-heavy dance music. A clear warm synthesizer lead plays the supplied melodic phrase with its recognizable pitch contour and rhythm. Deep controlled sub-bass answers the melody, tight punchy kick, crisp claps, syncopated percussion, spacious polished mix. A compact 15-second arrangement: immediate melodic entrance, a small energetic lift, and a deliberate final cadence. Instrumental only.",
    },
    {
        "id": "chamber",
        "family": "chamber",
        "mode": "ensemble",
        "name": "Chamber trio",
        "color": "#924c9e",
        "description": "Piano, violin and cello share the phrase with warmth and breathing room.",
        "prompt": "TrackType: Music, instrumental acoustic chamber trio of grand piano, solo violin and cello. An expressive violin plays the supplied melodic phrase with its recognizable pitch contour and rhythm. Piano adds restrained moving harmony and a delicate answering figure; warm cello provides a responsive bass line. Realistic acoustic instruments, coordinated phrasing, natural bowing and dynamics, intimate recital hall. A complete 15-second miniature, immediate melody and an intentional quiet final cadence. Instrumental only.",
    },
    {
        "id": "jazz",
        "family": "jazz",
        "mode": "ensemble",
        "name": "Jazz trio",
        "color": "#ee3a80",
        "description": "Piano, upright bass and brushed drums find a relaxed pocket around your melody.",
        "prompt": "TrackType: Music, instrumental acoustic jazz piano trio. Expressive grand piano plays the supplied melodic phrase with its recognizable pitch contour and rhythm. Rounded plucked upright bass, lightly brushed drums, relaxed settled pocket, tasteful warm reharmonization, sparse piano voicings and a brief bass answer between phrases. Intimate clear live-room sound, sensitive interaction. A complete 15-second miniature, immediate melodic entrance, short development and deliberate final cadence. Instrumental only.",
    },
]
NEGATIVE_PROMPT = "singing, speech, vocals, lyrics, choir, vocal samples, distorted audio, noise"


def runtime():
    folder = ROOT / "data/runtime"
    manifest = folder / "local-music.json"
    python = folder / "audio-env/bin/python"
    script = folder / "stable-audio-3/optimized/mlx/scripts/sa3_mlx.py"
    if not manifest.is_file() or not python.is_file() or not script.is_file():
        return None
    info = json.loads(manifest.read_text())
    weights = script.parents[1] / "models/mlx"
    if not all(
        (weights / name).is_file() and (weights / name).stat().st_size == entry[0]
        for name, entry in info["weights"].items()
    ):
        return None
    return {"python": python, "script": script, "manifest": info}


class LocalEnsembleProvider:
    name = PROVIDER

    def generate(self, request, folder):
        installed = runtime()
        if not installed:
            raise ValueError("The free local music model needs its one-time setup on this Mac.")
        folder = Path(folder)
        # This boundary receives only the saved synthesized guide, never the recording.
        samples = media.read_audio(request.reference, request.duration)
        start = media.playback_start(samples)
        samples = media.fit_audio(samples[start:], round(request.duration * media.SAMPLE_RATE))
        conditioning = folder / "wordless-melody.wav"
        media.write_audio(conditioning, samples)
        raw = folder / "model-output.wav"
        args = [
            str(installed["python"]),
            str(installed["script"]),
            "--dit",
            "medium",
            "--decoder",
            "same-l",
            "--seconds",
            str(request.duration),
            "--init-audio",
            str(conditioning),
            "--init-noise-level",
            "0.70",
            "--prompt",
            request.style["prompt"],
            "--negative-prompt",
            NEGATIVE_PROMPT,
            "--cfg",
            "2.0",
            "--steps",
            "8",
            "--seed",
            str(request.seed),
            "--out",
            str(raw),
        ]
        environment = {**os.environ, "HF_HUB_OFFLINE": "1", "HF_HUB_DISABLE_TELEMETRY": "1"}
        with (folder / "model.log").open("wb") as log:
            result = subprocess.run(args, stdout=log, stderr=subprocess.STDOUT, timeout=300, env=environment)
        if result.returncode or not raw.is_file():
            raise RuntimeError(
                "The local ensemble render failed. Its diagnostic log is saved with this attempt."
            )
        generated = media.read_audio(raw, request.duration)
        if np.max(np.abs(generated)) < 0.0001:
            raise ValueError("The local model returned silence. Try another interpretation.")
        onset = media.playback_start(generated)
        generated = media.fit_audio(generated[onset:], round(request.duration * media.SAMPLE_RATE))
        # Tiny edge fades prevent clicks, without altering notes or internal pauses.
        attack, release = round(0.005 * media.SAMPLE_RATE), round(0.08 * media.SAMPLE_RATE)
        generated[:attack] *= np.linspace(0, 1, attack)[:, None]
        generated[-release:] *= np.linspace(1, 0, release)[:, None]
        prepared = folder / "prepared.wav"
        media.write_audio(prepared, generated)
        output = folder / "audio.wav"
        mastering = media.master_audio(prepared, output)
        return AudioResult(
            output,
            {
                "provider": PROVIDER,
                "model": MODEL,
                "generation_cost_usd": 0,
                "execution": "local; model downloads disabled during generation",
                "runtime_commit": installed["manifest"]["runtime_commit"],
                "model_revision": installed["manifest"]["model_revision"],
                "conditioning_sha256": media.digest(conditioning),
                "guide_sha256": media.digest(request.reference),
                "source_recording_in_model_input": False,
                "init_noise_level": 0.70,
                "cfg": 2.0,
                "steps": 8,
                "seed": request.seed,
                "negative_prompt": NEGATIVE_PROMPT,
                "opening_seconds_removed": onset / media.SAMPLE_RATE,
                "mastering": mastering,
                "listening_review": "Needed: melody recognition, instrumental-only output and ensemble quality.",
            },
        )
