# C-W05 sample figure — imagegen prompt set

Generated with the built-in image_gen tool. Final artwork: c-w05-agent-campaign-sample-schematic.png.

## c-w05-agent-campaign-sample-prompt.txt

Use case: scientific-educational.
Create ONE exceptionally polished, publication-quality scientific sample figure for a top-tier interdisciplinary research article. Landscape canvas, approximately 3:2 aspect ratio, highest available resolution. This is a rigorous evidence-grounded multi-panel infographic with exquisite restrained scientific 3D illustration, NOT a poster, dashboard, slide deck, or journal cover. All text in English.

Subject: Two independent autonomous-agent crystallization campaigns in the same simulated chemical world, C-W05, with aligned material information and budgets of 12 versus 24 experimental batches. The agent selects materials and procedures, receives measurements and tool feedback, and forms subsequent predictions. Convey both the campaign scale and the operations inside individual experiments.

DESIGN:
Warm white background, deep graphite typography, exceptionally clean Swiss editorial grid, generous whitespace, crisp fine arrows and leader lines. Elegant sans-serif typography with clear hierarchy. Restrained teal, muted indigo, amber and vermilion palette; no neon. Beautiful semi-realistic miniature borosilicate glass reactors, translucent liquid, softly lit faceted crystals and precise analytical instrument silhouettes, integrated with sharp vector-like diagrams. Soft physically plausible light, subtle contact shadows, no heavy glossy UI cards. Scientific artistry supports comprehension. No cartoon robot, human, brain, fantasy molecule, decorative molecular wallpaper, laboratory photograph background, logos or watermarks.
Large readable title: "Autonomous experimentation, from action to generalization"
Small subtitle: "Crystallization | C-W05 | Aligned information"
Use four clean panels labelled a, b, c, d. Panel a spans the upper third; panels b and c occupy the lower left and middle; panel d is a compact quantitative column at the right. Keep long prose out of the figure.

PANEL a — "Two independent research trajectories"
A slim objective line: "Maximize crystal recovery | Purity ≥ 0.80 | Fines ≤ 0.50"
Two separately started horizontal campaign timelines, labelled "12 batches" and "24 batches". Do NOT connect the end of the 12-batch campaign to the beginning or midpoint of the 24-batch campaign. Budgets mean batches, not tool actions.
Upper timeline: exactly 12 small numbered nodes 1–12; restrained phase ribbons annotate:
1–4 "Catalysts"
5–7 "Solvents"
8–10 "Cooling endpoint"
11 "Seed amount"
12 "In-batch measurements".
Highlight node 10 with a small filled indigo selection mark and label "Selected: batch 10"; outline node 12 in teal and connect a fine magnification leader to panel b.
Lower timeline: exactly 24 small numbered nodes 1–24, enough spacing and legibility:
1–6 "Material exploration"
7–18 "Persistent fines constraint"
19 "Hotter, shorter reaction"
20 "First feasible batch"
21–24 "Refinement".
Make nodes 1–19 amber-toned and nodes 20–24 teal-toned, referring to the observed product-quality constraint. Highlight node 23 with the same indigo selection mark and label "Selected: batch 23"; connect it to panel c.
A small amber annotation by node 19: "Fines 0.528"
A teal annotation by node 20: "Fines 0.215"
No invented numerical trend curve.

PANEL b — "Inside batch 12 | 12-batch campaign"
Show a beautiful compact actual operation workflow with a small transparent jacketed reactor, temperature-control motif, an HPLC icon and three particle-measurement callouts. This is a stylized simulated laboratory rendering, not photographic evidence.
The exact executed sequence is:
"Charge" → "Heat" → "HPLC" → "Seed" → "280 K" → "Measure" → "250 K" → "Measure" → "Age" → "Measure" → "Filter" → "Final assay".
Use a refined two-row or serpentine layout only if necessary; direction must remain unambiguous. The three Measure positions are particle-size measurements, with three sparse little crystal/particle illustrations and the exact measured fines values:
after 280 K: "Fines 0.406"
after 250 K: "Fines 0.362"
after ageing: "Fines 0.352".
Let the cooling and measurement segment visually dominate this panel. Beautiful sparse coarse crystals and small fines in clear liquid; particle illustrations are schematic, not an exact observed micrograph. Label these readouts "Particle-size measurements". Show feedback returning to an abstract small decision junction, without thought bubbles or invented rationale. No claim that an unrecorded internal belief update occurred.

