"""Control wiring tests; do not imply model quality or successful note adherence."""

import numpy as np

from experiments.mrt2_trial import note_controls


def test_note_events_reach_model_and_free_registers_remain_available():
    sketch = {
        "source_origin_seconds": 2.0,
        "source_end_seconds": 4.0,
        "notes": [
            {"start": 2.0, "duration": 0.3, "midi": 60, "source_note_id": 0},
            {"start": 2.8, "duration": 0.4, "midi": 65, "source_note_id": 1},
            {"start": 3.8, "duration": 0.2, "midi": 62, "source_note_id": 2},
        ],
    }
    roll, mapping, policy = note_controls(sketch)
    assert roll.shape == (400, 128)
    assert set(np.unique(roll)) == {-1, 0, 1, 2}
    assert np.all(roll[:, 40] == -1) and np.all(roll[:, 61] == 0)
    assert [n["midi"] for n in mapping] == [60, 65, 62]
    for note in mapping:
        start, end = round(note["model_start"] * 25), round(note["model_end"] * 25)
        assert roll[start, note["midi"]] == 2
        assert np.all(roll[start + 1 : end, note["midi"]] == 1)
        assert roll[end, note["midi"]] == 0
    assert np.all(roll[350:, 60:66] == 0)
    assert policy["source_origin"] == 2.0


def test_connected_pitch_changes_allow_performer_articulation():
    sketch = {
        "source_origin_seconds": 0.0,
        "source_end_seconds": 2.0,
        "notes": [
            {"start": 0.0, "duration": 1.0, "midi": 60, "source_note_id": 0},
            {"start": 1.0, "duration": 1.0, "midi": 62, "source_note_id": 1},
        ],
    }
    roll, mapping, _ = note_controls(sketch)
    assert roll[round(mapping[0]["model_start"] * 25), 60] == 2
    assert roll[round(mapping[1]["model_start"] * 25), 62] == 3


def test_closer_profile_changes_guidance_without_changing_note_data():
    sketch = {
        "source_origin_seconds": 0.0,
        "source_end_seconds": 2.0,
        "notes": [
            {"start": 0.0, "duration": 1.0, "midi": 46, "source_note_id": 0},
            {"start": 1.0, "duration": 1.0, "midi": 65, "source_note_id": 1},
        ],
    }
    baseline, original_map, _ = note_controls(sketch)
    closer, closer_map, _ = note_controls(sketch, profile="closer")
    assert np.array_equal(baseline, closer)
    assert original_map == closer_map


def test_lead_profile_keeps_intervals_and_timing_and_leaves_room_for_bass():
    sketch = {
        "source_origin_seconds": 0.0,
        "source_end_seconds": 3.0,
        "notes": [
            {"start": 0.0, "duration": 0.5, "midi": 46, "source_note_id": 0},
            {"start": 1.0, "duration": 0.6, "midi": 54, "source_note_id": 1},
            {"start": 2.0, "duration": 1.0, "midi": 65, "source_note_id": 2},
        ],
    }
    _, baseline, _ = note_controls(sketch)
    roll, lead, policy = note_controls(sketch, profile="lead")
    assert policy["octave_shift_semitones"] == 12
    assert [n["model_start"] for n in lead] == [n["model_start"] for n in baseline]
    assert [n["model_end"] for n in lead] == [n["model_end"] for n in baseline]
    assert np.array_equal(np.diff([n["midi"] for n in lead]), np.diff([n["midi"] for n in baseline]))
    assert all(n["source_midi"] % 12 == n["midi"] % 12 for n in lead)
    assert np.all(roll[:, 40] == -1)
    assert np.all(roll[:, 80] == 0)
    for note in lead:
        assert roll[round(note["model_start"] * 25), note["midi"]] == note["onset_state"]
