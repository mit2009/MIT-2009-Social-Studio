# MIT 2.009 Candidate Studio

**One local application for making choices across Audio → Video → Keyword → Assembly.**

Generate three possibilities, compare, rate, select, and advance. Make three final mixes from your selected ingredients. Explain **“Why this one?”**, explicitly approve a version, and export the media with its provenance.

Built for Danny, Talla, and the 2.009 TAs, with a small student trial as the next milestone. The purpose is entertaining, inspiring stories about the course and interest in the **December 7, 2026 final presentations livestream**. Humans retain taste, authorship, and approval.

## Current direction: musical authorship

Danny's revised brief is a musical phrase interpreted by three convincing ensembles, with no recognizable lyrics. The interface now uses the Connect wordmark, supplied color palette and Outfit font, with one musical input and no bed/effects controls.

The melody check extracts estimated notes and plays a voice-free instrumental guide. **Make three versions** now offers three upbeat interpretations: Club bounce (plucked synth and club beat), Indie dance (electric guitar and plucked strings), and Brass bounce (trumpet, brass punches and a funk groove). None uses piano. Separate parts provide harmony, bass, percussion and replies using fragments of the phrase. No API account, subscription or paid generation service is used. A one-time instrument download is required; see [LOCAL-MUSIC.md](docs/LOCAL-MUSIC.md).

The goal remains convincing ensemble performances in which the person recognizes their own phrase. Listening review rejected the initial model drafts for insufficient sound quality. The local arranger combines recorded instruments with deliberately electronic voices, preserves the lead pitches, note order and relative onsets, and builds accompaniment from those notes. This remains a listening experiment; automated checks do not establish convincing musicianship. The earlier voice-effects experiments remain collapsed in history, with their files unchanged.

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

Open **http://127.0.0.1:8773**. Keep the terminal running while rendering. The server binds only to this computer. The core app needs no API key or account. Ensemble generation additionally needs the free instrument setup below.

Install FFmpeg with `brew install ffmpeg` on macOS or `sudo apt install ffmpeg` on Ubuntu/Debian. Check `ffmpeg -version` and `ffprobe -version` before starting. The build must include H.264/libx264 and ProRes encoders.

On a Mac, after setup, double-click **Open 2.009 Studio.command**. The older Test Studio shortcut also opens the new application.

Click **Try the sample project** or open a saved project, then **Find my melody**. The simple guide lets you check what the system heard. Install the free recorded instruments once:

```sh
.venv/bin/python scripts/install_instruments.py
```

Then click **Make three versions**, compare the three drafts, rate and select one. The setup downloads about 489 MB of CC0 instrument recordings into ignored `data/`; rendering works locally without a model or GPU. Your audio remains on this Mac.

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
