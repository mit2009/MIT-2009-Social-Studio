# Orchestration sweep and portable listening pack — September 23, 2026

Six real MRT2 outputs passed 15-second/48 kHz/stereo, finite-sample, immediate-start,
peak and source-integrity checks. Their note-control arrays and source-time maps
match B exactly; all raw model peaks are below full scale. Four control tests passed
in 2.60 seconds. Ruff, JavaScript syntax and diff checks passed. The earlier full
47-test result was not rerun for these isolated experiment and packaging scripts.

Eleven MP3 listening copies were decoded and checked; all nine orchestrations
retain exactly 15 seconds, with no full-scale decoded samples and true peaks below
0 dBTP. ZIP integrity and member equality passed. Source and earlier masters are
unchanged. Chrome showed all eleven playable files with no media errors; D/E
playback, A-to-B pausing, and desktop layout were checked. The built-in preview
crashed twice; Chrome worked. Feedback export displayed its prepared message, but
actual downloaded-file receipt was not verified. All test form input was cleared.
No new human ratings or selections were assigned.

See [the reproducible trial](house-band/MRT2-TRIAL.md) and private sweep verification
for measurements. Listening quality, recognition in the new styles, exact
instrumentation, phone-browser behavior and results on unseen sources remain open.

---

# Third MRT2 style comparison — September 23, 2026

Four melody-control tests passed in 1.27 seconds after adding an internal style
argument. Ruff and diff checks passed. A real render exercised the argument and
verified a 15-second, 48 kHz stereo export with a 5 ms audible start, −18.85 LUFS
and −1.00 dBTP. C's note-control array and source-time mapping are identical to B.
Original/source and all earlier audio hashes remain unchanged. Raw model audio
contains 22 full-scale channel samples out of 1,536,000; passing final peak checks
does not prove that model distortion is absent. C's listening evaluation is pending.
See [the trial notes](house-band/MRT2-TRIAL.md) for exact reproduction and diagnostics.
The existing 47-test full-suite result below predates this small style argument.

---

# MRT2 performance-engine audition — September 23, 2026

47 tests passed in 50.84 seconds. Two existing upstream deprecation warnings
remain. Four MRT2 control tests check note onsets, holds, releases, accompaniment
registers, connected-note articulation, identical closer-profile controls and
lead-profile interval/timing preservation after automatic octave placement.

The first model import failed with MLX 0.32.2. Matching upstream's 0.31.2 pin
resolved it; logs for both attempts are retained. One real MRT2 base render
passed 15-second/48 kHz/stereo, finite-sample, true-peak, audible-start and source
integrity checks. Actual measured true peak is -1.85 dBTP and loudness -17.99 LUFS.
Generation uses a separate local runtime with Python network connections blocked.
See [the reproducible trial](house-band/MRT2-TRIAL.md) for model/license pins,
method, limitations and artifacts. The reference received a positive sound-quality
result, with source recognition still needing improvement. Two new 15-second
comparisons passed export and source-integrity checks. Listening evaluation retained
both as viable interpretations with recognizable source material for this recording. Measured true peaks are −1.00 and
−4.61 dBTP, with audible starts near 5 ms. Raw A contains three full-scale samples;
B contains none. These diagnostics do not establish perceived sound quality.
The original reference and source hashes remain unchanged.

Listening review rejected the previous three sampler auditions for insufficient sound quality.
Their earlier technical success is not a musical success or creative approval.

---

# Audio-only house-band pilot

43 tests passed in 29.60 seconds for the isolated experiment, including five new
checks for rising/falling/steady expression cues, source-event preservation,
structural differences, deterministic plans and alternate project durations.
Two existing upstream deprecation warnings remain. The app code is unchanged.

The real three-candidate batch completed in 4.877 seconds on the current Mac.
Each output is a distinct 15-second, 48 kHz stereo WAV with immediate audible
signal and measured true peak below -1 dBTP. Source, normalized audio, initial
guide and prior corrected-guide hashes remain unchanged. Analysis and rendering
use no feedback text, manual crescendo or supplied climax timestamp. One seed
and one common guitar lead were used. This is a development example, not an
unseen-input test; musical arc, fidelity and ensemble quality require listening.
The run, stems, used samples and verification records are retained under the
private experiment folder. See [reproduction instructions](../experiments/README.md).

---

# Upbeat, no-piano audition revision

38 tests passed in 44.19 seconds on September 22, 2026; Ruff and JavaScript syntax checks passed. Two existing upstream test-client deprecation warnings remain. New checks cover the three distinct lead instruments, exact accepted pitch/onset preservation, absence of piano, replies fitting rests, bounded event timing, deterministic finite electronic voices, and synth tuning. The full API/export regression uses synthetic instrument fixtures and does not establish real-instrument quality.

The expanded catalog was installed and its files hash-verified. Separate waveform spot checks found guitar MIDI 59.01 against expected 59, trumpet 60.03 against 60, trombone 58.00 against 58 and plucked violin 59.81 against 60. These do not certify every recording or perceived tuning.

