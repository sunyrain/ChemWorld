# Local Reference Repositories

These repositories are shallow-cloned into `reference_repos/` for local reading
and feature mapping. The directory is ignored by Git and must not be committed
to ChemWorld.

The repositories are reference material only. ChemWorld implements its own
physical-chemistry core and does not copy source code from these projects.

## Local Snapshot

| Name | Local Path | Branch | Commit | Size | Remote |
| --- | --- | --- | --- | ---: | --- |
| Cantera | `reference_repos/cantera` | `main` | `67b9f12` | 15.8 MB | <https://github.com/Cantera/cantera.git> |
| CoolProp | `reference_repos/coolprop` | `master` | `0e67fe7` | 54.3 MB | <https://github.com/CoolProp/CoolProp.git> |
| thermo | `reference_repos/thermo` | `master` | `3c2fa0c` | 59.3 MB | <https://github.com/CalebBell/thermo.git> |
| chemicals | `reference_repos/chemicals` | `master` | `82faef9` | 98.3 MB | <https://github.com/CalebBell/chemicals.git> |
| fluids | `reference_repos/fluids` | `master` | `091070e` | 15.3 MB | <https://github.com/CalebBell/fluids.git> |
| phasepy | `reference_repos/phasepy` | `master` | `9376df1` | 4.8 MB | <https://github.com/gustavochm/phasepy.git> |
| IDAES | `reference_repos/idaes-pse` | `main` | `4275c45` | 71.3 MB | <https://github.com/IDAES/idaes-pse.git> |
| Reaktoro | `reference_repos/reaktoro` | `main` | `f587235` | 81.2 MB | <https://github.com/reaktoro/reaktoro.git> |
| pycalphad | `reference_repos/pycalphad` | `develop` | `144d83d` | 12.2 MB | <https://github.com/pycalphad/pycalphad.git> |
| teqp | `reference_repos/teqp` | `main` | `58a24fd` | 26.9 MB | <https://github.com/usnistgov/teqp.git> |
| thermopack | `reference_repos/thermopack` | `main` | `d68c794` | 192.6 MB | <https://github.com/thermotools/thermopack.git> |
| RMG-Py | `reference_repos/rmg-py` | `main` | `f3dc397` | 222.2 MB | <https://github.com/ReactionMechanismGenerator/RMG-Py.git> |

## Recreate The Snapshot

```powershell
$repos = @(
  @{name='cantera'; url='https://github.com/Cantera/cantera.git'},
  @{name='coolprop'; url='https://github.com/CoolProp/CoolProp.git'},
  @{name='thermo'; url='https://github.com/CalebBell/thermo.git'},
  @{name='chemicals'; url='https://github.com/CalebBell/chemicals.git'},
  @{name='fluids'; url='https://github.com/CalebBell/fluids.git'},
  @{name='phasepy'; url='https://github.com/gustavochm/phasepy.git'},
  @{name='idaes-pse'; url='https://github.com/IDAES/idaes-pse.git'},
  @{name='reaktoro'; url='https://github.com/reaktoro/reaktoro.git'},
  @{name='pycalphad'; url='https://github.com/pycalphad/pycalphad.git'},
  @{name='teqp'; url='https://github.com/usnistgov/teqp.git'},
  @{name='thermopack'; url='https://github.com/thermotools/thermopack.git'},
  @{name='rmg-py'; url='https://github.com/ReactionMechanismGenerator/RMG-Py.git'}
)
New-Item -ItemType Directory -Force -Path reference_repos | Out-Null
foreach ($repo in $repos) {
  git clone --depth 1 --single-branch $repo.url "reference_repos/$($repo.name)"
}
```

## Reading Map

Use this map to guide independent ChemWorld implementation work:

- Cantera: reaction mechanisms, rate-law taxonomy, reactor network concepts.
- CoolProp: property API design, high-accuracy thermophysical property scope.
- thermo / chemicals: compact chemical-engineering property correlations.
- fluids: dimensionless numbers, pressure drop, mixing, equipment utilities.
- phasepy: LLE/VLE workflows and activity-model organization.
- IDAES: process unit contracts, flowsheet organization, initialization ideas.
- Reaktoro: equilibrium problem statements, constraints, and reactive transport.
- pycalphad: Gibbs-energy models and phase-equilibrium data structures.
- teqp / thermopack: EOS architecture and phase-envelope workflows.
- RMG-Py: mechanism specification and reaction-family concepts.

## Rules For Contributors

- Do not copy source code from `reference_repos/`.
- If a formula is implemented, cite an original public source or textbook in
  ChemWorld docs/tests.
- If behavior is compared to a reference repo, write it as an optional reference
  test that skips when the package is absent.
- Keep reference repos out of commits, releases, wheels, and paper artifacts.

## Optional Validation Layer

ChemWorld's reference comparison utilities live in
`chemworld.physchem.reference_validation`. They are intentionally small:

- discover tracked reference backends and local source trees;
- temporarily add local reference repositories to `sys.path`;
- import optional packages only inside explicit validation calls;
- record scalar comparisons as JSON-friendly reports with `rtol`, `atol`,
  absolute error, relative error, and model-limit notes.

Default CI does not import external backends. The optional reference tests under
`tests/reference/` skip unless explicitly enabled:

```powershell
$env:CHEMWORLD_RUN_REFERENCE_TESTS = "1"
python -m pytest tests/reference
```

Current executable comparisons use `chemicals`, `fluids`, and a controlled
`thermo.property_package.Ideal` VLE case because those paths can run from the
local source snapshots in the development environment. The `thermo` comparison
checks ideal Raoult-law bubble/dew pressure and a two-phase TP flash against
ChemWorld's local phase-equilibrium kernel. Heavy or compiled backends such as
CoolProp, Cantera, phasepy, Reaktoro, pycalphad, thermopack, and teqp remain
tracked as validation targets, but are not considered complete until their
runtime dependencies are available and their comparisons run successfully.
