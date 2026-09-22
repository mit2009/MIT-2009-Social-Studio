import json
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from mit2009_studio import media
from mit2009_studio.demo import make_sources
from mit2009_studio.models import Generate, NewProject
from mit2009_studio.providers import ensemble
from mit2009_studio.server import create_app


@pytest.fixture
def local_runtime(tmp_path, monkeypatch):
    # A tiny stand-in exercises the subprocess/file boundary on CI without a 7 GB model.
    # Live-model sound quality is checked separately, never inferred from this fixture.
    script = tmp_path / "local_model.py"
    script.write_text("""import json, os, shutil, sys
from pathlib import Path
args = sys.argv[1:]
source = Path(args[args.index("--init-audio") + 1])
output = Path(args[args.index("--out") + 1])
shutil.copyfile(source, output)
output.with_suffix(".request.json").write_text(json.dumps({"args": args, "offline": os.environ.get("HF_HUB_OFFLINE")}))
""")
    runtime = {
        "python": Path(sys.executable),
        "script": script,
        "manifest": {"runtime_commit": "test-only", "model_revision": "test-only"},
    }
    monkeypatch.setattr(ensemble, "runtime", lambda: runtime)
    monkeypatch.setattr("mit2009_studio.server.runtime", lambda: runtime)
    return runtime


@pytest.mark.media
def test_free_ensemble_api_uses_only_wordless_guide(tmp_path, local_runtime):
    app = create_app(tmp_path / "data", start_worker=False)
    studio = app.state.studio
    source, _ = make_sources(tmp_path / "fixtures")
    project = studio.create_project(NewProject(name="Free ensembles", author="Test"))
    asset = studio.add_asset(project["id"], "reference", source.name, source)
    guide = studio.prepare_melody(asset["id"])
    before = media.digest(studio.store.path(asset["original_path"]))
    with TestClient(app) as client:
        response = client.post(
            f"/api/projects/{project['id']}/generate",
            headers={"X-Studio-Request": "1"},
            json={"stage": "audio", "asset_ids": [asset["id"]]},
        )
        assert response.status_code == 202, response.text
        app.state.worker.perform(app.state.worker.claim())
        detail = studio.detail(project["id"])
        assert len(detail["candidates"]) == 3
        assert {c["settings"]["style"]["id"] for c in detail["candidates"]} == {"dance", "chamber", "jazz"}
        assert detail["jobs"][0]["status"] == "done", detail["jobs"][0]["error"]
        assert detail["jobs"][0]["cost_usd"] == 0
        assert not detail["selections"] and not detail["approvals"]
        for c in detail["candidates"]:
            assert c["status"] == "ready" and c["rating"] is None
            assert c["settings"]["melody_guide"] == guide
            path = studio.store.path(c["artifacts"]["output"]["path"])
            media.verify_output(path, 15, audio=True)
            request = json.loads(path.with_name("model-output.request.json").read_text())
            assert request["offline"] == "1"
            assert str(studio.store.path(asset["path"])) not in request["args"]
            assert str(studio.store.path(asset["original_path"])) not in request["args"]
            process = c["analysis"]["process"]
            assert process["source_recording_in_model_input"] is False
            assert process["guide_sha256"] == guide["sha256"]
            assert process["generation_cost_usd"] == 0
            assert media.playback_start(media.read_audio(path)) < 480
        assert media.digest(studio.store.path(asset["original_path"])) == before


@pytest.mark.media
def test_ensemble_requires_checked_guide_and_rejects_tampering(studio, project, source_assets, local_runtime):
    asset = source_assets[0]
    request = Generate(stage="audio", asset_ids=[asset["id"]])
    with pytest.raises(ValueError, match="Check your melody"):
        studio.enqueue(project["id"], request, ensemble=True)
    guide = studio.prepare_melody(asset["id"])
    path = studio.store.path(guide["path"])
    path.write_bytes(path.read_bytes() + b"changed")
    with pytest.raises(ValueError, match="guide changed"):
        studio.enqueue(project["id"], request, ensemble=True)
    assert studio.detail(project["id"])["candidates"] == []