PANEL c — "Inside batch 23 | 24-batch campaign"
A complementary exquisite reactor-to-crystal procedure illustration, emphasizing tool feedback and actual thermal history.
Compact annotations:
"Heat: 450 K requested"
"413.84 K observed"
Then "Quench" followed by "Seed".
Show an amber/red dashed branch to "340 K" clearly crossed out and labelled "Rejected; no state change".
The successful solid-arrow route then runs "310 K → 280 K → 250 K" followed by "Age → Filter → Final assay".
The rejected 340 K attempt is NOT a successful cooling step and must not lie on the successful temperature trace.
Use glass reactor, a stepped cooling graphic with only the named temperatures, and a tasteful crystalline product illustration to make process history tangible.
A small outcome label below: "Recovery 0.570 | Purity 1.000 | Fines 0.142"
These are measured source-batch results, not noiseless truth and not the independent retest.
Keep precise scientific typography; do not invent unseen physical time-series or imply measured crystal morphology.

PANEL d — "Operation and prediction"
An impeccably typeset simple comparison table with column headings "12 batches" and "24 batches". Use thin rules, no decorative chart backgrounds. Exactly these four rows and values:
Small group heading "Independent retest"
"Recovery"          "0.504"   "0.581"
"Fines"             "0.462"   "0.193"
Small group heading "Held-out prediction MAE"
"Recovery"          "0.1153"  "0.0593"
"Purity"            "0.0112"  "0.0648"
Use subtle teal emphasis on improved retest recovery, retest fines, and recovery prediction; muted vermilion emphasis on worse purity prediction. Add small text "Lower MAE is better". Do not mix source-batch and retest values.
Below the table, a concise typographic takeaway: "Better operation does not imply uniform generalization."

FOOTER:
Small readable grey caption, exact wording:
"Selected case; independent sessions. Actions and observations are recorded; decision rationales were not logged."
Small separate tag: "Schematic rendering"

Scientific accuracy and beauty are equally important. Preserve all numerical values, experimental ordering, selected batch indices, and the independent-session distinction. Prefer beautifully edited whitespace and high legibility over excess detail. Make this feel like a carefully art-directed figure with professional scientific illustration, not a template infographic.


## c-w05-agent-campaign-sample-edit-prompt.txt

Edit this existing scientific figure into a much more elegant, abstract academic illustration. The supplied image is the EDIT TARGET. Keep its scientific subject, four-panel structure, title and evidence, but substantially simplify the visual treatment.

USER PRIORITY: The instruments must NOT be this realistic. Replace EVERY photorealistic apparatus with refined schematic icons: thin clean outlines, simple geometric vessel silhouettes, minimal two-tone flat fills, no metallic hardware, cables, screws, motors, pipes, control panels, realistic HPLC machine, photographic glass reflections, or rendered lab furniture. HPLC and particle measurement should be small abstract measurement symbols. Maintain a restrained artistic touch only in translucent liquid areas, a few elegant geometric crystal shapes, and soft color transitions. Think beautifully edited journal scientific illustration with vector-like precision and plenty of whitespace. The graphic must be intellectually sophisticated and visually calm, not a clip-art infographic and not a hardware catalogue. Warm white, graphite, restrained teal and indigo, muted amber for constraint failures and vermilion for rejected operation. Uniform thin strokes, consistent typography, no heavy panel boxes. Render at high resolution, landscape 3:2.

Preserve title "Autonomous experimentation, from action to generalization"
Subtitle "Crystallization | C-W05 | Aligned information"

PANEL a: "Two independent research trajectories".
Keep the objective "Maximize crystal recovery | Purity ≥ 0.80 | Fines ≤ 0.50".
Two independent horizontal rows:
12-batch row has exactly 12 numbered nodes: 1 2 3 4 5 6 7 8 9 10 11 12.
Stages: "Catalysts (1–4)", "Solvents (5–7)", "Cooling endpoint (8–10)", "Seed amount (11)", "In-batch measurements (12)".
Highlight 10 "Selected: batch 10"; node 12 leads to panel b.
REBUILD the 24-batch row to correct the incorrect numbering in the input. Exactly 24 equally spaced nodes, with exactly these numerals, once each and in order:
1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24.
No duplicated 10, 19 or 22, no extra nodes, no skipped 21.
Stages spelled exactly: "Material exploration (1–6)", "Persistent fines constraint (7–18)", "Hotter, shorter reaction (19)", "First feasible batch (20)", "Refinement (21–24)".
Nodes 1–19 amber; 20–24 teal; 23 highlighted indigo.
Precisely anchor "Fines 0.528" to node 19 and "Fines 0.215" to node 20.
"Selected: batch 23", leading to panel c.
Use the label "(independent run)" under both budget labels. Never connect the two campaigns.

