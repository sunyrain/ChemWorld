"""Opt-in P study presentation, scoped to one process; shared runtime files stay frozen."""

from __future__ import annotations

import copy
from contextlib import contextmanager

import chemworld.agent_interface as interface
import chemworld.envs.chemworld_env as env_module
from chemworld.runtime.phase_ledger_services import ChemWorldPhaseLedgerServices
from chemworld.runtime.species import MechanismSpeciesView

TASK = "reaction-to-purification"


def product_ids(view):
    """Resolve both explicit phase aliases of the same physical target product."""
    return tuple(
        sorted(
            set(view.target_species)
            | {
                species
                for species, aliases in view.mechanism.species_roles.items()
                if {"product_organic", "product_aqueous"}.intersection(aliases)
            }
        )
    )


class PSpeciesView(MechanismSpeciesView):
    @property
    def target_species(self):
        return product_ids(MechanismSpeciesView(self.mechanism))


def catalog():
    result = {
        "catalog_version": "p-anonymous-study-v1",
        "presentation": "anonymous_material_ids",
        "interpretation_policy": "Material indices are independent categories, "
        "not real identities.",
        "reagent": {
            "display_name": "Anonymous limiting reagent",
            "identity_kind": "mechanism_role",
        },
    }
    for key, role, prefix in (
        ("solvents", "solvent", "S"),
        ("extractants", "extractant", "X"),
        ("catalysts", "catalyst", "C"),
    ):
        result[key] = [
            {
                "index": i,
                "anonymous_material_id": f"{role}-{prefix}{i}",
                "display_name": f"{role}-{prefix}{i}",
                "identity_kind": "anonymous_benchmark_material",
            }
            for i in range(4)
        ]
    return result


@contextmanager
def presentation(dossier, goal, batches):
    """P-only public delivery and phase-complete target measurement; unchanged physics."""
    old_info = env_module.build_task_info
    old_profile = interface._task_prompt_profile
    old_labels = interface.material_choice_labels
    old_kernel = env_module.ChemWorldObservationKernel

    class PObservationKernel(old_kernel):
        @contextmanager
        def p_view(self, state):
            if state.metadata.get("full_process_task_id") != TASK:
                yield
                return
            view, phases = self.species_view, self.phase_ledgers
            self.species_view = PSpeciesView(self.compiled_mechanism)
            self.phase_ledgers = ChemWorldPhaseLedgerServices(self.species_view)
            try:
                yield
            finally:
                self.species_view, self.phase_ledgers = view, phases

        def _truth_values(self, state):
            with self.p_view(state):
                return super()._truth_values(state)

        def observe(self, state, action, rng):
            with self.p_view(state):
                return super().observe(state, action, rng)

    def info(env):
        result = old_info(env)
        if env.task_id == TASK:
            result.update(
                material_catalog=catalog(),
                material_information={"dossier": copy.deepcopy(dossier)},
                description=goal,
                task_goal=goal,
            )
            result["experiment_lifecycle"] = {
                **interface.experiment_lifecycle_contract(env.episode_mode),
                "planned_complete_experiments": batches,
                "explicit_terminate_required": True,
                "final_assay_required": True,
            }
        return result

    def profile(task_info, base):
        if task_info.get("task_id") != TASK:
            return old_profile(task_info, base)
        return {
            "task_goal": goal,
            "success_criteria": ["Maximize original-charge recovery at purity >=0.80."],
            "constraints": [
                f"Share resources across {batches} independent batches.",
                "Final assay closes a batch; continue until campaign_ended.",
            ],
            "measurement_policy": "Measurements use the declared selected material and "
            "consume sample. Recovery uses original reactant charge. Wash acts on organic.",
            "recommended_strategy": [],
            "failure_modes": ["budget exhausted", "quality failure"],
        }

    def labels(field, *, task_id=None):
        if task_id != TASK:
            return old_labels(field, task_id=task_id)
        key = {"solvent": "solvents", "extractant": "extractants", "catalyst": "catalysts"}.get(
            field
        )
        return {str(r["index"]): r["anonymous_material_id"] for r in catalog().get(key, [])}

    env_module.build_task_info = info
    interface._task_prompt_profile = profile
    interface.material_choice_labels = labels
    env_module.ChemWorldObservationKernel = PObservationKernel
    try:
        yield
    finally:
        env_module.build_task_info = old_info
        interface._task_prompt_profile = old_profile
        interface.material_choice_labels = old_labels
        env_module.ChemWorldObservationKernel = old_kernel
