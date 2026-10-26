# E11 performance-engine trial — September 23, 2026

Listening review rejected all three audio-only sampler auditions for insufficient
sound quality. Passing technical checks did not establish musical success. Stop generating more variants of that renderer as the next step.

One contrasting 15-second MRT2 base audition has now been rendered locally.
This is the first audition with a positive sound-quality result and is retained
as a reference for future comparisons. Source recognition still needs improvement;
this result does not establish a fidelity pass. Expressive arc and generality across other recordings remain
to be assessed separately.
No application integration, student deployment or architecture choice is implied.

## What this trial actually does

The existing analyzer re-extracts notes from the original recording. The adapter
fits their timeline into a 14-second phrase and sends 25-Hz pitch controls to
Magenta RealTime 2 base. Notes in the source register are constrained; other
registers remain available for accompaniment. Connected notes allow the model
to choose articulation instead of forcing every pitch change into a fresh attack.
The performer receives a fixed instrumental-funk style preset. The student
provides no text, climax timestamp, corrected melody or hand-drawn volume curve.

The model receives note controls, not the source waveform. No recorded voice is
mixed into the output. Generated vocal-like sounds remain possible. The current
MIDI channel does not transmit velocity or the measured dynamics curve; this is
a test of performance sound and note conditioning, not a completed expressive
analysis solution. Note conditioning is not proof that the generated audio follows
the notes. That requires listening and further comparative evaluation.

It generates 16 seconds to allow for startup and release. The listening master
skips 35 ms of startup, keeps 15 seconds, uses constant-gain mastering and a 200 ms
ending fade. The fade is boundary treatment, not evidence of a composed cadence.
Technical checks found an audible start at 5 ms, approximately −18 LUFS, true peak
−1.85 dBTP, finite stereo 48 kHz audio, and an unchanged source hash. Whole-trial
runtime was about 31 seconds on this Mac, excluding installation. This is one
observation, not a performance promise. The separate listening record now captures positive sound-quality feedback; no stars or publishing approval were assigned.

## Pinned implementation and licenses

