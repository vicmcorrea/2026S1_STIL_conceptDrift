# stil submission setup

source code for the diachronic semantic change pipeline used on the brpolicorpus floor speeches.

## setup

install `uv` if needed:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

then install the project environment:

```bash
uv sync
```

the workflow uses a hydra pipeline. configs live under `run/conf/`, and the main entrypoint is `run/pipeline/main.py`.

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

you can override hydra config values from the command line, for example:

```bash
uv run python run/pipeline/main.py task=prepare_corpus preprocess.n_process=4
```

## generate figures

```bash
uv run python run/pipeline/generate_paper_figures.py --experiment-root run/outputs/experiments/brpolicorpus_floor_yearly/<run_id> --output-dir run/outputs/figures
```
