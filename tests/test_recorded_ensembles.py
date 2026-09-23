"""Musical structure and sample integrity checks; no subjective quality claims."""

import hashlib
import json

import numpy as np
import pytest
import soundfile as sf
from fastapi.testclient import TestClient

from mit2009_studio import media
from mit2009_studio.models import Generate
from mit2009_studio.providers import arranged
from mit2009_studio.server import create_app


@pytest.fixture
def instrument_bank(tmp_path, monkeypatch):
    folder = tmp_path / "instruments"
    folder.mkdir()
    entries = []
    # Deliberately synthetic test fixtures keep CI independent of downloaded recordings.
    rate = 16000
    t = np.arange(rate * 2) / rate
    tone = 0.25 * np.sin(2 * np.pi * 261.6256 * t) * np.exp(-t)
    for instrument in (
        "guitar",
        "trumpet",
        "trombone",
        "piano",
        "violin",
        "cello",
        "violin_pizz",
        "cello_pizz",
        "bass",
        "hat",
        "snare",
        "kick",
    ):
        path = folder / f"{instrument}.wav"
        sf.write(path, tone, rate, subtype="PCM_16")
        data = path.read_bytes()
        entries.append(
            {
                "instrument": instrument,
                "midi": 60,
                "velocity": 70,
                "file": path.name,
                "bytes": len(data),
                "git_blob": hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest(),
            }
        )
    installed = {"folder": folder, "catalog": {"samples": entries}, "catalog_sha256": "test-only"}
    monkeypatch.setattr(arranged, "runtime", lambda: installed)
    monkeypatch.setattr("mit2009_studio.server.runtime", lambda: installed)
    return installed


def test_every_arrangement_keeps_note_order_pitch_and_relative_timing():
    # Includes short ornaments, internal rests, and a note very close to the end.
    score = {
        "notes": [
            {"midi": p, "start": t, "duration": d}
            for p, t, d in [(60, 0, 0.12), (64, 0.41, 0.09), (63, 0.5, 0.2), (67, 2.2, 0.4), (59, 14.8, 0.15)]
        ]
    }
    accompaniments = []
    for style in ("dance", "chamber", "jazz"):
        plan = arranged.arrange(score, style, 123)
        lead = [e for e in plan["events"] if e["role"] == "melody"]
        assert [(e["midi"], e["start"]) for e in lead] == [(n["midi"], n["start"]) for n in score["notes"]]
        assert all(e["instrument"] == "piano" for e in lead)
        assert all(0 <= e["start"] < 15 and e["duration"] > 0 for e in plan["events"])
        accompaniments.append(json.dumps([e for e in plan["events"] if e["role"] != "melody"]))
    assert len(set(accompaniments)) == 3
    shifted = {"notes": [{**n, "start": n["start"] + 1.2} for n in score["notes"][:3]]}
    assert [n["start"] for n in arranged.melody_notes(shifted)] == [0, 0.41, 0.5]


def test_sample_pitch_and_tamper_detection(instrument_bank):
    event = {"instrument": "piano", "midi": 69, "velocity": 70, "duration": 0.5}
    voice = arranged.InstrumentBank(instrument_bank).voice(event)
    y = voice[2400:18000, 0]
    nfft = 131072
    freq = np.argmax(np.abs(np.fft.rfft(y * np.hanning(len(y)), n=nfft))) * media.SAMPLE_RATE / nfft
    assert abs(freq - 440) < 1
    path = instrument_bank["folder"] / "piano.wav"
    path.write_bytes(path.read_bytes() + b"changed")
    with pytest.raises(ValueError, match="instrument changed"):
        arranged.InstrumentBank(instrument_bank).voice(event)


