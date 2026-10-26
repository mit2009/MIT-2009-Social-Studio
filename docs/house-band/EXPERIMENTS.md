# House-band experiments — reproducible proposals

**Status:** Danny has reviewed the research and started a bounded listening session with a new recording. Initial melody/dynamics checks and a three-candidate audio-only E01/E02/E04 pilot have been rendered. The pilot adds accompaniment and uses one seed; it is not the six-item solo control specified below. Listening review rejected the pilot for insufficient sound quality; do not generate more sampler variants as the next step. A single [E11 MRT2 performance trial](MRT2-TRIAL.md) received positive sound-quality feedback, followed by a request for stronger seed recognition. Two tighter-control comparisons have rendered. Danny confirmed that both work as choices and feel connected to the original seed; the other experiments remain unrun. They do not authorize building the complete application or selecting a permanent architecture. Return to the [research brief](README.md) for rationale and the [inventory](INVENTORY.md) for each dependency's license/platform notes.

## Audio-only interpretation requirement

The eventual student flow is record, hear interpretations and choose. Musical coaching and transcription approval must not be prerequisites. See [the audio-only test protocol](AUDIO-ONLY-INTERPRETATION.md). The hand-shaped crescendo is a development reference, not evidence of automatic interpretation.

## Common laboratory procedure

1. Work in a separate experiment directory or branch of the current project. Never mutate originals, the accepted melody or previous renders. Reuse existing decoding/mastering where useful, but do not modify the production provider or its exact-fidelity tests. New adventurous musicians need their own declared contract.
2. Read `inventory.json` and `sources.json`. Clone only the needed repositories, check out recorded commits, and initialize required submodules. Build a separate virtual environment/container per incompatible runtime. A commit pin is not a complete environment lock: record the resolver result, Python/native library versions, OS/CPU, plugin versions and assets after installation.
3. Every checkpoint/sample must have source URL, revision/hash, size and applicable terms in `assets.json`. Do not equate a code license with weight rights. If a selected asset's terms are unresolved, record the gate and choose a cleared alternative; do not silently download another model. This research did not accept gated model terms or install weights.
4. Preserve full input audio and generate analysis copies at each analyzer's expected sample rate. The 15-second output limit does not mean silently discarding all useful input after second 15. For this first run use the already accepted score; later choose/log an excerpt or an explicit time mapping.
5. Use `experiment-plan.json` for common output settings, seeds and parameter grids. Each run gets a fresh folder. Keep a `source_map` connecting original seconds, canonical seconds and transformed seconds. Save intermediate notes/curves/slices even when output is bad.
6. Save `candidate.wav`, optional stems, `events.json`/`source_map.json`, `run.json`, `checks.json` and `listening.json`. Never write invented listening scores. Do not automatically rate/select/approve candidates in Danny's working project.
7. Render offline. Disable network access after initial setup to check that there is no generation-time service dependency. Log API cost as zero only if no billable API is called; compute time, memory and disk use are separate resource costs.
8. Master to 48 kHz stereo, exactly `round(project.duration_seconds * 48000)` sample frames. V1 is 15.0 seconds/720,000 frames. Fit the musical ending inside that window; do not routinely chop off a long generated take and call it a finished composition. Keep an unmastered diagnostic when trimming/fading is necessary.

### Proposed run manifest

This is a file contract for experiments, not a new production schema:

```json
{
  "experiment_id": "E04",
  "project": {"duration_seconds": 15.0, "sample_rate": 48000, "channels": 2},
  "input": {"source_sha256": "record-at-run-time", "guide_sha256": "record-at-run-time", "analysis_variant": "accepted-guide"},
  "source_revisions": {},
  "environment_lock": "requirements-resolved.txt",
  "asset_manifest": "assets.json",
  "seed": 2009,
  "parameters": {},
  "preservation_policy": "motif-and-contour",
  "source_map": "source_map.json",
  "render_engine": "record-exact-version-and-patch",
  "elapsed_seconds": null,
  "peak_memory_bytes": null,
  "api_cost_usd": 0,
  "output_sha256": null,
  "technical_status": "not-run",
  "listening_status": "not-reviewed"
}
```

