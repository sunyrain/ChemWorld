# Figure 2: research-path redesign preview

This standalone preview addresses English Figure 2 (Chinese Figure 4), not the
operation/prediction figure. It has not replaced either manuscript asset.
Sources, experiment outcomes, selected procedures and the current published
figure remain intact.

## Why the existing figure feels out of place

The old composite mixes raster apparatus illustrations, repeated operation
icons, charts, large status marks and dense later accounts. The batch trajectories
occupy little space while the same process is drawn repeatedly. Readers must
distinguish research history, local changes, final recommendations and later K1
accounts before they can identify the evidence. Reducing bold text alone does
not resolve this hierarchy.

Figure 1 explains the instrument. Figure 2 should make an actual autonomous
research process concrete. Figures 3 onward then establish population-level
contrasts. This case belongs in the main text as a traceable example of the
research process, with its retrospective selection and inferential limits clear.

## Four connected panels

1. **Research trajectories.** Enlarge the two actual recovery plots. Retain all
   36 batches, infeasible outcomes, the feasible running best and selected batches.
   Remove inferred research-phase icons and the redundant feasibility strip.
2. **Successive experimental changes.** Directly report the cooling-endpoint
   change in batches 9/10 and the coupled heating/cooling changes in batches
   19/20, alongside their recovery/fines observations. No immediate thoughts are
   reconstructed. The 24-batch session's first feasible batch is 20, not its final
   selection at 23.
3. **Selected procedures.** Two restrained vector process lanes replace the
   apparatus collage. Preserve material identities, heating, quench difference,
   seed mass, cooling targets, holding and isolation. The arrows denote the order
   of operations, not a continuous measured temperature trajectory.
4. **Independent retests.** Source and retest observations appear together for
   recovery, fines and purity, with the two quality thresholds. This separates
   selected-source outcomes from evaluator observations and adds the previously
   hard-to-find retest purity values.

Regular-weight Arial, muted slate blue/teal and rust failure marks connect the
figure visually to the new Figures 3 and 6. Lowercase bold panel letters retain
the Figure 1 convention. No slide footer, decorative agent avatars, checkmark
badges or realistic objects are used. Later K1 accounts remain available in the
retained reports and Appendix D; they should not be interleaved with contemporaneous
actions in the main diagram.

## Caption draft

**Two independent research paths connect experimental exploration to a selected
procedure and its retest.** a, All 36 batch outcomes from a retrospectively
selected matched Aligned crystallization pair. Filled circles and crosses mark
quality-feasible and infeasible batches. Step lines show the best observed
feasible recovery, undefined before the first feasible batch; rings identify
the sealed selections. The 24-batch campaign is a separate session. b, Recorded
thermal changes and observed outcomes in two successive-batch comparisons.
Heating and cooling change together in batches 19/20; the particle-size check
performed in batch 19 is also omitted in batch 20. These comparisons do not
identify contemporaneous decision reasons or isolate individual causal effects.
c, Summaries of the selected executable procedures. Both charge 0.040 mol
reagent, 0.080 L solvent and 0.005 mol catalyst. Heating uses 400/600 rpm and
holding uses 200/100 rpm for the 12/24-batch selections. Each cooling stage lasts
4 h. Quench stops reaction chemistry while subsequent cooling and crystal growth
remain possible. Temperatures are requested targets. The rejected 340 K cooling
attempt in source batch 23 is retained in the record and excluded from the
executable recommendation. d, Original source observations and single independent
retests. Recovery excludes seed mass; fines are the number fraction below 20
micrometres. Quality requires purity at least 80%, fines at most 50% and particles
present. Both recommendations meet these requirements on retest. Single retests
are not reliability estimates, and this selected pair does not establish a
population budget effect.

## Data and outputs

The renderer reads the two retained source reports and original `summary.json`
under `workstreams/flagship_tasks/reports/work-ii-c-formal-20260920-v3-auto`.
It compares all 36 source-batch recovery/purity/fines values against the previous
figure input (absolute tolerance 1e-10 percentage points), checks the selections
at batches 10/23, and verifies that the canonical recommendation actions exactly
match the retest actions. It uses observed retest metrics, not hidden truth.

- [PNG preview](figure02-research-paths-preview.png)
- [Vector SVG](figure02-research-paths-preview.svg)
- [Retained values and procedures](data.json)

Rebuild from the repository root:

```powershell
uv run --no-sync python paper/tools/render_research_path_redesign.py
```

This is an editorial preview only. No new experiments, provider calls, simulator
runs, manuscript replacement or whole-paper PDF rebuild were performed.
