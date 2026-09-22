"""Download a pinned CC0 instrument subset; no accounts, plugins or model required."""

import hashlib
import json
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "mit2009_studio/instruments.json"
DESTINATION = ROOT / "data/instruments"


def valid(data, entry):
    header = f"blob {len(data)}\0".encode()
    return len(data) == entry["bytes"] and hashlib.sha1(header + data).hexdigest() == entry["git_blob"]


def install(entry):
    target = DESTINATION / entry["file"]
    if target.is_file() and valid(target.read_bytes(), entry):
        return
    url = (
        f"https://raw.githubusercontent.com/{entry['repository']}/{entry['revision']}/"
        + urllib.parse.quote(entry["source_path"])
    )
    with urllib.request.urlopen(url, timeout=120) as response:
        data = response.read()
    if not valid(data, entry):
        raise ValueError(f"Instrument download did not match its pinned hash: {entry['file']}")
    target.parent.mkdir(parents=True, exist_ok=True)
    partial = target.with_suffix(".download")
    partial.write_bytes(data)
    partial.replace(target)
    print(f"Ready: {target.name}", flush=True)


def main():
    catalog = json.loads(CATALOG.read_text())
    with ThreadPoolExecutor(max_workers=6) as pool:
        list(pool.map(install, catalog["samples"]))
    (DESTINATION / "ready.json").write_text(
        json.dumps(
            {
                "catalog_sha256": hashlib.sha256(CATALOG.read_bytes()).hexdigest(),
                "samples": len(catalog["samples"]),
                "license": "CC0-1.0",
            },
            indent=2,
        )
    )
    print("Recorded instruments are ready. All music rendering stays local and free.")


if __name__ == "__main__":
    main()