## Smallest first audition: E01 + E02 + E04

The original proposal used the accepted 31-note guide with SHA-256 `a8c22205bf1498fd1dace47777dac56820392e410c3a3c23f618e63bb0c16c0e` (score `44ba4997011855b25af51ab19989507786b54db7f6b224350823f94257143449`). Danny explicitly replaced that input with a new recording during the listening session. Use the new session's saved input manifest; do not revert to the old recording or infer acceptance of a guide from its being the newest file. The new detected notes and dynamics remain under development. For the next audio-only test, analyze the original recording afresh without feeding in hand-shaped guides or feedback. Keep score-only renderer comparisons labeled separately from end-to-end interpretation tests.

Use the existing local renderer and one unchanged lead patch across all three methods, with the same mix/mastering target. Use seeds **2009** and **2010**. Produce six candidates, retain the existing guide as reference, and randomize audition order. No new model download, student UI or server needed. The faithful player's seeds may change dynamics slightly while keeping all note times/pitches. Musical differences between E02 and E04 must be structural, not merely different random velocity or instrument settings.

Implement only a small file-to-file experiment driver. Suggested flow, not an existing executable command:

```text
load and verify accepted score
for musician in faithful, groove, motif:
    for seed in 2009, 2010:
        transform a copy using the recipe below
        render with the same existing lead patch
        measure and save a new 15-second result
present six anonymous auditions with the original guide available
```

Record separate 1–5 listening judgments for recognizable contribution, musical interest, desire to replay and difference from the other candidates. Also allow “none of these” and free-form remarks. This is a tiny design probe, not a statistical student-preference study. Decide whether to refine musical behavior, improve timbre, or explore the next musician; do not deploy on the strength of one successful input.

## E01 — Faithful player

**Question:** How expressive can a careful performance of the accepted idea sound before we alter its composition?

**Inputs/tools:** accepted note list and optional loudness curve; current recorded/synthetic bank initially. Later compare the *same* events through FluidSynth/Surge/SuperCollider to isolate renderer quality. No analysis model needed.

**Recipe:** remove only the initial wait; preserve all pitches, order and relative onsets. Cap each release before the next conflicting note; permit instrument-specific tails. Assign phrase-start accents of +6 MIDI velocity and seed-dependent variation bounded at ±4. Do not quantize, retune or add a stock backing track. For the first controlled comparison use one lead sound without new accompaniment.

**Variants:** seeds 2009/2010; renderer comparison is a later separate axis. **Outputs:** melody-only stem, exact event map, master. **Pass:** event equality to accepted score except removed origin; source hashes unchanged; immediate sound; no clipping. **Learning/failure:** a robotic result here indicates articulation/rendering problems, not failed melodic extraction. **Compute/integration:** already available Mac CPU; low. **Gate:** existing asset manifest. **Worth first trial:** yes.

## E02 — Groove translator

**Question:** Does giving a loose phrase a stronger rhythmic shape make it more engaging while still feeling authored by the student?

**Inputs/tools:** accepted events, onset confidence, optional tempo hypotheses; NumPy/pretty_midi or isobar. Keep E01's renderer.

**Recipe:** for the first audition use 120 BPM and a half-beat grid. Move each onset 50% toward its nearest grid point; resolve collisions in source order with at least 30 ms separation. Adjust note-offs to preserve articulation without overlap conflicts. Retain all pitches. For the second seed use the same grid but place the second eighth of each beat at a 0.60 beat swing position before the 50% interpolation. Map every shifted onset back to its source event. Keep a free-time control.

**Later grid:** 100/120/140 BPM × straight/swing × strength 0/0.5/1.0. These are interpretations, not claims about the original BPM. Fit the ending to the fixed 15 seconds without globally speeding an already fitting phrase unless explicitly logged.

**Pass:** monotonic note order, legal note lengths, no unintended deleted notes, recorded time warp. **Listening:** groove and recognition, not exact timing equality. **Failure:** a quantized phrase that loses its characteristic pickup or breath. **Compute/integration:** Mac/Linux CPU, low. **Gate:** no new model. **Worth first trial:** yes.

