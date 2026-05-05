from __future__ import annotations

import pandas as pd


def make_slice_id(date: pd.Timestamp, freq: str) -> str:
    if freq == "yearly":
        return f"{date.year}"
    raise ValueError(f"Unsupported frequency: {freq}")


def slice_sort_key(slice_id: str) -> tuple[int, int]:
    return (int(slice_id), 0)
