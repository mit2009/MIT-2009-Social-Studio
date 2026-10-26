# Interpret the seed without musical coaching

Product requirement: Interpret the source recording automatically, without requiring musical coaching.

The intended student experience is **record → hear different interpretations → choose**.
Students should not have to name notes, describe a crescendo, specify a climax time,
approve a transcription, or explain an arrangement before receiving useful results.
Development listening checks are research tools, not mandatory student steps.
Optional reactions or another take are fine; uncertainty should normally yield
several plausible interpretations instead of a music-theory questionnaire.

## What the current trial establishes

The first note guide flattened dynamics. A subsequent audition used measured
per-note levels. A hand-shaped demonstration explicitly encoded a late build
and a short ending to explore an expressive arc.
That demonstration is a creative reference, **not successful automatic analysis**.
It has not been creatively approved. These development exercises did not train a model.
The private source, intermediate scores, render scripts and checks are retained
under the current session's ignored experiment directory.

## Next bounded test

1. Run a separate audio-only analysis entry point. Its only creative input is the
   recording, plus fixed project settings and a reproducible variation seed.
   Do not feed it feedback text, manual dynamics knots, a target climax second,
   a filename-specific rule, or the hand-corrected guide. Infer its own notes
   and expression cues. Preserve the untouched source.
2. Consider pitch movement, relative level, attacks, sustained notes, rests,
   phrase boundaries and the manner of ending together. These are proposed
   signals, not proof of an inferred emotional arc. Phone gain and room noise
   can make raw volume misleading. Keep uncertainty and alternative hypotheses.
3. Save the inferred contour and source-time mapping before rendering. Report
   source, trimmed-playback and arranged timestamps separately; skipping an
   opening wait must not be mistaken for moving a climax within the phrase.
4. Produce a small number of distinct interpretations from the same analysis.
   At least one should follow the inferred arc conservatively. Musicians may
   express a build through phrasing, rhythm, harmonic tension, register or
   ensemble density as well as loudness. Keep 15-second composition masters,
   immediate audible starts and intentional endings.
5. Freeze and hash outputs before comparison against development feedback.
   Judge whether the original gesture, overall build, climax and ending survive.
   Do not count a clipping check or exact note match as success at interpretation.

This recording is now a **seen development example**, not a blind or held-out test.
An audio-only rerun can demonstrate input independence but cannot prove generality.
Later test unfamiliar recordings with contrasting arcs, including a flat phrase,
a descending/relaxing phrase, a sustained swell and rhythm-only input. Deliberately
avoid applying the same late crescendo to every seed. Keep annotations outside
renderer inputs and evaluate those examples only after candidate generation.

## Passing the experiment

- No generation-time musical coaching, paid API, remote recording upload or
  per-recording code adjustment.
- Traceable audio-derived analysis, uncertainty and source-time mapping.
- Finite, unclipped outputs of the configured duration and unchanged originals.
- Listening evidence that input-specific expression survives, including examples
  whose story differs from the present recording. Human selection remains central.

A first [heuristic audio-only pilot](../../experiments/README.md) is now implemented and has rendered three candidates. It has no coaching input; successful interpretation of the intended arc is not validated.
Keep the architecture provisional. This requirement augments the existing
[experiment protocols](EXPERIMENTS.md); it does not authorize a complete app rebuild.
