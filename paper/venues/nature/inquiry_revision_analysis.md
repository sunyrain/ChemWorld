\clearpage

## Core research histories and same-cohort evidence use

### Main-text trajectory index

Five core histories are selected from the complete reading of 300 new sessions, and two from the separately retained thirty matched-world sessions. Selection is explanatory and retrospective, not a frequency sample. These aliases remain attached to whole trajectories while individual judgments are traced within them. Exact locators are supplied in the portable evidence archive. All other cases remain in unified_case_index.json and the full per-session readings. No independent human second-rater review is claimed.

| Study | Condition | Key times |
| --- | --- | --- |
| Purification study A | Aligned; world 4; repetition 3 | Batches 8-10: wash and phase comparisons; note 3 after operation 158; batch 11 small wash; batch 12 no-wash repeat; final account and forecasts |
| Purification study B | Aligned; world 1; repetition 2 | Batches 1-4 low recovery; note 2 after operation 64; operations 65-66 add both commands; batches 5-8 use remaining stock; four later assays unavailable; note 3 excludes temperature inference |
| Reaction study A | Discovery; Opaque; world 1; repetition 1 | Batch 6 direct termination; batch 10 immediate quench; batch 11 unquenched wait; note 4 after operation 79; batch 12 quench then wait; note 5 after operation 88; subsequent forecasts |
| Electrochemical study A | Optimization; Opaque; world 1; repetition 1 | Batches 1-2 compare signs; note 2 after operation 56; batches 9-12 refine negative-potential procedure; terminal note limits scope; forecasts extend to untested positive potentials |
| Electrochemical study B | Optimization; Aligned; world 3; repetition 2 | Batches 1-10 screen materials and duration; note 3 after operation 70 predicts reverse-sign test; batch 11 reverses sign; batch 12 repeats positive recipe; note 4 after operation 84; forecasts retain reverse production |
| Matched-world study A | Retained matched worlds; repeat-03; EQ-P03-A-Opaque | Notes at operation cursors 0, 36 and 72; batches 7-12 implement denser sampling, a central repeat and higher loading; final forecast |
| Matched-world study B | Retained matched worlds; repeat-02; EQ-P01-A-Opaque | Note at cursor 50 precedes dilution; operations 51-56 implement the 0.75 to 0.375 M comparison; final note at 61; forecast Q09 |

Full archive paths and record selectors are retained in `core_history_index.json` in the portable evidence archive.

### Source-only references in the new crystallization opportunity cohort

This post hoc summary exposes reference errors already stored with the completed experiment. All fifteen Research sessions have twelve final source assays and twelve valid query forecasts. Of 180 assays, 179 have all four required numeric responses; one incomplete response record in world 1, repetition 3 is excluded from the references by the original eligibility rule, leaving eleven training assays in that session. The constant reference uses the mean of that session's response-complete public final-assay responses; the nearest-neighbour reference uses the existing public-recipe feature distance and one observed final assay. Neither fits to query truth. Both are scored against the same noiseless preassay targets as the agent. The references are diagnostics of available information, not alternative autonomous researchers or NoResearch arms. They produce point forecasts only. Means below weight worlds equally after averaging the three sessions within each world. No model or simulator was run.

\Needspace{8\baselineskip}

| Response | Agent MAE | Source mean MAE | Source neighbour MAE | Agent beats mean |
| --- | --- | --- | --- | --- |
| Purity | 0.016609 | 0.004496 | 0.007198 | 0/15 |
| Size index | 0.076408 | 0.017859 | 0.028908 | 0/15 |
| Recovery | 0.115792 | 0.188282 | 0.185762 | 14/15 |
| Fines | 0.301102 | 0.292221 | 0.277943 | 7/15 |

