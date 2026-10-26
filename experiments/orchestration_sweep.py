"""Render a bounded, reproducible orchestration sweep using the existing local trial."""

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np
import soundfile as sf

from mit2009_studio import media

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--reference", type=Path, required=True)
    args = parser.parse_args()
    source = args.source.resolve()
    reference = args.reference.resolve()
    folder = args.output.resolve()
    config = json.loads((ROOT / "docs/house-band/orchestration-sweep.json").read_text())
    assert config["project_duration_seconds"] == 15.0
    source_hash = media.digest(source)
    original_controls = np.load(reference / "note-control.npy")
    original_mapping = json.loads((reference / "source-map.json").read_text())
    folder.mkdir(parents=True, exist_ok=False)
    (folder / "manifest.json").write_text(json.dumps(config, indent=2) + "\n")
    reproduction = folder / "reproduction"
    reproduction.mkdir()
    for name in ("orchestration_sweep.py", "mrt2_trial.py", "mrt2_worker.py", "audio_only.py"):
        shutil.copy2(ROOT / "experiments" / name, reproduction / name)
    records = []
    for variant in config["variants"]:
        target = folder / variant["id"]
        print(f"Rendering {variant['label']}: {variant['name']}", flush=True)
        command = [
            sys.executable,
            "-m",
            "experiments.mrt2_trial",
            str(source),
            str(target),
            "--seed",
            str(config["seed"]),
            "--profile",
            config["profile"],
            "--style",
            variant["style"],
        ]
        with (folder / f"{variant['id']}-run.log").open("w") as log:
            result = subprocess.run(command, cwd=ROOT, stdout=log, stderr=subprocess.STDOUT, timeout=300)
        if result.returncode:
            raise RuntimeError(f"Render failed; inspect {variant['id']}-run.log")
        checks = json.loads((target / "checks.json").read_text())
        assert media.digest(source) == source_hash == checks["source_sha256"]
        assert np.array_equal(np.load(target / "note-control.npy"), original_controls)
        assert json.loads((target / "source-map.json").read_text()) == original_mapping
        assert checks["duration"] == 15.0 and checks["paid_api_calls"] == 0
        raw, rate = sf.read(target / "model-raw.wav", always_2d=True)
        assert np.isfinite(raw).all() and rate == 48000
        records.append(
            {
                **variant,
                "output_sha256": checks["output_sha256"],
                "controls_and_mapping_match_reference": True,
                "elapsed_seconds": checks["elapsed_seconds"],
                "lufs": checks["measured_lufs"],
                "true_peak_dbtp": checks["true_peak_dbfs"],
                "first_audible_seconds": checks["first_audible_seconds"],
                "raw_peak": float(np.max(np.abs(raw))),
                "raw_full_scale_channel_samples": int(np.count_nonzero(np.abs(raw) >= 1)),
                "raw_channel_samples": raw.size,
                "listening_status": "pending",
            }
        )
        (folder / "verification.json").write_text(
            json.dumps(
                {
                    "source_sha256": source_hash,
                    "reference": str(reference),
                    "runs": records,
                    "complete": len(records) == len(config["variants"]),
                    "limitation": "Technical checks and unchanged controls do not prove musical quality or fidelity.",
                },
                indent=2,
            )
            + "\n"
        )
        print(f"Ready {variant['label']}: {checks['elapsed_seconds']:.1f}s render, checks passed", flush=True)


if __name__ == "__main__":
    main()
