# W04 12-batch figure concepts

Generated with the built-in ImageGen tool. These are visual concepts, not manuscript figures. Neither image has been inserted into the paper.

## Shared design prompt

Publication-style 2D scientific infographic on white, landscape around 4:3. Use thin charcoal rules, mostly black text, restrained teal for feasible outcomes and rust for failures, consistent sans-serif typography, and flat process glyphs. No global title, decorative AI avatar, crystal artwork, gradients, heavy colored backgrounds, or photorealistic equipment. Panel a is a compact 12-batch status strip occupying at most 15% of the height. Panel b enlarges one complete original experiment and its in-process and final observations. Panel c shows selected recorded transitions and outcomes. A separate note labels K1 as written after all twelve batches; do not present it as contemporaneous reasoning.

## MisIndexed variant

Panel a: B1–4 fail; B5–10 feasible; B11 fails; B12 feasible. Mark B5 first feasible, B8 selected, B11 fines 72.6%, and the fines limit at 50%. Panel b: original B8 procedure: charge reagent, S2 and C1; heat toward 355 K for 1 h at 300 rpm; cool toward 325 K for 2 h; add 1 mg seed; cool toward 250 K for 4 h; hold 4 h at 100 rpm; particle-size check, filter, terminate, final assay. Process fines 26.6%; final recovery 45.5%, purity 98.2%, fines 25.4%. Panel c: selected, not necessarily adjacent, transitions: B1–4 fines around 100%; B5 changed quench/cooling history and achieved 30.3% fines; B5–7 endpoints 275→265→250 K with recovery 40.0→42.8→45.0%; B8 used 1 mg seed and reached 45.5% recovery; B11 raised concentration and had 72.6% fines; B12 returned to B8 recipe and had 26.9% fines. K1 note: quench-related nucleation is an interpretation and multiple conditions changed together.

The final targeted edit renamed panel c “Selected experimental transitions (intermediate batches omitted)” and its right header “Later test or result,” avoiding an implication that B8 and B11 were consecutive.

### MisIndexed decision concept v2

ImageGen edited the user-provided original concept into `w04-misindexed-12-batch-decision-concept-v2.png`. Prompt: preserve the complete B8 process and its readings; use the manuscript palette (charcoal `#24292D`, muted grey `#6A737B`, grid `#D7DDE1`, restrained teal `#277F8A`, MisIndexed copper `#BC7850`, failure rust `#A35F42`); replace panel a's status-only strip with compact, actual 12-point fines and recovery tracks and a 50% fines threshold; replace panel c's loose observation boxes with three observed–working question–next test–result loops. Label working questions as author reconstructions from recorded actions rather than contemporaneous model messages, and label K1 as written after research. A targeted ImageGen edit made B11's recovery marker rust because that batch failed the fines constraint.

The twelve source values supplied to ImageGen, in B1–B12 order, were fines (%) `99.7, 100.0, 99.5, 100.0, 30.3, 29.4, 25.4, 25.4, 26.9, 27.8, 72.6, 26.9` and seed-excluded recovery (%) `38.1, 22.6, 22.4, 24.8, 40.0, 42.8, 45.0, 45.5, 44.6, 44.7, 44.6, 44.1`. Panel c groups B1–5 (early thermal-history change), B5–8 (endpoint/seed refinements), and B8–12 (concentration challenge, return and repeat). B9–10 are explicitly indicated as additional probes so B8→B11 is not drawn as an adjacent transition.

### MisIndexed decision concept v3

ImageGen edited v2 into `w04-misindexed-12-batch-decision-concept-v3.png`, changing only panel c. The prompt replaced three U-shaped decision loops with three horizontal rows under four columns: `Observed → Agent question* → Next tested action → Outcome`. Exactly three straight rightward arrows per row; no return, curved, vertical or dotted arrows. Each question has a small charcoal line drawing of an agent at an open notebook and a restrained thought bubble. The three rows respectively show B1–4→B5, B5→B6–8, and B8/B9–10→B11/B12. The footnote states that questions were reconstructed from actions rather than recorded contemporaneous model quotes and that K1 followed research. A targeted edit recolored the B8/B9–10 text teal because these batches were feasible. Panels a and b, including all numbers, remain unchanged.

## Opaque variant

Panel a: exactly twelve cells; B1–11 fail, B12 alone is feasible with 46.8% fines. Do not print individual B1–11 percentages; mark the 50% fines limit. Panel b: original B12 procedure: charge 0.040 mol reagent, 0.080 L S0 and 0.005 mol C1; heat toward 360 K for 1 h at 500 rpm; add 50 mg seed before cooling; no quench; cool toward 330→315→300→285 K for 4 h each; four 4 h holds at 100 rpm; particle-size check, filter, terminate, final assay. Process fines 47.0%; final recovery 45.3%, purity 99.3%, fines 46.8%. Independent retest fines 48.3%. Panel c: recorded failed strategies: B1–4 quenched catalyst screen, B5–7 quenched solvent screen, B8 1.0 g total seed, B9 prolonged aging, B11 reheating, and B12 change to seed before cooling, omit quench and stage cooling. K1 note: early quench may have formed persistent fines, but B12 changed several conditions together.

The final targeted edit removed invented per-batch fines percentages from panel a while preserving the status of all twelve batches and the verified B12 value.

Sources: `workstreams/flagship_tasks/reports/work-ii-c-formal-20260920-v3-auto/C-W04-B12-E-MisIndexed.md`, `C-W04-B12-E-Opaque.md`, and the corresponding local original trajectories. The images abbreviate actions and do not reproduce all source data.
