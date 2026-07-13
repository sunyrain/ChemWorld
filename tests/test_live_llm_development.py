from __future__ import annotations

import json

import pytest

from chemworld.eval.formal_matrix import build_formal_matrix_plan
from chemworld.eval.live_llm_development import (
    build_live_llm_development_bundle,
    prepare_live_llm_development,
)


def test_live_pilot_is_exact_paired_core_matrix_without_seed_disclosure() -> None:
    bundle = build_live_llm_development_bundle(stage="live_pilot")
    plan = build_formal_matrix_plan(bundle.manifest)
    serialized = json.dumps(bundle.manifest, sort_keys=True)

    assert bundle.pair_count == 1
    assert bundle.cell_count == 4 * 2 * 3
    assert bundle.maximum_provider_call_count == 480
    assert len(plan.cells) == bundle.cell_count
    assert set(plan.spectrum_conditions_by_method["live_llm_a"]) == {
        "assigned",
        "unassigned",
        "masked",
    }
    assert bundle.manifest["metadata"]["development_contract"]["bench_accessed"] is False
    assert "10000" not in serialized
    assert all("world_seed" not in cell for cell in bundle.manifest["cells"])


def test_development_matrix_uses_only_four_public_dev_pairs() -> None:
    bundle = build_live_llm_development_bundle(stage="development_matrix")
    plan = build_formal_matrix_plan(bundle.manifest)

    assert bundle.pair_count == 4
    assert bundle.cell_count == 4 * 2 * 3 * 4
    assert bundle.maximum_provider_call_count == 3840
    assert plan.checkpoints == (1, 2, 4)
    assert plan.limits.api_max_concurrency == 4
    assert plan.limits.matrix_monetary_cost_usd_limit == bundle.cell_count * 2.0


def test_live_development_rejects_bench_reference_or_partial_spectrum_design() -> None:
    with pytest.raises(ValueError, match="stage must"):
        build_live_llm_development_bundle(stage="bench")
    with pytest.raises(ValueError, match="three spectrum"):
        build_live_llm_development_bundle(
            stage="live_pilot", spectrum_conditions=("assigned", "masked")
        )
    with pytest.raises(ValueError, match="outside the public formal range"):
        build_live_llm_development_bundle(stage="development_matrix", seeds=(12_000,))


def test_prepare_writes_private_runtimes_outside_public_report_tree(tmp_path) -> None:
    bundle, manifest_path, runtime_root, output_root = prepare_live_llm_development(
        stage="live_pilot",
        cache_root=tmp_path,
    )

    assert manifest_path.is_file()
    assert runtime_root.is_dir()
    assert len(list(runtime_root.glob("*.json"))) == bundle.cell_count
    assert not output_root.exists()
    runtime = json.loads(next(runtime_root.glob("*.json")).read_text(encoding="utf-8"))
    assert runtime["world_seed"] == 10_000
    assert "world_seed" not in json.loads(manifest_path.read_text(encoding="utf-8"))["cells"][0]
