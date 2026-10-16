"""Runtime limits for the authorized six-system matrix; no scientific changes."""

from __future__ import annotations

import json
import os
import sys
from functools import wraps

WORKER_ENV = {
    "OPENBLAS_NUM_THREADS": "1",
    "OMP_NUM_THREADS": "1",
    "MKL_NUM_THREADS": "1",
    "NUMEXPR_NUM_THREADS": "1",
    "TOKIO_WORKER_THREADS": "2",
    "RAYON_NUM_THREADS": "2",
}


def apply_environment():
    os.environ.update(WORKER_ENV)


def with_thread_limits(command):
    command = list(command)
    for server in ("chemworld_lab", "research_notebook", "public_numerics"):
        for key, value in WORKER_ENV.items():
            setting = f"mcp_servers.{server}.env.{key}={json.dumps(value)}"
            if setting not in command:
                command += ["-c", setting]
    return command


def bounded_builder(builder):
    if getattr(builder, "_unified_bounded", False):
        return builder

    @wraps(builder)
    def bounded(*args, **kwargs):
        command = with_thread_limits(builder(*args, **kwargs))
        # Followups use numerical tools only. Disabled entries still need transport
        # definitions when the CLI parses the merged MCP configuration.
        for server in ("chemworld_lab", "research_notebook"):
            command += ["-c", f"mcp_servers.{server}.enabled=false"]
            command += ["-c", f"mcp_servers.{server}.command={json.dumps(sys.executable)}"]
        return command

    bounded._unified_bounded = True
    return bounded


def bounded_notebook(base, *, final_recommendation_required=True):
    from chemworld.agents.campaign_notebook import with_notebook

    notebook_base = with_notebook(base)

    class BoundedNotebookAgent(notebook_base):
        def _command(self, *, instructions_path, schema_path):
            command = super()._command(instructions_path=instructions_path, schema_path=schema_path)
            if not final_recommendation_required:
                instructions = instructions_path.read_text(encoding="utf-8").replace(
                    "Finalize any source-stage notes before committing your final recommendation.",
                    "Finalize any source-stage notes before your final completion handoff.",
                )
                instructions_path.write_text(instructions, encoding="utf-8")
                (self.output / "source-instructions.txt").write_text(instructions, encoding="utf-8")
            return with_thread_limits(command)

    return BoundedNotebookAgent
