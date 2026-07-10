from __future__ import annotations

from chemworld.eval.seed_suite import (
    PRIVATE_EVAL_SALT_ENV,
    SEED_SUITE_SCHEMA_VERSION,
    official_seed_suite,
    official_seeds_for_task,
    private_eval_salt_policy,
    task_seed_plan,
)
from chemworld.tasks import CORE_TASK_IDS, get_task


def test_core_seed_suite_matches_task_registry() -> None:
    suite = official_seed_suite()

    assert suite["schema_version"] == SEED_SUITE_SCHEMA_VERSION
    assert tuple(suite["task_ids"]) == CORE_TASK_IDS
    for task_id in CORE_TASK_IDS:
        assert suite["task_seed_plan"][task_id] == list(get_task(task_id).seeds)
        assert official_seeds_for_task(task_id) == list(get_task(task_id).seeds)


def test_private_eval_seed_suite_exposes_policy_without_publishing_hidden_seeds() -> None:
    suite = official_seed_suite(["public-private-generalization"])
    entry = suite["entries"][0]

    assert entry["world_split"] == "private-eval"
    assert entry["published_seeds"] == "maintainer-controlled"
    assert entry["runnable_seeds"] == list(get_task("public-private-generalization").seeds)
    assert entry["hidden_eval_policy"]["salt_environment_variable"] == PRIVATE_EVAL_SALT_ENV
    assert "public_placeholder_seeds" in entry["hidden_eval_policy"]
    assert suite["private_eval_salt_policy"] == private_eval_salt_policy()


def test_task_seed_plan_allows_explicit_smoke_override() -> None:
    plan = task_seed_plan(["reaction-to-assay", "partition-discovery"], override_seeds=[7])

    assert plan == {"reaction-to-assay": [7], "partition-discovery": [7]}
