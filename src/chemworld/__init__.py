"""ChemWorld-Bench public package entrypoint."""

from chemworld.registration import ENV_ID, ENV_IDS, register_envs

__version__ = "0.1.0"
__all__ = ["ENV_ID", "ENV_IDS", "__version__", "register_envs"]

register_envs()