| Session | Response | Agent MAE | Source mean MAE |
| --- | --- | --- | --- |
| repeat-01/W01 | Purity | 0.027117 | 0.004324 |
| repeat-01/W01 | Size index | 0.068380 | 0.015815 |
| repeat-01/W01 | Recovery | 0.047861 | 0.170143 |
| repeat-01/W01 | Fines | 0.357739 | 0.328699 |
| repeat-01/W02 | Purity | 0.006942 | 0.004217 |
| repeat-01/W02 | Size index | 0.070200 | 0.015657 |
| repeat-01/W02 | Recovery | 0.158912 | 0.172245 |
| repeat-01/W02 | Fines | 0.336200 | 0.272344 |
| repeat-01/W03 | Purity | 0.030796 | 0.004327 |
| repeat-01/W03 | Size index | 0.090569 | 0.021677 |
| repeat-01/W03 | Recovery | 0.098008 | 0.171039 |
| repeat-01/W03 | Fines | 0.308632 | 0.354471 |
| repeat-01/W04 | Purity | 0.008567 | 0.004471 |
| repeat-01/W04 | Size index | 0.071652 | 0.015686 |
| repeat-01/W04 | Recovery | 0.121634 | 0.233266 |
| repeat-01/W04 | Fines | 0.324135 | 0.259065 |
| repeat-01/W05 | Purity | 0.026932 | 0.004268 |
| repeat-01/W05 | Size index | 0.040076 | 0.019350 |
| repeat-01/W05 | Recovery | 0.126182 | 0.285032 |
| repeat-01/W05 | Fines | 0.285731 | 0.324408 |
| repeat-02/W01 | Purity | 0.017788 | 0.004328 |
| repeat-02/W01 | Size index | 0.024673 | 0.016110 |
| repeat-02/W01 | Recovery | 0.102709 | 0.179936 |
| repeat-02/W01 | Fines | 0.218377 | 0.290147 |
| repeat-02/W02 | Purity | 0.021315 | 0.004217 |
| repeat-02/W02 | Size index | 0.086866 | 0.015657 |
| repeat-02/W02 | Recovery | 0.098842 | 0.233702 |
| repeat-02/W02 | Fines | 0.394405 | 0.208088 |
| repeat-02/W03 | Purity | 0.011298 | 0.004257 |
| repeat-02/W03 | Size index | 0.027690 | 0.021677 |
| repeat-02/W03 | Recovery | 0.134281 | 0.193938 |
| repeat-02/W03 | Fines | 0.313637 | 0.354471 |
| repeat-02/W04 | Purity | 0.022794 | 0.004782 |
| repeat-02/W04 | Size index | 0.129569 | 0.016622 |
| repeat-02/W04 | Recovery | 0.117143 | 0.068968 |
| repeat-02/W04 | Fines | 0.289968 | 0.252701 |
| repeat-02/W05 | Purity | 0.015678 | 0.004723 |
| repeat-02/W05 | Size index | 0.139120 | 0.019350 |
| repeat-02/W05 | Recovery | 0.115765 | 0.151415 |
| repeat-02/W05 | Fines | 0.189354 | 0.322389 |
| repeat-03/W01 | Purity | 0.005993 | 0.005690 |
| repeat-03/W01 | Size index | 0.108632 | 0.016987 |
| repeat-03/W01 | Recovery | 0.118293 | 0.148436 |
| repeat-03/W01 | Fines | 0.315640 | 0.221309 |
| repeat-03/W02 | Purity | 0.011113 | 0.004332 |
| repeat-03/W02 | Size index | 0.071866 | 0.015657 |
| repeat-03/W02 | Recovery | 0.137246 | 0.226386 |
| repeat-03/W02 | Fines | 0.338572 | 0.237156 |
| repeat-03/W03 | Purity | 0.019853 | 0.004982 |
| repeat-03/W03 | Size index | 0.099359 | 0.021677 |
| repeat-03/W03 | Recovery | 0.126781 | 0.127220 |
| repeat-03/W03 | Fines | 0.273653 | 0.354471 |
| repeat-03/W04 | Purity | 0.012295 | 0.004310 |
| repeat-03/W04 | Size index | 0.040432 | 0.015686 |
| repeat-03/W04 | Recovery | 0.044129 | 0.212215 |
| repeat-03/W04 | Fines | 0.270875 | 0.252701 |
| repeat-03/W05 | Purity | 0.010661 | 0.004203 |
| repeat-03/W05 | Size index | 0.077036 | 0.020283 |
| repeat-03/W05 | Recovery | 0.189099 | 0.250285 |
| repeat-03/W05 | Fines | 0.299611 | 0.350891 |

### Interface ambiguity in the supporting reconstruction case