The actual three-draft batch finished in 4.717 seconds with zero API cost. Independent checks found three distinct 15-second, 48 kHz stereo masters, finite samples, no clipping, immediate audible signal and all 31 accepted lead pitches/onsets preserved. No arrangement contains piano events. Original, normalized-source, accepted-score and guide hashes remain unchanged. The saved report is under ignored `data/verification/upbeat-hooks/report.json`; stems and scores are beside each render.

The embedded browser displayed Club bounce, Indie dance and Brass bounce with 15-second players. Club bounce playback advanced without a media error. Ratings, selections and approval remain unset by the assistant. Technical checks cannot establish fun, professional musicianship or college-student appeal; those require listening review.

---

# Recorded-instrument quality revision

Listening review rejected the first model drafts because sound quality did not meet the target. The revised engine performs the accepted note score with a recorded grand piano and independently written accompaniment. It does not treat the earlier passing technical tests as evidence of satisfactory sound.

34 tests passed in 30.11 seconds on September 22, 2026; Ruff and JavaScript syntax checks passed. Four new tests cover exact lead pitch/order/onset preservation across all three styles (including a note near the end), sample pitch shifting, rejection of changed samples and score files, and the complete three-draft API/export path. CI uses explicitly synthetic instrument fixtures and makes no claim about real acoustic sound quality.

The actual pinned libraries were installed and checked separately. Measurement caught a one-octave naming difference in the cello and bass libraries, which was corrected in the catalog. A quiet bass take with an unstable attack was excluded. Final piano/violin/cello/bass spot checks measured MIDI pitches 60.038, 59.939, 39.974 and 40.026 respectively against expected 60, 60, 40 and 40. These are spot checks, not a complete perceptual evaluation of the library.

The final live batch completed in 3.884 seconds. All three outputs preserve the 31 accepted lead notes and relative onsets, are distinct 15-second 48 kHz stereo WAVs, start with audible signal, remain below clipping, and match their recorded hashes. The original recording, normalized source and accepted guide hashes are unchanged. Measurements, stem files and arrangement scores are under ignored `data/verification/recorded-ensembles/` and `data/candidate-engine/renders/`. The embedded browser displayed all three new cards, and Piano & strings playback advanced without a media error. Ratings, selection and approval were not set by the assistant.

Naturalness, harmony, phrasing and ensemble quality still need Danny's listening review. The heuristic accompaniment and sample articulation are material limitations; see LOCAL-MUSIC.md.

---

# Free local ensemble milestone

30 tests passed in 27.20 seconds on September 22, 2026. Ruff and JavaScript syntax checks passed. The two new ensemble tests exercise the real subprocess/file boundary with a clearly identified stand-in: exactly three choices, only the synthesized guide passed to the renderer, offline settings, guide integrity, zero API cost, unchanged originals, and no automatic creative decisions. Those tests run without model weights on CI and do not establish musical quality.

A separate live run used the pinned Stable Audio 3 Medium model and official MLX runtime on Danny's Mac. All three drafts finished in 14.459 seconds total: bass-heavy dance 7.189 seconds, chamber trio 3.686 seconds, and jazz trio 3.560 seconds. This is one observed run, not promised latency. No account, paid request or recording upload was used.

The three distinct exported WAVs were independently checked: 15 seconds, 48 kHz stereo, finite samples, peaks below clipping, audible signal in the first 100 ms, matching artifact hashes, and the accepted guide's hash in every render record. The original recording and normalized source hashes were unchanged. Private measurements and render logs remain under ignored `data/verification/local-ensembles/` and `data/candidate-engine/renders/`.

The embedded browser displayed three ready cards with play/rating/download controls, retained the reference and melody players, and kept the retired experiments collapsed. Dance playback advanced without a media error; all three players loaded 15-second durations. Ratings and approval were left untouched. Musical fidelity, instrumental-only output, and convincing ensemble performance still need listening review; technical checks cannot prove them.

---

# Immediate playback update

28 tests passed in 23.99 seconds on September 22. Added checks for soft opening notes, internal rests, unchanged originals/15-second masters, cached listening copies, byte-range playback and actual candidate preview endpoints. The melody API test now includes room noise before the phrase. Ruff and JavaScript syntax checks passed.

Danny's current reference preview skips 2.864 seconds; the melody preview skips about 2.939 seconds. Both contain substantial audio in the first 100 ms. The local measurement report is under ignored `data/verification/playback/`. Reference and melody Play controls, shorter player durations, and switching between tracks were verified in the embedded browser. One browser tab crashed during automation; a fresh tab successfully played both files. These checks establish playback behavior, not professional orchestration quality.

---

# Earlier music/Connect preparation milestone

25 tests passed in 20.77 seconds on September 22, including four new melody checks: recovery of a known eight-note phrase and timing, rejection of noise, synthesis from only notes/timing, and API persistence/caching with the old voice-effects route disabled. Code and JavaScript syntax checks passed. The existing 21 tests retain coverage of the earlier DSP and downstream media infrastructure; they do not establish professional orchestration quality.

