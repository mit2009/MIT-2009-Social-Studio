# House band: inventory ranked by purpose

Verified September 22, 2026. This is a research inventory, not a list of tested integrations. See [the research brief](README.md) and [experiment protocols](EXPERIMENTS.md).

**Purpose priority:** 1 = start with this for its particular job; 2 = next useful alternative; 3 = targeted/specialist trial; 4 = defer, historical comparator or unresolved dependency. Equal numbers are peers, not a global ranking. One tool may appear under two purposes. Recommendations are engineering judgments, not benchmark results.

**Hardware planning profiles (estimates, not measured minimums):** CPU-light = modern laptop, roughly 8 GB RAM; CPU-neural = start with 16 GB RAM and one 15-second file, no training; Apple-neural = Apple Silicon trial, budget 16–32+ GB unified memory and checkpoint disk space; Server-neural = isolated Linux environment, initially budget 16–24 GB VRAM and 32 GB RAM, then measure the specific model. Where upstream gives a requirement, the entry overrides this planning estimate. Do not infer a GPU requirement from use of a neural network. This Mac reports arm64 and 48 GiB unified/system memory; no new tool has been benchmarked here.

**Maintenance method:** date is the latest default-branch commit, not a promise of support or meaningful feature development. Recent = within six months; intermittent = six to eighteen months; quiet = older. Archived is explicit GitHub status. Source snapshots record full commits and README/license blob hashes. Asset libraries may remain useful with old commits. Compatibility is documented or inferred as stated; untested is not unsupported.

**Licenses:** code, weights, datasets, samples and plugins are separate. NC/restricted weights are kept as conditional research options and are not described as permissive open-source components. Unknown terms stay unknown. Public downloadability is not a redistribution grant. No paid license or API is proposed.


## A. Optional cleanup and isolation

