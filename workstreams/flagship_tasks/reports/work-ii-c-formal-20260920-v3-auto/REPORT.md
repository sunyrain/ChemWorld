# Crystallization formal experiment

Postprocessing update, 21 September: [all thirty public baselines are now available](BASELINE_REANALYSIS.md). Two parser omissions were repaired; the other twenty-eight results reproduced exactly. The historical exports below retain their original parser diagnostics. Source experiments, predictions, posttests, retests and the 11/12 source nonconformance are unchanged.

Phase: ended_with_incomplete_chains.

Started: 30/30; complete chains: 29/30; failures: 1.
Sealed batches: 539/540; additional live unsealed batches: 0. Posttests: 90/90.

Qualification world results sealed: 5/5. A sealed failure is not a qualified world.

- C-W01: passed=True; failed checks: none.
- C-W02: passed=True; failed checks: none.
- C-W03: passed=True; failed checks: none.
- C-W04: passed=True; failed checks: none.
- C-W05: passed=True; failed checks: none.

Additional interrupted-attempt consumption: 81 reference final assays, 1441 operations, 20 model sources. These do not count as sealed qualification units.

| Cell | Status | Batches | K1/Q/K2 |
| --- | --- | ---: | ---: |
| [C-W01-B12-E-Opaque](C-W01-B12-E-Opaque.md) | completed | 12/12 | 3/3 |
| [C-W01-B12-E-Aligned](C-W01-B12-E-Aligned.md) | completed | 12/12 | 3/3 |
| [C-W01-B12-E-MisIndexed](C-W01-B12-E-MisIndexed.md) | completed | 12/12 | 3/3 |
| [C-W01-B24-E-Opaque](C-W01-B24-E-Opaque.md) | completed | 24/24 | 3/3 |
| [C-W01-B24-E-Aligned](C-W01-B24-E-Aligned.md) | completed | 24/24 | 3/3 |
| [C-W01-B24-E-MisIndexed](C-W01-B24-E-MisIndexed.md) | completed | 24/24 | 3/3 |
| [C-W02-B24-E-Aligned](C-W02-B24-E-Aligned.md) | completed | 24/24 | 3/3 |
| [C-W02-B24-E-MisIndexed](C-W02-B24-E-MisIndexed.md) | completed | 24/24 | 3/3 |
| [C-W02-B24-E-Opaque](C-W02-B24-E-Opaque.md) | completed | 24/24 | 3/3 |
| [C-W02-B12-E-Aligned](C-W02-B12-E-Aligned.md) | completed | 12/12 | 3/3 |
| [C-W02-B12-E-MisIndexed](C-W02-B12-E-MisIndexed.md) | completed | 12/12 | 3/3 |
| [C-W02-B12-E-Opaque](C-W02-B12-E-Opaque.md) | failed | 11/12 | 3/3 |
| [C-W03-B12-E-MisIndexed](C-W03-B12-E-MisIndexed.md) | completed | 12/12 | 3/3 |
| [C-W03-B12-E-Opaque](C-W03-B12-E-Opaque.md) | completed | 12/12 | 3/3 |
| [C-W03-B12-E-Aligned](C-W03-B12-E-Aligned.md) | completed | 12/12 | 3/3 |
| [C-W03-B24-E-MisIndexed](C-W03-B24-E-MisIndexed.md) | completed | 24/24 | 3/3 |
| [C-W03-B24-E-Opaque](C-W03-B24-E-Opaque.md) | completed | 24/24 | 3/3 |
| [C-W03-B24-E-Aligned](C-W03-B24-E-Aligned.md) | completed | 24/24 | 3/3 |
| [C-W04-B24-E-Opaque](C-W04-B24-E-Opaque.md) | completed | 24/24 | 3/3 |
| [C-W04-B24-E-Aligned](C-W04-B24-E-Aligned.md) | completed | 24/24 | 3/3 |
| [C-W04-B24-E-MisIndexed](C-W04-B24-E-MisIndexed.md) | completed | 24/24 | 3/3 |
| [C-W04-B12-E-Opaque](C-W04-B12-E-Opaque.md) | completed | 12/12 | 3/3 |
| [C-W04-B12-E-Aligned](C-W04-B12-E-Aligned.md) | completed | 12/12 | 3/3 |
| [C-W04-B12-E-MisIndexed](C-W04-B12-E-MisIndexed.md) | completed | 12/12 | 3/3 |
| [C-W05-B12-E-Aligned](C-W05-B12-E-Aligned.md) | completed | 12/12 | 3/3 |
| [C-W05-B12-E-MisIndexed](C-W05-B12-E-MisIndexed.md) | completed | 12/12 | 3/3 |
| [C-W05-B12-E-Opaque](C-W05-B12-E-Opaque.md) | completed | 12/12 | 3/3 |
| [C-W05-B24-E-Aligned](C-W05-B24-E-Aligned.md) | completed | 24/24 | 3/3 |
| [C-W05-B24-E-MisIndexed](C-W05-B24-E-MisIndexed.md) | completed | 24/24 | 3/3 |
| [C-W05-B24-E-Opaque](C-W05-B24-E-Opaque.md) | completed | 24/24 | 3/3 |

Scientific infeasibility is retained separately from execution failure. Query truth is never returned to model sessions.