The Connect logo/palette/Outfit preview and preparation of Danny's melody were exercised in the in-app browser. Its guide appeared and earlier experiments remained collapsed in history. The original graphics ZIP's seven icons and Outfit font match the existing kit byte-for-byte. No live model, paid request, ensemble performance or human approval has been tested or generated in this milestone.

The current `scripts/browser_smoke.cjs` tests the melody/Connect preview against a disposable local server, generates a synthetic sample, checks the single-input interface and three planned ensembles, prepares a guide, reloads saved work and checks desktop/narrow layouts. Use the setup below. The older full four-stage browser script and report remain preserved at `0cfe313`; the historical results below describe that version.

---

# Testing and observed results

## Everyday checks

Install from the root README, with FFmpeg and FFprobe on PATH, then run:

```sh
.venv/bin/python -m pytest -q
.venv/bin/ruff check .
```

The suite uses temporary data, creates its own sound/images, and does not alter working projects or call a paid provider. Tests exercise rules and exported media, rather than only checking that rendering functions returned successfully.

| Coverage | Evidence checked |
|---|---|
| Workflow | Distinct families; single Keyword; fixed duration; valid stars; rate before select; complete batches before approval; cross-project input rejection |
| Accountability | Rating history; retained five-star winners; no approval from a rating; explicit explanation/confirmation; immutable snapshots and export hashes |
| Persistence | Reopen the database; retain artifacts/history after upstream changes; invalidate affected downstream selections |
| Jobs | Single-worker lock; interrupted-job recovery; completed candidates retained; explicit retry; recorded rendering failures |
| Media | Real 15-second audio/video/alpha text/final outputs in both orientations at reduced test dimensions; 450 frames at 30 fps; 48 kHz stereo; actual transparent and opaque pixels |
| Audio | All nine styles produce finite audible output; Original Mix preserves the source excerpt; supplied bed/effect change the mix |
| API | Local Host/Origin and mutation-header checks; invalid file/setting rejection; failed uploads leave no asset record |

GitHub Actions runs the Python checks on Ubuntu with Python 3.12 and FFmpeg. It does not run the optional browser test or claim subjective creative quality.

## Optional browser test

The current browser test prepares a note-only melody guide and does not rate, approve, export or call a cloud provider. Always use the disposable data directory below. The earlier full workflow test is preserved in Git history as described above.

In one terminal:

```sh
.venv/bin/python -m mit2009_studio.server --port 8774 --data-dir data/verification/studio
```

In another:

```sh
npm ci
npx playwright install chromium
node scripts/browser_smoke.cjs
```

An already installed Google Chrome can be used with `STUDIO_CHROME=1 node scripts/browser_smoke.cjs`. Node/Playwright are optional verification tools, not application runtime requirements. The default test creates a synthetic practice project.

Optional environment settings:

- `STUDIO_TEST_URL`: disposable server URL; default `http://127.0.0.1:8774`.
- `STUDIO_QA_OUTPUT`: report/screenshot directory; default `data/verification/browser`.
- `STUDIO_TEST_AUDIO`: supported by the historical full-workflow script only.
- `STUDIO_TEST_PHOTOS`: supported by the historical full-workflow script only.

Inspect the resulting media yourself. Numerical checks cannot establish legibility across every photograph, aesthetic difference, musical suitability, or a satisfying story.

## Observed on September 22, 2026

- **21 tests passed** in 19.52 seconds on Danny's Mac. Ruff and JavaScript syntax checks passed. Two upstream Starlette/AnyIO test-client deprecation warnings remain; neither is a test failure.
- A complete full-resolution browser run with Danny's 19.712-second recording, three existing course photographs and CONNECT completed generation, rating, selection, all three final mixes, automated test approval, export and reload. It produced 13 candidates and no browser script errors. Desktop and 390-pixel layouts had no horizontal overflow; screenshots were inspected.
- In that one run, audio took 1.930 seconds, video 26.073, text 23.203 and assembly 17.704. These are observations for this Mac and input, not promised latency.
- The complete source recording remains saved. The generated candidates use its first 15 seconds. Private inputs, outputs and browser reports are under ignored `data/`, not in Git.
- Automated decisions are confined to the verification store. Danny's separate working project contains generated audio options but no automatic stars, selection or approval.
- The read-only HPR audit passed for all three repositories: their commits and tracked-file fingerprints matched the pre-work baseline.

A fresh temporary Git clone with a new Python 3.12 environment installed successfully from the pinned requirements. Dependency consistency, the command-line launcher and Ruff passed; all 21 tests passed again in 21.26 seconds. Full-resolution artifacts were independently probed: all 13 outputs are 15 seconds, all nine video/text/final files contain 450 frames at 1080 × 1920, alpha masters use ProRes, and the export hash matches its automated approval snapshot. The independent [GitHub Actions run](https://github.com/dannygoldfield/MIT-2009-Social-Studio/actions/runs/35749953362) passed on Ubuntu for implementation commit `9416a3c`, including installation, code checks and all 21 tests. The canonical Mac checkout was then confirmed running from `Projects/MIT-2009-Social-Studio`; all 164 pre-existing private files retained their original hashes. No learned model/provider, paid request, cloud deployment, student access control or subjective listening approval is claimed by these checks.
