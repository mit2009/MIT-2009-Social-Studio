# Free local ensemble generation

Danny requires this workflow to be free. There is no paid API adapter, credit purchase, account requirement, cloud generation or audio upload. Stable Audio 3 Medium runs on the Mac through the official Apple Silicon MLX runtime. Ordinary computer power/storage use remains local.

## One-time setup

Install the main app first, then run from the repository:

```sh
.venv/bin/python scripts/install_local_music.py
```

This setup needs an Apple Silicon Mac, internet access for the initial downloads, and approximately 8 GB of free disk space. The script installs into `data/runtime/audio-env`, keeps upstream code under `data/runtime/stable-audio-3`, verifies all four model files against pinned SHA-256 checksums, and enables generation only after setup succeeds. Dependencies are separate from the studio server environment. Interrupted weight downloads can resume by running setup again.

Runtime revision: `779434a908193105335fd8d833418603625b2859` from the [official repository](https://github.com/Stability-AI/stable-audio-3/tree/779434a908193105335fd8d833418603625b2859/optimized/mlx).
Model revision: `da6edc54ddba10bfd79a077102ded687f80e882b` from the [official optimized model](https://huggingface.co/stabilityai/stable-audio-3-optimized/tree/da6edc54ddba10bfd79a077102ded687f80e882b/MLX).

After installation, generation sets `HF_HUB_OFFLINE=1` and disables Hugging Face telemetry. The runtime receives only the synthesized wordless guide and style prompt. It receives neither the original recording nor a transcript. No public Gradio server is launched.

## User flow

Upload one phrase → Find my melody → listen → Make three versions → compare/rate/select → continue to photographs. There is no bed/effects chooser or provider settings panel. Every request creates three fresh candidate files. Generation, ratings and final creative approval remain separate actions.

The current three briefs are bass-heavy dance, piano/violin/cello chamber trio, and piano/upright-bass/brushed-drums jazz trio. The model is conditioned on the saved guide with transformation level 0.70, guidance 2.0 and eight steps. These are starting experiment settings, not guarantees of fidelity. Prompts, seeds, guide hashes and model/runtime revisions are retained with candidates. Each worker subprocess has a five-minute timeout; retry is explicit and preserves completed candidates.

Masters are verified as 15-second 48 kHz stereo WAVs, given conservative constant-gain mastering, and checked for finite audible samples. Opening silence is removed for a prompt entrance; internal rests stay intact. The existing original recording, guide and earlier renders are never rewritten.

## Quality and licensing limits

A note guide can be misread; a generative arrangement can drift from the melody or add unwanted vocal-like material. Technical tests cannot establish convincing musicianship. Listen to each actual output and compare it with the accepted guide before using it.

This local prototype evaluates the model for the course project. Weights use the [Stability AI Community License](https://stability.ai/license), and the bundled T5Gemma encoder has Gemma terms. The source runtime is MIT-licensed. These are distinct from an unrestricted license for institutional/commercial deployment; review the applicable model terms before any wider deployment. There is no paid fallback: a missing or failed local model produces a clear setup/error message.