PANEL b: "Inside batch 12 | 12-batch campaign".
Replace the realistic instrument flow by a beautifully clean schematic operation sequence and three measurement readouts. IMPORTANT CORRECTIONS:
The heat step in this panel is 360 K REQUESTED, not 450 K. Remove the wrong 450 K instrument display from the original. Write only "Heat: 360 K requested".
This is the LAST experimental batch. DELETE the entire "Next experiment (selection & procedure)" box, the return-to-Charge arrow and the "Experimental feedback" loop from the original. There is no next batch.
The actual chronological route must be unambiguous:
Charge → Heat → HPLC → Seed → Cool to 280 K → particle-size measurement → Cool to 250 K → particle-size measurement → Age → particle-size measurement → Filter → Final assay → Campaign complete.
You may lay this out in two or three orderly horizontal rows linked by obvious arrows; avoid crossed arrows and leave whitespace.
Make the middle sequence visually dominant: abstract liquid vessel at 280 K, a small particle-measurement icon and "Fines 0.406"; vessel at 250 K, measurement icon and "Fines 0.362"; Age, measurement icon and "Fines 0.352".
A few softly colored geometric crystals are sufficient. No photorealistic particle inset or fabricated spectrum.
Final assay must occur AFTER Filter, never before it.
End with a small label "Campaign complete". This is a selected batch visualization, not a fictitious feedback loop.

PANEL c: "Inside batch 23 | 24-batch campaign".
Abstract process schematic with a restrained artistic crystal motif.
Heat label: "450 K requested" and "413.84 K observed".
Then "Quench" → "Seed".
A dashed vermilion rejected branch says "340 K" and "Rejected; no state change", with a small x.
Solid successful route: "310 K → 280 K → 250 K" then "Age → Filter → Final assay".
The 340 K rejected request must NOT look like a completed cooling stage.
Outcome exactly: "Recovery 0.570 | Purity 1.000 | Fines 0.142".
No temperature value printed on any instrument display. Text annotations only.
No fabricated continuous time series or physical crystal micrographs.

PANEL d: "Operation and prediction".
Keep the clean exact comparison table, with columns "12 batches" and "24 batches":
Independent retest:
Recovery 0.504 0.581
Fines 0.462 0.193
Held-out prediction MAE:
Recovery 0.1153 0.0593
Purity 0.0112 0.0648
"Lower MAE is better"
Teal for improvements; subtle vermilion for 0.0648.
Takeaway: "Better operation does not imply uniform generalization."

Footer, readable small grey text:
"Selected case; independent sessions. Actions and observations are recorded; decision rationales were not logged."
Small tag "Schematic rendering".

Do not introduce extra numerical data or embellish unrecorded agent reasoning. Prioritize sophisticated abstract visual design, accurate text, correct node numbering and clear experimental sequence.


## c-w05-agent-campaign-sample-final-edit-prompt.txt

Edit the supplied scientific figure with ONE strictly local correction. Preserve the entire existing abstract academic style, typography, layout, title, panels b/c/d, all other text and numerical data. DO NOT redraw instruments, panels b/c/d or the 12-batch row.

ONLY change the LOWER timeline in panel a, the one labelled "24 batches". Its current many small numbered circles contain duplicate 15 and 23. Instead of trying to renumber dozens of circles, REMOVE ALL of the little numbered circles from this 24-batch row and replace them with exactly FIVE clean, spacious stage markers aligned under the five existing colored phase ribbons. Keep their connecting horizontal line. The five marker labels are exactly:
"1–6" beneath Material exploration
"7–18" beneath Persistent fines constraint
"19" beneath Hotter, shorter reaction
"20" beneath First feasible batch
"21–24" beneath Refinement.
Use compact pill-shaped range markers if necessary. First three amber, fourth teal, fifth teal with a subtle indigo accent. Exactly five markers, no other batch-number circles in this lower row.
Keep the callout "Fines 0.528" anchored to marker "19".
Keep "Fines 0.215" anchored to marker "20".
Keep a separate small callout "Selected: batch 23" under the "21–24" refinement stage, with an indigo pointer into that stage. The dashed leader "To panel c" originates from this selected-batch callout, not from a fictitious numbered circle.
Do not change the 12-batch row; its existing numbering is correct.
Do not change any figures or text in panels b, c and d.
Preserve the white background, restrained teal/indigo/amber palette, clean line icons, soft geometric crystal rendering and all scientific values. This is a precise local correction, not a redesign.
