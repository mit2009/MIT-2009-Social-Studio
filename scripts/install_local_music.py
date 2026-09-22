"""One-time, project-local install of pinned Stable Audio 3 Medium for Apple Silicon."""

import hashlib
import json
import os
import platform
import subprocess
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / "data/runtime/stable-audio-3"
COMMIT = "779434a908193105335fd8d833418603625b2859"
MODEL_REVISION = "da6edc54ddba10bfd79a077102ded687f80e882b"
WEIGHTS = {
    "dit_medium_f16.npz": (2907300946, "f9e5647ea3225818657d47d47ae4b34afa29c0568206ca89566c1a758944a38e"),
    "same_l_decoder_f32.npz": (
        1704311976,
        "84924be2122d3a20fce443f40b782d9cd88e8e73707476326003ac47659a2287",
    ),
    "same_l_encoder_f32.npz": (
        1704313504,
        "c5caafc6bd29fc3d4cb7a08b0d3725041fa2100711f86a4f05d2638c532871d2",
    ),
    "t5gemma_f16.npz": (567443068, "8deb20489f36d9aec539f26c9c67321f99bc5fe300d470435ed6e76be4f16bbd"),
}


def sha256(path):
    with path.open("rb") as source:
        return hashlib.file_digest(source, "sha256").hexdigest()


def download(name):
    size, checksum = WEIGHTS[name]
    target = RUNTIME / "optimized/mlx/models/mlx" / name
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.is_file() and target.stat().st_size == size and sha256(target) == checksum:
        print(f"Verified {name}", flush=True)
        return
    temporary = target.with_suffix(".download")
    offset = temporary.stat().st_size if temporary.exists() else 0
    if offset < size:
        url = (
            f"https://huggingface.co/stabilityai/stable-audio-3-optimized/resolve/{MODEL_REVISION}/MLX/{name}"
        )
        request = urllib.request.Request(url, headers={"Range": f"bytes={offset}-"} if offset else {})
        print(f"Downloading {name} ({size / 1e9:.2f} GB), resuming at {offset / 1e9:.2f} GB", flush=True)
        with urllib.request.urlopen(request, timeout=120) as response:
            if offset and response.status != 206:
                offset = 0
            last_report = offset
            with temporary.open("ab" if offset else "wb") as output:
                while chunk := response.read(1024 * 1024):
                    output.write(chunk)
                    offset += len(chunk)
                    if offset - last_report > 256 * 1024 * 1024:
                        print(f"  {name}: {offset / size:.0%}", flush=True)
                        last_report = offset
    if temporary.stat().st_size != size or sha256(temporary) != checksum:
        raise RuntimeError(f"Incomplete or invalid model file: {name}. No model was enabled.")
    temporary.replace(target)
    print(f"Verified {name}", flush=True)


def main():
    if platform.system() != "Darwin" or platform.machine() != "arm64":
        raise SystemExit("This local music runtime needs an Apple Silicon Mac.")
    if not RUNTIME.exists():
        subprocess.run(
            [
                "git",
                "clone",
                "--filter=blob:none",
                "--no-checkout",
                "https://github.com/Stability-AI/stable-audio-3.git",
                str(RUNTIME),
            ],
            check=True,
        )
        subprocess.run(["git", "-C", str(RUNTIME), "checkout", COMMIT], check=True)
    actual = subprocess.check_output(["git", "-C", str(RUNTIME), "rev-parse", "HEAD"], text=True).strip()
    if actual != COMMIT:
        raise SystemExit("The local runtime differs from the pinned revision; review it before installing.")
    with ThreadPoolExecutor(max_workers=4) as pool:
        list(pool.map(download, WEIGHTS))
    # Dependencies live in their own environment, never in the studio's server environment.
    python = ROOT / "data/runtime/audio-env/bin/python"
    if not python.is_file():
        subprocess.run([sys.executable, "-m", "venv", str(python.parents[1])], check=True)
    subprocess.run(
        [str(python), "-m", "pip", "install", "-r", str(ROOT / "requirements-audio.lock.txt")], check=True
    )
    environment = {**os.environ, "HF_HUB_OFFLINE": "1", "HF_HUB_DISABLE_TELEMETRY": "1"}
    subprocess.run(
        [str(python), "-c", "import mlx.core as mx; assert mx.metal.is_available(), 'Metal GPU is unavailable'; print('Local music ready')"],
        check=True,
        env=environment,
    )
    manifest = {
        "runtime_commit": COMMIT,
        "model_revision": MODEL_REVISION,
        "model": "Stable Audio 3 Medium",
        "weights": WEIGHTS,
        "generation_cost_usd": 0,
    }
    (ROOT / "data/runtime/local-music.json").write_text(json.dumps(manifest, indent=2))
    print("Local music is ready. Generation stays on this Mac and uses no API credits.")


if __name__ == "__main__":
    main()
