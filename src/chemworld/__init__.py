"""Public entrypoint for the ChemWorld physical-chemistry world environment."""

from chemworld.registration import ENV_ID, ENV_IDS, register_envs
from chemworld.validation import validate_action, validate_recipe
from chemworld.world.composition import (
    WORLD_COMPOSITION_SCHEMA_VERSION,
    CompiledWorldComposition,
    WorldCompatibilityReport,
    WorldCompositionDiagnostic,
    WorldCompositionError,
    WorldCompositionSpec,
    check_world_composition_compatibility,
    compile_world_composition,
)

__version__ = "0.2.0"
__all__ = [
    "ENV_ID",
    "ENV_IDS",
    "WORLD_COMPOSITION_SCHEMA_VERSION",
    "CompiledWorldComposition",
    "WorldCompatibilityReport",
    "WorldCompositionDiagnostic",
    "WorldCompositionError",
    "WorldCompositionSpec",
    "__version__",
    "check_world_composition_compatibility",
    "compile_world_composition",
    "register_envs",
    "validate_action",
    "validate_recipe",
]

register_envs()
