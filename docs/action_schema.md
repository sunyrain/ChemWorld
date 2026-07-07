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

Validation has three layers:

- schema validation for JSON shape and scalar types;
- task policy for allowed operations and instruments;
- constitution preconditions for current-state physical validity.

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
