"""Reaction-law module for ChemWorld.

The numerical ODE implementation is still provided by the validated
semi-mechanistic transition kernel. This module gives the reaction laws a
stable world-layer home so scenarios, docs, and validators do not treat the
reactor as a standalone game.
"""

from dataclasses import dataclass

from chemworld.core.batch_reactor import R_GAS, ChemWorldTransitionKernel, batch_reactor_reactions


@dataclass(frozen=True)
class ReactionModuleSpec:
    module_id: str = "reaction"
    version: str = "0.2"
    laws: tuple[str, ...] = (
        "arrhenius_kinetics",
        "catalyst_solvent_effects",
        "byproduct_formation",
        "product_degradation",
        "catalyst_deactivation",
    )

    def to_dict(self) -> dict[str, object]:
        return {
            "module_id": self.module_id,
            "version": self.version,
            "laws": list(self.laws),
            "gas_constant_J_per_mol_K": R_GAS,
            "reactions": [reaction.to_dict() for reaction in batch_reactor_reactions()],
        }


__all__ = ["ChemWorldTransitionKernel", "ReactionModuleSpec", "batch_reactor_reactions"]