The public reaction record contains two 600 s requests with outer `ok: true` and `experiment_completed: true`, alongside `transaction_status: rolled_back`, `Transaction rolled back: constitution_failed`, and zero temperature/time changes. The terminal account nevertheless interprets this as 1,200 s without reaction and later forecasts invoke the resulting history effect. Conflicting success and rollback signals therefore coexist in what the researcher could read. This case concerns interface presentation, reconstruction of experimental history and later judgment; it does not isolate a chemical-reasoning failure or show that the false account guided earlier source actions. Another retained session explicitly excludes rolled-back heating from its chemical evidence. Their public records are preserved in the archive.

The supporting execution-state source is also located by `core_history_index.json` in the portable evidence archive.

### Exact world-level contrasts for the quantitative figures

Values average available sessions within the fixed world; lines connect different conditions, not successive states of one researcher. No confidence interval or population significance estimate is inferred from five worlds.

| Contrast | World | First arm | Second arm | First | Second |
| --- | --- | --- | --- | --- | --- |
| EC operating score | W01 | discovery | optimization | 0.459632 | 0.575253 |
| EC operating score | W02 | discovery | optimization | 0.473791 | 0.637564 |
| EC operating score | W03 | discovery | optimization | 0.577530 | 0.658915 |
| EC operating score | W04 | discovery | optimization | 0.387887 | 0.574185 |
| EC operating score | W05 | discovery | optimization | 0.507545 | 0.480318 |
| EC operating yield | W01 | discovery | optimization | 0.100273 | 0.439865 |
| EC operating yield | W02 | discovery | optimization | 0.161895 | 0.453575 |
| EC operating yield | W03 | discovery | optimization | 0.204481 | 0.567896 |
| EC operating yield | W04 | discovery | optimization | 0.076972 | 0.442531 |
| EC operating yield | W05 | discovery | optimization | 0.111237 | 0.208626 |
| EC score MAE | W01 | discovery | optimization | 0.158453 | 0.189030 |
| EC score MAE | W02 | discovery | optimization | 0.155817 | 0.163966 |
| EC score MAE | W03 | discovery | optimization | 0.122798 | 0.148287 |
| EC score MAE | W04 | discovery | optimization | 0.165603 | 0.198762 |
| EC score MAE | W05 | discovery | optimization | 0.167022 | 0.214282 |
| EC yield MAE | W01 | discovery | optimization | 0.061966 | 0.082740 |
| EC yield MAE | W02 | discovery | optimization | 0.071663 | 0.079994 |
| EC yield MAE | W03 | discovery | optimization | 0.056623 | 0.064126 |
| EC yield MAE | W04 | discovery | optimization | 0.067084 | 0.077356 |
| EC yield MAE | W05 | discovery | optimization | 0.075179 | 0.086120 |
| EC Faradaic MAE | W01 | discovery | optimization | 0.175364 | 0.232565 |
| EC Faradaic MAE | W02 | discovery | optimization | 0.188116 | 0.221573 |
| EC Faradaic MAE | W03 | discovery | optimization | 0.148873 | 0.179177 |
| EC Faradaic MAE | W04 | discovery | optimization | 0.160320 | 0.223794 |
| EC Faradaic MAE | W05 | discovery | optimization | 0.165625 | 0.251887 |
| RX operating score | W01 | Opaque | Aligned | 0.164965 | 0.410339 |
| RX operating score | W02 | Opaque | Aligned | 0.167654 | 0.401876 |
| RX operating score | W03 | Opaque | Aligned | 0.343337 | 0.467024 |
| RX operating score | W04 | Opaque | Aligned | 0.343173 | 0.461530 |
| RX operating score | W05 | Opaque | Aligned | 0.348259 | 0.473761 |
| RX operating yield | W01 | Opaque | Aligned | 0.379477 | 0.679752 |
| RX operating yield | W02 | Opaque | Aligned | 0.317379 | 0.626353 |
| RX operating yield | W03 | Opaque | Aligned | 0.685587 | 0.746694 |
| RX operating yield | W04 | Opaque | Aligned | 0.671190 | 0.753751 |
| RX operating yield | W05 | Opaque | Aligned | 0.697269 | 0.751411 |
| RX risk MAE | W01 | Opaque | Aligned | 0.181897 | 0.160300 |
| RX risk MAE | W02 | Opaque | Aligned | 0.255896 | 0.085367 |
| RX risk MAE | W03 | Opaque | Aligned | 0.274299 | 0.109202 |
| RX risk MAE | W04 | Opaque | Aligned | 0.117388 | 0.085237 |
| RX risk MAE | W05 | Opaque | Aligned | 0.365209 | 0.173087 |
| RX conversion MAE | W01 | Opaque | Aligned | 0.110849 | 0.204147 |
| RX conversion MAE | W02 | Opaque | Aligned | 0.048577 | 0.050513 |
| RX conversion MAE | W03 | Opaque | Aligned | 0.004695 | 0.234176 |
| RX conversion MAE | W04 | Opaque | Aligned | 0.006040 | 0.141381 |
| RX conversion MAE | W05 | Opaque | Aligned | 0.007418 | 0.167267 |
| C purity MAE | W01 | NoResearch | Research | 0.152672 | 0.016966 |
| C purity MAE | W02 | NoResearch | Research | 0.138427 | 0.013124 |
| C purity MAE | W03 | NoResearch | Research | 0.154020 | 0.020649 |
| C purity MAE | W04 | NoResearch | Research | 0.117794 | 0.014552 |
| C purity MAE | W05 | NoResearch | Research | 0.129727 | 0.017757 |
| C size MAE | W01 | NoResearch | Research | 0.257521 | 0.067229 |
| C size MAE | W02 | NoResearch | Research | 0.219922 | 0.076311 |
| C size MAE | W03 | NoResearch | Research | 0.204531 | 0.072540 |
| C size MAE | W04 | NoResearch | Research | 0.265124 | 0.080551 |
| C size MAE | W05 | NoResearch | Research | 0.233842 | 0.085410 |
| C recovery MAE | W01 | NoResearch | Research | 0.101444 | 0.089621 |
| C recovery MAE | W02 | NoResearch | Research | 0.116638 | 0.131667 |
| C recovery MAE | W03 | NoResearch | Research | 0.089683 | 0.119690 |
| C recovery MAE | W04 | NoResearch | Research | 0.175712 | 0.094302 |
| C recovery MAE | W05 | NoResearch | Research | 0.193132 | 0.143682 |
| C fines MAE | W01 | NoResearch | Research | 0.414218 | 0.297252 |
| C fines MAE | W02 | NoResearch | Research | 0.447546 | 0.356392 |
| C fines MAE | W03 | NoResearch | Research | 0.295352 | 0.298641 |
| C fines MAE | W04 | NoResearch | Research | 0.396913 | 0.294992 |
| C fines MAE | W05 | NoResearch | Research | 0.330115 | 0.258232 |
| C purity coverage | W01 | NoResearch | Research | 0.416667 | 0.972222 |
| C purity coverage | W02 | NoResearch | Research | 0.694444 | 1.000000 |
| C purity coverage | W03 | NoResearch | Research | 0.333333 | 0.972222 |
| C purity coverage | W04 | NoResearch | Research | 0.694444 | 1.000000 |
| C purity coverage | W05 | NoResearch | Research | 0.194444 | 0.972222 |
| C fines interval score | W01 | NoResearch | Research | 1.495489 | 1.660246 |
| C fines interval score | W02 | NoResearch | Research | 1.456775 | 2.218475 |
| C fines interval score | W03 | NoResearch | Research | 1.365044 | 1.884619 |
| C fines interval score | W04 | NoResearch | Research | 1.528390 | 1.692614 |
| C fines interval score | W05 | NoResearch | Research | 1.551302 | 1.567729 |
| EQ all macro MAE | W01 | NoResearch | Research | 0.174482 | 0.057096 |
| EQ all macro MAE | W02 | NoResearch | Research | 0.101026 | 0.040502 |
| EQ all macro MAE | W03 | NoResearch | Research | 0.102890 | 0.033076 |
| EQ all macro MAE | W04 | NoResearch | Research | 0.180595 | 0.028111 |
| EQ all macro MAE | W05 | NoResearch | Research | 0.101434 | 0.019374 |
| EQ dilute macro MAE | W01 | NoResearch | Research | 0.124277 | 0.204175 |
| EQ dilute macro MAE | W02 | NoResearch | Research | 0.021608 | 0.087108 |
| EQ dilute macro MAE | W03 | NoResearch | Research | 0.015246 | 0.081634 |
| EQ dilute macro MAE | W04 | NoResearch | Research | 0.106636 | 0.090199 |
| EQ dilute macro MAE | W05 | NoResearch | Research | 0.039570 | 0.055269 |
