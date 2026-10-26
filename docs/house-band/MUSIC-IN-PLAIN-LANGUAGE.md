# Music in plain language

You can judge the result without knowing music theory. “That sounds like my idea,”
“more bounce,” “too busy,” or “the ending lost its lift” are useful feedback.

Imagine singing “daaa, da-da, daaa” while tapping your foot. Your foot can mark a
steady **beat**. How fast it taps is **tempo**. The long and short “da” sounds make
**rhythm**. Which sounds are higher or lower gives the phrase its **pitches**.
The pitches together with their timing form the **melody**.

| Term | Plain meaning | Something you might say |
| --- | --- | --- |
| Pitch | How high or low one musical sound is. | “That note goes higher.” |
| Melody | The tune: a sequence of pitches and their timing. | “I can still hum my original idea.” |
| Contour | The overall rising, falling or level shape of a melody. | “It climbs, hangs there, then drops.” |
| Beat / pulse | The regular underlying tick you might tap your foot to. Not every note falls on it. | “I can tap along.” |
| Tempo | How fast that underlying pulse moves, often measured in beats per minute. | “Make it faster.” |
| Rhythm | The pattern of sounds and silences: their placement and lengths. | “Long, short-short, pause, long.” |
| Meter | How beats group into recurring patterns, often threes or fours. | “It has a one-two-three sway.” |
| Groove | How the timing and accents feel together: straight, swinging, bouncing, driving or relaxed. | “More bounce, without making it faster.” |
| Harmony / chords | Notes sounding together and the supporting chords around a tune. Different chords can change how the same melody feels. | “Keep the tune but make the surroundings warmer.” |
| Timbre (TAM-ber) | The character of a sound. A violin and trumpet can play the same pitch and sound different. | “Less buzzy, more woody.” |
| Orchestration | Which instruments play which parts: who carries the tune, supports it or answers it. It applies to any ensemble. | “Give the tune to a saxophone, with bass and drums underneath.” |
| Dynamics | Changes in musical loudness or intensity. A crescendo is a gradual increase in loudness. | “Build toward the end.” |
| Articulation | How individual notes begin, connect and end: short, smooth, sharp, breathy or accented. | “More flowing; less pecking at each note.” |
| Phrasing | How notes are grouped and shaped into musical sentences, with breaths and emphasis. | “Let that thought finish before answering it.” |
| Texture / density | How many things are happening and how they fit together. | “Start sparse, then let the whole band join.” |
| Form / development | How the piece unfolds: repeats, changes, builds, returns and endings. | “Say the idea, explore it, then bring it back.” |

A **bass line** is the low supporting part. A **countermelody** is a second tune
that complements the main one. A **motif** is a short, memorable fragment that
can be repeated or developed. A **key** is a tonal home or center and the notes
associated with it; a very short phrase may suggest several possible keys.
An **arrangement** is the broader plan for a performance, including harmony,
groove, structure and orchestration.

In everyday speech, “the beat” can also mean the drum pattern or an entire backing
track. It helps to say whether you mean the steady pulse, the drums, or the overall
feel. Likewise, “more energetic” could mean faster tempo, sharper attacks, stronger
accents, more instruments, a higher melody, or some combination.

## What can come from a short recording?

Some things can be measured directly: the waveform's timing and level. Others must
be estimated: pitch, note boundaries, pulse, phrases, and which changes matter
musically. Background noise, phone processing, slides between notes and loose
rhythm make those estimates uncertain. Tapping can convey rhythm without a clear
melody. A single held note can convey an expressive swell without a beat.

| Feature | In this prototype today | Practical limit |
| --- | --- | --- |
| Melody / pitch / contour | Estimated from the recording, reduced to discrete notes and passed to the band. | Pitch slides, octave errors and extra split notes can occur. |
| Note timing, lengths and gaps | Estimated and preserved proportionally when fitting the phrase into the output. | This is not the same as establishing a correct tempo or meter. The control grid is 40 ms. |
| Loudness / dynamic shape | Measured and saved in the analysis. | The current MRT2 note-control route does not pass those measurements to the model. A generated crescendo is not proof it followed the source's swell. Phone level is not identical to expressive intent. |
| Phrasing / articulation | Gaps and connected-note timing supply partial clues. | Phrase interpretation is basic; the performer chooses much of the articulation. |
| Tempo / beat / meter | Potential analysis targets; not reliable source-derived controls in this trial. | A short, freely sung phrase may support several plausible pulses or none. An earlier rough tempo estimate is not a verified musical beat. |
| Harmony / key | The band supplies musical context around the notes. | One sung melody rarely specifies unique chords; compatible alternatives are part of the experiment. |
| Instruments / groove / texture | Requested through a fixed internal style description for each variant. | The model interprets these descriptions; they do not guarantee an exact ensemble or isolated control of one variable. |
| Emotional arc / climax / ending | Evaluated by listening; still an open development target. | Feeling and intent cannot be read directly from one number. Current ending treatment includes a short fade. |

A musical build can be conveyed by rising pitch, increasing loudness,
more active rhythm, denser orchestration, harmonic tension and how phrases breathe.
We should learn which cues the seed contains and test how they survive. We should
not automatically give every recording the same late build.

## This listening round stays within the experiment plan

A and B were both positively received as connected to this seed. Keep them as
references. Six new versions D–I use B's note settings, the same source recording,
model, random seed and 15-second output length. Only the style description changes.
That explores ensemble directions; since a style can change instrumentation,
groove and harmony together, it is not a clean test of any single musical variable.
C, the earlier dance-pop attempt, remains available and has not been rated.

For now ask listeners:

1. Can you recognize the original idea? (1 = no connection, 5 = clearly connected.)
2. Do you enjoy the musical result? (1 = not appealing, 5 = would happily keep it.)
3. What feels different or memorable? Which versions seem too similar?

More than one good choice is a successful outcome. We do not need a forced winner.
The next tests should use unfamiliar recordings, including different expressive
arcs and tapping, before committing to an application architecture. This round
uses a familiar development recording and cannot establish performance for all
students. The vocabulary is a reference for discussion, not required student input.
