# Audio-only house-band pilot

**Listening result:** All three first-run candidates were rejected for insufficient sound quality. Keep this batch as a failed baseline. Next test a different performance engine before more sampler variations.

This isolated command uses the original audio as its only creative input. It
re-extracts notes and measured expression, then makes three local interpretations.
No production provider, web interface or database migration is involved.

From the repository root, using its installed virtual environment and CC0
instrument bank:

```sh
.venv/bin/python -m experiments.audio_only /absolute/path/to/recording.m4a data/experiments/a-new-run
```

Use a fresh output folder; existing folders are never overwritten. Seed defaults
to 2009 (`--seed 2010` produces another reproducible variation). The project
setting defaults to 15 seconds. An optional `--config project.json` accepts only
`{"duration_seconds": 15.0}`; duration is not exposed as a student control.
Recordings from 0.2 to 60 seconds are supported in this bounded pilot; longer
inputs are rejected rather than silently truncated. No model or new package is
needed beyond the existing project environment. An unavailable instrument bank
causes a clear error, not an automatic download or paid fallback.

## What differs

- **Follow the phrase:** detected pitches/order and timing proportions survive a
  logged uniform fit to the project duration; measured dynamics and sparse backing.
- **Find the groove:** the same pitches with halfway-to-grid timing, a bass groove
  and percussion. Alternate seeds can introduce a swing offset.
- **Play with the idea:** an initial statement followed by sequenced/inverted
  fragments traceable to source notes and a return to the source's final pitch.

These are adapted E01/E02/E04 trials, with accompaniment and one seed per first
comparison. They are not the originally proposed six solo-renderer controls.
All three use one guitar lead patch so instrument choice does not account for
the structural difference. Harmony is a heuristic fitted to source notes.

## Expression and limits

Analysis preserves per-note measured levels, quantized pitch, timing, confidence
and phrase boundaries. A second expression hypothesis combines level and register.
No target climax time, feedback text, corrected score, or manual curve is accepted.
A continuous pitch model, source separation and advanced expression modeling are
not implemented here. Melody splitting, octave errors, phone gain, sample
articulation and heuristic harmony remain limitations. Fixed-grid accompaniment
is a style choice, not a claim that the original was performed at that tempo.

The current recording is a seen development example. Running from audio alone
establishes input independence; it does not establish generalization or successful
understanding of a story. Compare outputs by listening and later use unfamiliar
inputs with contrasting contours, as specified in
[the audio-only protocol](../docs/house-band/AUDIO-ONLY-INTERPRETATION.md).

## Reproduction and verification

The output folder retains fresh analysis, source time mappings, arrangement
scores, actual sample hashes, separate melody/accompaniment stems, unmastered
audio, mastered WAVs and checks. `run.json` records the input/script/catalog
hashes, configuration, versions and measured runtime. It never records creative
approval. Use the repository's existing requirements and instrument installer
instructions for another machine; record its resolved environment separately.

```sh
.venv/bin/python -m pytest -q tests/test_audio_only_pilot.py
```

Tests use known rising, falling and steady signals to catch a forced late climax,
plus preservation, transformation, determinism and project-duration boundaries.
The render command checks finite audio, exact duration, audible start and true
peak. Export checks cannot certify musical quality.
