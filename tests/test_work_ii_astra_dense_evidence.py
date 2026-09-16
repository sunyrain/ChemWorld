from copy import deepcopy

import pytest
from scripts import run_work_ii_astra_dense_evidence as dense


def source_rows():
    rows = []
    for w in dense.base.TRAIN:
        for i, p in enumerate(dense.screen.grid()):
            h = {"yield": i / 100, "conversion": i / 100, "selectivity": 0.9}
            terminal = {
                "crystal_yield": 0.2 if w.endswith("C1") else 0.8,
                "crystal_purity": 0.95,
                "utility_per_hour": 0.1,
            }
            resource = {
                "process_time_s": 2000,
                "cost_units": 0.2,
                "sample_consumed_L": 0.0007,
                "measurement_cost_units": 0.32,
            }
            public = {
                "world": w,
                "plan": p,
                "upstream_hplc": h,
                "terminal": terminal,
                "actual_quench_temperature_K": 300,
                "actual_cooling_temperature_K": 280,
            }
            rows.append(
                {
                    "world": w,
                    "name": f"grid/{w}/{i:02d}",
                    "plan": p,
                    "public": public,
                    "resources": resource,
                }
            )
    return rows


def test_fixed_queries_and_lossless_public_columns():
    assert len(dense.queries()) == 18
    source = source_rows()
    table = dense.compact_table(source)
    assert len(table["rows"]) == 144
    assert all(len(r) == len(table["columns"]) for r in table["rows"])
    row = dict(zip(table["columns"], table["rows"][5], strict=True))
    assert row["upstream_yield"] == source[5]["public"]["upstream_hplc"]["yield"]
    assert row["tR_s"] == source[5]["plan"]["reaction_duration_s"]
    bad = deepcopy(source)
    bad[0]["world"] = "R1C2"
    with pytest.raises(ValueError):
        dense.compact_table(bad)
    with pytest.raises(ValueError):
        dense.reference_predictions(bad)


def test_reference_composes_from_same_r_and_same_c_only():
    result = dense.reference_predictions(source_rows())["component_knn3"]
    assert len(result) == 18
    for key, prediction in result.items():
        assert prediction["reaction_yield"] == int(key[-2:]) / 100
        assert prediction["crystal_yield"] == pytest.approx(0.8 if key.startswith("R1") else 0.2)


def test_readout_rejects_partial_nan_boolean_and_out_of_domain():
    result = {
        "predictions": {q: dict.fromkeys(dense.base.METRICS, 0.5) for q in dense.queries()},
        "selections": dict.fromkeys(dense.base.WORLDS, 0),
    }
    assert dense.valid_readout(result)
    bad = deepcopy(result)
    bad["selections"]["R1C1"] = True
    assert not dense.valid_readout(bad)
    bad["selections"]["R1C1"] = 72
    assert not dense.valid_readout(bad)
    bad = deepcopy(result)
    bad["predictions"][next(iter(dense.queries()))]["reaction_yield"] = float("nan")
    assert not dense.valid_readout(bad)
    bad = deepcopy(result)
    bad["predictions"].pop(next(iter(dense.queries())))
    assert not dense.valid_readout(bad)