## E03 — Reharmonizing trio

**Question:** Can different harmonic interpretations make the same melody feel warm, tense or unexpectedly playful?

**Inputs/tools:** note events, optional key hypotheses; music21 plus custom search; MMA as an alternate accompaniment backend.

**Recipe:** divide into phrase-aware harmonic windows, initially 2 seconds. Evaluate major/minor triads and selected seventh chords across all roots, retaining the top three paths with dynamic programming. Score weighted melody-note compatibility, common tones and modest bass movement; do not assume C major or force all chromatic notes into a scale. Use explicit weights (1.0 compatibility, 0.25 common-tone reward, 0.10 per semitone bass-motion cost) as an initial experimental recipe, not musical truth. Add bass on window entrances and sparse inner voices in rests. Keep the melody unchanged.

**Variants:** stable triads; seventh-chord color; one deliberate contrasting chord followed by resolution. Use identical tone patches to compare harmony. **Pass:** lead unchanged; bass/inner voices in declared ranges; no dropped final note. **Failure:** short notes drive rapid chord switching, voice crossing or inappropriate confident key labels. **Compute/integration:** CPU, medium custom work. **Gate:** use own chord rules, not an unreviewed score corpus. **Next alternatives:** AccoMontage2 only after its external data/checkpoint terms are resolved; JJazzLab for manual accompaniment comparison.

## E04 — Motif improviser

**Question:** Does developing a small fragment feel more like a band engaging with an idea than playing it once with accompaniment?

**Inputs/tools:** accepted events; small custom/isobar rules first; Notochord is an independently labeled comparison, not secretly mixed into this recipe.

**Recipe for the first audition:** choose the opening three reliable notes as motif A. Preserve their relative pitch intervals and normalized inter-onset ratios. Build a 15-second form: recognizable opening from 0–4 seconds, motif repetitions/sequences from 4–9, an answering transformation from 9–13, and a final held source note plus decay from 13–15. Seed 2009 repeats then sequences the motif up a diatonic step only if a key hypothesis is reliable; otherwise transpose by two semitones and label it. Seed 2010 inverts the motif intervals around its first pitch for the answer, then returns to its original final interval. Bound pitches to the renderer's usable range and keep at least one literal motif statement.

**Notochord follow-up:** use the pinned repository's `Notochord.feed`/`sample` API and `simple_harmonizer` example, feed source note-on/off events, constrain pitch/instrument ranges, and cap generated events and time. Archive the exact checkpoint terms/hash before use. No MIDI loopback or paid DAW required for an offline adapter. [Official API/example](https://github.com/Intelligent-Instruments-Lab/notochord).

**Pass:** deterministic rule output for fixed seed; mapping for literal/transposed/inverted notes; intentional ending. **Failure:** endless repetition or an unrelated solo. **Compute/integration:** first recipe CPU/low; Notochord medium and CPU-neural. **Worth first trial:** yes.

## E05 — Tap-to-band drummer

**Question:** Can someone with no pitched input still hear that they made a musical idea?

**Inputs/tools:** tapping/clapping/beatboxing fixture; librosa/aubio onset times and energy; existing synthesized percussion, later Hydrogen as comparator.

**Recipe:** detect attacks with 50 ms minimum spacing, preserve relative accents, and derive at most three tempo hypotheses from inter-onset intervals. The first option keeps attack times; a second aligns them halfway to a grid; a third uses a Euclidean 3-of-8 or 5-of-8 answering pattern in gaps. Map stronger/lower-spectrum attacks to kick, contrasting attacks to snare and small replies to hats. This mapping is heuristic, not a claim to recognize drum classes. Add a one-note bass response at selected accents if useful; never fabricate a transcribed melody.

**Pass:** every literal drum attack links to a detected tap; rhythmic-only input succeeds with no pitch array. **Failure:** machinery triggers a dense false beat, or tempo is reported confidently from too few attacks. **Compute/integration:** CPU, low–medium. **Listening:** recognizable rhythm, groove and agency. **Assets:** synthesized hits first, then explicitly licensed drumkit comparison.

