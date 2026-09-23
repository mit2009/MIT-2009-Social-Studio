# Free local musical arrangements

The accepted phrase should feel engaging and musical for current college students. The earlier tones did not meet the sound-quality target; the current arranger explores alternatives to piano with three distinct lead sounds and grooves. These are listening auditions, not a verified claim of professional performance or student appeal.

## Setup and sources

After installing the core app, run:

```sh
.venv/bin/python scripts/install_instruments.py
```

The installer downloads 372 selected WAV/FLAC recordings (about 489 MB) into ignored `data/instruments`. It verifies pinned Git blob hashes and records the catalog hash. Re-running installs missing files and verifies existing ones. No account, subscription, plugin, GPU or paid API is needed. Rendering makes no network requests. Existing NumPy, SciPy and SoundFile dependencies perform sampling and mixing.

Strings, plucked bass, trumpet and trombone come from [VSCO 2 CE](https://github.com/sgossner/VSCO-2-CE/tree/440300901dfe9275fd84e0b7763af1f8443ae62e). Acoustic percussion and the earlier arrangements' Steinway B come from [VCSL](https://github.com/sgossner/VCSL/tree/c1ea7bcc3c7309650ab0da9d15c9cd1fbc4a4c7e). Electric guitar comes from [FreePats](https://github.com/freepats/electric-guitar-FSBS-clean/tree/192cf0d9bf2c4ba6ead8e3524ba3f78818e4fe91). All three libraries declare CC0-1.0. Source paths, revisions, root notes and file hashes live in `mit2009_studio/instruments.json`; recordings stay out of Git.

Cello, contrabass, trumpet and trombone filenames label middle C as C3. Their catalog root notes include a one-octave correction, spot-checked against waveform fundamentals. One quiet bass take with an unstable pitch attack remains excluded. Each used recording is hash-checked before decoding.

## Three current auditions

| Version | Lead and supporting parts | Accompaniment pulse |
|---|---|---|
| Club bounce | Detuned plucked synth, offbeat sub-bass, electronic kick/clap, recorded hats | 136 BPM |
| Indie dance | Recorded electric guitar, plucked violin replies, bass, electronic kick/clap and recorded hats | 122 BPM |
| Brass bounce | Recorded trumpet hook, short trombone chords, bass and recorded drums | 112 BPM |

None uses piano. Electronic sounds are deliberately synthesized locally; they are not represented as acoustic recordings. The source recording, sung words and vocal samples are never mixed into these compositions.

The accepted score is snapshotted by hash alongside its unchanged audible guide. Each lead note retains pitch, order and relative onset; only the opening wait is removed. Short articulation, entrance accents, offbeat chord stabs and phrase-derived replies provide motion. Replies fit the longer rests. A two-hit ending appears when the phrase leaves room for it. The lead keeps its original expressive timing rather than being silently quantized to the accompaniment.

A heuristic fits triads to local note windows and favors common tones between adjacent harmonies. It does not force a major key. Sample velocity layers, alternate takes where available, stereo placement and a short room response vary the performance. No stock backing track is looped. Each render saves a fresh `arrangement.json`, separate melody/accompaniment stems, and the 15-second 48 kHz stereo master. Previous drafts and the melody guide stay saved; ratings, selection and creative approval remain human actions.

## Limits and listening review

A brighter instrument and faster beat do not guarantee fun. Harmony can be unsuitable for chromatic phrases, the fixed pulse can conflict with expressive timing, and sample articulation is limited. Very short notes can sound fragmented. The accepted score may itself need correction, but this change does not silently alter it. Listen for phrase recognition, tone, groove, blend and an intentional ending. Then test contrasting examples with a few students rather than assuming one genre represents everyone.

[Spotify's 2025 US college-student listening report](https://newsroom.spotify.com/2025-05-01/best-in-class-college-student-listening-graduation-2025/) informed the choice to offer varied sounds. It concerns Spotify Student-plan listeners, not an MIT audience study or proof these arrangements will appeal.

## Earlier experiments

Previous piano-based arrangements remain playable in history. Their scores and files are preserved; the original arrangement branch remains available for explicit historical retries. Legacy style IDs (`dance`, `chamber`, `jazz`) remain internal for compatibility; the saved `feel` value chooses the current upbeat arrangement.

The first free model adapter remains in `providers/ensemble.py`. Existing model jobs retain their original renderer when explicitly retried. No automatic fallback or paid service is enabled. Its 6.9 GB weights and isolated MLX environment remain local, are unnecessary for the current workflow, and have separate Stability Community and Gemma terms.
