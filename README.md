# Diachronic semantic change in Brazilian political discourse

Code and frozen result summaries for the STIL 2026 paper *A Comparative
Framework for Diachronic Lexical Semantic Change in Brazilian Portuguese
Political Discourse*.

The pipeline compares a TF–IDF lexical-salience baseline, aligned Word2Vec
embeddings, and contextual BERT representations on yearly BrPoliCorpus floor
speeches from 2000 through 2023.

## Setup

Python 3.12 and [uv](https://docs.astral.sh/uv/) are required.

```bash
uv sync --group dev
uv run python -m spacy download pt_core_news_sm
```

## Quick validation

The tests use a small bundled fixture and do not require the full corpus.

```bash
uv run pytest
uv run ruff check .
```

## Data

The raw corpus is not redistributed here. The download helper reads the
official BrPoliCorpus v1.1.0 file manifest and stores the Parliamentary Floor
CSVs under `data/raw/BrPoliCorpus-Dataset/exports/floor/`.

```bash
uv run python run/pipeline/download_brpolicorpus.py --skip-existing
```

BrPoliCorpus is maintained at
[rll307/BrPoliCorpus](https://github.com/rll307/BrPoliCorpus) and archived under
[doi:10.25824/redu/YCFPIV](https://doi.org/10.25824/redu/YCFPIV).

## Run the analysis

The complete workflow is config driven through Hydra.

```bash
uv run python run/pipeline/run_pipeline.py --skip-download
```

Individual stages can also be run directly.

```bash
uv run python run/pipeline/main.py task=prepare_corpus preprocess.n_process=4
uv run python run/pipeline/main.py task=cross_method_agreement
```

Generated artifacts are written to `run/outputs/`, which is excluded from git.

## Reproduce the paper figures

`results/frozen_run/` contains only the compact derived tables needed by the
figure generator. It contains no speech text or contextual occurrence samples.

```bash
uv run python run/pipeline/generate_paper_figures.py \
  --experiment-root results/frozen_run \
  --output-dir run/outputs/paper_figures
```

## Layout

```text
src/stil_semantic_change/  analysis package
run/conf/                  Hydra configuration
run/pipeline/              command-line entrypoints
tests/                     unit tests and toy corpus
results/frozen_run/        compact paper-figure inputs
```

## License and citation

The code and configuration are released under the MIT License. BrPoliCorpus
remains subject to its CC BY-NC 4.0 source license. Citation metadata is
provided in `CITATION.cff`.