@pytest.mark.media
def test_recorded_api_produces_three_verified_drafts(studio, project, source_assets, instrument_bank):
    asset = source_assets[0]
    guide = studio.prepare_melody(asset["id"])
    original_hash = media.digest(studio.store.path(asset["original_path"]))
    app = create_app(studio.store.root, start_worker=False)
    with TestClient(app) as client:
        response = client.post(
            f"/api/projects/{project['id']}/generate",
            headers={"X-Studio-Request": "1"},
            json={"stage": "audio", "asset_ids": [asset["id"]]},
        )
        assert response.status_code == 202, response.text
        app.state.worker.perform(app.state.worker.claim())
        detail = studio.detail(project["id"])
        assert detail["jobs"][0]["status"] == "done", detail["jobs"][0]["error"]
        assert len(detail["candidates"]) == 3
        assert not detail["selections"] and not detail["approvals"]
        for c in detail["candidates"]:
            assert c["settings"]["provider"] == arranged.PROVIDER and c["rating"] is None
            assert c["settings"]["melody_guide"]["score_sha256"]
            path = studio.store.path(c["artifacts"]["output"]["path"])
            media.verify_output(path, 15, audio=True)
            assert c["analysis"]["process"]["guide_sha256"] == guide["sha256"]
            assert c["analysis"]["process"]["generation_cost_usd"] == 0
            assert np.isfinite(media.read_audio(path)).all()
            assert path.with_name("melody-stem.wav").is_file()
            assert path.with_name("arrangement.json").is_file()
        assert media.digest(studio.store.path(asset["original_path"])) == original_hash


@pytest.mark.media
def test_worker_rejects_changed_score(studio, project, source_assets, instrument_bank):
    asset = source_assets[0]
    guide = studio.prepare_melody(asset["id"])
    studio.enqueue(project["id"], Generate(stage="audio", asset_ids=[asset["id"]]), ensemble=True)
    path = studio.store.path(guide["score_path"])
    score = json.loads(path.read_text())
    score["notes"][0]["midi"] += 1
    path.write_text(json.dumps(score))
    app = create_app(studio.store.root, start_worker=False)
    app.state.worker.perform(app.state.worker.claim())
    detail = studio.detail(project["id"])
    assert detail["jobs"][0]["status"] == "failed"
    assert "score changed" in detail["jobs"][0]["error"]
    assert not any(c["status"] == "ready" for c in detail["candidates"])


@pytest.mark.parametrize("style,lead", [("dance", "synth_pluck"), ("chamber", "guitar"), ("jazz", "trumpet")])
def test_upbeat_versions_keep_the_phrase_without_piano(style, lead):
    score = {
        "notes": [
            {"midi": p, "start": t, "duration": 0.16}
            for p, t in [(60, 0), (64, 0.48), (67, 2.8), (65, 3.2), (59, 14.8)]
        ]
    }
    plan = arranged.arrange(score, style, 29, feel="upbeat")
    melody = [e for e in plan["events"] if e["role"] == "melody"]
    assert [(e["midi"], e["start"]) for e in melody] == [(n["midi"], n["start"]) for n in score["notes"]]
    assert {e["instrument"] for e in melody} == {lead}
    assert "piano" not in {e["instrument"] for e in plan["events"]}
    assert any(e.get("part") == "phrase answer" for e in plan["events"])
    for answer in (e for e in plan["events"] if e.get("part") == "phrase answer"):
        assert not any(
            n["start"] < answer["start"] + answer["duration"] and n["start"] + n["duration"] > answer["start"]
            for n in score["notes"]
        )
    assert all(e["start"] >= 0 and e["start"] + e["duration"] <= 15.000001 for e in plan["events"])


def test_electronic_voices_are_finite_pitched_and_repeatable():
    from mit2009_studio.providers.electronic import VOICES, voice

    for name in VOICES:
        event = {"instrument": name, "midi": 60, "duration": 0.4, "velocity": 95, "start": 0.25}
        a = voice(event)
        assert a.shape[1] == 2 and np.isfinite(a).all()
        assert 0.01 < np.max(np.abs(a)) < 1
        assert np.array_equal(a, voice(event))
    event["instrument"] = "synth_pluck"
    y = voice(event)[1200:15000, 0]
    nfft = 131072
    fundamental = np.argmax(np.abs(np.fft.rfft(y * np.hanning(len(y)), n=nfft))) * media.SAMPLE_RATE / nfft
    assert abs(fundamental - 261.6256) < 2
