from __future__ import annotations

import argparse
import logging
from pathlib import Path

from stil_semantic_change.contextual.apd_reanalysis import run_apd_reanalysis

PROJECT_ROOT = Path(__file__).resolve().parents[2]
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(name)s %(levelname)s %(message)s",
)
logger = logging.getLogger(__name__)


def main() -> None:
    parser = argparse.ArgumentParser(description="run apd reanalysis.")
    parser.add_argument(
        "--experiment-root",
        type=Path,
        required=True,
        help="Completed experiment root under run/outputs/experiments",
    )
    args = parser.parse_args()
    artifacts_root = PROJECT_ROOT / "run" / "outputs"
    bert_root = args.experiment_root.resolve() / "scores" / "bert_confirmatory"
    output_root = artifacts_root / "apd_reanalysis"
    if not bert_root.exists():
        logger.error("bert output not found: %s", bert_root)
        raise SystemExit(1)
    result = run_apd_reanalysis(bert_root, output_root)
    print("\n" + "=" * 70)
    print("apd reanalysis complete")
    print("=" * 70)
    print(f"lemmas scored: {result['n_lemmas']}")
    print(f"score rows: {result['n_score_rows']}")
    print(f"trajectory rows: {result['n_trajectory_rows']}")
    print()
    print("apd vs prt agreement:")
    for row in result["agreement"]:
        layer = row["layer"]
        metric = row["metric"]
        value = row["value"]
        if metric == "spearman_rho":
            print(f"  layer {layer}: spearman rho = {value:.4f}")
        elif metric == "spearman_pvalue":
            print(f"  layer {layer}: p-value = {value:.2e}")
        elif metric.startswith("top_"):
            k = metric.split("_")[1]
            print(f"  layer {layer}: top-{k} overlap = {int(value)}/{row['max_possible']}")
    print(f"\noutputs written to: {output_root}")


if __name__ == "__main__":
    main()
