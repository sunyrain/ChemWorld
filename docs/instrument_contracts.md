# Instrument Contracts

Instrument observations are partial, noisy, and costly. Every instrument exposes
a formal contract:

- `instrument_id`
- observable keys
- raw signal schema
- processed estimate schema
- uncertainty model
- noise model
- cost
- latency
- sample consumption
- destructive flag
- termination requirement
- calibration profile

Current instruments:

- `uvvis`: low-cost proxy for yield, conversion, and phase ratio.
- `gc`: volatile/byproduct and degradation signal.
- `hplc`: chromatography-style yield, selectivity, byproduct, and purity signal.
- `final_assay`: leaderboard-grade terminal measurement.

Raw signals are plot-ready JSON packets:

- HPLC and GC expose `time_min`, `intensity`, `peaks`, baseline, and
  normalization metadata.
- UV-vis exposes `wavelength_nm`, `absorbance`, Beer-Lambert species-band
  metadata when species amounts are available, and labeled fallback proxy bands
  when only aggregate task fields are available.
- Final assay exposes a multi-instrument packet with HPLC, GC, UV-vis, IR, NMR,
  and calibrated mass-balance summaries.

The raw signal is for analysis, teaching, and agent tool use. Gym observations
remain scalar and stable; richer spectra live in trajectory `raw_signal` and
`info["raw_signal"]`.

Final assay is the official source for `leaderboard_score`.
