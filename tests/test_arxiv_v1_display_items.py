from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "paper/figures/first-paper-world-instrument-v1" / "first-paper-figure-data-v1.json"
SCRIPT = ROOT / "scripts/render_arxiv_v1_display_items.py"


def test_display_items_are_regenerated_from_current_bound_figure_data(tmp_path: Path) -> None:
    output = tmp_path / "display-items.md"
    result = subprocess.run(
        [sys.executable, str(SCRIPT), str(DATA), "--output", str(output)],
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    data = json.loads(DATA.read_text(encoding="utf-8"))
    rendered = output.read_text(encoding="utf-8")
    assert data["figure_data_sha256"] not in rendered
    assert "SHA-256" not in rendered
    assert "release label" not in rendered
    assert "### Table 1" in rendered
    assert "### Table 5" in rendered
    titles = [
        "Figure 1 | Object hierarchy and public instrument contract.",
        "Figure 2 | Coverage-guided construction beyond the reference task identities.",
        "Figure 3 | Full-census qualification of the virtual instrument.",
        "Figure 4 | Deterministic cases exercise lifecycle and failure semantics.",
        "Figure 5 | Controlled forks change one private component under an invariant "
        "public contract.",
        "Figure 6 | Instrument records distinguish endpoint, process and execution status.",
    ]
    positions = [rendered.index(title) for title in titles]
    assert positions == sorted(positions)
    for required in (
        "1,786",
        "192",
        "89-action census",
        "24 provider-free traces",
        "493,092",
        "440,832",
        "52,260",
        "2,973",
        "near-zero raw terminal",
    ):
        assert required in rendered
    for excluded in (
        "DeepSeek-based",
        "Codex-based complete system",
        "120 closed lifecycles",
        "latent-terminal",
        "scalar intelligence score",
    ):
        assert excluded not in rendered


def test_tracked_display_items_match_a_fresh_render(tmp_path: Path) -> None:
    output = tmp_path / "display-items.md"
    subprocess.run(
        [sys.executable, str(SCRIPT), str(DATA), "--output", str(output)],
        check=True,
        capture_output=True,
        text=True,
    )
    tracked = ROOT / "paper/experimental_intelligence_v1_display_items.md"
    assert (
        hashlib.sha256(output.read_bytes()).digest()
        == hashlib.sha256(tracked.read_bytes()).digest()
    )