## E06 — Phrase memory player

**Question:** Can a lightweight sequence-memory musician make interesting continuations without a pretrained large model?

**Inputs/tools:** Dicy2 Python plus a small corpus built from the student's own analyzed fragments; use 2–5-note chunks labeled by interval contour and duration class.

**Recipe:** segment at rests or change points; retain source IDs. Start with the literal first fragment, then request 8–12 seconds of guided recombination using shared contour/ending labels, disallow immediate repeat more than twice, and close with the original ending. Compare constrained scenario-following with a freer sequence. If the source has only one or two usable fragments, report insufficient memory and do not pretend the corpus was rich.

**Entry point:** pinned Dicy2 README's example scripts and OSC/server documentation; initialize its submodule. The Python core does not require purchasing Max or Ableton. Render event output separately. [Dicy2 Python](https://github.com/DYCI2/Dicy2-python).

**Pass:** every selected fragment traces to the local corpus; no tutorial musician recordings imported. **Failure:** a repetitive loop that adds no development. **Compute/integration:** Mac CPU, medium–high; Linux portability must be tested. **Gate:** GPL core obligations; external demo assets excluded.

## E07 — Granular sculptor

**Question:** Can tiny pieces of the idea become a playable rhythmic texture while retaining its contour or pulse?

**Inputs/tools:** voice-free canonical guide initially, or nonvocal taps; SuperCollider/Csound/pyo. Avoid raw sung words in the default experiment.

**Recipe:** grains of 40/80/120 ms, Hann envelopes, overlap densities 10/25 grains per second, bounded stereo spread and source-position jitter. Compare chronological scan, onset-locked scan, and reversed grain order while retaining an occasional forward motif. Grain pitch follows the contour for one variant; another uses octave-related transpositions. Reserve a 0.5-second decay and cap simultaneous grains at 32.

**Pass:** finite output, no boundary clicks, deterministic scheduling, logged source positions. **Failure:** loudness disguises sameness, source identity vanishes, or raw-vocal words remain recognizable. A speech recognizer cannot certify unintelligibility; listen. **Compute/integration:** CPU, medium. **Why unusual:** the student's sound structure becomes an instrument without requiring successful MIDI extraction.

## E08 — Mosaic orchestrator

**Question:** What if a band reconstructs the gesture using many small acoustic sound fragments instead of translating everything into notes?

**Inputs/tools:** guide audio or nonvocal source; FluCoMa core/CLI or SuperCollider binding; a small selected CC0 instrument corpus.

**Recipe:** segment target at attacks and novelty boundaries, minimum 60 ms. Extract RMS, spectral centroid and pitch where reliable. Standardize features within the corpus; retrieve nearest 3/5 candidates using a pitch-heavy metric for tonal segments and spectral/energy features for unpitched segments. Schedule matched fragments at target onsets with 10 ms fades, allow at most two overlapping layers initially, and penalize repeating the same sample more than twice. Compare exact nearest match with seeded choice among five neighbors.

