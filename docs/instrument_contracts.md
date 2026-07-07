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

Final assay is the official source for `leaderboard_score`.
