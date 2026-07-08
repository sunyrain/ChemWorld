# Action And Recipe Schema

ChemWorld uses one operation language:

```json
{
  "operation": "add_solvent",
  "volume_L": 0.02,
  "solvent": 1
}
```

Higher-level recipes are compiled into operation sequences:

```json
{
  "steps": [
    {"operation": "add_solvent", "volume_L": 0.02, "solvent": 1},
    {"operation": "add_reagent", "amount_mol": 0.01}
  ]
}
```

Recipe steps may contain high-level process macros such as `wash`, `dry`, and
`concentrate`. The recipe compiler expands them into executable operation
sequences before validation or execution. For example, `wash` expands to
`add_extractant -> mix -> settle -> separate_phase`, and the compiled actions
carry `compiled_from_macro` metadata for auditability.

Validation has three layers:

- schema validation for JSON shape and scalar types;
- task policy for allowed operations and instruments;
- constitution preconditions for current-state physical validity.

`chemworld validate-recipe --task ...` checks the compiled steps, not only the
source recipe. A macro is valid only if the task allows every operation produced
by the expansion.

CLI:

```bash
chemworld validate-action --task reaction-to-purification --action action.json
chemworld validate-recipe --task reaction-to-purification --recipe recipe.json
```

Python:

```python
from chemworld.validation import validate_action, validate_recipe
```

Packaged JSON schema files live under `chemworld.schemas`. CI checks that these
files match the runtime Python schema constants, so the CLI, SDK, docs, and
student-facing validation contract do not drift apart.