| Priority | Tool | Input | First use | Test decision |
|---|---|---|---|---|
| 1 | [noisereduce](#t01) | Audio | Cheap raw-versus-light-cleanup analysis branch. | Yes: compare against doing nothing. |
| 2 | [DeepFilterNet](#t02) | Audio | Stronger cleanup comparator for noisy singing. | Yes after raw baseline. |
| 2 | [RNNoise](#t03) | Audio | Low-cost machinery/noise reduction comparator. | Yes, optional speech-like singing branch. |
| 3 | [audio-separator](#t04) | Audio | Compare selected separation models behind one adapter. | Conditional: useful if isolation proves necessary. |
| 3 | [Demucs, maintained author repository](#t05) | Audio | Optional isolation when music masks the gesture. | Conditional: separation stress test, never mandatory. |
| 4 | [Open-Unmix](#t06) | Audio | Scientific separation baseline. | Later comparator; Demucs first. |

<a id="t01"></a>

### T01 · noisereduce

[Repository](https://github.com/timsainb/noisereduce) · [Reviewed README](https://github.com/timsainb/noisereduce/blob/51c85343d6fe7695f7641f96b6a8f9e7e66be59b/README.md) · [License evidence](https://github.com/timsainb/noisereduce/blob/51c85343d6fe7695f7641f96b6a8f9e7e66be59b/LICENSE)

**Purpose priority 1.** Stationary/nonstationary spectral gating. Input: Audio. Role: Cheap raw-versus-light-cleanup analysis branch.

**License:** MIT **Maintenance:** Quiet default branch; latest default-branch commit 2024-10-06.

**Hardware:** CPU-light. **GPU:** No. **Mac:** Yes; verify current arm64 package/build. **Linux/server:** Yes; suitable for a local batch worker.

**Limits:** Can remove weak harmonics and whistle energy; not speaker separation or dereverberation. **Integration:** Low: NumPy audio in/out. **Worth testing:** Yes: compare against doing nothing.

<a id="t02"></a>

### T02 · DeepFilterNet

[Repository](https://github.com/Rikorose/DeepFilterNet) · [Reviewed README](https://github.com/Rikorose/DeepFilterNet/blob/d375b2d8309e0935d165700c91da9de862a99c31/README.md) · [License evidence](https://github.com/Rikorose/DeepFilterNet/blob/d375b2d8309e0935d165700c91da9de862a99c31/LICENSE)

**Purpose priority 2.** Full-band speech enhancement using deep filtering. Input: Audio. Role: Stronger cleanup comparator for noisy singing.

**License:** MIT OR Apache-2.0 code; archive the chosen bundled model notices. **Maintenance:** Quiet default branch; latest default-branch commit 2024-10-17.

**Hardware:** CPU-neural. **GPU:** No. **Mac:** Upstream supports macOS; Rust/Python packaging needs a smoke test. **Linux/server:** Supported; training tested on Linux.

**Limits:** Not a guaranteed hum/whistle preserver; overlapping voices remain difficult. **Integration:** Medium: isolated Rust/Python runtime and model. **Worth testing:** Yes after raw baseline.

<a id="t03"></a>

### T03 · RNNoise

[Repository](https://github.com/xiph/rnnoise) · [Reviewed README](https://github.com/xiph/rnnoise/blob/70f1d256acd4b34a572f999a05c87bf00b67730d/README) · [License evidence](https://github.com/xiph/rnnoise/blob/70f1d256acd4b34a572f999a05c87bf00b67730d/COPYING)

**Purpose priority 2.** Small recurrent speech-noise suppressor in C. Input: Audio. Role: Low-cost machinery/noise reduction comparator.

**License:** BSD-3-Clause code; record downloaded model provenance separately. **Maintenance:** Quiet default branch; latest default-branch commit 2025-02-22.

**Hardware:** CPU-light. **GPU:** No. **Mac:** Yes; verify current arm64 package/build. **Linux/server:** Yes; suitable for a local batch worker.

**Limits:** Speech prior can suppress music; 48 kHz framing and model assets need handling. **Integration:** Medium: compile C and wrap frames. **Worth testing:** Yes, optional speech-like singing branch.

<a id="t04"></a>

### T04 · audio-separator

[Repository](https://github.com/nomadkaraoke/python-audio-separator) · [Reviewed README](https://github.com/nomadkaraoke/python-audio-separator/blob/bf1164aa0f1ee1d1d0ef0f09b315f7659fc06bab/README.md) · [License evidence](https://github.com/nomadkaraoke/python-audio-separator/blob/bf1164aa0f1ee1d1d0ef0f09b315f7659fc06bab/LICENSE)

**Purpose priority 3.** CLI/Python wrapper around multiple music-separation architectures. Input: Audio. Role: Compare selected separation models behind one adapter.

**License:** MIT wrapper; model licenses vary and must be recorded individually. **Maintenance:** Recent default-branch activity; latest default-branch commit 2026-08-27.

**Hardware:** CPU-neural. **GPU:** No for CPU models; optional acceleration varies.. **Mac:** Apple Silicon CoreML/MPS documented; version-specific Torch requirements. **Linux/server:** Yes; suitable for a local batch worker.

**Limits:** Wrapper license does not cover every downloadable checkpoint; broad model choice adds variability. **Integration:** Medium: pin one model, not the whole model menu. **Worth testing:** Conditional: useful if isolation proves necessary.

<a id="t05"></a>

### T05 · Demucs, maintained author repository

[Repository](https://github.com/adefossez/demucs) · [Reviewed README](https://github.com/adefossez/demucs/blob/2883f3db65617d6d178c6ed10d869dc14e44e59b/README.md) · [License evidence](https://github.com/adefossez/demucs/blob/2883f3db65617d6d178c6ed10d869dc14e44e59b/LICENSE)

**Purpose priority 3.** Separates music mixtures into source stems. Input: Audio. Role: Optional isolation when music masks the gesture.

**License:** MIT repository; pin the exact pretrained asset and retain its notices. **Maintenance:** Recent default-branch activity; latest default-branch commit 2026-08-31.

**Hardware:** CPU-neural. **GPU:** Not required; CUDA helpful for throughput.. **Mac:** CPU feasible; test chosen Torch backend separately. **Linux/server:** Yes; suitable for a local batch worker.

**Limits:** Does not identify which nearby voice belongs to the student; short noisy memos differ from music training data. Original facebookresearch repository is archived. **Integration:** Medium: separate PyTorch process. **Worth testing:** Conditional: separation stress test, never mandatory.

<a id="t06"></a>

### T06 · Open-Unmix

[Repository](https://github.com/sigsep/open-unmix-pytorch) · [Reviewed README](https://github.com/sigsep/open-unmix-pytorch/blob/fb672c9584997c2b05e148eeaa65b4c23ed4693b/README.md) · [License evidence](https://github.com/sigsep/open-unmix-pytorch/blob/fb672c9584997c2b05e148eeaa65b4c23ed4693b/LICENSE)

**Purpose priority 4.** Reference music-source-separation implementation. Input: Audio. Role: Scientific separation baseline.

**License:** MIT code; default umxl weights CC-BY-NC-SA-4.0. **Maintenance:** Quiet default branch; latest default-branch commit 2024-04-16.

**Hardware:** CPU-neural. **GPU:** No; optional CUDA.. **Mac:** Yes; verify current arm64 package/build. **Linux/server:** Yes; suitable for a local batch worker.

**Limits:** Music stems do not solve arbitrary background conversation; older stack. **Integration:** Medium. **Worth testing:** Later comparator; Demucs first.

## B. Extract melody, rhythm and uncertainty

| Priority | Tool | Input | First use | Test decision |
|---|---|---|---|---|
| 1 | [Basic Pitch](#t07) | Audio | Independent transcription hypothesis alongside pYIN. | Yes: first transcription challenger. |
| 1 | [librosa / pYIN](#t08) | Audio | Existing monophonic baseline; tap onsets, pitch contours and confidence. | Yes: retain as baseline. |
| 2 | [aubio](#t09) | Audio | Low-cost tapping and onset baseline; eventual live feedback. | Yes for tapping and latency comparison. |
| 2 | [PESTO](#t10) | Audio | Fast pitch-contour challenger, especially for expressive input. | Yes: alongside torchcrepe, not an assumed winner. |
| 2 | [torchcrepe](#t11) | Audio | Continuous f0 and confidence for hum/whistle; compare octave errors. | Yes: alternative pitch hypothesis. |
| 3 | [Beat This!](#t12) | Audio | Optional beat-grid candidates for rhythm-rich recordings. | Yes on tapping and longer rhythmic fixtures. |
| 3 | [Essentia](#t13) | Audio | Rich comparison features and corpus matching. | Yes selectively when librosa lacks a needed descriptor. |
| 3 | [MuScriptor](#t14) | Audio | New polyphonic challenger for instrument/mixed inputs. | Conditional research trial; not the permissive default. |
| 4 | [CREPE original](#t15) | Audio | Reference implementation for pitch comparison. | Defer unless reproducibility comparison needs it. |
| 4 | [madmom](#t16) | Audio | Legacy beat/downbeat baseline. | Defer; Beat This! first. |
| 4 | [MT3](#t17) | Audio | Research comparator for polyphonic inputs. | Defer to server transcription study. |
| 4 | [NeuralNote v2](#t18) | Audio | Manual inspection/reference tool for inferred MIDI. | Later; use underlying models for automation. |

<a id="t07"></a>

### T07 · Basic Pitch

[Repository](https://github.com/spotify/basic-pitch) · [Reviewed README](https://github.com/spotify/basic-pitch/blob/fa5997af0a8210982619003269994a1be25eddf3/README.md) · [License evidence](https://github.com/spotify/basic-pitch/blob/fa5997af0a8210982619003269994a1be25eddf3/LICENSE)

**Purpose priority 1.** Lightweight audio-to-MIDI transcription with pitch bends and polyphonic support. Input: Audio. Role: Independent transcription hypothesis alongside pYIN.

**License:** Apache-2.0 repository; preserve distributed model notices. **Maintenance:** Intermittent / older activity; latest default-branch commit 2025-11-13.

**Hardware:** CPU-neural. **GPU:** No. **Mac:** Supported; begin with separate Python 3.10 environment per M1 documentation. **Linux/server:** Supported; TFLite/ONNX backend must be pinned.

**Limits:** Works best with one instrument; may invent extra notes in noise. README has old M1/Python guidance: isolate dependencies. **Integration:** Medium: CoreML/ONNX/TFLite choice and event conversion. **Worth testing:** Yes: first transcription challenger.

<a id="t08"></a>

### T08 · librosa / pYIN

[Repository](https://github.com/librosa/librosa) · [Reviewed README](https://github.com/librosa/librosa/blob/c6968062a931d39d5d923597c92459c2c32c6b49/README.md) · [License evidence](https://github.com/librosa/librosa/blob/c6968062a931d39d5d923597c92459c2c32c6b49/LICENSE.md)

**Purpose priority 1.** Pitch, onset, spectral, tempo and feature analysis. Input: Audio. Role: Existing monophonic baseline; tap onsets, pitch contours and confidence.

**License:** ISC **Maintenance:** Recent default-branch activity; latest default-branch commit 2026-09-21.

**Hardware:** CPU-light. **GPU:** No. **Mac:** Already running on this Apple Silicon Mac. **Linux/server:** Supported Python stack; suitable for batch analysis.

**Limits:** Beat estimates on a short rubato phrase are ambiguous; octave mistakes and note splitting need review. **Integration:** Low: already used in the prototype. **Worth testing:** Yes: retain as baseline.

<a id="t09"></a>

### T09 · aubio

[Repository](https://github.com/aubio/aubio) · [Reviewed README](https://github.com/aubio/aubio/blob/ad5cf975aed08cc4562dd008cf9f83b12b82ffb8/README.md) · [License evidence](https://github.com/aubio/aubio/blob/ad5cf975aed08cc4562dd008cf9f83b12b82ffb8/COPYING)

**Purpose priority 2.** Compact C tools for pitch, onsets, tempo and silence. Input: Audio. Role: Low-cost tapping and onset baseline; eventual live feedback.

**License:** GPL-3.0 **Maintenance:** Recent default-branch activity; latest default-branch commit 2026-04-10.

**Hardware:** CPU-light. **GPU:** No. **Mac:** Yes; verify current arm64 package/build. **Linux/server:** Yes; suitable for a local batch worker.

**Limits:** No orchestration; Python/native build compatibility needs checking. **Integration:** Low–medium: CLI or C binding. **Worth testing:** Yes for tapping and latency comparison.

<a id="t10"></a>

### T10 · PESTO

[Repository](https://github.com/SonyCSLParis/pesto) · [Reviewed README](https://github.com/SonyCSLParis/pesto/blob/62bc0c9702558f19af4593752947fb9db1eadac9/README.md) · [License evidence](https://github.com/SonyCSLParis/pesto/blob/62bc0c9702558f19af4593752947fb9db1eadac9/LICENSE.md)

**Purpose priority 2.** Self-supervised monophonic pitch estimator; CPU default, streaming/export paths. Input: Audio. Role: Fast pitch-contour challenger, especially for expressive input.

**License:** LGPL-3.0 code; retain separate notices for the selected pretrained checkpoint. **Maintenance:** Intermittent / older activity; latest default-branch commit 2025-10-15.

**Hardware:** CPU-neural. **GPU:** No; CPU default, optional GPU.. **Mac:** Yes; verify current arm64 package/build. **Linux/server:** Yes; suitable for a local batch worker.

**Limits:** Still needs voicing thresholds and note segmentation; robustness on shop noise untested. **Integration:** Medium: isolated Torch inference. **Worth testing:** Yes: alongside torchcrepe, not an assumed winner.

<a id="t11"></a>

### T11 · torchcrepe

[Repository](https://github.com/maxrmorrison/torchcrepe) · [Reviewed README](https://github.com/maxrmorrison/torchcrepe/blob/19e2ec3d494c0797a5ff2a11408ec5838fba6681/README.md) · [License evidence](https://github.com/maxrmorrison/torchcrepe/blob/19e2ec3d494c0797a5ff2a11408ec5838fba6681/LICENSE)

**Purpose priority 2.** PyTorch CREPE pitch and periodicity inference with decoding/silence controls. Input: Audio. Role: Continuous f0 and confidence for hum/whistle; compare octave errors.

**License:** MIT **Maintenance:** Intermittent / older activity; latest default-branch commit 2025-05-16.

**Hardware:** CPU-neural. **GPU:** No; supports CPU or CUDA.. **Mac:** Yes; verify current arm64 package/build. **Linux/server:** Yes; suitable for a local batch worker.

**Limits:** Monophonic, not note segmentation; percussion has no meaningful f0. **Integration:** Medium: Torch plus note-segmentation adapter. **Worth testing:** Yes: alternative pitch hypothesis.

<a id="t12"></a>

### T12 · Beat This!

[Repository](https://github.com/CPJKU/beat_this) · [Reviewed README](https://github.com/CPJKU/beat_this/blob/b95c8ab0c58c2d9fcfd40508ae8dffbc05ac4f5c/README.md) · [License evidence](https://github.com/CPJKU/beat_this/blob/b95c8ab0c58c2d9fcfd40508ae8dffbc05ac4f5c/LICENSE)

**Purpose priority 3.** Neural beat and downbeat prediction without mandatory DBN postprocessing. Input: Audio. Role: Optional beat-grid candidates for rhythm-rich recordings.

**License:** MIT code AND published weights, explicitly stated upstream. **Maintenance:** Recent default-branch activity; latest default-branch commit 2026-05-28.

**Hardware:** CPU-neural. **GPU:** No; documented CPU fallback.. **Mac:** Yes; verify current arm64 package/build. **Linux/server:** Yes; suitable for a local batch worker.

**Limits:** A few free-time notes do not establish meter; do not force a grid from weak evidence. **Integration:** Medium: Torch/checkpoint; keep DBN disabled initially. **Worth testing:** Yes on tapping and longer rhythmic fixtures.

<a id="t13"></a>

### T13 · Essentia

[Repository](https://github.com/MTG/essentia) · [Reviewed README](https://github.com/MTG/essentia/blob/f6db1f605c72afc889cf0ac82048277a7c75a455/README.md) · [License evidence](https://github.com/MTG/essentia/blob/f6db1f605c72afc889cf0ac82048277a7c75a455/COPYING.txt)

**Purpose priority 3.** Large C++/Python MIR toolkit for tonal, rhythmic and timbral descriptors. Input: Audio. Role: Rich comparison features and corpus matching.

**License:** AGPL-3.0 code; commercial alternative exists but is not proposed; model terms separate. **Maintenance:** Recent default-branch activity; latest default-branch commit 2026-09-21.

**Hardware:** CPU-light. **GPU:** No. **Mac:** Yes; verify current arm64 package/build. **Linux/server:** Yes; suitable for a local batch worker.

**Limits:** Larger native integration; learned models have distinct terms; AGPL matters for a hosted product. **Integration:** Medium–high. **Worth testing:** Yes selectively when librosa lacks a needed descriptor.

<a id="t14"></a>

### T14 · MuScriptor

[Repository](https://github.com/muscriptor/muscriptor) · [Reviewed README](https://github.com/muscriptor/muscriptor/blob/7f213afecf23bd6a1b8672aa223690ee9807cefb/README.md) · [License evidence](https://github.com/muscriptor/muscriptor/blob/7f213afecf23bd6a1b8672aa223690ee9807cefb/LICENSE)

**Purpose priority 3.** Multi-instrument transcription to MIDI and optionally sheet music. Input: Audio. Role: New polyphonic challenger for instrument/mixed inputs.

**License:** MIT code; weights CC-BY-NC-4.0, gated download. **Maintenance:** Recent default-branch activity; latest default-branch commit 2026-09-04.

**Hardware:** Apple-neural. **GPU:** Small can use CPU; GPU strongly preferred for medium/large.. **Mac:** Apple Silicon MPS documented; Intel requires older Python/Torch. **Linux/server:** Supported; CPU small or CUDA larger models.

**Limits:** Weights require account/license acceptance; substantially larger than Basic Pitch. Quantized notation struggles with rubato. **Integration:** Medium–high: isolated runtime and explicit model selection. **Worth testing:** Conditional research trial; not the permissive default.

<a id="t15"></a>

### T15 · CREPE original

[Repository](https://github.com/marl/crepe) · [Reviewed README](https://github.com/marl/crepe/blob/c9b71ce61491454125a0693f584f7244f29d9884/README.md) · [License evidence](https://github.com/marl/crepe/blob/c9b71ce61491454125a0693f584f7244f29d9884/LICENSE)

**Purpose priority 4.** Original TensorFlow monophonic pitch estimator. Input: Audio. Role: Reference implementation for pitch comparison.

**License:** MIT **Maintenance:** Quiet default branch; latest default-branch commit 2024-08-19.

**Hardware:** CPU-neural. **GPU:** No; optional acceleration.. **Mac:** Yes; verify current arm64 package/build. **Linux/server:** Yes; suitable for a local batch worker.

**Limits:** Older TensorFlow stack; redundant with torchcrepe for initial trial. **Integration:** Medium. **Worth testing:** Defer unless reproducibility comparison needs it.

<a id="t16"></a>

### T16 · madmom

[Repository](https://github.com/CPJKU/madmom) · [Reviewed README](https://github.com/CPJKU/madmom/blob/27f032e8947204902c675e5e341a3faf5dc86dae/README.rst) · [License evidence](https://github.com/CPJKU/madmom/blob/27f032e8947204902c675e5e341a3faf5dc86dae/LICENSE)

**Purpose priority 4.** Established MIR tools including learned rhythm and beat processors. Input: Audio. Role: Legacy beat/downbeat baseline.

**License:** BSD-3-Clause code; data/models CC-BY-NC-SA-4.0. **Maintenance:** Quiet default branch; latest default-branch commit 2024-08-25.

**Hardware:** CPU-neural. **GPU:** No. **Mac:** Yes; verify current arm64 package/build. **Linux/server:** Yes; suitable for a local batch worker.

**Limits:** Old Python/NumPy compatibility and restricted model/data terms. **Integration:** High relative to current alternatives. **Worth testing:** Defer; Beat This! first.

<a id="t17"></a>

### T17 · MT3

[Repository](https://github.com/magenta/mt3) · [Reviewed README](https://github.com/magenta/mt3/blob/6bc4cfc749b7c746bcf2f72e4063158db83cc51c/README.md) · [License evidence](https://github.com/magenta/mt3/blob/6bc4cfc749b7c746bcf2f72e4063158db83cc51c/LICENSE)

**Purpose priority 4.** T5X multi-instrument transcription. Input: Audio. Role: Research comparator for polyphonic inputs.

**License:** Apache-2.0 code; verify specific checkpoint terms. **Maintenance:** Recent default-branch activity; latest default-branch commit 2026-09-15.

**Hardware:** Server-neural. **GPU:** Practical accelerator recommended; minimum memory not established here.. **Mac:** Not an immediate Mac choice; CPU port unverified. **Linux/server:** Research-oriented JAX environment; prefer accelerator server.

**Limits:** JAX/T5X checkpoint stack is disproportionate for one hum; no verified Mac path here. **Integration:** High. **Worth testing:** Defer to server transcription study.

<a id="t18"></a>

### T18 · NeuralNote v2

[Repository](https://github.com/DamRsn/NeuralNote) · [Reviewed README](https://github.com/DamRsn/NeuralNote/blob/20ca45ad7b4429dea05a9321020b62bf2ff32fae/README.md) · [License evidence](https://github.com/DamRsn/NeuralNote/blob/20ca45ad7b4429dea05a9321020b62bf2ff32fae/LICENSE)

**Purpose priority 4.** Desktop transcription editor/plugin now based on MuScriptor. Input: Audio. Role: Manual inspection/reference tool for inferred MIDI.

**License:** Apache-2.0 code; MuScriptor weights CC-BY-NC-4.0. **Maintenance:** Recent default-branch activity; latest default-branch commit 2026-09-16.

**Hardware:** Apple-neural. **GPU:** Small CPU possible; medium/large GPU recommended.. **Mac:** Supported source build; Metal path documented. **Linux/server:** v2 currently unsupported upstream.

**Limits:** Current v2 is source-build only; do not confuse old Basic Pitch v1 binaries with v2. Linux not yet supported. **Integration:** High for headless use; medium for manual research. **Worth testing:** Later; use underlying models for automation.

## C. Shared events and musical structure

| Priority | Tool | Input | First use | Test decision |
|---|---|---|---|---|
| 1 | [Mido](#t19) | MIDI/events | Interchange and exact event serialization. | Yes: narrow interchange adapter. |
| 1 | [pretty_midi](#t20) | MIDI/events | Motif manipulation and MIDI export around canonical JSON. | Yes: easy experiment glue. |
| 2 | [music21](#t21) | Symbolic scores | Candidate harmonies and constrained voice leading. | Yes: rules-based harmonist. |
| 3 | [Partitura](#t22) | MIDI/MusicXML | Retain performance timing separately from notated score. | Later if score/performance alignment becomes central. |
| 4 | [MusPy](#t23) | Symbolic music | Batch research metrics and interchangeable representations. | Later; avoid replacing the existing small event format. |

<a id="t19"></a>

### T19 · Mido

[Repository](https://github.com/mido/mido) · [Reviewed README](https://github.com/mido/mido/blob/7c1de5df224a5f0c602af8158c8fc25497ad351b/README.rst) · [License evidence](https://github.com/mido/mido/blob/7c1de5df224a5f0c602af8158c8fc25497ad351b/LICENSE)

**Purpose priority 1.** Reads/writes MIDI messages, files and ports. Input: MIDI/events. Role: Interchange and exact event serialization.

**License:** MIT code; documentation has separate attribution terms. **Maintenance:** Recent default-branch activity; latest default-branch commit 2026-09-16.

**Hardware:** CPU-light. **GPU:** No. **Mac:** Yes; verify current arm64 package/build. **Linux/server:** Yes; suitable for a local batch worker.

**Limits:** MIDI alone does not store analysis uncertainty or source provenance. **Integration:** Low. **Worth testing:** Yes: narrow interchange adapter.

<a id="t20"></a>

### T20 · pretty_midi

[Repository](https://github.com/craffel/pretty-midi) · [Reviewed README](https://github.com/craffel/pretty-midi/blob/646f7d3b938ba8216f9dd5c4d3f23d017fa0d22e/README.md) · [License evidence](https://github.com/craffel/pretty-midi/blob/646f7d3b938ba8216f9dd5c4d3f23d017fa0d22e/LICENSE.txt)

**Purpose priority 1.** Convenient note/instrument objects with times in seconds. Input: MIDI/events. Role: Motif manipulation and MIDI export around canonical JSON.

**License:** MIT **Maintenance:** Intermittent / older activity; latest default-branch commit 2025-10-08.

**Hardware:** CPU-light. **GPU:** No. **Mac:** Yes; verify current arm64 package/build. **Linux/server:** Yes; suitable for a local batch worker.

**Limits:** Does not infer musical intent; basic synthesis needs a soundfont/renderer. **Integration:** Low. **Worth testing:** Yes: easy experiment glue.

<a id="t21"></a>

### T21 · music21

[Repository](https://github.com/cuthbertLab/music21) · [Reviewed README](https://github.com/cuthbertLab/music21/blob/2b884f60cab094b54fc9561577366d2e5dca2ac0/README.md) · [License evidence](https://github.com/cuthbertLab/music21/blob/2b884f60cab094b54fc9561577366d2e5dca2ac0/LICENSE)

**Purpose priority 2.** Music-theory, chord, key, interval and score-analysis toolkit. Input: Symbolic scores. Role: Candidate harmonies and constrained voice leading.

**License:** BSD-3-Clause code; corpus score licenses separate. **Maintenance:** Recent default-branch activity; latest default-branch commit 2026-09-21.

**Hardware:** CPU-light. **GPU:** No. **Mac:** Yes; verify current arm64 package/build. **Linux/server:** Yes; suitable for a local batch worker.

**Limits:** Not an automatic tasteful arranger; a short phrase may support several keys. Bundled scores have separate rights. **Integration:** Low–medium. **Worth testing:** Yes: rules-based harmonist.

<a id="t22"></a>

### T22 · Partitura

[Repository](https://github.com/CPJKU/partitura) · [Reviewed README](https://github.com/CPJKU/partitura/blob/427ff875bd5a49a0eec894fdd7c6631ed7f597ea/README.md) · [License evidence](https://github.com/CPJKU/partitura/blob/427ff875bd5a49a0eec894fdd7c6631ed7f597ea/LICENSE)

**Purpose priority 3.** Symbolic scores, performances, timing and alignment utilities. Input: MIDI/MusicXML. Role: Retain performance timing separately from notated score.

**License:** Apache-2.0 **Maintenance:** Recent default-branch activity; latest default-branch commit 2026-05-25.

**Hardware:** CPU-light. **GPU:** No. **Mac:** Yes; verify current arm64 package/build. **Linux/server:** Yes; suitable for a local batch worker.

**Limits:** More abstraction than required for first note-list experiment. **Integration:** Medium. **Worth testing:** Later if score/performance alignment becomes central.

<a id="t23"></a>

### T23 · MusPy

[Repository](https://github.com/salu133445/muspy) · [Reviewed README](https://github.com/salu133445/muspy/blob/2e1dc660dde6974c1693147f528d7437019d9580/README.md) · [License evidence](https://github.com/salu133445/muspy/blob/2e1dc660dde6974c1693147f528d7437019d9580/LICENSE)

**Purpose priority 4.** Data I/O, datasets and evaluation utilities for symbolic generation. Input: Symbolic music. Role: Batch research metrics and interchangeable representations.

**License:** MIT **Maintenance:** Quiet default branch; latest default-branch commit 2024-01-25.

**Hardware:** CPU-light. **GPU:** No. **Mac:** Yes; verify current arm64 package/build. **Linux/server:** Yes; suitable for a local batch worker.

**Limits:** Quiet repository; datasets have their own licenses; metrics are not aesthetic scores. **Integration:** Low–medium. **Worth testing:** Later; avoid replacing the existing small event format.

## D. Composition and accompaniment

| Priority | Tool | Input | First use | Test decision |
|---|---|---|---|---|
| 1 | [isobar](#t24) | Events/MIDI/OSC | Motif permutation, probability, polyrhythm and repeatable variations. | Yes: first playful symbolic musician. |
| 1 | [music21 harmonization recipes](#t25) | Events/chord hypotheses | Deterministic alternative harmonies with source-note anchors. | Yes: cheap explanatory baseline. |
| 2 | [Dicy2 Python](#t26) | Labeled symbolic sequences / corpus events | A memory-based improviser responding to motif labels. | Yes: unusual CPU experiment. |
| 2 | [MMA](#t27) | Chord chart and directives | Bass/drum/accompaniment band given proposed harmony. | Yes: practical conventional band baseline. |
| 2 | [Notochord](#t28) | MIDI events, not raw audio | Condition on the student phrase and trade short responses. | Yes: small neural improviser. |
| 3 | [JJazzLab](#t29) | Chord symbols/style | Human audition benchmark; possibly export accompaniment MIDI. | Yes manually; do not make it the core service. |
| 3 | [SCAMP](#t30) | Events/Python | Polymetric/countermelodic performer with flexible timing. | Yes if expressive timing exceeds isobar needs. |
| 4 | [AccoMontage2](#t31) | Melody MIDI | Study phrase-level accompaniment and chord alternatives. | Hold execution until external dataset/checkpoint terms verified. |
| 4 | [GETMusic within Muzic](#t32) | MIDI source tracks | Condition on melody, generate bass/drums/guitar independently. | Later server comparison. |
| 4 | [Impro-Visor](#t33) | Lead sheets/chords | Unexpected phrase grammars and solo development. | Research/reference before integration. |
| 4 | [Magenta / MusicVAE / GrooVAE](#t34) | MIDI / quantized patterns | MIDI phrase variation and groove-template research. | Historical comparison only, not first dependency. |
| 4 | [MusicLang](#t35) | Symbolic music | Chord-relative phrase transformations. | Conditional; isobar/music21 simpler initially. |

<a id="t24"></a>

### T24 · isobar

[Repository](https://github.com/ideoforms/isobar) · [Reviewed README](https://github.com/ideoforms/isobar/blob/71f5e9f004e947a32c9ecba22e32daed08bef425/README.md) · [License evidence](https://github.com/ideoforms/isobar/blob/71f5e9f004e947a32c9ecba22e32daed08bef425/LICENSE.md)

**Purpose priority 1.** Composable patterns and timeline scheduling. Input: Events/MIDI/OSC. Role: Motif permutation, probability, polyrhythm and repeatable variations.

**License:** MIT **Maintenance:** Recent default-branch activity; latest default-branch commit 2026-09-06.

**Hardware:** CPU-light. **GPU:** No. **Mac:** Yes; verify current arm64 package/build. **Linux/server:** Yes; suitable for a local batch worker.

**Limits:** Requires musical rules and a renderer; randomness alone is not diversity. **Integration:** Low–medium. **Worth testing:** Yes: first playful symbolic musician.

<a id="t25"></a>

### T25 · music21 harmonization recipes

[Repository](https://github.com/cuthbertLab/music21) · [Reviewed README](https://github.com/cuthbertLab/music21/blob/2b884f60cab094b54fc9561577366d2e5dca2ac0/README.md) · [License evidence](https://github.com/cuthbertLab/music21/blob/2b884f60cab094b54fc9561577366d2e5dca2ac0/LICENSE)

**Purpose priority 1.** Theory utilities can support a small custom search over chords and voice leading. Input: Events/chord hypotheses. Role: Deterministic alternative harmonies with source-note anchors.

**License:** BSD-3-Clause code; avoid unreviewed corpus material. **Maintenance:** Recent default-branch activity; latest default-branch commit 2026-09-21.

**Hardware:** CPU-light. **GPU:** No. **Mac:** Yes; verify current arm64 package/build. **Linux/server:** Yes; suitable for a local batch worker.

**Limits:** The harmonizer must be written; this is a proposed use, not an existing house-band API. **Integration:** Medium custom recipe. **Worth testing:** Yes: cheap explanatory baseline.

<a id="t26"></a>

### T26 · Dicy2 Python

[Repository](https://github.com/DYCI2/Dicy2-python) · [Reviewed README](https://github.com/DYCI2/Dicy2-python/blob/ec139cdef2c41d859aa4be28d671d7057655fcd1/README.md) · [License evidence](https://github.com/DYCI2/Dicy2-python/blob/ec139cdef2c41d859aa4be28d671d7057655fcd1/LICENSE)

**Purpose priority 2.** Interactive sequence-generation agents and guided recombination. Input: Labeled symbolic sequences / corpus events. Role: A memory-based improviser responding to motif labels.

**License:** GPL-3.0 core; tutorial musician recordings are not general-use sample assets. **Maintenance:** Intermittent / older activity; latest default-branch commit 2025-05-09.

**Hardware:** CPU-light. **GPU:** No. **Mac:** Upstream tested macOS; Python >=3.9. **Linux/server:** Likely portable, explicitly not upstream-tested per README.

**Limits:** Very short input may offer little memory; audio segmentation/rendering is separate. Max/Live frontends are unnecessary. **Integration:** Medium–high: corpus labels, submodule and adapter. **Worth testing:** Yes: unusual CPU experiment.

<a id="t27"></a>

### T27 · MMA

[Repository](https://github.com/infojunkie/mma) · [Reviewed README](https://github.com/infojunkie/mma/blob/c52943c31aa1e64fa9b5313620d5065f91c22773/README) · [License evidence](https://github.com/infojunkie/mma/blob/c52943c31aa1e64fa9b5313620d5065f91c22773/LICENSE)

**Purpose priority 2.** Generates MIDI accompaniment from chords and reusable rhythmic patterns. Input: Chord chart and directives. Role: Bass/drum/accompaniment band given proposed harmony.

**License:** GPL-2.0; inspect bundled pattern notices. **Maintenance:** Recent default-branch activity; latest default-branch commit 2026-06-20.

**Hardware:** CPU-light. **GPU:** No. **Mac:** Python CLI expected; official Mac information available. **Linux/server:** Supported command-line workflow.

**Limits:** Not audio-to-music; melody needs separate analysis. GitHub is a mirror of author releases. **Integration:** Medium: write directives and render MIDI. **Worth testing:** Yes: practical conventional band baseline.

<a id="t28"></a>

### T28 · Notochord

[Repository](https://github.com/Intelligent-Instruments-Lab/notochord) · [Reviewed README](https://github.com/Intelligent-Instruments-Lab/notochord/blob/a17ddd350e7fe45271b21f0e16672e3abfadb5f0/README.md) · [License evidence](https://github.com/Intelligent-Instruments-Lab/notochord/blob/a17ddd350e7fe45271b21f0e16672e3abfadb5f0/LICENSE)

**Purpose priority 2.** Neural model predicts instruments, pitch, time and velocity interactively. Input: MIDI events, not raw audio. Role: Condition on the student phrase and trade short responses.

**License:** MIT code; selected pretrained checkpoint terms require explicit record. **Maintenance:** Intermittent / older activity; latest default-branch commit 2026-02-23.

**Hardware:** CPU-neural. **GPU:** No for initial inference; recommended for training.. **Mac:** Documented Python/macOS use; CPU first. **Linux/server:** Python/Torch expected; verify dependencies.

**Limits:** MIDI must be rendered; source identity may drift; archive checkpoint terms separately. **Integration:** Medium: feed/sample API and bounded offline loop. **Worth testing:** Yes: small neural improviser.

<a id="t29"></a>

### T29 · JJazzLab

[Repository](https://github.com/jjazzboss/JJazzLab) · [Reviewed README](https://github.com/jjazzboss/JJazzLab/blob/cd1944afdf8a18b659cdbf63538b6df625a515ec/README.md) · [License evidence](https://github.com/jjazzboss/JJazzLab/blob/cd1944afdf8a18b659cdbf63538b6df625a515ec/LICENSE)

**Purpose priority 3.** Desktop backing-track generator with rhythm engines and synthesis. Input: Chord symbols/style. Role: Human audition benchmark; possibly export accompaniment MIDI.

**License:** LGPL-2.1 repository; verify each style/soundfont asset. **Maintenance:** Recent default-branch activity; latest default-branch commit 2026-04-13.

**Hardware:** CPU-light. **GPU:** No. **Mac:** Official Mac installer. **Linux/server:** Official Linux installer; headless batch path needs investigation.

**Limits:** Desktop integration heavier than CLI; style and soundfont rights separate. **Integration:** High for server automation; low for manual audition. **Worth testing:** Yes manually; do not make it the core service.

<a id="t30"></a>

### T30 · SCAMP

[Repository](https://github.com/MarcTheSpark/scamp) · [Reviewed README](https://github.com/MarcTheSpark/scamp/blob/4dc97d9fef36386617d30f8a06ee19516c6dfde6/README.md) · [License evidence](https://github.com/MarcTheSpark/scamp/blob/4dc97d9fef36386617d30f8a06ee19516c6dfde6/LICENSE.txt)

**Purpose priority 3.** Schedules expressive notes, envelopes, tempo layers and playback. Input: Events/Python. Role: Polymetric/countermelodic performer with flexible timing.

**License:** GPL-3.0 **Maintenance:** Recent default-branch activity; latest default-branch commit 2026-09-14.

**Hardware:** CPU-light. **GPU:** No. **Mac:** Yes; verify current arm64 package/build. **Linux/server:** Yes; suitable for a local batch worker.

**Limits:** Framework, not a composer; live scheduling must be adapted for deterministic offline export. **Integration:** Medium. **Worth testing:** Yes if expressive timing exceeds isobar needs.

<a id="t31"></a>

### T31 · AccoMontage2

[Repository](https://github.com/billyblu2000/AccoMontage2) · [Reviewed README](https://github.com/billyblu2000/AccoMontage2/blob/39184ae5cd8be1de289d116d12b69892a034f1b6/docs/README.md) · [License evidence](https://github.com/billyblu2000/AccoMontage2/blob/39184ae5cd8be1de289d116d12b69892a034f1b6/LICENSE)

**Purpose priority 4.** Retrieval-based harmonization and piano-texture arrangement. Input: Melody MIDI. Role: Study phrase-level accompaniment and chord alternatives.

**License:** MIT code; external chord dataset and checkpoint terms unresolved. **Maintenance:** Quiet default branch; latest default-branch commit 2023-05-03.

**Hardware:** Server-neural. **GPU:** Check chosen texture model; harmonization may run CPU.. **Mac:** Unverified; Python/Torch components may port. **Linux/server:** Prefer isolated research environment.

**Limits:** Assumes structured tonal phrases; external data derives from a MIDI pack; dataset/checkpoint availability and rights unresolved. Piano texture can be reassigned but idiom persists. **Integration:** High. **Worth testing:** Hold execution until external dataset/checkpoint terms verified.

<a id="t32"></a>

### T32 · GETMusic within Muzic

[Repository](https://github.com/microsoft/muzic) · [Reviewed README](https://github.com/microsoft/muzic/blob/2b8739671ba06f819f31f568b8a79da581aaf6f9/README.md) · [License evidence](https://github.com/microsoft/muzic/blob/2b8739671ba06f819f31f568b8a79da581aaf6f9/LICENSE)

**Purpose priority 4.** Diffusion completion of selected missing symbolic instrument tracks. Input: MIDI source tracks. Role: Condition on melody, generate bass/drums/guitar independently.

**License:** MIT repository code; external checkpoint/training material terms not established. **Maintenance:** Recent default-branch activity; latest default-branch commit 2026-08-05.

**Hardware:** Server-neural. **GPU:** Practical CUDA path; minimum VRAM not established.. **Mac:** No verified immediate path; CUDA-oriented recipe. **Linux/server:** Documented CUDA research setup.

**Limits:** Old CUDA/Torch recipe, limited instrument vocabulary, dataset domain gap; checkpoint permissions need verification. **Integration:** High. **Worth testing:** Later server comparison.

<a id="t33"></a>

### T33 · Impro-Visor

[Repository](https://github.com/Impro-Visor/Impro-Visor) · [Reviewed README](https://github.com/Impro-Visor/Impro-Visor/blob/550bbb554962249aceb0e82a72142e3e5b3c0d4a/README.txt) · [License evidence](https://github.com/Impro-Visor/Impro-Visor/blob/550bbb554962249aceb0e82a72142e3e5b3c0d4a/LICENSE.txt)

**Purpose priority 4.** Grammar-based jazz improvisation and accompaniment environment. Input: Lead sheets/chords. Role: Unexpected phrase grammars and solo development.

**License:** GPL-2.0 **Maintenance:** Quiet default branch; latest default-branch commit 2019-06-19.

**Hardware:** CPU-light. **GPU:** No. **Mac:** Yes; verify current arm64 package/build. **Linux/server:** Yes; suitable for a local batch worker.

**Limits:** Old Java-focused desktop; installation advice is dated; never disable Mac security to test it. **Integration:** High integration. **Worth testing:** Research/reference before integration.

<a id="t34"></a>

### T34 · Magenta / MusicVAE / GrooVAE

[Repository](https://github.com/magenta/magenta) · [Reviewed README](https://github.com/magenta/magenta/blob/c15687ebd1c1cc12658cd468c737d3c24c02b918/README.md) · [License evidence](https://github.com/magenta/magenta/blob/c15687ebd1c1cc12658cd468c737d3c24c02b918/LICENSE)

**Purpose priority 4.** Symbolic variation/interpolation and expressive drum timing models. Input: MIDI / quantized patterns. Role: MIDI phrase variation and groove-template research.

**License:** Apache-2.0 code; verify checkpoint/dataset terms separately. **Maintenance:** Archived; latest default-branch commit 2026-01-06.

**Hardware:** CPU-neural. **GPU:** Inference model-dependent; training generally accelerated.. **Mac:** Yes; verify current arm64 package/build. **Linux/server:** Yes; suitable for a local batch worker.

**Limits:** Archived parent repository, old TensorFlow dependencies, model-specific terms and fixed sequence shapes. **Integration:** High. **Worth testing:** Historical comparison only, not first dependency.

<a id="t35"></a>

### T35 · MusicLang

[Repository](https://github.com/MusicLang/musiclang) · [Reviewed README](https://github.com/MusicLang/musiclang/blob/6d1f4afc88cdbc7be3635862cafd980e41e77f67/README.md) · [License evidence](https://github.com/MusicLang/musiclang/blob/6d1f4afc88cdbc7be3635862cafd980e41e77f67/LICENSE.md)

**Purpose priority 4.** Tonal DSL for composing and transforming scores; prediction split into another package. Input: Symbolic music. Role: Chord-relative phrase transformations.

**License:** LICENSE: BSD-2-Clause; README conflicts. Separate predict package/models declare GPL-3.0. **Maintenance:** Quiet default branch; latest default-branch commit 2024-03-25.

**Hardware:** CPU-light. **GPU:** No. **Mac:** Yes; verify current arm64 package/build. **Linux/server:** Yes; suitable for a local batch worker.

**Limits:** Quiet code; README says BSD-3 but LICENSE is BSD-2; resolve discrepancy before distribution. **Integration:** Medium. **Worth testing:** Conditional; isobar/music21 simpler initially.

## E. Render instruments, drums and physical models

| Priority | Tool | Input | First use | Test decision |
|---|---|---|---|---|
| 1 | [FluidSynth](#t36) | MIDI + SoundFont | Simple common renderer for comparing symbolic musicians. | Yes as neutral rendering baseline. |
| 1 | [SuperCollider](#t37) | Events/audio/control | One CPU renderer for conservative instruments, granular voices and experimental bands. | Yes: strongest broad experimental workbench. |
| 2 | [Csound](#t38) | Score/orchestra/audio | Offline 15-second procedural performers. | Yes, especially granular and physical-model experiments. |
| 2 | [Faust](#t39) | DSP code/audio/control | Physical-model plucks, resonators, synths and a future browser renderer. | Yes: unusual instrument designer. |
| 2 | [Hydrogen](#t40) | Drum patterns/MIDI/OSC | Compare tap-derived drum arrangements and curated kits. | Yes: drum design/reference. |
| 2 | [Pure Data](#t41) | Audio/control/patches | Granular/resonator patches driven by extracted gestures. | Yes: lightweight alternative to SuperCollider. |
| 2 | [Surge XT](#t42) | MIDI/control | Contemporary lead/bass/pad tone for event musicians. | Yes: sound-quality comparison. |
| 3 | [plugdata](#t43) | Audio/Pd patches | Fast visual patch audition without a commercial DAW. | Yes for patch discovery; export a small headless patch later. |
| 3 | [pyo](#t44) | Audio/Python/control | Python-native granular and audio-reactive musicians. | Yes as alternate granular implementation. |
| 3 | [Sonic Pi](#t45) | Code/sample audio/MIDI | Rapid human-designed genre/rhythm prototypes. | Yes as a musical sketchpad, not compulsory runtime. |
| 4 | [sfizz](#t46) | SFZ + MIDI | Richer performance of open instrument samples. | Conditional renderer trial; FluidSynth/current sampler first. |

<a id="t36"></a>

### T36 · FluidSynth

[Repository](https://github.com/FluidSynth/fluidsynth) · [Reviewed README](https://github.com/FluidSynth/fluidsynth/blob/71e85b2ca6bf48641ba7e2261d8f2640ae473773/README.md) · [License evidence](https://github.com/FluidSynth/fluidsynth/blob/71e85b2ca6bf48641ba7e2261d8f2640ae473773/LICENSE)

**Purpose priority 1.** Mature sample-based MIDI synthesizer with offline rendering. Input: MIDI + SoundFont. Role: Simple common renderer for comparing symbolic musicians.

**License:** LGPL-2.1 library; each SoundFont has independent terms. **Maintenance:** Recent default-branch activity; latest default-branch commit 2026-09-19.

**Hardware:** CPU-light. **GPU:** No. **Mac:** Yes; verify current arm64 package/build. **Linux/server:** Yes; suitable for a local batch worker.

**Limits:** Sound quality depends on the chosen soundfont; default General MIDI sounds may fall short of the target. **Integration:** Low. **Worth testing:** Yes as neutral rendering baseline.

<a id="t37"></a>

### T37 · SuperCollider

[Repository](https://github.com/supercollider/supercollider) · [Reviewed README](https://github.com/supercollider/supercollider/blob/0eb48471d2d79f7e6c9819d49f2f4b84bbd34631/README.md) · [License evidence](https://github.com/supercollider/supercollider/blob/0eb48471d2d79f7e6c9819d49f2f4b84bbd34631/COPYING)

**Purpose priority 1.** Programmable synthesis, sampling, patterns and non-real-time rendering. Input: Events/audio/control. Role: One CPU renderer for conservative instruments, granular voices and experimental bands.

**License:** GPL-3.0 **Maintenance:** Recent default-branch activity; latest default-branch commit 2026-09-22.

**Hardware:** CPU-light. **GPU:** No. **Mac:** Yes; verify current arm64 package/build. **Linux/server:** Yes; suitable for a local batch worker.

**Limits:** Requires SynthDefs and musical programming; defaults do not guarantee good tone. **Integration:** Medium: isolated command-line score/render process. **Worth testing:** Yes: strongest broad experimental workbench.

<a id="t38"></a>

### T38 · Csound

[Repository](https://github.com/csound/csound) · [Reviewed README](https://github.com/csound/csound/blob/abde351017f5579c64db209f1705902364bc0408/README.md) · [License evidence](https://github.com/csound/csound/blob/abde351017f5579c64db209f1705902364bc0408/COPYING)

**Purpose priority 2.** Mature synthesis engine with physical-model, spectral and granular opcodes. Input: Score/orchestra/audio. Role: Offline 15-second procedural performers.

**License:** LGPL-2.1 **Maintenance:** Recent default-branch activity; latest default-branch commit 2026-09-22.

**Hardware:** CPU-light. **GPU:** No. **Mac:** Yes; verify current arm64 package/build. **Linux/server:** Yes; suitable for a local batch worker.

**Limits:** Another specialist language; opcode/preset quality varies. **Integration:** Medium: score files and command-line render. **Worth testing:** Yes, especially granular and physical-model experiments.

<a id="t39"></a>

### T39 · Faust

[Repository](https://github.com/grame-cncm/faust) · [Reviewed README](https://github.com/grame-cncm/faust/blob/3758c84c51eaac8965de1ad78cdea60b2c2ffb4e/README.md) · [License evidence](https://github.com/grame-cncm/faust/blob/3758c84c51eaac8965de1ad78cdea60b2c2ffb4e/COPYING.txt)

**Purpose priority 2.** Compiles signal-processing programs into native/WebAssembly targets. Input: DSP code/audio/control. Role: Physical-model plucks, resonators, synths and a future browser renderer.

**License:** Compiler LGPL-2.1-or-later; library/architecture exceptions and generated output must be checked individually. **Maintenance:** Recent default-branch activity; latest default-branch commit 2026-09-22.

**Hardware:** CPU-light. **GPU:** No. **Mac:** Yes; verify current arm64 package/build. **Linux/server:** Yes; suitable for a local batch worker.

**Limits:** Not a music arranger; compiler/library/generated-code terms differ. **Integration:** Medium–high standalone; easier via DawDreamer. **Worth testing:** Yes: unusual instrument designer.

<a id="t40"></a>

### T40 · Hydrogen

[Repository](https://github.com/hydrogen-music/hydrogen) · [Reviewed README](https://github.com/hydrogen-music/hydrogen/blob/7440c1175574a624d518d820ff7fcc597b11c4f3/README.md) · [License evidence](https://github.com/hydrogen-music/hydrogen/blob/7440c1175574a624d518d820ff7fcc597b11c4f3/COPYING)

**Purpose priority 2.** Pattern-based drum machine and sample playback. Input: Drum patterns/MIDI/OSC. Role: Compare tap-derived drum arrangements and curated kits.

**License:** GPL-2.0 code; drumkit assets separately licensed. **Maintenance:** Recent default-branch activity; latest default-branch commit 2026-09-11.

**Hardware:** CPU-light. **GPU:** No. **Mac:** Yes; verify current arm64 package/build. **Linux/server:** Yes; suitable for a local batch worker.

**Limits:** Drumkit licenses vary; desktop app heavier than a small sampler. **Integration:** Medium: song/pattern export or MIDI/OSC. **Worth testing:** Yes: drum design/reference.

<a id="t41"></a>

### T41 · Pure Data

[Repository](https://github.com/pure-data/pure-data) · [Reviewed README](https://github.com/pure-data/pure-data/blob/5ba779f36411d530ff6dbd7b29ac75a31534e51e/README.txt) · [License evidence](https://github.com/pure-data/pure-data/blob/5ba779f36411d530ff6dbd7b29ac75a31534e51e/LICENSE.txt)

**Purpose priority 2.** Visual dataflow synthesis and DSP, usable without a graphical front end. Input: Audio/control/patches. Role: Granular/resonator patches driven by extracted gestures.

**License:** BSD-style 3-clause core; externals separately licensed. **Maintenance:** Recent default-branch activity; latest default-branch commit 2026-09-22.

**Hardware:** CPU-light. **GPU:** No. **Mac:** Yes; verify current arm64 package/build. **Linux/server:** Yes; suitable for a local batch worker.

**Limits:** Third-party externals add builds and licenses; keep first patch vanilla. **Integration:** Medium. **Worth testing:** Yes: lightweight alternative to SuperCollider.

<a id="t42"></a>

### T42 · Surge XT

[Repository](https://github.com/surge-synthesizer/surge) · [Reviewed README](https://github.com/surge-synthesizer/surge/blob/58914e59c608ed4384ba6002e44c3465c58b2e71/README.md) · [License evidence](https://github.com/surge-synthesizer/surge/blob/58914e59c608ed4384ba6002e44c3465c58b2e71/LICENSE)

**Purpose priority 2.** Open-source hybrid software synthesizer. Input: MIDI/control. Role: Contemporary lead/bass/pad tone for event musicians.

**License:** GPL-3.0 code; inspect factory/third-party patch and wavetable notices. **Maintenance:** Recent default-branch activity; latest default-branch commit 2026-09-18.

**Hardware:** CPU-light. **GPU:** No. **Mac:** Yes; verify current arm64 package/build. **Linux/server:** Yes; suitable for a local batch worker.

**Limits:** Plugin preset/state handling and architecture matching; composition still separate. **Integration:** Medium with a headless plugin host. **Worth testing:** Yes: sound-quality comparison.

<a id="t43"></a>

### T43 · plugdata

[Repository](https://github.com/plugdata-team/plugdata) · [Reviewed README](https://github.com/plugdata-team/plugdata/blob/85c64c33ea293d77863127321a9bfae2e327816a/README.md) · [License evidence](https://github.com/plugdata-team/plugdata/blob/85c64c33ea293d77863127321a9bfae2e327816a/LICENSE)

**Purpose priority 3.** Modern Pure Data-based standalone and plugin environment. Input: Audio/Pd patches. Role: Fast visual patch audition without a commercial DAW.

**License:** GPL-3.0 repository; bundled external licenses vary. **Maintenance:** Recent default-branch activity; latest default-branch commit 2026-09-22.

**Hardware:** CPU-light. **GPU:** No. **Mac:** Yes; verify current arm64 package/build. **Linux/server:** Yes; suitable for a local batch worker.

**Limits:** GUI is helpful for researcher, unnecessary for student/server runtime. **Integration:** Medium manual, higher automation. **Worth testing:** Yes for patch discovery; export a small headless patch later.

<a id="t44"></a>

### T44 · pyo

[Repository](https://github.com/belangeo/pyo) · [Reviewed README](https://github.com/belangeo/pyo/blob/bbd1d6ea87023d3cb2fe002e4b6b6e3ce35c831a/README.md) · [License evidence](https://github.com/belangeo/pyo/blob/bbd1d6ea87023d3cb2fe002e4b6b6e3ce35c831a/LICENSE)

**Purpose priority 3.** C-backed Python DSP, synthesis and granulation objects. Input: Audio/Python/control. Role: Python-native granular and audio-reactive musicians.

**License:** LGPL-3.0 **Maintenance:** Recent default-branch activity; latest default-branch commit 2026-07-15.

**Hardware:** CPU-light. **GPU:** No. **Mac:** README lists Intel/arm64 Python wheels. **Linux/server:** Supported; native dependencies/build may be needed.

**Limits:** Native audio dependencies; verify offline server mode and wheels. **Integration:** Medium. **Worth testing:** Yes as alternate granular implementation.

<a id="t45"></a>

### T45 · Sonic Pi

[Repository](https://github.com/sonic-pi-net/sonic-pi) · [Reviewed README](https://github.com/sonic-pi-net/sonic-pi/blob/aaaef697834c044b52e0005d31213430834ea48f/README.md) · [License evidence](https://github.com/sonic-pi-net/sonic-pi/blob/aaaef697834c044b52e0005d31213430834ea48f/LICENSE.md)

**Purpose priority 3.** Live-coded synthesis, sampling and scheduling. Input: Code/sample audio/MIDI. Role: Rapid human-designed genre/rhythm prototypes.

**License:** Main code MIT; bundled GPL components affect binaries; samples have individual notices/exceptions. **Maintenance:** Recent default-branch activity; latest default-branch commit 2026-09-20.

**Hardware:** CPU-light. **GPU:** No. **Mac:** Yes; verify current arm64 package/build. **Linux/server:** Yes; suitable for a local batch worker.

**Limits:** Desktop workflow and engine dependencies complicate unattended rendering. **Integration:** Medium manual, high service integration. **Worth testing:** Yes as a musical sketchpad, not compulsory runtime.

<a id="t46"></a>

### T46 · sfizz

[Repository](https://github.com/sfztools/sfizz) · [Reviewed README](https://github.com/sfztools/sfizz/blob/f5c6e29f23b8057867c08e88f5f6ac6738baa30b/README.md) · [License evidence](https://github.com/sfztools/sfizz/blob/f5c6e29f23b8057867c08e88f5f6ac6738baa30b/LICENSE)

**Purpose priority 4.** SFZ sample playback with articulations and velocity regions. Input: SFZ + MIDI. Role: Richer performance of open instrument samples.

**License:** BSD-2-Clause core; dependencies and SFZ assets separate. **Maintenance:** Archived; latest default-branch commit 2025-03-17.

**Hardware:** CPU-light. **GPU:** No. **Mac:** Yes; verify current arm64 package/build. **Linux/server:** Yes; suitable for a local batch worker.

**Limits:** Repository archived; choose and pin a maintained distribution/fork before depending on it. No successor verified here. **Integration:** Medium native library/plugin. **Worth testing:** Conditional renderer trial; FluidSynth/current sampler first.

## F. Audio transformations and offline hosts

| Priority | Tool | Input | First use | Test decision |
|---|---|---|---|---|
| 1 | [Pedalboard](#t47) | Audio/MIDI/plugin state | Compact effects chain and scripted plugin rendering. | Yes: practical transformation layer. |
| 1 | [Signalsmith Stretch](#t48) | Audio | Independent phrase tempo/pitch changes and controlled chopping. | Yes: permissive DSP candidate. |
| 2 | [DawDreamer](#t49) | Audio/MIDI/graphs | Common instrument host for reproducible musician auditions. | Yes when one simple renderer no longer suffices. |
| 2 | [Rubber Band](#t50) | Audio | Groove fitting and audio-fragment transformations. | Yes: established comparison for Signalsmith. |
| 4 | [dasp-pytorch](#t51) | Audio/tensor controls | Fit or explore processing settings rather than generate compositions. | Later sound-design research. |

<a id="t47"></a>

### T47 · Pedalboard

[Repository](https://github.com/spotify/pedalboard) · [Reviewed README](https://github.com/spotify/pedalboard/blob/d4e18fcf822e1602e014a24ddd670d8a9bf8a3f9/README.md) · [License evidence](https://github.com/spotify/pedalboard/blob/d4e18fcf822e1602e014a24ddd670d8a9bf8a3f9/LICENSE)

**Purpose priority 1.** Audio effects, file I/O and VST3/AU instrument/effect hosting. Input: Audio/MIDI/plugin state. Role: Compact effects chain and scripted plugin rendering.

**License:** GPL-3.0 host; plugin/model/sample licenses separate. **Maintenance:** Recent default-branch activity; latest default-branch commit 2026-09-09.

**Hardware:** CPU-light. **GPU:** No. **Mac:** Intel/Apple Silicon wheels; AU and VST3. **Linux/server:** x86_64/aarch64 wheels; VST3, not AU.

**Limits:** Host license does not license plugins; Apple/Linux plugin formats and builds differ. **Integration:** Low–medium. **Worth testing:** Yes: practical transformation layer.

<a id="t48"></a>

### T48 · Signalsmith Stretch

[Repository](https://github.com/Signalsmith-Audio/signalsmith-stretch) · [Reviewed README](https://github.com/Signalsmith-Audio/signalsmith-stretch/blob/57b93f4e9206a089a45387eaa39bdc9f310d3308/README.md) · [License evidence](https://github.com/Signalsmith-Audio/signalsmith-stretch/blob/57b93f4e9206a089a45387eaa39bdc9f310d3308/LICENSE.txt)

**Purpose priority 1.** C++ time stretching and pitch shifting. Input: Audio. Role: Independent phrase tempo/pitch changes and controlled chopping.

**License:** MIT **Maintenance:** Intermittent / older activity; latest default-branch commit 2026-01-24.

**Hardware:** CPU-light. **GPU:** No. **Mac:** Yes; verify current arm64 package/build. **Linux/server:** Yes; suitable for a local batch worker.

**Limits:** Transient artifacts and latency/alignment must be measured; needs binding. **Integration:** Medium C++ wrapper. **Worth testing:** Yes: permissive DSP candidate.

<a id="t49"></a>

### T49 · DawDreamer

[Repository](https://github.com/DBraun/DawDreamer) · [Reviewed README](https://github.com/DBraun/DawDreamer/blob/727469f1317e96d0acee80d19fd57aeb0dbd0948/README.md) · [License evidence](https://github.com/DBraun/DawDreamer/blob/727469f1317e96d0acee80d19fd57aeb0dbd0948/LICENSE)

**Purpose priority 2.** Offline Python audio graphs, VST instruments, Faust and parameter automation. Input: Audio/MIDI/graphs. Role: Common instrument host for reproducible musician auditions.

**License:** GPL-3.0 host; plugins and Faust components retain separate terms. **Maintenance:** Recent default-branch activity; latest default-branch commit 2026-08-12.

**Hardware:** CPU-light. **GPU:** No. **Mac:** Intel/arm64 supported; current README Python 3.11–3.14. **Linux/server:** x86_64/aarch64 supported; headless plugins must be tested.

**Limits:** Native/plugin complexity; README warns of LLVM import-order conflicts. Isolate from ML workers. **Integration:** Medium. **Worth testing:** Yes when one simple renderer no longer suffices.

<a id="t50"></a>

### T50 · Rubber Band

[Repository](https://github.com/breakfastquay/rubberband) · [Reviewed README](https://github.com/breakfastquay/rubberband/blob/e4296ac80b1170018a110bc326fd0d45a0eb27d6/README.md) · [License evidence](https://github.com/breakfastquay/rubberband/blob/e4296ac80b1170018a110bc326fd0d45a0eb27d6/COPYING)

**Purpose priority 2.** Independent tempo and pitch processing with CLI/library. Input: Audio. Role: Groove fitting and audio-fragment transformations.

**License:** GPL-2.0-or-later open-source path; commercial alternative not needed for research. **Maintenance:** Quiet default branch; latest default-branch commit 2025-02-27.

**Hardware:** CPU-light. **GPU:** No. **Mac:** Yes; verify current arm64 package/build. **Linux/server:** Yes; suitable for a local batch worker.

**Limits:** Extreme ratios smear attacks; Python wrappers may also require installed CLI. **Integration:** Low–medium. **Worth testing:** Yes: established comparison for Signalsmith.

<a id="t51"></a>

### T51 · dasp-pytorch

[Repository](https://github.com/csteinmetz1/dasp-pytorch) · [Reviewed README](https://github.com/csteinmetz1/dasp-pytorch/blob/c9ae0126e1c441979b93995da061503a0abdceff/README.md) · [License evidence](https://github.com/csteinmetz1/dasp-pytorch/blob/c9ae0126e1c441979b93995da061503a0abdceff/LICENSE)

**Purpose priority 4.** Differentiable EQ, compression, reverb, distortion and stereo processing. Input: Audio/tensor controls. Role: Fit or explore processing settings rather than generate compositions.

**License:** Apache-2.0 **Maintenance:** Quiet default branch; latest default-branch commit 2023-12-04.

**Hardware:** CPU-neural. **GPU:** No for basic processing; useful for optimization/training.. **Mac:** Yes; verify current arm64 package/build. **Linux/server:** Yes; suitable for a local batch worker.

**Limits:** Not a ready automatic mixer; optimization/model work needed. **Integration:** Medium–high. **Worth testing:** Later sound-design research.

## G. Corpus, granular and spectral experimenters

| Priority | Tool | Input | First use | Test decision |
|---|---|---|---|---|
| 1 | [FluCoMa](#t52) | Audio corpus + target/features | Rebuild the student phrase from source-derived or CC0 grains; rhythm/texture route without MIDI. | Yes: especially promising unusual musician. |
| 3 | [PaulXStretch](#t53) | Audio | Turn a short gesture into an evolving texture; contrast to groove-based bands. | Yes as a strange audition, not a default band. |
| 4 | [AudioGuide](#t54) | Target audio + corpus audio | Audio-to-audio mosaic/orchestration without a score bottleneck. | Research first; hold execution/adoption until terms established. |

<a id="t52"></a>

### T52 · FluCoMa

[Repository](https://github.com/flucoma/flucoma-core) · [Reviewed README](https://github.com/flucoma/flucoma-core/blob/0626d7a3438060965231f034eca07b981ec36fc4/README.md) · [License evidence](https://github.com/flucoma/flucoma-core/blob/0626d7a3438060965231f034eca07b981ec36fc4/LICENSE.md)

**Purpose priority 1.** Slicing, descriptors, decomposition, clustering and matching for creative audio. Input: Audio corpus + target/features. Role: Rebuild the student phrase from source-derived or CC0 grains; rhythm/texture route without MIDI.

**License:** BSD-3-Clause core and CLI; host/environment licenses separate. **Maintenance:** Recent default-branch activity; latest default-branch commit 2026-04-11.

**Hardware:** CPU-light. **GPU:** No. **Mac:** Core documents Apple Silicon support. **Linux/server:** C++17 Linux supported; CLI useful for workers.

**Limits:** Toolkit, not one-click orchestration; corpus selection and scheduling matter. **Integration:** Medium: CLI/SC/Pd binding; native build. **Worth testing:** Yes: especially promising unusual musician.

<a id="t53"></a>

### T53 · PaulXStretch

[Repository](https://github.com/essej/paulxstretch) · [Reviewed README](https://github.com/essej/paulxstretch/blob/b6175e904a445809b45b3a5ee8e18501055cd2ef/README.md) · [License evidence](https://github.com/essej/paulxstretch/blob/b6175e904a445809b45b3a5ee8e18501055cd2ef/LICENSE)

**Purpose priority 3.** Extreme spectral time stretching and spectral sound transformation. Input: Audio. Role: Turn a short gesture into an evolving texture; contrast to groove-based bands.

**License:** GPL-3.0 with section-7 distribution exceptions. **Maintenance:** Quiet default branch; latest default-branch commit 2022-10-02.

**Hardware:** CPU-light. **GPU:** No. **Mac:** Mac app/plugin available; verify current arm64 packaging. **Linux/server:** Source build documented.

**Limits:** Rhythm and lyric intelligibility can change unpredictably; desktop/plugin integration. **Integration:** Medium manual; high unattended adapter. **Worth testing:** Yes as a strange audition, not a default band.

<a id="t54"></a>

### T54 · AudioGuide

[Repository](https://github.com/benhackbarth/audioguide) · [Reviewed README](https://github.com/benhackbarth/audioguide/blob/12c2337c6cafcba307c3398849fe0a7e71c31c0b/README.md) · [License evidence](https://github.com/benhackbarth/audioguide)

**Purpose priority 4.** Offline concatenative synthesis with descriptor matching and layered output. Input: Target audio + corpus audio. Role: Audio-to-audio mosaic/orchestration without a score bottleneck.

**License:** Unresolved: no recognized root license returned; do not infer permission from public GitHub. **Maintenance:** Quiet default branch; latest default-branch commit 2024-11-12.

**Hardware:** CPU-light. **GPU:** No. **Mac:** Traditional Mac-oriented research stack; current arm64 path unverified. **Linux/server:** Python/Csound plausible; dependency portability unverified.

**Limits:** License not identified in API/README audit; analysis dependencies and corpus rights need verification. **Integration:** High relative to FluCoMa. **Worth testing:** Research first; hold execution/adoption until terms established.

## H. Neural transformation and audio rendering

| Priority | Tool | Input | First use | Test decision |
|---|---|---|---|---|
| 1 | [Magenta RealTime 2](#t55) | MIDI + context audio + audio/text style | A neural session band following the canonical notes while developing sound. | Yes: first larger-model audition, separate from cheap baseline. |
| 2 | [DDSP](#t56) | Audio-derived f0/loudness or control curves | Preserve pitch slides and dynamics while replacing vocal timbre. | Yes: expressive instrument transformation. |
| 2 | [RAVE](#t57) | Audio | Strange performer preserving gestures/texture rather than exact notes. | Conditional research audition with recorded license scope. |
| 3 | [ACE-Step 1.5](#t58) | Source/reference audio + controls | A freer cover musician using source audio, not a text-only prompt. | Yes after cheaper baselines, bounded source-fidelity test. |
| 3 | [AFTER](#t59) | Structure audio/MIDI + timbre audio | Experimental session musician blending melody structure with another sound. | Conditional: later timbre-control study. |
| 4 | [AudioCraft / MusicGen Melody](#t60) | Melody audio/chroma + text | Historical neural melodic-conditioning baseline. | Later bounded server comparator. |
| 4 | [DDSP-VST](#t61) | Audio or MIDI | Manual listening reference for DDSP without designing an instrument. | Historical/demo comparison only. |
| 4 | [stable-audio-tools](#t62) | Audio/init audio/conditioning, model-dependent | Alternative audio transformation worker when a suitable checkpoint is identified. | Defer unless a specific checkpoint answers a new question. |

<a id="t55"></a>

### T55 · Magenta RealTime 2

[Repository](https://github.com/magenta/magenta-realtime) · [Reviewed README](https://github.com/magenta/magenta-realtime/blob/694a545e4ba0b88bf1150137b129582166d3e07f/README.md) · [License evidence](https://github.com/magenta/magenta-realtime/blob/694a545e4ba0b88bf1150137b129582166d3e07f/LICENSE)

**Purpose priority 1.** Local streaming instrumental generation with per-frame MIDI control. Input: MIDI + context audio + audio/text style. Role: A neural session band following the canonical notes while developing sound.

**License:** Apache-2.0 code; weights CC-BY-4.0 plus model-card usage terms. **Maintenance:** Recent default-branch activity; latest default-branch commit 2026-07-30.

**Hardware:** Apple-neural. **GPU:** Apple integrated GPU or NVIDIA practical; no paid API needed.. **Mac:** Official small 230M model supports Apple Silicon; larger 2.4B model performance varies by chip. **Linux/server:** Official Python offline NVIDIA path; no CPU performance claim.

**Limits:** Style audio is not exact melody control; use MIDI channel. Vocallike sounds remain possible; fidelity and 15-second endings untested. **Integration:** Medium–high: dedicated MLX worker and event bridge. **Worth testing:** Yes: first larger-model audition, separate from cheap baseline.

<a id="t56"></a>

### T56 · DDSP

[Repository](https://github.com/magenta/ddsp) · [Reviewed README](https://github.com/magenta/ddsp/blob/6b6b8a31832290b1ef756c15129b1e32446acb10/README.md) · [License evidence](https://github.com/magenta/ddsp/blob/6b6b8a31832290b1ef756c15129b1e32446acb10/LICENSE)

**Purpose priority 2.** Differentiable harmonic/noise synthesis and trained timbre transfer. Input: Audio-derived f0/loudness or control curves. Role: Preserve pitch slides and dynamics while replacing vocal timbre.

**License:** Apache-2.0 code; preserve chosen model asset notices. **Maintenance:** Recent default-branch activity; latest default-branch commit 2026-09-22.

**Hardware:** CPU-neural. **GPU:** Pretrained inference may use CPU; training preferably GPU.. **Mac:** CPU/TensorFlow possible; arm64 version compatibility needs verification. **Linux/server:** Documented TensorFlow stack.

**Limits:** Usually monophonic and target-model range limited; not a complete arranger. **Integration:** Medium–high: isolate TensorFlow and checkpoint. **Worth testing:** Yes: expressive instrument transformation.

<a id="t57"></a>

### T57 · RAVE

[Repository](https://github.com/acids-ircam/RAVE) · [Reviewed README](https://github.com/acids-ircam/RAVE/blob/f048ec4569afba7c6ba38d590be8a07b8ab24840/README.md) · [License evidence](https://github.com/acids-ircam/RAVE/blob/f048ec4569afba7c6ba38d590be8a07b8ab24840/LICENSE)

**Purpose priority 2.** Fast learned audio autoencoding, latent manipulation and timbre transfer. Input: Audio. Role: Strange performer preserving gestures/texture rather than exact notes.

**License:** CC-BY-NC-4.0 repository; inspect each pretrained model license. **Maintenance:** Intermittent / older activity; latest default-branch commit 2025-04-26.

**Hardware:** CPU-neural. **GPU:** Not required for suitable pretrained inference; training variants list 5–32 GB GPU minima.. **Mac:** Mac plugin documented; exported CPU inference plausible. **Linux/server:** Python/offline generation supported.

**Limits:** Not guaranteed pitch or word removal; model domain strongly affects result. NC code is source-available, not permissive OSS. **Integration:** Medium inference; high custom training. **Worth testing:** Conditional research audition with recorded license scope.

<a id="t58"></a>

### T58 · ACE-Step 1.5

[Repository](https://github.com/ace-step/ACE-Step-1.5) · [Reviewed README](https://github.com/ace-step/ACE-Step-1.5/blob/ca1e85fe9430179831e6bc6be790c332190a3866/README.md) · [License evidence](https://github.com/ace-step/ACE-Step-1.5/blob/ca1e85fe9430179831e6bc6be790c332190a3866/LICENSE)

**Purpose priority 3.** Local music generation, cover/repainting and audio editing modes. Input: Source/reference audio + controls. Role: A freer cover musician using source audio, not a text-only prompt.

**License:** MIT code; verify exact model-card terms for selected DiT/LM checkpoints. **Maintenance:** Recent default-branch activity; latest default-branch commit 2026-08-29.

**Hardware:** Apple-neural. **GPU:** Not strictly; CPU supported. Small/offload and XL have very different memory needs.. **Mac:** Official Apple Silicon MLX launch path. **Linux/server:** CUDA/ROCm/CPU documented; CUDA usually preferable.

**Limits:** Reference-style conditioning differs from source/cover conditioning. Can lose motif or introduce voice; variants have different capabilities. **Integration:** Medium–high: isolated worker, model download and pinned mode. **Worth testing:** Yes after cheaper baselines, bounded source-fidelity test.

<a id="t59"></a>

### T59 · AFTER

[Repository](https://github.com/acids-ircam/AFTER) · [Reviewed README](https://github.com/acids-ircam/AFTER/blob/60ced7671b229f2164a7a0e6a1d9b5971e9b6ccb/README.md) · [License evidence](https://github.com/acids-ircam/AFTER/blob/60ced7671b229f2164a7a0e6a1d9b5971e9b6ccb/LICENSE.md)

**Purpose priority 3.** Latent diffusion transfers structure and timbre from different sources. Input: Structure audio/MIDI + timbre audio. Role: Experimental session musician blending melody structure with another sound.

**License:** CC-BY-NC-4.0 code; checkpoint terms must also be preserved. **Maintenance:** Recent default-branch activity; latest default-branch commit 2026-07-29.

**Hardware:** Apple-neural. **GPU:** Acceleration recommended; CPU path exists for parts, performance unverified.. **Mac:** Current README documents MPS support. **Linux/server:** CUDA research path documented.

**Limits:** Research integration; model/codec matching; default demos use paid hosts, but Python notebooks provide a local route. **Integration:** High. **Worth testing:** Conditional: later timbre-control study.

<a id="t60"></a>

### T60 · AudioCraft / MusicGen Melody

[Repository](https://github.com/facebookresearch/audiocraft) · [Reviewed README](https://github.com/facebookresearch/audiocraft/blob/896ec7c47f5e5d1e5aa1e4b260c4405328bf009d/README.md) · [License evidence](https://github.com/facebookresearch/audiocraft/blob/896ec7c47f5e5d1e5aa1e4b260c4405328bf009d/LICENSE)

**Purpose priority 4.** Audio generation conditioned on a melodic audio signal. Input: Melody audio/chroma + text. Role: Historical neural melodic-conditioning baseline.

**License:** MIT code; model weights CC-BY-NC-4.0. **Maintenance:** Quiet default branch; latest default-branch commit 2025-03-13.

**Hardware:** Server-neural. **GPU:** Practical GPU recommended; upstream recommends 16 GB for medium models.. **Mac:** CPU experimentation possible but not a practical first path; MPS compatibility unverified. **Linux/server:** Primary PyTorch/CUDA path.

**Limits:** Chroma conditioning is coarse; may not preserve note timing. Older stack and NC weights. **Integration:** High. **Worth testing:** Later bounded server comparator.

<a id="t61"></a>

### T61 · DDSP-VST

[Repository](https://github.com/magenta/ddsp-vst) · [Reviewed README](https://github.com/magenta/ddsp-vst/blob/f2996e97f9469f3956a6b8e9d2d9b50b6555e1e9/README.md) · [License evidence](https://github.com/magenta/ddsp-vst/blob/f2996e97f9469f3956a6b8e9d2d9b50b6555e1e9/LICENSE)

**Purpose priority 4.** Packaged DDSP instruments/effects for timbre-transfer audition. Input: Audio or MIDI. Role: Manual listening reference for DDSP without designing an instrument.

**License:** Apache-2.0 code; dependencies and embedded model notices separate. **Maintenance:** Archived; latest default-branch commit 2023-05-19.

**Hardware:** CPU-neural. **GPU:** No intended for real-time plugin inference.. **Mac:** Mac builds documented; current OS/arm64 compatibility unverified. **Linux/server:** No equivalent turnkey Linux release established here.

**Limits:** Archived repository; platform builds and pretrained instrument terms need checking. **Integration:** Medium manual; high headless automation. **Worth testing:** Historical/demo comparison only.

<a id="t62"></a>

### T62 · stable-audio-tools

[Repository](https://github.com/Stability-AI/stable-audio-tools) · [Reviewed README](https://github.com/Stability-AI/stable-audio-tools/blob/3241adba4fc2a85cf5b29d9eb68d42f40a28e820/README.md) · [License evidence](https://github.com/Stability-AI/stable-audio-tools/blob/3241adba4fc2a85cf5b29d9eb68d42f40a28e820/LICENSE)

**Purpose priority 4.** Training/inference toolkit for several audio model types. Input: Audio/init audio/conditioning, model-dependent. Role: Alternative audio transformation worker when a suitable checkpoint is identified.

**License:** MIT code; checkpoint-specific terms may be restrictive or gated. **Maintenance:** Recent default-branch activity; latest default-branch commit 2026-05-26.

**Hardware:** Server-neural. **GPU:** Model-dependent; practical GPU for larger diffusion checkpoints.. **Mac:** No universal supported path for all checkpoints; previous MLX experiment was a separate runtime. **Linux/server:** Primary PyTorch/CUDA research path.

**Limits:** Toolkit alone provides no fidelity guarantee; model availability and licenses separate. Existing Stable Audio trial did not meet the target sound quality. **Integration:** High. **Worth testing:** Defer unless a specific checkpoint answers a new question.

## I. Open instrument recordings

| Priority | Tool | Input | First use | Test decision |
|---|---|---|---|---|
| 1 | [VCSL](#t63) | Recorded samples | Percussion/odd instruments and controlled renderer comparisons. | Yes: existing subset is a useful control. |
| 1 | [VSCO 2 Community Edition](#t64) | Recorded samples/SFZ | Existing recorded voices; common audition material. | Yes: already installed subset and technical spot checks. |
| 2 | [FreePats clean electric guitar](#t65) | Recorded samples/SFZ | Existing guitar control; riff, arpeggio and processing experiments. | Yes: retain for like-for-like comparisons. |

<a id="t63"></a>

### T63 · VCSL

[Repository](https://github.com/sgossner/VCSL) · [Reviewed README](https://github.com/sgossner/VCSL/blob/c1ea7bcc3c7309650ab0da9d15c9cd1fbc4a4c7e/README.md) · [License evidence](https://github.com/sgossner/VCSL/blob/c1ea7bcc3c7309650ab0da9d15c9cd1fbc4a4c7e/LICENSE)

**Purpose priority 1.** Broad open instrument and percussion collection. Input: Recorded samples. Role: Percussion/odd instruments and controlled renderer comparisons.

**License:** CC0-1.0 **Maintenance:** Intermittent / older activity; latest default-branch commit 2026-01-14.

**Hardware:** CPU-light; sample storage. **GPU:** No. **Mac:** Portable files; existing subset works. **Linux/server:** Portable files; requires a sampler.

**Limits:** Library license does not solve articulation or arranging; download only selected assets. **Integration:** Low. **Worth testing:** Yes: existing subset is a useful control.

<a id="t64"></a>

### T64 · VSCO 2 Community Edition

[Repository](https://github.com/sgossner/VSCO-2-CE) · [Reviewed README](https://github.com/sgossner/VSCO-2-CE/blob/440300901dfe9275fd84e0b7763af1f8443ae62e/README.md) · [License evidence](https://github.com/sgossner/VSCO-2-CE/blob/440300901dfe9275fd84e0b7763af1f8443ae62e/LICENSE)

**Purpose priority 1.** Acoustic instrument recordings including strings and brass. Input: Recorded samples/SFZ. Role: Existing recorded voices; common audition material.

**License:** CC0-1.0 **Maintenance:** Quiet default branch; latest default-branch commit 2020-08-05.

**Hardware:** CPU-light; sample storage. **GPU:** No. **Mac:** Portable recordings; current subset already works. **Linux/server:** Portable recordings; requires a sampler.

**Limits:** Sampling/articulation quality varies; an old asset release is not necessarily a maintenance problem. **Integration:** Low with current bank; medium full SFZ mapping. **Worth testing:** Yes: already installed subset and technical spot checks.

<a id="t65"></a>

### T65 · FreePats clean electric guitar

[Repository](https://github.com/freepats/electric-guitar-FSBS-clean) · [Reviewed README](https://github.com/freepats/electric-guitar-FSBS-clean/blob/192cf0d9bf2c4ba6ead8e3524ba3f78818e4fe91/README.txt) · [License evidence](https://github.com/freepats/electric-guitar-FSBS-clean/blob/192cf0d9bf2c4ba6ead8e3524ba3f78818e4fe91/LICENSE.txt)

**Purpose priority 2.** Clean electric-guitar multisamples. Input: Recorded samples/SFZ. Role: Existing guitar control; riff, arpeggio and processing experiments.

**License:** CC0-1.0 **Maintenance:** Recent default-branch activity; latest default-branch commit 2026-08-07.

**Hardware:** CPU-light; sample storage. **GPU:** No. **Mac:** Portable files; existing subset works. **Linux/server:** Portable files; requires a sampler.

**Limits:** Clean samples still need phrasing, release and effects; not realistic guitar technique by default. **Integration:** Low with current bank. **Worth testing:** Yes: retain for like-for-like comparisons.
