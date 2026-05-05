from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="run the full pipeline.")
    parser.add_argument("--skip-download", action="store_true")
    parser.add_argument("--skip-apd", action="store_true")
    parser.add_argument("--skip-figures", action="store_true")
    return parser.parse_args()


def run_command(command: list[str]) -> None:
    subprocess.run(command, cwd=PROJECT_ROOT, check=True)


def latest_experiment_root() -> Path:
    experiments_dir = PROJECT_ROOT / "run" / "outputs" / "experiments" / "brpolicorpus_floor_yearly"
    runs = [path for path in experiments_dir.iterdir() if path.is_dir()]
    if not runs:
        raise FileNotFoundError(f"No experiment directories found under {experiments_dir}")
    return max(runs, key=lambda path: path.stat().st_mtime)


def main() -> None:
    args = parse_args()
    python = sys.executable
    if not args.skip_download:
        run_command([python, "run/pipeline/download_brpolicorpus.py", "--skip-existing"])
    run_command([python, "run/pipeline/main.py", "task=cross_method_agreement"])
    experiment_root = latest_experiment_root()
    if not args.skip_apd:
        run_command(
            [python, "run/pipeline/apd_reanalysis.py", "--experiment-root", str(experiment_root)]
        )
    if not args.skip_figures:
        run_command(
            [
                python,
                "run/pipeline/generate_paper_figures.py",
                "--experiment-root",
                str(experiment_root),
                "--output-dir",
                "run/outputs/figures",
            ]
        )
    print(f"Experiment root: {experiment_root}")


if __name__ == "__main__":
    main()
