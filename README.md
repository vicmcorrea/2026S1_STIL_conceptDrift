# stil submission setup

source code for the diachronic semantic change pipeline used on the brpolicorpus floor speeches.

## setup

```bash
uv sync
```

## download data

```bash
uv run python run/pipeline/download_brpolicorpus.py --skip-existing
```

this downloads brpolicorpus into `data/raw/`. the data files are not included in this repository.

## run pipeline

```bash
uv run python run/pipeline/run_pipeline.py --skip-download
```

outputs are written to `run/outputs/`.

## run stages manually

```bash
uv run python run/pipeline/main.py task=cross_method_agreement
```

## generate figures

```bash
uv run python run/pipeline/generate_paper_figures.py --experiment-root run/outputs/experiments/brpolicorpus_floor_yearly/<run_id> --output-dir run/outputs/figures
```
