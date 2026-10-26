"""Contrasting expression fixtures and transformation contracts, not aesthetic scores."""

import numpy as np
import pytest

from experiments.audio_only import expression, make_plan


def fixture(gains):
    rate = 8000
    y = np.zeros((rate * 6, 2))
    notes = []
    for i, gain in enumerate(gains):
        start, length = 0.1 + i * 0.8, 0.6
        t = np.arange(round(length * rate)) / rate
        tone = 0.1 * gain * np.sin(2 * np.pi * 220 * t)
        at = round(start * rate)
        y[at : at + len(tone)] = tone[:, None]
        notes.append({"midi": 57, "start": start, "duration": length, "confidence": 1.0, "source_note_id": i})
    return y, notes, rate


@pytest.mark.parametrize(
    "gains,expected", [([0.2, 0.4, 0.6, 0.8, 1.0], 1), ([1.0, 0.8, 0.6, 0.4, 0.2], -1), ([1.0] * 5, 0)]
)
def test_audio_contour_does_not_always_invent_late_climax(gains, expected):
    audio, notes, rate = fixture(gains)
    cues = expression(audio, notes, rate)
    shape = np.array([c["gain_db"] for c in cues])
    if expected == 0:
        assert np.ptp(shape) < 0.1
    else:
        assert (shape[-1] - shape[0]) * expected > 8
        assert np.all(np.diff(shape) * expected >= 0)


def sketch():
    _, notes, _ = fixture([1.0] * 5)
    notes = [
        {**n, "midi": p, "gain_db": g, "gesture_gain_db": g}
        for n, p, g in zip(notes, [57, 60, 62, 65, 62], [-8, -5, -2, 0, -3], strict=True)
    ]
    return {"notes": notes, "source_origin_seconds": 0.1, "source_end_seconds": 3.9}


def test_musicians_change_structure_and_keep_traceable_source_contribution():
    source = sketch()
    plans = {k: make_plan(source, k, 2009) for k in ("faithful", "groove", "riff")}
    lead = {k: [e for e in p["events"] if e["role"] == "melody"] for k, p in plans.items()}
    expected = [n["midi"] for n in source["notes"]]
    assert [e["midi"] for e in lead["faithful"]] == expected
    assert [e["midi"] for e in lead["groove"]] == expected
    assert [e["start"] for e in lead["faithful"]] != [e["start"] for e in lead["groove"]]
    assert len(lead["riff"]) > len(expected)
    assert all("source_note_id" in e for events in lead.values() for e in events)
    original_intervals = np.diff([n["start"] for n in source["notes"]])
    fitted_intervals = np.diff([n["start"] for n in lead["faithful"]])
    assert np.ptp(fitted_intervals / original_intervals) < 1e-5
    for kind, plan in plans.items():
        assert plan == make_plan(source, kind, 2009)
        assert all(
            0 <= e["start"] < 15 and 0 < e["duration"] <= 15 - e["start"] + 1e-6 for e in plan["events"]
        )
        assert all(e["instrument"] != "piano" for e in plan["events"])


def test_short_project_setting_remains_bounded():
    for kind in ("faithful", "groove", "riff"):
        plan = make_plan(sketch(), kind, 2010, 7.0)
        assert all(e["start"] + e["duration"] < 7 for e in plan["events"])
