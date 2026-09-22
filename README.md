# MIT 2.009 Candidate Studio

**One local application for making choices across Audio → Video → Keyword → Assembly.**

Generate three possibilities, compare, rate, select, and advance. Make three final mixes from your selected ingredients. Explain **“Why this one?”**, explicitly approve a version, and export the media with its provenance.

Built for Danny, Talla, and the 2.009 TAs, with a small student trial as the next milestone. The purpose is entertaining, inspiring stories about the course and interest in the **December 7, 2026 final presentations livestream**. Humans retain taste, authorship, and approval.

## Current direction: musical authorship

Danny's revised brief is a musical phrase interpreted by three convincing ensembles, with no recognizable lyrics. The interface now uses the Connect wordmark, supplied color palette and Outfit font, with one musical input and no bed/effects controls.

The melody check extracts estimated notes and plays a voice-free instrumental guide. **Make three versions** uses Stable Audio 3 Medium locally on Apple Silicon to create bass-heavy dance, chamber trio and jazz trio drafts. No API account, subscription or paid generation service is used. A one-time model setup is required; see [LOCAL-MUSIC.md](docs/LOCAL-MUSIC.md).

The goal remains convincing ensemble performances in which the person recognizes their own phrase. These are experimental model-generated drafts, not a claim that the professional-quality goal has been met. Listen for melody fidelity, believable interplay, and unwanted vocal sounds. The earlier voice-effects experiments remain collapsed in history, with their files unchanged.

The existing comparison/rating/selection, video, alpha Keyword, assembly, provenance and approval/export infrastructure remains. The original procedural release is preserved at `0cfe313`.

## Run locally

Use **Python 3.12+** and **FFmpeg/FFprobe** on macOS or Linux. Windows users should use WSL; native Windows is not supported by the worker lock.

```sh
git clone https://github.com/dannygoldfield/MIT-2009-Social-Studio.git
cd MIT-2009-Social-Studio
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements-lock.txt
.venv/bin/python -m pip install --no-build-isolation --no-deps -e .
.venv/bin/python -m mit2009_studio.server
```

Open **http://127.0.0.1:8773**. Keep the terminal running while rendering. The server binds only to this computer. The core app needs no API key or account. Ensemble generation additionally needs the free Apple Silicon setup below.

Install FFmpeg with `brew install ffmpeg` on macOS or `sudo apt install ffmpeg` on Ubuntu/Debian. Check `ffmpeg -version` and `ffprobe -version` before starting. The build must include H.264/libx264 and ProRes encoders.

On a Mac, after setup, double-click **Open 2.009 Studio.command**. The older Test Studio shortcut also opens the new application.

Click **Try the sample project** or open a saved project, then **Find my melody**. The simple guide lets you check what the system heard. On an Apple Silicon Mac, install the free local generator once:

```sh
.venv/bin/python scripts/install_local_music.py
```

Then click **Make three versions**, compare the three drafts, rate and select one. The setup downloads about 6.9 GB of model weights plus dependencies into ignored `data/`; each generation runs offline. Your audio remains on this Mac.

## Keep your work

By default, private work lives in **`data/candidate-engine/`**, separate from the previous studio's data layout. Back up that entire folder while the server is stopped. Source media and generated artifacts remain local and are excluded from Git.

```sh
.venv/bin/python -m mit2009_studio.server --port 8773 --data-dir /path/to/private/studio-data
```

Do not run two studio processes against the same folder. The app deliberately does not migrate old library records or reinterpret old approval flags. The previous implementation is preserved in Git at commit `6bc6d1a`.

## Verify your setup

```sh
.venv/bin/python -m pytest -q
.venv/bin/ruff check mit2009_studio tests
```

Tests render actual 15-second audio/video/text/assembly at smaller dimensions for speed, in both orientations. They inspect duration, frame counts, audio, actual transparent pixels, persistence, approval/export integrity, failure recovery, and selection rules. The previous full-resolution browser workflow applies to the preserved procedural release; current melody/brand checks are described in [TESTING.md](docs/TESTING.md).

## Start here, Talla

Read [TALLA.md](docs/TALLA.md), then [ARCHITECTURE.md](docs/ARCHITECTURE.md). Please challenge the design. In particular, help decide how to improve personal-audio interpretation and how little infrastructure we need for a small student alpha.

- [Content pipeline playbook](docs/CONTENT-PIPELINE.md): the accumulated product rules.
- [Architecture and data](docs/ARCHITECTURE.md): modules, persistence, jobs, provenance, APIs.
- [Discovery and research](docs/DISCOVERY-2026-09-22.md): inspected prior work, alternatives, licenses, and provider shortlist.
- [Testing](docs/TESTING.md): repeatable checks and observed results.
- [Known limitations and student alpha](docs/LIMITATIONS.md): unfinished work and readiness gates.
- [Reuse and licensing](docs/REUSE.md): origins and dependency considerations.

The generated API schema is available locally at `/openapi.json`; API usage is described in ARCHITECTURE.md. No external documentation scripts are required. Source-level configuration is in `mit2009_studio/presets.json`; `STUDIO_PRESETS` can point to a separate editable JSON file. There is deliberately no style editor or elaborate prompting interface yet.
