# Virtual Spectroscopy

ChemWorld instruments generate plot-ready virtual signals in addition to scalar
processed estimates. These signals make the environment feel more like an
experiment workflow without claiming to predict real spectra for a real
molecule.

## Signal Types

- `hplc_chromatogram`: retention-time axis, normalized intensity trace, and
  reactant/product/impurity peak annotations.
- `gc_chromatogram`: retention-time axis, normalized intensity trace, and
  volatile byproduct, degradation, solvent-loss, and distillate peaks.
- `uvvis_spectrum`: wavelength axis and absorbance trace. When species amounts
  are available, UV-vis bands use the Beer-Lambert relation with explicit path
  length, sample dilution, blank absorbance, and calibration uncertainty;
  aggregate-score fallback bands remain labeled as proxies.
- `ir_spectrum`: wavenumber axis and low-resolution transmittance trace for
  product, impurity, degradation, and residual-solvent proxies.
- `nmr_1h_spectrum`: chemical-shift axis and normalized intensity trace for
  product and impurity proxies.

## Where Signals Live

Gym observations stay scalar so RL agents can use a stable observation space.
Virtual spectra are stored in:

- `info["raw_signal"]` during `env.step`;
- trajectory JSONL `raw_signal`;
- instrument contract `raw_signal_schema`.

Processed estimates such as `yield`, `conversion`, `purity`, and `recovery` are
stored separately in `processed_estimate`. Measurement uncertainty is stored in
`uncertainty`.

## Design Boundary

These signals are synthetic, semi-mechanistic teaching and benchmark signals.
The UV-vis species path now has one reference-validated analytical slice:

```text
Beer-Lambert: A = A_blank + epsilon * l * c_cuvette
c_cuvette = c_reactor / dilution_factor
```

Calibration runs fit `A = slope * c_reactor + intercept` and report residual
standard deviation, LOD, LOQ, and slope uncertainty. HPLC, GC, IR, and NMR are
still compact virtual instruments rather than empirical spectrum predictors.

They are designed to support:
They are designed to support:

- instrument-selection strategies;
- partial-observation reasoning;
- LLM/tool-agent parsing;
- plotting in tutorials and reports;
- replayable benchmark logs.

They are not intended to replace RDKit, quantum chemistry, or experimental
spectral prediction.

For plotting in notebooks, install the notebook extra:

```bash
python -m pip install -e ".[notebooks]"
```
