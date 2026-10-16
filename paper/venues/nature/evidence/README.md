# Retained evidence for manuscript review

This package exposes existing evidence, not additional experiments or new independent coding. The comparison is Opaque: no instance archival relationship was supplied. All 15 scientific-input pairs match after excluding only the campaign identifier. The exact public contracts, initial states and material information are in public_inputs.json.

- assessment_protocol.json: exact public query actions and retained evaluation prompts, excluding private world parameters and provider configuration.
- opportunity_query_predictions.csv: 1,044 query-response rows, including estimates, 80% intervals, held-out means and all five reference observations for 29 valid forecasts. Truth was not given to agents.
- opportunity_session_responses.csv: all 270 planned session/group/response cells; missing values remain empty, not zero.
- opportunity_world_responses.csv: 90 world/group/response means, with valid-session counts.
- focal_equilibrium_study.json: both matched sessions for Equilibrium study A, including source operations, full public notebook versions and sealed accounts. This is the new 0.085/0.716032 case, not the historical 0.092/0.51730 case.
- process_window_eligibility.csv: all 178 adjacent version pairs across 90 sessions. All have new final assays; 92 also have a committed non-measurement/non-termination operation after the later note. The remaining 86 lack that continuation.
- process_windows.json: all 92 retained codes, full adjacent notes, exact quotation locations, operation cursors, selected execution anchors and source paths.
- process_public_records.json: all 90 public session histories, including rejected operations and the 86 pairs excluded from the action-linked window definition.
- summary.json: exact counts, means and decomposition.

Window eligibility is determined from timing, new assays and later committed actions before semantic plan matching. It does not test whether a particular plan succeeds. Nevertheless, requiring subsequent committed research conditions the sample on continued activity. The selected immediate-plan labels do not enumerate every proposal; partly matched, rejected or unexecuted proposals remain in full notes and operation records. Terminal revisions are not classified as no learning. A second independent coder has not been added.

Reproduce from repository: uv run --no-sync python paper/tools/build_nature_review_evidence.py. The producer recomputes world means and window eligibility, checks all 182 quotations and their temporal anchors, and preserves the missing forecast. This producer also invokes build_abductive_evidence.py for the seven selected judgment histories (explanation_histories.json), focal_equilibrium_assays.csv and corrected_c_source_assays.csv, corrected_c_query_responses.csv, corrected_c_session_responses.csv and corrected_c_distribution_summary.json. These are retrospective, single-analyst derived analyses, not new experiments or full-cohort explanatory coding. Run plot_abductive_evidence.py for the six new data-derived figures; the conceptual Figure 1 remains ImageGen.
