"""Lively accompaniment around the user's unchanged accepted melody."""

import numpy as np


def arrange_upbeat(score, style, seed, duration=15):
    from .arranged import close_pitch, harmonize, melody_notes

    notes = melody_notes(score)
    rng = np.random.default_rng(seed)
    end = max(n["start"] + n["duration"] for n in notes)
    bpm = {"dance": 136, "chamber": 122, "jazz": 112}[style]
    beat, bar = 60 / bpm, 240 / bpm
    chords = harmonize(notes, end, bar)
    lead = {"dance": "synth_pluck", "chamber": "guitar", "jazz": "trumpet"}[style]
    events = []

    def add(instrument, pitch, start, length, velocity, role="accompaniment", pan=0, part="groove"):
        if start < 0 or start >= duration or (role != "melody" and start >= duration - 0.5):
            return
        events.append(
            {
                "instrument": instrument,
                "midi": int(pitch),
                "start": round(start, 6),
                "duration": round(min(length, duration - start), 6),
                "velocity": int(np.clip(velocity, 20, 108)),
                "role": role,
                "pan": pan,
                "articulation": "detached",
                "part": part,
            }
        )

    for i, n in enumerate(notes):
        gap = notes[i + 1]["start"] - n["start"] if i + 1 < len(notes) else 1
        # The phrase keeps the user's rhythm. Accent its entrances without quantizing it.
        accent = 7 if i == 0 or n["start"] - notes[i - 1]["start"] > 0.6 else 0
        velocity = 83 + accent + 5 * np.sin(i * 0.8) + rng.normal(0, 1.5)
        length = min(max(n["duration"], 0.13), max(0.07, gap - 0.012))
        add(lead, n["midi"], n["start"], length, velocity, "melody", -0.06, "original phrase")

    previous = [55, 60, 64]
    for k, chord in enumerate(chords):
        start, root = chord["start"], chord["root"]
        pcs = [(root + i) % 12 for i in chord["intervals"]]
        bass = close_pitch(root, 40, 34, 48)
        voicing = sorted(close_pitch(pc, previous[i], 50, 72) for i, pc in enumerate(pcs))
        previous = voicing
        lift = 0 if k == 0 else 5 if k < len(chords) - 1 else 2
        for b in range(4):
            at = start + b * beat
            if at >= end:
                break
            if style == "chamber":
                # Plucked low strings and answering upper strings make a bouncing texture.
                if b % 2 == 0:
                    p = bass if b == 0 else close_pitch(pcs[2], bass, 36, 55)
                    add("bass", p, at, beat * 0.42, 72 + lift, pan=0.24, part="plucked pulse")
                upper = close_pitch(pcs[(b + k) % 3], 69, 60, 81)
                add(
                    "violin_pizz",
                    upper,
                    at + beat * 0.5,
                    beat * 0.26,
                    60 + lift + (4 if b % 2 else 0),
                    pan=-0.25,
                    part="offbeat strings",
                )
                add("club_kick", 36, at, 0.18, 73 + lift, part="indie dance beat")
                add("hat", 42, at + beat * 0.5, 0.08, 46 + lift, pan=0.22, part="offbeat hats")
                if b % 2:
                    add("clap", 38, at + 0.005, 0.15, 67 + lift, pan=-0.1, part="backbeat")
            elif style == "dance":
                add("club_kick", 36, at, 0.19, 83 + lift, part="dance pulse")
                add("hat", 42, at, 0.07, 35 + lift, pan=0.22, part="eighth notes")
                add("hat", 42, at + beat * 0.5, 0.10, 57 + lift, pan=0.22, part="eighth notes")
                if b % 2:
                    add("clap", 38, at + 0.005, 0.15, 83 + lift, pan=-0.1, part="backbeat")
                # Offbeat octave bass leaves room for each kick attack.
                p = bass + (12 if b == 3 else 0)
                add("sub", p, at + beat * 0.5, beat * 0.34, 86 + lift, part="offbeat bass")
            else:
                # Root/third/fifth/approach bass with a syncopated funk rhythm section.
                p = close_pitch(pcs[min(b, 2)], bass + b, 31, 52)
                if b == 3 and k + 1 < len(chords):
                    next_root = close_pitch(chords[k + 1]["root"], p, 34, 48)
                    p = next_root + (1 if p > next_root else -1)
                add(
                    "bass",
                    p,
                    at + rng.uniform(0, 0.006),
                    beat * 0.66,
                    76 + lift - b % 2 * 5,
                    pan=0.05,
                    part="funk bass",
                )
                add("hat", 42, at, 0.09, 42 + lift, pan=0.2, part="funk pulse")
                if b % 2 == 0:
                    add("hat", 42, at + beat * 0.75, 0.07, 34 + lift, pan=0.2, part="funk pickup")
                if b % 2:
                    add("snare", 38, at + 0.006, 0.13, 48 + lift, pan=-0.12, part="backbeat")
                if b in (0, 2):
                    add("kick", 36, at, 0.17, 39 + lift, part="light kick")
        offsets = {"dance": [0.5, 1.75, 2.5, 3.5], "jazz": [0.75, 2.5], "chamber": [0.5, 2.5, 3.5]}[style]
        for off in offsets:
            at = start + off * beat
            if at >= end:
                continue
            # Short chord accents have a rhythmic role, not a sustained pad.
            for j, p in enumerate(voicing):
                add(
                    "trombone" if style == "jazz" else lead,
                    p,
                    at + j * 0.006,
                    beat * 0.27,
                    (57 if style == "dance" else 46) + lift + j * 2,
                    pan=-0.06,
                    part="chord accents",
                )

    # Reply using tiny fragments of the user's own phrase, only in its longer rests.
    for i, n in enumerate(notes[:-1]):
        left = n["start"] + n["duration"] + 0.14
        right = notes[i + 1]["start"] - 0.13
        fragment = notes[max(0, i - 1) : i + 1]
        spacing = beat * 0.5
        if right - left < len(fragment) * spacing + 0.08:
            continue
        start = left + min(0.1, (right - left - len(fragment) * spacing) / 2)
        for j, source in enumerate(fragment):
            p = source["midi"] + 12
            while p > 84:
                p -= 12
            add(
                lead,
                p,
                start + j * spacing,
                beat * 0.24,
                60 + j * 5,
                pan=-0.22 if style == "chamber" else 0.12,
                part="phrase answer",
            )

    # A compact two-hit tag provides a finish, with a full second for the decay.
    tag = end + 0.18
    if tag + beat * 0.75 < duration - 1:
        last = chords[-1]
        for hit in range(2):
            at = tag + hit * beat * 0.75
            for j, interval in enumerate(last["intervals"]):
                add(
                    lead,
                    close_pitch(last["root"] + interval, 57 + j * 3, 46, 78),
                    at + j * 0.005,
                    0.15 if hit == 0 else 0.35,
                    66 - hit * 4,
                    pan=-0.06,
                    part="closing tag",
                )
            if style == "chamber":
                add(
                    "bass",
                    close_pitch(last["root"], 43, 36, 55),
                    at,
                    0.25,
                    71,
                    pan=0.24,
                    part="closing tag",
                )
            else:
                add(
                    "bass" if style == "jazz" else "sub",
                    close_pitch(last["root"], 40, 34, 48),
                    at,
                    0.3,
                    72,
                    part="closing tag",
                )
    return {
        "version": 2,
        "feel": "upbeat",
        "style": style,
        "melody_notes": notes,
        "chords": chords,
        "events": sorted(events, key=lambda e: e["start"]),
        "accompaniment_bpm": bpm,
        "note": "Lead pitch/order/onsets preserved. Groove, articulation and answers are livelier; listening review is required.",
    }
