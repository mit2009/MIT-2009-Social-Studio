"""Isolated official MRT2 worker. Receives note controls, never source audio."""

import importlib.metadata
import json
import sys
import time
from pathlib import Path

import mlx.core as mx
import numpy as np
import soundfile as sf
from magenta_rt import MagentaRT2StdMlxfn, paths
from magenta_rt.config import DRUM_PIANOROLL, MUSICCOCA, PIANOROLL_WITH_ONSETS


def main():
    job = json.loads(Path(sys.argv[1]).read_text())
    folder = Path(job["output_folder"])
    paths.set_magenta_home(job["assets_root"])

    # Generation needs no network. Block Python socket connections explicitly.
    def offline(event, args):
        if event in ("socket.connect", "socket.getaddrinfo"):
            raise RuntimeError("Network use is disabled during local generation.")

    sys.addaudithook(offline)
    started = time.perf_counter()
    mx.random.seed(job["seed"])
    scales = job.get("cfg_scales", {"musiccoca": 3.0, "notes": 2.0, "drums": 1.0})
    model = MagentaRT2StdMlxfn(size="mrt2_base", temperature=1.1, top_k=30, cfg_scales=scales)
    print("Model loaded", flush=True)
    style = model.tokenize_style(model.embed_style(job["style"], use_mapper=True, seed=job["seed"]))
    roll = np.load(folder / "note-control.npy")
    assert roll.shape == (job["frames"], 128)
    state, chunks = None, []
    for i, notes in enumerate(roll):
        wav, state = model.generate(
            conditioning={MUSICCOCA.key: style, PIANOROLL_WITH_ONSETS.key: notes, DRUM_PIANOROLL.key: [-1]},
            frames=1,
            state=state,
        )
        chunk = np.asarray(wav.samples)
        chunks.append(chunk)
        if (i + 1) % 100 == 0:
            print(f"Generated {(i + 1) / 25:.1f} seconds", flush=True)
    audio = np.concatenate(chunks)
    assert audio.shape == (job["frames"] * 1920, 2) and np.isfinite(audio).all()
    sf.write(folder / "model-raw.wav", audio, 48000, subtype="FLOAT")
    (folder / "worker.json").write_text(
        json.dumps(
            {
                "elapsed_seconds": time.perf_counter() - started,
                "raw_peak": float(np.max(np.abs(audio))),
                "shape": list(audio.shape),
                "python_network_connections_blocked": True,
                "paid_api_calls": 0,
                "model": "mrt2_base",
                "style_tokens": style.tolist(),
                "packages": sorted(
                    {(d.metadata["Name"], d.version) for d in importlib.metadata.distributions()}
                ),
                "temperature": 1.1,
                "top_k": 30,
                "cfg_scales": scales,
                "source_audio_in_model_input": False,
                "perceptual_review": None,
            },
            indent=2,
        )
        + "\n"
    )
    print("Raw audition saved", flush=True)


if __name__ == "__main__":
    main()
