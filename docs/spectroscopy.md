# Virtual Spectroscopy

ChemWorld instruments generate plot-ready virtual signals in addition to scalar
processed estimates. These signals make the environment feel more like an
experiment workflow without claiming to predict real spectra for a real
molecule.

## Signal Types

- `hplc_chromatogram`: retention-time axis, normalized intensity trace,
  retention-factor metadata, plate-count peak widths, adjacent-peak resolution,
  and reactant/product/impurity peak annotations.
- `gc_chromatogram`: retention-time axis, normalized intensity trace,
  retention-factor metadata, plate-count peak widths, adjacent-peak resolution,
  and volatile byproduct/degradation/product peaks.
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
HPLC/GC species paths now have a reference-validated analytical slice:

```text
k' = (t_R - t_M) / t_M
t_R = t_M * (1 + k')
w_b = 4 * t_R / sqrt(N)
R_s = 2 * (t_R2 - t_R1) / (w_b1 + w_b2)
```

UV-vis species path also has one reference-validated analytical slice:

```text
Beer-Lambert: A = A_blank + epsilon * l * c_cuvette
c_cuvette = c_reactor / dilution_factor
```

UV-vis calibration runs fit `A = slope * c_reactor + intercept` and report
residual standard deviation, LOD, LOQ, and slope uncertainty. HPLC/GC
calibration runs report retention-factor and theoretical-plate estimates. IR
and NMR are still compact virtual instruments rather than empirical spectrum
predictors.

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
