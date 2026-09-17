# FL fixed-hardware system redesign result v1.1.0

Status: **0/15 qualified-development; stable scientific failure retained**

The v1.0.1 contract changed effective reactor volume when residence time was
changed. Version 1.1.0 fixes the reactor at 18 mL with a 4 mm internal diameter,
uses flow rate as the public control, and derives residence time as `tau=V/Q`.
All 15 units were therefore requalified; no v1.0.1 PASS was carried forward.

The canary passed. Entity, parametric, and structural blocks completed with no
platform or physical failures and every trajectory exact-replayed. Independent
full reruns reproduced every summary and World-report hash.

| Locus | Primary + replay | Qualified Worlds | Stable failure |
| --- | ---: | ---: | --- |
| Entity | 60 + 60 | 0/5 | Q5 identifiability; Q8 noise robustness |
| Parametric | 60 + 60 | 0/5 | Q5 throughout; Q7/Q8 in most Worlds |
| Structural | 90 + 90 | 0/5 | Q5 identifiability; Q7 behavioral relevance |

Summary SHA-256 values:

- entity: `5294da66166bc0daa64641f2adc02b18a47c145d9d449e283e7aac9152586b31`;
- parametric: `1b346a97729970506bab686a29aa9b3f9337705aa24b32a71b8f08b7cdcba976`;
- structural: `62053f1e0b6e2b5796eef844b4b3a896ab8f7f7e3d91285a7fad197747f396b9`;
- current FL registry: `2eeea7693c4a890bb0837c020e96ac97272c98e36002b5d6509eea511d17c698`.

These results show that the corrected execution contract is reproducible but
the present benchmark questions are too weak or insufficiently robust. The
thresholds were not lowered and a stronger private law was not introduced after
seeing the formal outcomes. A future v1.2 redesign must be a new preregistered
iteration, not a rewrite of this evidence.

Participant execution remains unauthorized.
