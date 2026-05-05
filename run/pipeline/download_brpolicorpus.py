from __future__ import annotations

import argparse
import json
import tarfile
import urllib.request
import zipfile
from pathlib import Path

ZENODO_RECORD_ID = "5040241"
EXPECTED_FLOOR_DIR = Path("exports/floor")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Download BrPoliCorpus from Zenodo.")
    parser.add_argument("--record-id", default=ZENODO_RECORD_ID)
    parser.add_argument("--output-dir", type=Path, default=Path("data/raw/BrPoliCorpus-Dataset"))
    parser.add_argument("--skip-existing", action="store_true")
    parser.add_argument("--no-extract", action="store_true")
    return parser.parse_args()


def read_json_url(url: str) -> dict:
    with urllib.request.urlopen(url) as response:
        return json.loads(response.read().decode("utf-8"))


def download_file(url: str, output_path: Path, skip_existing: bool) -> None:
    if skip_existing and output_path.exists():
        return
    output_path.parent.mkdir(parents=True, exist_ok=True)
    urllib.request.urlretrieve(url, output_path)


def extract_archive(path: Path, output_dir: Path) -> None:
    if path.suffix == ".zip":
        with zipfile.ZipFile(path) as archive:
            archive.extractall(output_dir)
        return
    if path.suffixes[-2:] in ([".tar", ".gz"], [".tar", ".bz2"], [".tar", ".xz"]):
        with tarfile.open(path) as archive:
            archive.extractall(output_dir)


def main() -> None:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    metadata = read_json_url(f"https://zenodo.org/api/records/{args.record_id}")
    downloads_dir = args.output_dir / "downloads"
    for file_info in metadata.get("files", []):
        file_name = file_info["key"]
        file_url = file_info["links"]["self"]
        output_path = downloads_dir / file_name
        download_file(file_url, output_path, args.skip_existing)
        if not args.no_extract:
            extract_archive(output_path, args.output_dir)
    expected_dir = args.output_dir / EXPECTED_FLOOR_DIR
    if expected_dir.exists():
        print(f"Ready: {expected_dir}")
    else:
        print(f"Downloaded files to {downloads_dir}")
        print(f"Expected CSV directory not found at {expected_dir}")
        print("Inspect the extracted folder and set dataset.raw_dir if the archive layout differs.")


if __name__ == "__main__":
    main()
