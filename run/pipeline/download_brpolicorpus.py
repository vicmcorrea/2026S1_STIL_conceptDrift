from __future__ import annotations

import argparse
import re
import shutil
import urllib.request
from dataclasses import dataclass
from pathlib import Path

FLOOR_SOURCE_URL = "https://raw.githubusercontent.com/rll307/BrPoliCorpus/v1.1.0/R/Floor.R"
DEFAULT_OUTPUT_DIR = Path("data/raw/BrPoliCorpus-Dataset/exports/floor")
FUNCTION_RE = re.compile(
    r"download_(?P<name>Floor_\d+_data)\s*<-\s*function\(\)\s*\{"
    r".*?file_id\s*<-\s*['\"](?P<url>https://drive\.google\.com/[^'\"]+)['\"]",
    flags=re.DOTALL,
)


@dataclass(frozen=True)
class FloorFile:
    name: str
    url: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Download the official BrPoliCorpus Parliamentary Floor CSV files."
    )
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--skip-existing", action="store_true")
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Download only the first N files, mainly for checking the setup.",
    )
    return parser.parse_args()


def read_text_url(url: str) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": "stil-reproducibility/1.0"})
    with urllib.request.urlopen(request) as response:
        return response.read().decode("utf-8")


def discover_floor_files(source: str) -> list[FloorFile]:
    files = [
        FloorFile(name=f"{match.group('name')}.csv", url=match.group("url"))
        for match in FUNCTION_RE.finditer(source)
    ]
    if not files:
        raise ValueError("No Parliamentary Floor download entries were found upstream")
    return sorted(files, key=lambda item: int(re.search(r"\d+", item.name).group()))


def download_file(file: FloorFile, output_dir: Path, skip_existing: bool) -> Path:
    output_path = output_dir / file.name
    if skip_existing and output_path.exists() and output_path.stat().st_size > 0:
        return output_path

    output_path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = output_path.with_suffix(".csv.part")
    request = urllib.request.Request(
        file.url,
        headers={"User-Agent": "stil-reproducibility/1.0"},
    )
    try:
        with urllib.request.urlopen(request) as response, temporary_path.open("wb") as handle:
            shutil.copyfileobj(response, handle)
        if temporary_path.stat().st_size == 0:
            raise ValueError(f"Downloaded an empty file for {file.name}")
        temporary_path.replace(output_path)
    finally:
        temporary_path.unlink(missing_ok=True)
    return output_path


def main() -> None:
    args = parse_args()
    files = discover_floor_files(read_text_url(FLOOR_SOURCE_URL))
    if args.limit is not None:
        if args.limit < 1:
            raise ValueError("--limit must be greater than zero")
        files = files[: args.limit]

    for index, file in enumerate(files, start=1):
        output_path = download_file(file, args.output_dir, args.skip_existing)
        print(f"[{index}/{len(files)}] {output_path}")


if __name__ == "__main__":
    main()
