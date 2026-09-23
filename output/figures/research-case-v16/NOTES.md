# Research case: quench semantics, case choice and batch progress

Deliverables: [extended figure](c-w05-research-paths-v16.png), [PowerPoint](../../pptx/c-w05-research-paths-v16.pptx), [standalone curves](batch-progress.pdf), [source-precision values](batch-progress.csv), and [case-screen summary](data.json).

## Interpretation

Quench in this environment both lowers temperature to `max(298.15, current_temperature - 45)` K and marks reaction chemistry stopped. Subsequent thermal/crystallization operations remain possible. No quench does not mean no cooling: reaction chemistry can continue during subsequent cooling/holding. Implementation: `src/chemworld/runtime/primitive_services.py`, `quench`, and `src/chemworld/runtime/reaction_thermal_services.py`, the quenched thermal branch. The two source sessions have different materials and other conditions; their outcome difference does not isolate the effect of quenching.

The report screen includes 30 retained C reports, 29 labelled completed and one retained failed session with 11 of its scheduled 12 batches. There are 539 recorded batch summaries. These counts describe this report directory, not a new experimental block. The failed source is retained in the machine summary and is not treated as a complete illustrative pair.

The current W05 Aligned pair remains useful because it separates early feasibility from subsequent optimization. The 12-batch session first meets quality constraints at batch 1, with recovery 34.6997%, then attains its largest feasible point estimate at batch 10, 51.1736% (+16.4739 percentage points). The 24-batch session has no feasible batch until batch 20 (52.8704%); batch 23 gives its largest feasible point estimate, 56.9887%.

An alternative W04 Aligned pair better illustrates failure to find a feasible process within one session: the 12-batch session has 0/12 feasible batches, whereas the independent 24-batch session first becomes feasible at batch 17, with its best feasible recovery 41.8685% at batch 21. It offers no pair of quality-feasible final procedures, so it is less suitable for the present recipe/retest comparison. W03 Opaque also starts with infeasibility in both sessions (first feasible batches 2 and 11), but its best feasible recoveries round to 49.0% and 41.2%, respectively, with more complex thermal histories. It is another illustration of divergent research paths, not a general budget-benefit result. These cases are post hoc illustrative choices, not an estimate of the cohort-wide budget effect.

## Plot rules

The figure retains all 36 original W05 Aligned batch results. A filled circle denotes a quality-feasible batch; a rust-coloured cross denotes a quality-infeasible batch. Quality requires purity >=0.80, fines <=0.50 and positive crystal size, consistent with the existing figure. All 36 batches meet the purity threshold. The lower panels show fines and the 50% limit. The staircase is the running maximum of observed recovery among feasible batches only; no best-feasible value is drawn before the first feasible batch. Recovery excludes seed mass.

The two sessions are independent and are not joined into a single sequence or treated as one run continued after batch 12. The chart is a descriptive source trajectory, not replicated uncertainty evidence. Full-precision source values are retained in CSV/JSON; native Excel chart workbooks use 12 significant digits. The native chart caches were compared with the source values within 1e-8 percentage points after export.

## Layout and source preservation

The figure is now 1800 × 3440 CSS pixels in the one-slide PowerPoint and 3600 × 6880 pixels in the final PNG. The existing panel a/b artwork and selected-recipe icon row are preserved from `output/imagegen/c-w05-research-paths-v15.png` and uniformly scaled. Four progress charts and the larger c reflection/measurement/retest labels are native editable objects. The whole illustration is not claimed to be a fully editable vector. No generative image tool drew the numerical curves.

The c reflections remain condensed K1 accounts, explicitly labelled later reflections. The original agents and recipe artwork are retained; the reflection region has more height, regular-width Arial text and separate lines. The final PNG was exported from PowerPoint and visually reviewed, including enlarged chart and c regions. Native chart lines are explicitly unsmoothed; cross markers use no fill and a coloured outline. Package/geometry checks have no findings. No new experiments, manuscript modifications or full-paper PDF rebuild.

## Rebuild

From the repository's locked environment, run:

```powershell
uv run --no-sync python paper/tools/prepare_research_case_figure.py
uv run --no-sync node paper/tools/build_research_case_figure.mjs
& paper/tools/export_research_case_figure.ps1
```

The final PowerPoint-native export step is necessary: the intermediate generic preview renderer does not preserve every marker style, and the initial chart package otherwise inherits PowerPoint smoothing defaults. Original source reports and all prior figure versions remain unchanged.
