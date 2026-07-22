from __future__ import annotations

import pandas as pd

from stil_semantic_change.reporting.paper_figures import (
    _rank_to_percentile,
    _rank_within_panel,
)


def test_global_ranks_are_normalized_within_fixed_panel() -> None:
    global_ranks = pd.Series([900, 3, 100], index=["low", "high", "middle"])

    panel_ranks = _rank_within_panel(global_ranks)
    percentiles = _rank_to_percentile(panel_ranks)

    assert panel_ranks.to_dict() == {"low": 3.0, "high": 1.0, "middle": 2.0}
    assert percentiles.to_dict() == {"low": 0.0, "high": 1.0, "middle": 0.5}
