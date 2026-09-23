# Known limitations and next steps

> Free local recorded-instrument arrangements are implemented without a GPU requirement. Professional ensemble quality and recognizable melodic authorship remain listening criteria, not proven by passing software tests. The older DSP recipes remain for history/regression only.

## Deliberately unfinished

- The current arranger preserves accepted melody pitches/onsets but uses heuristic harmony and accompaniment. It can sound mechanical or harmonize poorly, and has no true legato string transitions. The new synth, electric-guitar and brass versions target a more upbeat feel, but college-student appeal and professional ensemble quality need listening trials. The fixed accompaniment pulse can clash with a rubato lead; preserving the accepted melody does not prove a convincing groove. Setup requires about 489 MB of free instrument downloads. The earlier model and its separate license/runtime remain historical.
- One local declared author per project; no verified identity, separate per-action collaborators, access control or tamper-proof audit log. Anyone using this local instance can access its projects.
- Three current audio arrangements, three visual families, three text families and three assembly recipes. Nine historical DSP audio recipes remain internal. Style files are editable, but new algorithms need implementation. No conversational refinement/prompt editor. Another batch is a fresh explicit generation request.
- Original Mix uses the first 15 seconds. Long recordings are cropped to that excerpt, short ones padded with silence. The complete original remains saved. No trim-point picker yet.
- The three assembly variants preserve selected files and change compositing, crop, title delay/scale/position and audio fades. They do not yet rebuild video cut timing from original photographs.
- Audio analysis is RMS/onset heuristics. Tempo may be unknown or wrong; the pYIN melody estimate can be wrong. No source separation or verified harmonic matching is claimed. Text placement does not recognize faces/subjects.
- Center cropping can exclude a subject. Bold deformation can be unflattering. Review actual outputs. No face-aware framing, captioning or accessible transcript export yet.
- Font coverage is limited to bundled Outfit; unsupported scripts/emoji may render as missing glyphs. The Keyword validator does not promise support for every writing system.
- ProRes alpha can use substantial disk space. No storage quota, retention UI, trash, garbage collection or project deletion yet. Back up the entire private data folder with the server stopped.
- One server/worker. Native Windows unsupported; use WSL. Jobs continue when a browser closes; stopping the process interrupts work. Retry is explicit. Progress is per operation/frame, not a reliable ETA.
- A manual retry preserves successful candidates. No partial candidate resume, cancellation UI, or distributed worker recovery. No cloud retry/cost reconciliation exists because no cloud calls exist.
- Thumbnail wave shapes in audio cards are decorative. Numerical audio analysis is recorded separately.
- No old-data migration; the previous studio is preserved in Git history and its existing data are left alone.
- No course-library integration or public site. No automatic posting. No automatic final explanation or approval.

## Before a small student alpha

Target: a supervised Story Officer trial around October 6, 2026, conditional on readiness rather than a guaranteed launch date.

1. Danny/Talla complete several real stories and observe where selection becomes confusing. Decide whether local output quality proves enough of the hypothesis; if not, test another free arrangement approach against the same accepted melodies.
2. Choose one hosting/deployment approach and verified identity mechanism. Add project-level permissions and record actual actors on contributions/reviews/approvals.
3. Add upload/content limits beyond local convenience, rate/spend limits, media-use consent and retention/deletion policies, and a safe process for inappropriate submissions.
4. Isolate rendering from the web process, add real cancellation/timeouts, define storage quotas, and test recovery and backup/restore. Choose PostgreSQL/object storage only if the chosen hosting/concurrency requires them.
5. Test a bounded simultaneous-user scenario and a simple support path. Define what “submit” means, who reviews it, and how students see provenance.
6. Start with a small supervised group, observe complete sessions, and fix the biggest friction before increasing access. Do not invite 100+ students to the local prototype.

## Later, if evidence supports it

Reference-driven AI, richer contextual analysis, course library, Key Phrase, other durations, richer editing, and approved-content supply to a future public website. Do not build adaptive taste learning merely because ratings exist.
