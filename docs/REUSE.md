# Reuse, independence and licensing

The canonical 2.009 studio has been updated in place. The old implementation remains available in Git at `6bc6d1a`. No HPR source checkout, data store or media bank is a runtime dependency, and those projects were not changed.

## What was adapted

- FFmpeg raw-frame writing, image orientation/profile handling, H.264 output conventions, and constant-gain loudness measurement were adapted from this repository's prior `media.py` and `render.py`.
- HPR Audio Generator's seeded ingredient/recipe separation informed the new local provider. Its copied integer-sample mixing package was removed from the current runtime in favor of a small NumPy implementation suited to reference interpretations and Original Mix.
- Rubber Reality's scanline/strip displacement and complete-frame blend approach informed the liquid photo treatment. No browser animation engine was imported.
- HPR Umbrella informed immutable IDs, candidate histories and assembly of separately selected files. Its registry, archive, sequencing and publication infrastructure were not copied into this app.
- The 2026 Connect brand assets and Outfit font remain from the prior studio. Outfit is distributed under its included `web/brand-2026/OFL.txt`.

The inspected HPR commits and hashes remain in `hpr-read-only-baseline.json`. The optional `tools/check_hpr_unchanged.py` checks these local repositories read-only and is not required elsewhere.

## Third-party boundaries

FastAPI uses MIT terms. The installed NumPy 2.5.3 metadata declares `BSD-3-Clause AND 0BSD AND MIT AND Zlib AND CC0-1.0`; Pillow 12.3.0 declares `MIT-CMU`. Consult their bundled notices for component-specific terms. FFmpeg's license depends on how it is built; libx264-enabled builds introduce GPL considerations. We invoke the user's installed FFmpeg and do not bundle a binary. The current application is a private collaboration repository, without a new application-level open-source license declaration.

librosa 1.0.0 (ISC) is now a pinned dependency used through its pYIN API for a note-only melody guide; its code is not vendored. No code was copied from Remotion, MoviePy, ComfyUI, AudioCraft, ACE-Step, or stable-audio-tools. Their research recommendations and license distinctions are recorded in DISCOVERY-2026-09-22.md. Code licenses do not automatically establish model-weight rights, generated-output rights or source-media permissions.

## Media

`demo.py` creates synthetic geometry and a simple procedural melody for a rights-clear practice workflow. It does not reproduce a commercial song or contain student photographs. Danny's provided recording and real course photographs used for verification stay under ignored private `data/` and were not added to Git. The existing MIT sound source notes are historical reference documentation; no external sound library is silently bundled or uploaded.

## Free local music model

The optional renderer calls the official Stable Audio 3 MLX runtime at pinned revision `779434a908193105335fd8d833418603625b2859`. Its source remains an independent ignored checkout under this project's `data/runtime/`, with upstream MIT license retained. Four NPZ weight files are downloaded from Stability AI's optimized-model repository at `da6edc54ddba10bfd79a077102ded687f80e882b` and verified against published SHA-256 hashes. Weight licensing is Stability AI Community License; T5Gemma has separate Gemma terms. No model weights or private audio enter Git. The optional environment is isolated and pinned in `requirements-audio.lock.txt`. See LOCAL-MUSIC.md for the scope and deployment caveat.

## Recorded instruments (September 22 revision)

The new phrase arranger and sample playback code are independent implementations in this repository. Recorded sounds are a pinned subset of Sam Gossner/Versilian Studios' [VSCO 2 CE](https://github.com/sgossner/VSCO-2-CE) (Sam Gossner and Simon Dalzell recordings, Elan Hickler/Soundemote sample cutting) and [VCSL](https://github.com/sgossner/VCSL), both CC0-1.0. The complete source paths, revisions and blob hashes are in `mit2009_studio/instruments.json`; downloaded WAV/FLAC files stay under ignored `data/instruments`. Electric-guitar recordings are the CC0 [FreePats electric-guitar-FSBS-clean](https://github.com/freepats/electric-guitar-FSBS-clean/tree/192cf0d9bf2c4ba6ead8e3524ba3f78818e4fe91) library at that pinned revision. The synth pluck, club kick and clap are original local waveform code, not sampled commercial recordings. No HPR asset or runtime is used. The earlier model adapter remains historical and its distinct model licenses still apply to that experiment.
