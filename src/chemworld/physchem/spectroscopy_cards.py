"""Spectroscopy model cards for ChemWorld."""

from __future__ import annotations

from chemworld.physchem.maturity import MaturityLevel, ModelCard, ValidationEvidence


def spectroscopy_model_cards() -> tuple[ModelCard, ...]:
    return (
        ModelCard(
            model_id="beer_lambert_uvvis",
            module_id="spectroscopy_instruments",
            title="Beer-Lambert UV-vis Calibration Model",
            maturity=MaturityLevel.REFERENCE_VALIDATED,
            summary=(
                "UV-vis absorbance and species calibration are generated from "
                "the Beer-Lambert relation with explicit path length, effective "
                "sample dilution, blank absorbance, detection limits, and "
                "linear calibration residuals."
            ),
            equations=(
                "Beer-Lambert: A = A_blank + epsilon * l * c_cuvette",
                "c_cuvette = c_reactor / dilution_factor",
                "calibration: A = slope * c_reactor + intercept",
                "LOD = 3.3 * sigma_residual / slope",
                "LOQ = 10 * sigma_residual / slope",
            ),
            assumptions=(
                "single dominant band per virtual species role",
                "linear absorbance range after explicit dilution",
                "baseline drift and Gaussian band shape are synthetic instrument effects",
                "molar absorptivities are benchmark parameters, not molecule-specific data",
            ),
            validity_limits=(
                "requires finite nonnegative concentrations",
                "requires positive molar absorptivity and optical path length",
                "does not model scattering, stray light, saturation, or real solvent baselines",
                "not a substitute for empirical UV-vis databases or quantum spectra",
            ),
            failure_modes=(
                "negative concentration or invalid optical parameters raise ValueError",
                "calibration standards with no concentration span raise ValueError",
                "nonpositive fitted slope raises ValueError",
            ),
            units={
                "absorbance": "dimensionless",
                "molar_absorptivity": "L mol^-1 cm^-1",
                "path_length": "cm",
                "concentration": "mol/L",
                "wavelength": "nm",
            },
            reference_reading=(
                (
                    "Beer-Lambert analytical relation used directly as the "
                    "reference equation for public instrument behavior."
                ),
                (
                    "reference_repos/chemicals/docs/developers.rst notes UV-Vis "
                    "spectral databases such as NIST as future data sources, but "
                    "does not implement an instrument model."
                ),
                (
                    "Local spectroscopy implementation read in "
                    "src/chemworld/physchem/spectroscopy.py and "
                    "src/chemworld/world/spectra.py."
                ),
            ),
            validation_evidence=(
                ValidationEvidence(
                    evidence_id="beer_lambert_linear_calibration",
                    evidence_type="analytical",
                    description=(
                        "Noiseless standards recover the declared effective "
                        "Beer-Lambert slope and molar absorptivity."
                    ),
                    status="implemented",
                    command_or_path="tests/test_spectroscopy.py",
                    tolerance="1e-12 relative for noiseless calibration",
                ),
                ValidationEvidence(
                    evidence_id="uvvis_species_signal_uses_band_metadata",
                    evidence_type="unit_test",
                    description=(
                        "UV-vis species spectra carry path length, dilution, "
                        "absorptivity, and Beer-Lambert model metadata."
                    ),
                    status="implemented",
                    command_or_path="tests/test_spectroscopy.py",
                ),
            ),
            intended_use=(
                "virtual UV-vis calibration in ChemWorld benchmark tasks",
                "teaching instrument selection and calibration uncertainty",
                "LLM/tool-agent parsing of raw spectra and processed estimates",
            ),
        ),
        ModelCard(
            model_id="chromatography_retention_plate",
            module_id="spectroscopy_instruments",
            title="Chromatography Retention And Plate-Count Calibration Model",
            maturity=MaturityLevel.REFERENCE_VALIDATED,
            summary=(
                "HPLC and GC retention-time traces are generated from explicit "
                "dead time, retention factor, theoretical plate count, baseline "
                "peak width, detector response calibration, and adjacent-peak "
                "resolution equations."
            ),
            equations=(
                "retention factor: k' = (t_R - t_M) / t_M",
                "retention time: t_R = t_M * (1 + k')",
                "baseline width: w_b = 4 * t_R / sqrt(N)",
                "theoretical plates: N = 16 * (t_R / w_b)^2",
                "resolution: R_s = 2 * (t_R2 - t_R1) / (w_b1 + w_b2)",
            ),
            assumptions=(
                "one Gaussian peak per visible species in the virtual method",
                "role-based benchmark retention factors with deterministic species offsets",
                "constant plate count per method",
                "area calibration is linear over the benchmark concentration range",
            ),
            validity_limits=(
                "requires positive dead time and theoretical plate count",
                "requires retention time at least as large as dead time",
                "does not model gradient elution, temperature programming, tailing, or columns",
                "not a substitute for empirical retention-index or LSER databases",
            ),
            failure_modes=(
                "negative retention factor raises ValueError",
                "invalid baseline widths or dead time raise ValueError",
                "calibration data with inconsistent lengths raise ValueError",
            ),
            units={
                "dead_time": "min",
                "retention_time": "min",
                "baseline_width": "min",
                "concentration": "mol/L",
                "response": "arbitrary detector area",
            },
            reference_reading=(
                (
                    "Public chromatography equations for k', theoretical "
                    "plates, baseline width, and resolution are used directly "
                    "as analytical reference cases."
                ),
                (
                    "reference_repos/rmg-py/documentation/source/users/rmg/"
                    "liquids.rst cites chromatography/LSER references by "
                    "Vitha-Carr and Poole, but does not implement an instrument kernel."
                ),
                (
                    "Local spectroscopy implementation read in "
                    "src/chemworld/physchem/spectroscopy.py and "
                    "src/chemworld/world/spectra.py."
                ),
            ),
            validation_evidence=(
                ValidationEvidence(
                    evidence_id="chromatography_retention_equations",
                    evidence_type="analytical",
                    description=(
                        "Unit tests verify retention factor, retention time, "
                        "baseline width, theoretical plates, and resolution formulas."
                    ),
                    status="implemented",
                    command_or_path="tests/test_spectroscopy.py",
                    tolerance="floating-point pytest.approx",
                ),
                ValidationEvidence(
                    evidence_id="chromatography_species_signal_metadata",
                    evidence_type="unit_test",
                    description=(
                        "HPLC/GC species peaks carry model id, dead time, "
                        "retention factor, plate count, width, and resolution metadata."
                    ),
                    status="implemented",
                    command_or_path="tests/test_spectroscopy.py",
                ),
            ),
            intended_use=(
                "virtual HPLC/GC retention calibration in ChemWorld tasks",
                "teaching peak width, overlap, and method resolution tradeoffs",
                "LLM/tool-agent parsing of chromatograms and calibrated estimates",
            ),
        ),
        ModelCard(
            model_id="ir_functional_group_bands",
            module_id="spectroscopy_instruments",
            title="IR Functional-Group Band Model",
            maturity=MaturityLevel.REFERENCE_VALIDATED,
            summary=(
                "IR spectra are generated from a compact curated functional-group "
                "band catalog with formula/role-triggered assignments, explicit "
                "wavenumber units, broadening, transmittance-mode signal synthesis, "
                "and overlap/interference diagnostics."
            ),
            equations=(
                "band response: R_i = alpha_group * c_species",
                "Gaussian band: I = A / (sigma sqrt(2 pi)) exp[-0.5 ((nu-nu0)/sigma)^2]",
                "Lorentzian broad O-H band: I = A (gamma/pi) / ((nu-nu0)^2 + gamma^2)",
                "transmittance signal: T = clip(1 - sum(I_i) - baseline, 0, 1)",
                "overlap flag: |nu_i - nu_j| <= 0.55 * (width_i + width_j)",
            ),
            assumptions=(
                "formula-level functional-group triggers are intentionally coarse",
                "band centers and widths are local benchmark parameters",
                "broad O-H bands use a Lorentzian shape to mimic low-resolution tails",
                "overlap diagnostics are qualitative and intended for agent reasoning",
            ),
            validity_limits=(
                "requires a molecular formula for strict functional-group assignment",
                "does not infer connectivity, stereochemistry, solvent shifts, or real databases",
                "not a replacement for empirical IR libraries or quantum vibrational spectra",
            ),
            failure_modes=(
                "missing strict formula raises ValueError",
                "nonpositive wavenumber, width, or intensity raises ValueError",
                "invalid peak shape raises ValueError",
            ),
            units={
                "wavenumber": "cm^-1",
                "width": "cm^-1",
                "concentration": "mol/L",
                "transmittance": "dimensionless",
            },
            reference_reading=(
                (
                    "Public organic spectroscopy band tables motivate the "
                    "carbonyl, hydroxyl, C-H, fingerprint, and heteroatom proxy "
                    "regions; ChemWorld stores only compact local benchmark bands."
                ),
                (
                    "reference_repos/chemicals/docs/developers.rst notes IR, "
                    "NMR, and MS spectral databases such as NIST as future data "
                    "sources, but does not implement an instrument kernel."
                ),
                (
                    "Local spectroscopy implementation read in "
                    "src/chemworld/physchem/spectroscopy.py and "
                    "src/chemworld/world/spectra.py."
                ),
            ),
            validation_evidence=(
                ValidationEvidence(
                    evidence_id="ir_functional_group_assignment",
                    evidence_type="unit_test",
                    description=(
                        "Formula-triggered carbonyl, hydroxyl, C-H, and fingerprint "
                        "bands are assigned with explicit metadata and broadening."
                    ),
                    status="implemented",
                    command_or_path="tests/test_spectroscopy.py",
                ),
                ValidationEvidence(
                    evidence_id="ir_signal_interference_metadata",
                    evidence_type="unit_test",
                    description=(
                        "IR raw-signal packets expose functional-group metadata, "
                        "transmittance bounds, and unresolved-band interference flags."
                    ),
                    status="implemented",
                    command_or_path="tests/test_spectroscopy.py",
                ),
            ),
            intended_use=(
                "virtual IR functional-group reasoning in ChemWorld tasks",
                "LLM/tool-agent parsing of raw final-assay packets",
                "teaching qualitative band overlap and instrument uncertainty",
            ),
        ),
    )




__all__ = [
    "spectroscopy_model_cards",
]
