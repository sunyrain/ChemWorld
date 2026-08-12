from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

from chemworld.eval.provenance import canonical_json_sha256
from chemworld.eval.work_ii_ae_formal_cohort import (
    load_ae_formal_cohort,
    validate_ae_public_cells,
)
from chemworld.eval.work_ii_formal import FORMAL_ARMS, build_formal_preflight

ROOT = Path(__file__).resolve().parents[1]
DESIGN = ROOT / "configs/benchmark/work_ii_formal_design_v0.2.json"
ANALYSIS = ROOT / "configs/benchmark/work_ii_analysis_plan_v0.2.json"


def _load(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def _cells(public: dict[str, list[int]]) -> list[dict[str, object]]:
    return [
        {
            "c2_locus": "A_E",
            "task_id": task_id,
            "world_seed": seed,
            "world_split": "public_formal",
            "prior_arm": arm,
        }
        for task_id, seeds in public.items()
        for seed in seeds
        for arm in FORMAL_ARMS
    ]


def test_v02_design_and_analysis_bind_exact_qualification_cohort() -> None:
    design = _load(DESIGN)
    analysis = _load(ANALYSIS)
    public, construction, errors = load_ae_formal_cohort(ROOT, design)

    assert errors == []
    assert analysis["schema_version"] == "chemworld-work-ii-analysis-plan-0.3"
    assert analysis["analysis_plan_id"] == "work-ii-fixed-law-prior-analysis-v0.4"
    assert analysis["design_binding"] == {
        "path": "configs/benchmark/work_ii_formal_design_v0.2.json",
        "sha256": canonical_json_sha256(design),
    }
    assert len({seed for seeds in public.values() for seed in seeds}) == 25
    assert len({seed for seeds in construction.values() for seed in seeds}) == 25
    assert not (
        {seed for seeds in public.values() for seed in seeds}
        & {seed for seeds in construction.values() for seed in seeds}
    )
    assert validate_ae_public_cells(ROOT, design, _cells(public)) == []


def test_v02_cohort_validator_rejects_construction_or_rehashed_design_tampering() -> None:
    design = _load(DESIGN)
    public, construction, errors = load_ae_formal_cohort(ROOT, design)
    assert errors == []

    cells = _cells(public)
    cells[0]["world_seed"] = next(iter(construction.values()))[0]
    assert any(
        "participant cells" in error or "construction identity" in error
        for error in validate_ae_public_cells(ROOT, design, cells)
    )

    tampered = deepcopy(design)
    tampered["world_cohort"]["public_formal"]["task_world_seeds"][
        "electrochemical-conversion"
    ][0] += 1
    _, _, tamper_errors = load_ae_formal_cohort(ROOT, tampered)
    assert any("differ from A-E heldout" in error for error in tamper_errors)


def test_v02_formal_preflight_materializes_only_new_public_ae_cells() -> None:
    design = _load(DESIGN)
    _, construction, errors = load_ae_formal_cohort(ROOT, design)
    assert errors == []

    report = build_formal_preflight(ROOT, DESIGN, ANALYSIS)
    ae_cells = [cell for cell in report["cells"] if cell["c2_locus"] == "A_E"]
    construction_seeds = {
        seed for seeds in construction.values() for seed in seeds
    }

    assert len(ae_cells) == 75
    assert validate_ae_public_cells(ROOT, design, ae_cells) == []
    assert not {cell["world_seed"] for cell in ae_cells} & construction_seeds
    assert report["world_split_contract"]["construction_participant_cell_count"] == 0