- [Official source](https://github.com/magenta/magenta-realtime), commit
  `694a545e4ba0b88bf1150137b129582166d3e07f`; Apache-2.0.
- Official sequence-layers submodule, commit
  `c85a637a1afae8f4f2d4edb458f2111b5f44ae52`.
- [Official weights](https://huggingface.co/google/magenta-realtime-2), revision
  `010aa0dcb0dfd27b24f0ad07b4dad63e8f9521cc`; CC-BY-4.0 plus the
  [model-card usage terms](https://github.com/magenta/magenta-realtime/blob/694a545e4ba0b88bf1150137b129582166d3e07f/MODEL.md).
  Attribution: Magenta RealTime 2, Google DeepMind / Google LLC, 2026.
- Six public ungated assets are downloaded with SHA-256 and size verification.
  The exported base graph includes its decoder; this note-control trial needs
  only the text/style resources in addition to the graph and state.
- Dependencies are isolated in `data/runtime/mrt2-env`; the working app environment
  is unchanged. [Mac dependency lock](../../requirements-mrt2.lock.txt).

MLX 0.32.2 failed to load the official exported graph with “Invalid string size”.
The successful retry uses **MLX and mlx-metal 0.31.2**, matching the upstream
Python lockfile. Retain this pin; the failed attempt's log is preserved separately.
This trial makes no claim about Linux compatibility or other hardware.

## Reproduce on another Apple Silicon Mac

From an installed Studio checkout with its existing app environment:

```sh
git clone https://github.com/magenta/magenta-realtime.git data/runtime/magenta-realtime
git -C data/runtime/magenta-realtime checkout 694a545e4ba0b88bf1150137b129582166d3e07f
git -C data/runtime/magenta-realtime submodule update --init --recursive
.venv/bin/python -m venv data/runtime/mrt2-env
data/runtime/mrt2-env/bin/python -m pip install -r requirements-mrt2.lock.txt
data/runtime/mrt2-env/bin/python -m pip install --no-deps -e data/runtime/magenta-realtime
.venv/bin/python scripts/install_mrt2_trial.py
.venv/bin/python -m experiments.mrt2_trial /absolute/path/to/input.m4a data/experiments/new-mrt2-run
```

Use a fresh output directory; the adapter refuses overwrites. All downloads stay
under the project. Generation uses offline settings and a Python socket audit
hook; it does not call a paid service or upload audio. Initial public dependency
and model downloads require network access.

The output directory stores analysis, source-time mapping, per-frame note
controls, model input settings, raw and mastered audio, worker package versions,
export checks and attribution. `checks.json` pins the adapter and worker hashes.
Tests in `tests/test_mrt2_control.py` cover actual control values, starts, holds,
releases, masked accompaniment registers and connected-note articulation. They
verify wiring, not model quality.

## Seed-recognition comparison — September 23, 2026

The successful `mrt2-05` reference and original recording remain byte-for-byte
unchanged. Detailed listening records remain private. Two comparisons were
presented to evaluate stronger source recognition:

| Run / profile | Change from reference | Measured LUFS / true peak | Elapsed |
| --- | --- | --- | --- |
| A: `mrt2-06-closer` / `closer` | Note guidance 2 → 4; identical control roll, pitches and timing | −18.66 / −1.00 dBTP | 30.02 s |
| B: `mrt2-07-lead` / `lead` | A's guidance plus automatic whole-octave lead placement and a wider constrained register | −18.01 / −4.61 dBTP | 31.15 s |

For this input, B raises all notes by one octave (58–77) and constrains pitches
55–89 to reduce competing lead material; the bass register remains free. The
intervals and mapped source timing remain unchanged. This is an arrangement
hypothesis, not proof that the melody will be more audible. Stronger conditioning
may reduce musical freedom or sound quality. Both runs retain the same model,
style preset, seed 2009 and analysis method. No user-authored musical corrections
or original vocal waveform enter generation.

Both exports are 15-second, 48 kHz stereo WAVs, with signal beginning at about
5 ms. A's raw model waveform contains three full-scale channel samples out of
1,536,000; B contains none. The final true peaks pass the export ceiling, but
mastering cannot undo any distortion already generated by the model. Raw
measurements are saved separately from export checks.

Reproduce with the installation above, using new output folders:

```sh
.venv/bin/python -m experiments.mrt2_trial /absolute/path/to/input.m4a data/experiments/new-closer --profile closer
.venv/bin/python -m experiments.mrt2_trial /absolute/path/to/input.m4a data/experiments/new-lead --profile lead
```

The default `benchmark` profile retains the earlier controls and guidance. Adapter
and worker snapshots are saved in each run's `reproduction/` folder; restore them
to their original `experiments/` paths in an isolated checkout if needed, because
they resolve the runtime relative to the repository. Record hashes and dependencies;
identical model seeds alone are not a cross-platform reproducibility guarantee.
Private `recognition-comparison-01.json` links the runs and their listening feedback. Four control tests now check onsets, holds, releases, articulation,
unchanged A controls, B's octave/interval/timing preservation and free bass range.

**Listening outcome:** Both variants are retained as viable choices with
recognizable source material. Detailed responses remain in private listening
records; the public record retains the technical outcome without personal quotes.
No preferred winner, rating or permission to publish was inferred.

**Next experiment:** retain A and B, and test one contrasting dance-pop preset
with B's note controls. This is a style-transfer comparison; it does not change
the extraction or prescribe a crescendo. Ending, expression and unseen recordings
remain future checks before choosing an application architecture.


## C: contrasting dance-pop preset

With A and B retained as viable choices, `mrt2-08-dance` tests a third direction.
The `lead` profile, seed 2009, model and note guidance match B. Both the note-control
array and the source-time mapping are identical to B; only the style preset changes.
The internal adapter now accepts `--style` and records it in the job and checks.
The default remains the original funk-band preset. This is an experiment option,
not a student-facing text requirement or application change.

Reproduce after the same installation, using a fresh output folder:

```sh
.venv/bin/python -m experiments.mrt2_trial /absolute/path/to/input.m4a data/experiments/new-dance --profile lead --style 'instrumental dance pop, soaring melodic synthesizer lead, deep pulsing synth bass, punchy four on the floor kick, crisp handclaps, shimmering percussion, energetic uplifting club groove'
```

The render took 30.17 seconds and exported 15 seconds of stereo 48 kHz audio,
with a 5 ms audible start, −18.85 LUFS and −1.00 dBTP. The raw waveform has 22
full-scale channel samples out of 1,536,000; mastering does not establish their
inaudibility. Source and all prior audition hashes remain unchanged. The adapter
and worker snapshots, settings, attribution and `comparison.json` accompany the
output. Four targeted control tests passed; Ruff and diff checks passed. The
previous full-suite result remains 47 passing tests; it was not rerun for this
style argument. Use `python -m pytest` from the repository root, since the direct
pytest executable did not include the repository on its import path here.

C awaits listening for musical contrast, quality and seed recognition. A and B
remain the two viable choices supported by the earlier listening evaluation. No winner
or final application architecture has been selected.


## Six orchestration directions and a peer listening pack

This round explores more orchestration options and explains musical variables
in plain language while keeping the test plan intact. D–I are a bounded style
exploration using the same source, MRT2 base, seed 2009 and B's `lead` profile.
Only the style description changes. Style descriptions can affect instruments,
harmony and groove together; this round does not isolate those variables or
prove exact instrument compliance. The names describe intended directions.

| Letter | Direction | Render seconds | LUFS | True peak dBTP |
| --- | --- | --- | --- | --- |
| D | String trio | 30.71 | -18.00 | -6.80 |
| E | Brass and drums | 32.35 | -18.01 | -4.08 |
| F | Marimba and hand drums | 38.07 | -18.00 | -1.88 |
| G | Jazz quartet with saxophone | 38.37 | -18.00 | -5.11 |
| H | Indie rock band | 30.38 | -17.99 | -4.18 |
| I | Cinematic orchestra | 29.89 | -18.00 | -2.80 |

Each export is exactly 15 seconds, 48 kHz stereo, finite, with audible signal
near 5 ms. All six note-control arrays and source-time maps equal B's; all raw
model peaks are below full scale. Source and earlier audition hashes are unchanged.
These are technical observations, not listening judgments. All six await review.

Reproduce using the existing MRT2 installation and fresh output folders:

```sh
.venv/bin/python -m experiments.orchestration_sweep /absolute/path/to/input.m4a data/experiments/new-orchestration-round --reference /absolute/path/to/baseline-run
```

The reference must be generated from that same source using the `lead` profile.
The checked-in `orchestration-sweep.json` pins all six style texts. The runner saves
its manifest, script snapshots, logs, note controls, raw/mastered audio, attribution
and per-output verification. This round lives under the private session's
`orchestration-sweep-01/` directory. No new paid service, model or app integration.

The portable `Connect-House-Band-Listening-01.zip` contains A–I, the original seed
listening copy, the plain melody reference, an offline HTML listening sheet, a
music-word guide, a manifest and attribution. It is about 3.6 MB. MP3s use 192 kb/s
and a constant −1 dB relative to the source masters for encoding headroom. Decoded
orchestration lengths remain exactly 15 seconds; all encoded true peaks are below
0 dBTP. Only the source listening copy skips its initial quiet (about 48 ms).
Source and guide retain their own lengths. The package contains no internal source
paths or feedback records and has not been uploaded or sent.

Regenerate the listening pack after this session layout is available:

```sh
.venv/bin/python -m experiments.build_listening_pack /absolute/path/to/session /absolute/path/to/input.m4a /absolute/path/to/new-listening-pack
```

Chrome loaded all eleven players without media errors and showed nine 15-second
orchestrations. Playback and one-player-at-a-time behavior were exercised. The
built-in browser crashed twice; Chrome was used for the final desktop inspection.
The optional feedback button displayed its prepared message, but the browser's
download event timed out and actual file receipt was not verified. Reviewers may
instead send letters and comments directly. No feedback is uploaded or retained
by the page, and the testing form was cleared.

Four melody-control tests passed in 2.60 seconds; Ruff, JavaScript syntax and diff
checks passed. The ZIP was read back and each member compared with its source.
See [Music in plain language](MUSIC-IN-PLAIN-LANGUAGE.md) for definitions and the
important distinction between detected cues and invented accompaniment.

**Next:** collect seed-recognition, musical-appeal and difference/similarity feedback.
Then test unfamiliar recordings and expressive arcs. This remains a seen-source
experiment; preserve the open question of automatic dynamics and intentional endings.
