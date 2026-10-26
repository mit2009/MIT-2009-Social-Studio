"""Download pinned public MRT2 base assets; no authentication or audio upload."""

import hashlib
import json
import shutil
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "data/runtime/mrt2-assets"
REPO = "google/magenta-realtime-2"
REVISION = "010aa0dcb0dfd27b24f0ad07b4dad63e8f9521cc"
NEEDED = {
    "models/mrt2_base/mrt2_base.mlxfn",
    "models/mrt2_base/mrt2_base_state.safetensors",
    "resources/musiccoca/spm.model",
    "resources/musiccoca/text_encoder.tflite",
    "resources/musiccoca/mapper.tflite",
    "resources/musiccoca/pretrained_vector_quantizer.tflite",
}


def digest(path):
    with path.open("rb") as f:
        return hashlib.file_digest(f, "sha256").hexdigest()


def main():
    DEST.mkdir(parents=True, exist_ok=True)
    url = f"https://huggingface.co/api/models/{REPO}/revision/{REVISION}?blobs=true"
    with urllib.request.urlopen(url, timeout=30) as response:
        metadata = json.load(response)
    if metadata.get("gated"):
        raise RuntimeError("Public ungated download required; stop for review.")
    files = [f for f in metadata["siblings"] if f["rfilename"] in NEEDED]
    assert len(files) == len(NEEDED)
    (DEST / "upstream-metadata.json").write_text(json.dumps(metadata, indent=2))

    def download(entry):
        path = DEST / entry["rfilename"]
        path.parent.mkdir(parents=True, exist_ok=True)
        expected = entry["lfs"]["sha256"]
        if path.is_file() and path.stat().st_size == entry["size"] and digest(path) == expected:
            return
        partial = path.with_suffix(path.suffix + ".partial")
        url = f"https://huggingface.co/{REPO}/resolve/{REVISION}/{entry['rfilename']}"
        print(f"Downloading {path.name}: {entry['size'] / 1e6:.1f} MB", flush=True)
        with urllib.request.urlopen(url, timeout=60) as response, partial.open("wb") as output:
            shutil.copyfileobj(response, output, 1024 * 1024)
        assert partial.stat().st_size == entry["size"] and digest(partial) == expected
        partial.replace(path)
        print(f"Verified {path.name}", flush=True)

    with ThreadPoolExecutor(max_workers=3) as pool:
        list(pool.map(download, files))
    shutil.copyfile(ROOT / "data/runtime/magenta-realtime/MODEL.md", DEST / "MODEL.md")
    shutil.copyfile(ROOT / "data/runtime/magenta-realtime/LICENSE", DEST / "CODE-LICENSE")
    (DEST / "assets.json").write_text(
        json.dumps(
            {
                "repo": REPO,
                "revision": REVISION,
                "code_commit": "694a545e4ba0b88bf1150137b129582166d3e07f",
                "code_license": "Apache-2.0",
                "weights_license": "CC-BY-4.0 plus usage terms in MODEL.md",
                "attribution": "Magenta RealTime 2, Google DeepMind / Google LLC, 2026",
                "files": files,
                "source_audio_uploaded": False,
            },
            indent=2,
        )
    )
    print("Pinned model assets verified.", flush=True)


if __name__ == "__main__":
    main()
