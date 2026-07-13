from __future__ import annotations

from chemworld.eval.classic_development import (
    build_development_cells,
    run_classic_development_audit,
)


def test_development_cells_use_only_public_ranges_and_paired_method_rng() -> None:
    cells = build_development_cells(
        tasks=("partition-discovery",),
        methods=("random", "lhs"),
        train_seeds=(10_000,),
        dev_seeds=(11_000,),
        complete_experiments=5,
    )
    assert len(cells) == 4
    for split, seed in (("train", 10_000), ("dev", 11_000)):
        paired = [cell for cell in cells if cell.split == split]
        assert {cell.world_seed for cell in paired} == {seed}
        assert len({cell.method_seed for cell in paired}) == 1
        assert all(cell.world_interventions for cell in paired)
        assert all(cell.world_interventions[0]["mode"] != "extrapolation" for cell in paired)
        assert all(len(cell.formal_protocol_sha256) == 64 for cell in paired)
        assert all(len(cell.method_artifact_sha256) == 64 for cell in paired)
        assert all(len(cell.source_commit) == 40 for cell in paired)


def test_development_audit_is_resumable_deterministic_and_never_formal_when_partial(
    tmp_path,
) -> None:
    kwargs = {
        "tasks": ("partition-discovery",),
        "methods": ("random", "structured_gp_ei"),
        "train_seeds": (10_000,),
        "dev_seeds": (11_000,),
        "complete_experiments": 5,
        "workers": 1,
        "cache_root": tmp_path / "cache",
        "report_path": tmp_path / "report.json",
    }
    first = run_classic_development_audit(**kwargs)
    second = run_classic_development_audit(**kwargs)
    assert first == second
    assert first["formal_classic_matrix_ready"] is False
    assert first["status"] == "development_diagnostic_only"
    assert first["bench_results_present"] is False
    assert first["reference_search_results_used"] is False
    assert first["acceptance"]["all_method_controls_pass"] is True
    assert first["method_summaries"]["structured_gp_ei"]["acquisition_effective"] is True
    assert first["method_summaries"]["random"]["deterministic_replay"] is True