**Artifacts:** target slices, descriptors/scaler, corpus manifest, selected fragment map, isolated layers. **Pass:** reconstructable sample choices, bounded overlap, no unlicensed corpus. **Failure:** mismatched dynamics or pitch dominates; note-free signals should not be forced to tonal matches. **Compute/integration:** Mac/Linux CPU, medium. **Gate:** source/sample rights. **Alternate:** AudioGuide studies the same family but remains on hold until licensing/dependencies are established. [FluCoMa developer documentation](https://develop.flucoma.org/).

## E09 — Physical instrument builder

**Question:** Can the shape of a student's gesture excite a satisfying new instrument rather than imitate a keyboard patch?

**Inputs/tools:** pitch/onset/loudness curves; Faust or Csound physical/resonator modules; optional DawDreamer renderer.

**Recipe:** map pitch to a plucked-string or resonator-bank frequency, onset strength to excitation amplitude and loudness slope to damping. Compare three material settings: short wooden pluck, bright metallic resonance, soft sustained resonator. Use source onset times first, then let its attacks excite an octave-related countervoice. Bound decay and feedback; use a limiter as a guard, not to hide unstable DSP.

**Pass:** stable output across silence, loud impulses, extreme pitch and repeated attacks; source-controlled parameters logged. **Failure:** ringing masks phrasing, or a new timbre merely repeats the same flat line. **Compute/integration:** CPU, medium–high. **Gate:** pin Faust library/module and its license, not just compiler license. **Learning:** tests synthesis design independently of a large music model.

## E10 — Timbre shape-shifter

**Question:** Can continuous pitch and dynamics carry expression that discrete notes lose?

**Inputs/tools:** clean/optional-cleanup f0 and loudness curves, original audio retained separately. First DDSP pretrained monophonic instrument; then RAVE as a separately labeled latent-transform trial, or AFTER's structure/timbre notebooks.

**Recipe:** DDSP preserves a continuous f0 trajectory within the target model's range, comparing raw pitch with gentle correction only when a tonal hypothesis is credible. Record every shift/normalization. RAVE receives guide or nonvocal audio and tests small latent perturbations, with reconstruction as its control. AFTER uses the guide as structure and a cleared CC0 timbre example; begin from upstream audio-to-audio/MIDI notebook, not a commercial-host patch. These are sub-experiments with distinct manifests, not interchangeable models.

**Pass:** no hidden vocal mixing; curves/latent settings saved; input/control duration map retained. **Failure:** model erases attacks, turns noise into voice-like artifacts, or loses recognizable contour. **Compute:** DDSP/RAVE pretrained inference may run on CPU; AFTER documents MPS. New training belongs on a separate GPU lane. **Integration:** medium–high. **Gate:** DDSP checkpoint terms; RAVE/AFTER NC licenses require a scoped research decision before use. [DDSP demos](https://github.com/magenta/ddsp), [RAVE offline usage](https://github.com/acids-ircam/RAVE), [AFTER notebooks](https://github.com/acids-ircam/AFTER).

## E11 — MIDI-following neural band

**Question:** Can a local audio model make a richer ensemble while being given the actual notes rather than just a style description?

**Inputs/tools:** canonical note events → Magenta RealTime 2 small; use its official note-control example. Keep voice-free guide as a listening reference.

**Recipe:** start with `mrt2_small` (230M), fixed seed and a neutral instrumental style. Map note states at the model's 25 Hz frame rate: off, sustain and onset; follow the pinned model card's values and example implementation. Compare strict note conditioning with a relaxed/partially masked condition. Generate 375 model frames for 15 seconds, allow codec padding internally, and save the alignment/crop. First compare two musical treatments with the same conditioning, then compare small/base only if memory/runtime justify it. Audio embeddings influence style and are not substituted for the MIDI condition.

**Setup direction, not a completed install:** isolated Python 3.12; official `magenta-rt[mlx]` package or the pinned source commit; `mrt models init` and model selection documented upstream. Use `examples/jam`/the note-control implementation to wire MIDI. The documented text-only `mrt mlx generate` command is merely an installation smoke test and does not complete this experiment. Do not invent a CLI MIDI flag. Record downloaded model/resource revisions and hashes. [README](https://github.com/magenta/magenta-realtime), [model contract](https://github.com/magenta/magenta-realtime/blob/main/MODEL.md), [models](https://github.com/magenta/magenta-realtime/blob/main/docs/models.md).

**Pass:** correct MIDI-frame alignment and local execution; measured latency/memory; no voice output accepted without review. **Failure:** impressive background music unrelated to the input, or a cutoff instead of an ending. **Compute:** Apple Silicon integrated GPU; NVIDIA Python alternative. **Gate:** Apache code, CC-BY model weights and model-card terms. **Integration:** medium–high. **Status:** promising research candidate, not previously benchmarked here.

## E12 — Free cover artist

**Question:** Does a more adventurous audio-to-audio performer produce useful surprises beyond the symbolic methods?

**Inputs/tools:** E01's instrumental rendering as source audio; ACE-Step 1.5 in source/cover mode, not reference-style-only conditioning. Do not send raw sung words by default.

**Recipe:** choose one documented cover-capable small DiT variant from the pinned model table; fix duration at 15 seconds and request instrumental output. Compare source preservation strengths 0.4/0.7/0.9 only if the selected mode exposes a corresponding control; otherwise record the actual supported control and do not invent a parameter. Use seeds 2009/2010 and the same source. Listen for phrase recognition, development and unwanted vocals. Log the exact source field, task type, model and conditioning controls.

**Reproduction entry:** pinned `docs/en/INFERENCE.md` and model capability table; isolate its environment and checkpoint cache. Source audio and reference/style audio are separate concepts in this system. A generative mode that ignores source audio is not a valid completion of E12. [ACE-Step 1.5](https://github.com/ace-step/ACE-Step-1.5), [inference guide](https://github.com/ace-step/ACE-Step-1.5/blob/main/docs/en/INFERENCE.md).

**Pass:** input conditioning demonstrably enabled; source/output manifest; fixed duration; no network generation call. **Failure:** unrelated genre music, recognizable sung words, unstable memory, or six near-duplicates. **Compute:** Apple MLX trial; Linux GPU for throughput; no claim of a fixed RAM/VRAM minimum across variants. **Gate:** exact DiT and optional LM model cards. **Integration:** medium–high. **Comparison:** MusicGen Melody is a later server control with NC weights, not an additional required dependency.

## Analysis stress test, after the first musical audition

Use twelve locally stored, consented/original fixtures: two clean pitched gestures; two deliberately off-key/loose versions; two whistles/glissandi; two tap-only rhythms; two versions with stationary machinery noise; one reverberant phrase; one with overlapping conversation. Existing private song-based input remains a regression fixture, not a public demo.

For controlled perturbations of known clean fixtures, compare clean/raw/noisereduce branches at +20/+10/0 dB SNR, plus separately generated reverberation and volume changes. Do not combine every impairment at once initially. Run pYIN and Basic Pitch first; add torchcrepe/PESTO only when their independent contour may resolve a failure. Run onset extraction on every fixture, even when no reliable pitch exists. Test a silent/noise-only negative control and permit “no reliable melody.”

Measure voiced/unvoiced errors, octave errors, onset precision/recall within a stated tolerance, and note F1 where ground truth exists. Inspect contour errors in cents separately from note segmentation. For tap input, use onset/rhythm measures, not pitch metrics. Denoising succeeds only if it improves the relevant extraction or listening result without removing the gesture. Quantization/tuning are optional interpretations; never overwrite raw estimates.

## Technical checks for each audition

- Finite stereo samples, exactly 720,000 frames at 48 kHz; files decode independently.
- No sample clipping; measure true peak with FFmpeg or an equivalent oversampled meter, aiming at or below −1 dBTP. Target comparable loudness around the current −18 LUFS, while preserving intended dynamics and rejecting silence/noise masquerading as music.
- Meaningful signal in the first 100 ms when the source begins immediately. If an intentional pickup/rest is preserved, label it; do not add a decorative intro before every student's idea.
- First/last transitions inspected for clicks, abrupt crop and release tails. A correct duration alone is insufficient.
- E01/E03 exact lead preservation; E02 logged monotonic timing map; E04/E06 motif provenance; E05 rhythmic provenance; E07/E08 source-slice lineage; E09 control curves; E10–E12 model/input/conditioning traces.
- Same seed/config produces the same event plan for deterministic musicians. Neural/device audio may vary; record that boundary rather than promising bit-identical output.
- CPU time, wall time, peak memory, asset disk size and failures recorded. No throughput claim inferred from upstream marketing benchmarks.
- Listening stays human: recognition, musical interest, movement/groove where intended, contrast, undesirable vocals and “would keep.” Technical checks never auto-approve a piece.

## Outcome sheet

| Experiment | Install/environment lock | Input and seed | Technical result | What remains recognizable | What surprised us | Keep / revise / drop | Listener/date |
|---|---|---|---|---|---|---|---|
| Not run | — | — | — | — | — | Awaiting Danny's review | — |

An experiment is successful if it teaches us something specific—even if the musician is dropped. The first decision is which bounded audition to run, not which architecture to commit to.
