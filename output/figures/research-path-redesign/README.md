# Figure 2: experiments, interpretation, prediction and critique

This standalone preview addresses English Figure 2 (Chinese Figure 4), not the
operation/prediction figure. It has not replaced either manuscript asset.

## The role of the case

Figure 1 explains the instrument. Figure 2 should show how an actual autonomous
researcher uses it: what happens in the experiments, how the agent interprets
those observations, what the explanation predicts, and which weaknesses the
agent subsequently recognizes. Later figures establish population-level
contrasts. Removing the accounts from this case left an operation history
without its scientific interpretation; the revised design restores that link.

The two sessions find feasible procedures and offer qualified mechanistic
accounts. Both nevertheless predict a reduction in fines under a new thermal
intervention, whereas the withheld reference rises from about 35% to 100%.
Their subsequent critiques recognize an untested assumption and, in the
24-batch case, an underused negative result. These are documented public
accounts, not a reconstruction of unrecorded internal reasoning.

## Four connected panels

1. **Experimental trajectories and delivery.** All 36 batches from two
   independent 12/24-batch sessions remain visible, including infeasible
   outcomes, feasible running maxima, and selected batches 10/23. Independent
   evaluator retests appear below the plots. The 24-batch session first achieves
   feasibility at batch 20; it is not a continuation of the 12-batch session.
2. **Mechanistic interpretation (K1, after research).** Selected observations
   sit beside the agent's own explanations and acknowledged uncertainties:
   recovery versus fines under deeper cooling, coupled upstream/cooling changes,
   unresolved differences and an unmeasured seed-conditioning mechanism.
3. **Sealed prediction (Q).** Both agents invoke preferential dissolution of
   fines when predicting a new thermal intervention. The plots retain all four
   original 80% prediction intervals and place the withheld simulator reference
   in a separate grey panel. The comparison makes the erroneous predicted
   direction visible without treating the interpretation as established truth.
4. **Critique and proposed next experiments (K2).** After Q, without target
   feedback, the agents identify weaknesses in their own accounts and propose
   follow-up experiments. The proposals were not executed. In particular, the
   24-batch agent explicitly says it underused a null result while relying on
   the favorable textbook explanation for thermal cycling.

Displayed account text is author-condensed, not verbatim dialogue.
[Exact public excerpts](PUBLIC_ACCOUNTS.md) are linked to the retained reports
and checked by the renderer. The inspected source traces contain 449 operation
records with no supplied decision audit; their public messages contain only
the final campaign summaries. Thus K1/Q/K2 provide the verifiable explanation
sequence. They must not be drawn as contemporaneous reasons for individual
earlier actions.

Regular-weight Arial, muted slate blue/teal and rust failure marks connect the
figure visually to Figures 3 and 6. Lowercase bold panel letters retain the
Figure 1 convention. There are no realistic objects, agent avatars, decorative
status badges or slide footer.

## Caption draft

**From experiments to mechanistic accounts, sealed predictions and critique.**
a, Two independent Aligned crystallization sessions in the same retrospectively
selected world. All 36 batches are shown. Circles and crosses indicate quality
feasibility; step lines show the best feasible observed recovery, undefined
before first feasibility. Rings mark the sealed recommendations. The independent
retests are evaluator readouts. b, Selected observations and author-condensed
interpretations from the agents' original K1 reports, written after research.
The stated nucleation, upstream-coupling and seed-conditioning explanations are
agent interpretations. Heating and cooling change together in batches 19/20;
the comparison does not isolate their causal effects. c, Original sealed fines
forecasts for replacing a two-hour hold at 278.15 K with heating towards 315 K
for one hour and recooling towards 278.15 K for one hour, after the same
preceding recipe. Error bars retain the original 80% prediction intervals.
The grey panel shows the noise-free simulator reference, unavailable to the
agents. d, Condensed K2 critiques and proposed next experiments, obtained after
Q without reference feedback; the proposals were not executed. Temperatures
are requested targets. Recovery excludes seed mass; fines are the number
fraction below 20 micrometres. Quality requires purity at least 80%, fines at
most 50% and particles present. This selected pair illustrates the research
process; it does not estimate a population budget effect or identify unrecorded
internal reasoning. Single retests do not estimate reliability.

## Retained procedure details

Both selected recipes charge 0.040 mol reagent, 0.080 L solvent and 0.005 mol
catalyst. The 12-batch selection uses S1/C3, heating towards 360 K for 60 min at
400 rpm, no quench, 20 mg seed, direct cooling towards 250 K for 4 h and a 4 h
hold at 200 rpm. The 24-batch selection uses S2/C1, heating towards 450 K for
15 min at 600 rpm, a quench, 50 mg seed, staged cooling towards 310/280/250 K
for 4 h each and a 4 h hold at 100 rpm. Both end with filtration, termination
and final assay. Quench stops reaction chemistry while subsequent crystal
growth remains possible. The rejected 340 K cooling attempt in source batch
23 remains in the record and is excluded from the executable recommendation.
The particle-size check in batch 19 was omitted in batch 20. Complete actions,
retained observations and all three retest metrics remain in `data.json`.

## Data and outputs

The renderer reads the two retained source reports and original `summary.json`
under `workstreams/flagship_tasks/reports/work-ii-c-formal-20260920-v3-auto`.
It compares all 36 source-batch recovery/purity/fines values against the previous
figure input (absolute tolerance 1e-10 percentage points), checks the selections
at batches 10/23, and verifies exact canonical recommendation/retest action
equality. Retest values are observed metrics. It checks every quoted public
passage, the four forecast intervals, and the prediction/reference differences
against the retained contrast analysis. The cached reference levels are also
checked directly against the original qualification file when available.

- [PNG preview](figure02-research-paths-preview.png)
- [Vector SVG](figure02-research-paths-preview.svg)
- [Retained values and procedures](data.json)
- [Exact public accounts](PUBLIC_ACCOUNTS.md)

Rebuild from the repository root:

```powershell
uv run --no-sync python paper/tools/render_research_path_redesign.py
```

This is an editorial preview only. No new experiments, provider calls, simulator
runs, manuscript replacement or whole-paper PDF rebuild were performed.
