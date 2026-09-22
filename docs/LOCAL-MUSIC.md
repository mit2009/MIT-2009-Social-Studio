# Free local recorded-instrument arrangements

Listening review rejected the first Stable Audio 3 drafts because sound quality did not meet the target. The default engine is now a score-driven sampler and arranger, with recordings of acoustic instruments. This is an attempt to improve tone and preserve the phrase, not a verified claim of professional performance.

## Setup and sources

After installing the core app, run:

```sh
.venv/bin/python scripts/install_instruments.py
```

The installer downloads 140 selected WAV recordings (about 364 MB) into ignored `data/instruments`. It verifies pinned Git blob hashes and records the catalog hash. It needs no account, subscription, plugin, GPU or paid API. Rendering makes no network requests. The app's existing NumPy, SciPy and SoundFile dependencies perform the sampling and mixing.

The grand piano is the close-miked Steinway B from [VCSL](https://github.com/sgossner/VCSL/tree/c1ea7bcc3c7309650ab0da9d15c9cd1fbc4a4c7e). Violin, cello section and plucked contrabass come from [VSCO 2 CE](https://github.com/sgossner/VSCO-2-CE/tree/440300901dfe9275fd84e0b7763af1f8443ae62e). Percussion comes from VCSL. Both source libraries declare CC0-1.0. The pinned catalog is `mit2009_studio/instruments.json`; recordings stay out of Git.

The cello and contrabass samples label middle C as C3, unlike the piano and violin samples. Their catalog root notes include a one-octave correction, checked against actual waveform fundamentals. One quiet bass take with an unstable pitch attack was excluded in favor of its alternate take. The sampler checks each used file's hash before decoding it.

## What the arranger does

The accepted score is snapshotted by hash alongside the unchanged audible guide. Every melody note retains its pitch, order and relative onset. Only the opening wait is removed. A recorded grand piano plays this line, with small dynamic variations and acoustic release tails. There are no vocal samples, source-recording samples, lyrics or generative voice output in this engine.

The three arrangements are Piano house (piano, electronic sub-bass and recorded percussion), Piano & strings (piano, solo violin and cello section), and Acoustic jazz trio (piano, plucked contrabass and light recorded drums). The dance sub-bass is intentionally synthesized; it is not labeled as an acoustic recording. The cello source is a section, and the drums use light hits/sticks, not a claimed brush recording.

A small heuristic fits triads to local note windows, favors common tones between adjacent harmonies, adds restrained inner parts and phrase-ending answers, and balances accompaniment below the melody. The lead remains rubato while accompaniment has a pulse. Sample velocity layers, round-robin alternatives where available, panning and a short room response vary the performance. The sampler never loops a stock backing track.

Each render saves a fresh `arrangement.json`, separate melody/accompaniment stems, and the 15-second 48 kHz stereo master. Previous drafts and the melody guide are never overwritten. Ratings, selection and creative approval remain Danny's actions.

## Limits and listening review

Recorded instruments improve the source material but cannot guarantee a convincing ensemble. The arranger is a heuristic, not a musician: harmony can be unsuitable for a chromatic phrase, accompaniment may not follow expressive timing well, and strings do not have a true legato transition engine. Very short extracted notes can still sound fragmented. The accepted score may itself need correction, but this change does not silently alter it. Listen for tone, phrasing, blend and recognition before calling the quality goal met.

## Earlier model experiment

The first free model adapter remains in `providers/ensemble.py`, and its drafts are accessible under Earlier ensemble versions. New requests use recorded instruments. Existing model jobs retain their original renderer when explicitly retried; no automatic fallback or paid service is enabled. Its 6.9 GB weights and isolated MLX environment remain local. The model experiment is not needed for the current workflow and is subject to its separate Stability Community and Gemma terms.
