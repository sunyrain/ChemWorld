from copy import deepcopy

import numpy as np
import pytest

from chemworld.eval.work_ii_public_endpoint_reference import (
    FAMILIES,
    clipped_normal_mean,
    endpoints,
    fit_public,
    public_contract,
)


def packet():
    contract = public_contract(299.1)
    queries = [
        {
            "query_id": str(i),
            "reference_partition_coefficient": d,
            "feature_values": {
                "mix_duration_s": 180 if i % 2 else 480,
                "stirring_speed_rpm": 450 if i % 2 else 950,
                "extractant_volume_L": 0.018,
                "aqueous_phase_volume_L": 0.012,
            },
        }
        for i, d in enumerate((1.3, 1.7, 2.2, 2.5, 2.9, 3.2, 4.0, 5.0))
    ]
    linear = endpoints(queries, contract, FAMILIES[0], [], noisy_mean=False)
    target = endpoints(queries, contract, FAMILIES[1], [1.63], noisy_mean=False)
    for i, q in enumerate(queries):
        q["reference_linear_observations"] = linear[q["query_id"]]
        q["target_observations"] = target[q["query_id"]]
        # Distinct paired noise, serialized as float32, must cancel without a private seed.
        for field in ("reference_linear_observations", "target_observations"):
            q[field]["product_in_organic"] = float(
                np.float32(q[field]["product_in_organic"] + 0.001 * (i - 4))
            )
    return {
        "complete_observation_contract": contract,
        "evidence": queries[:6],
        "scoring_action_queries": [
            {k: v for k, v in q.items() if "observations" not in k} for q in queries[6:]
        ],
    }


def test_public_fit_selects_family_without_target_or_held_out_labels():
    data = packet()
    before = deepcopy(data)
    fitted = fit_public(data)
    assert data == before
    assert fitted["selected_family"] == FAMILIES[1]
    power = next(row for row in fitted["families"] if row["family"] == FAMILIES[1])
    assert power["parameters"][0] == pytest.approx(1.63, abs=1e-5)
    assert fitted["organic_rmse_margin"] >= 1e-4
    assert len(power["predictions"]) == 2


def test_clipped_pair_is_failure_not_discarded():
    data = packet()
    data["evidence"][0]["target_observations"]["product_in_organic"] = 1.0
    with pytest.raises(ValueError, match="censored"):
        fit_public(data)


def test_noise_boundary_means_and_phase_removal():
    assert clipped_normal_mean(0, 0.01) == pytest.approx(0.01 / np.sqrt(2 * np.pi))
    assert clipped_normal_mean(1, 0.012) == pytest.approx(1 - 0.012 / np.sqrt(2 * np.pi))
    data = packet()
    values = endpoints(
        data["scoring_action_queries"],
        data["complete_observation_contract"],
        FAMILIES[0],
        [],
        noisy_mean=False,
    )
    for value in values.values():
        assert value["product_in_aqueous"] == 0
        assert value["phase_ratio"] == 1
        assert value["score"] == pytest.approx(0.85 * value["product_in_organic"] - 0.1)
