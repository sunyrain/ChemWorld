from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "benchmark" / "releases" / "chemworld-serious-v1" / "arxiv-v1-derived-data.json"
SCRIPT = ROOT / "scripts" / "render_arxiv_v1_display_items.py"


def test_display_items_are_regenerated_from_the_bound_data(tmp_path: Path) -> None:
    output = tmp_path / "display-items.md"
    result = subprocess.run(
        [sys.executable, str(SCRIPT), str(DERIVED), "--output", str(output)],
        check=False,
        capture_output=True,
        text=True,
    )
    data = json.loads(DERIVED.read_text(encoding="utf-8"))
    assert result.returncode == (0 if data["g2_v0_5"] is not None else 2)
    rendered = output.read_text(encoding="utf-8")
    assert data["derived_data_sha256"] in rendered
    assert "### Table 1" in rendered
    assert "### Table 4" in rendered
    assert "**Figure 1" in rendered
    assert "**Figure 6" in rendered
    if data["g2_v0_5"] is None:
        assert "no interim replication values are rendered" in rendered
    else:
        replication = data["g2_v0_5"]
        branch = replication["interpretation"]["selected_branch"]
        policy = replication["interpretation"]["mapping_policy"]
        matrix = replication["matrix"]
        assert branch["branch_id"] in rendered
        assert "contrasts frequently changed direction" in rendered
        assert "does not identify a causal provider effect" in rendered
        assert "variance-dominance relation" in rendered
        assert "provider-trajectory variability dominated" not in rendered
        assert policy["sha256"] in rendered
        assert f"{matrix['completed_cell_count']} completed cells" in rendered
        assert f"{matrix['right_censored_cell_count']} right-censored cells" in rendered
        assert f"{matrix['completed_pair_count']} complete pairs" in rendered
        assert "pre-specified trajectory pairs" in rendered
        assert "Δ mean score" in rendered
        assert "Δ discovery" in rendered
        assert "does not identify a causal provider effect" in rendered


def test_tracked_display_items_match_a_fresh_render(tmp_path: Path) -> None:
    output = tmp_path / "display-items.md"
    subprocess.run(
        [sys.executable, str(SCRIPT), str(DERIVED), "--output", str(output)],
        check=False,
        capture_output=True,
        text=True,
    )
    tracked = ROOT / "paper" / "experimental_intelligence_v1_display_items.md"
    rendered_hash = hashlib.sha256(output.read_bytes()).digest()
    tracked_hash = hashlib.sha256(tracked.read_bytes()).digest()
    assert rendered_hash == tracked_hash
