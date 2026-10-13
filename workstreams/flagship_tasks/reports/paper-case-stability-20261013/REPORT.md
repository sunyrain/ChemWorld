# Fixed-case notebook stability — three fresh repetitions

Descriptive development results. The previous six cases are separate references, excluded from means and sample SDs. Each case has three planned independent sessions; batches, predictions and reference observations are not independent Agent replicates.

Terminal 18/18; complete chains 17/18; source batches 252/252; sealed posttests 58/60.

Scheduling: initially serial; see scheduling_amendment in summary.json for any user-authorized concurrency change. Participant conditions and denominators remain fixed; equal provider service load is not assumed.

| Case | Repeat | Status | Batches | Operations | Rollbacks | Note versions | Reads | Record |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| EC-discovery | repeat-01 | completed | 12/12 | 84 | 0 | 3 | 0 | [notes](repeat-01/EC-discovery-notebook.md), [reports](repeat-01/EC-discovery-reports.md) |
| EC-optimization | repeat-01 | completed | 12/12 | 85 | 0 | 3 | 0 | [notes](repeat-01/EC-optimization-notebook.md), [reports](repeat-01/EC-optimization-reports.md) |
| EQ-Sol | repeat-01 | completed | 12/12 | 63 | 3 | 2 | 0 | [notes](repeat-01/EQ-Sol-notebook.md), [reports](repeat-01/EQ-Sol-reports.md) |
| EQ-Astra | repeat-01 | retained_nonconforming | 12/12 | 63 | 0 | 4 | 0 | [notes](repeat-01/EQ-Astra-notebook.md), [reports](repeat-01/EQ-Astra-reports.md) |
| C-12 | repeat-01 | completed | 12/12 | 241 | 19 | 2 | 0 | [notes](repeat-01/C-12-notebook.md), [reports](repeat-01/C-12-reports.md) |
| C-24 | repeat-01 | completed | 24/24 | 425 | 8 | 4 | 0 | [notes](repeat-01/C-24-notebook.md), [reports](repeat-01/C-24-reports.md) |
| EC-discovery | repeat-02 | completed | 12/12 | 84 | 0 | 3 | 0 | [notes](repeat-02/EC-discovery-notebook.md), [reports](repeat-02/EC-discovery-reports.md) |
| EC-optimization | repeat-02 | completed | 12/12 | 90 | 0 | 4 | 0 | [notes](repeat-02/EC-optimization-notebook.md), [reports](repeat-02/EC-optimization-reports.md) |
| EQ-Sol | repeat-02 | completed | 12/12 | 60 | 0 | 2 | 0 | [notes](repeat-02/EQ-Sol-notebook.md), [reports](repeat-02/EQ-Sol-reports.md) |
| EQ-Astra | repeat-02 | completed | 12/12 | 63 | 0 | 4 | 0 | [notes](repeat-02/EQ-Astra-notebook.md), [reports](repeat-02/EQ-Astra-reports.md) |
| C-12 | repeat-02 | completed | 12/12 | 256 | 3 | 3 | 0 | [notes](repeat-02/C-12-notebook.md), [reports](repeat-02/C-12-reports.md) |
| C-24 | repeat-02 | completed | 24/24 | 754 | 427 | 6 | 0 | [notes](repeat-02/C-24-notebook.md), [reports](repeat-02/C-24-reports.md) |
| EC-discovery | repeat-03 | completed | 12/12 | 84 | 0 | 4 | 0 | [notes](repeat-03/EC-discovery-notebook.md), [reports](repeat-03/EC-discovery-reports.md) |
| EC-optimization | repeat-03 | completed | 12/12 | 86 | 0 | 4 | 0 | [notes](repeat-03/EC-optimization-notebook.md), [reports](repeat-03/EC-optimization-reports.md) |
| EQ-Sol | repeat-03 | completed | 12/12 | 61 | 0 | 2 | 0 | [notes](repeat-03/EQ-Sol-notebook.md), [reports](repeat-03/EQ-Sol-reports.md) |
| EQ-Astra | repeat-03 | completed | 12/12 | 72 | 3 | 5 | 0 | [notes](repeat-03/EQ-Astra-notebook.md), [reports](repeat-03/EQ-Astra-reports.md) |
| C-12 | repeat-03 | completed | 12/12 | 179 | 0 | 5 | 0 | [notes](repeat-03/C-12-notebook.md), [reports](repeat-03/C-12-reports.md) |
| C-24 | repeat-03 | completed | 24/24 | 269 | 23 | 5 | 0 | [notes](repeat-03/C-24-notebook.md), [reports](repeat-03/C-24-reports.md) |

## EC-discovery

| Metric | Previous | R1 | R2 | R3 | n/3 | Mean | SD | Min-max |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| electrochemical_selectivity_coverage80 | 1 | 0.5 | 0.833333 | 0.5 | 3/3 | 0.611111 | 0.19245 | 0.5 to 0.833333 |
| electrochemical_selectivity_mae | 0.0508904 | 0.468929 | 0.134182 | 0.445726 | 3/3 | 0.349613 | 0.186929 | 0.134182 to 0.468929 |
| energy_efficiency_coverage80 | 0.583333 | 0.166667 | 0.833333 | 0.5 | 3/3 | 0.5 | 0.333333 | 0.166667 to 0.833333 |
| energy_efficiency_mae | 0.216359 | 0.421233 | 0.0595273 | 0.378199 | 3/3 | 0.28632 | 0.197583 | 0.0595273 to 0.421233 |
| faradaic_efficiency_coverage80 | 0.5 | 0.25 | 0.833333 | 0.5 | 3/3 | 0.527778 | 0.292657 | 0.25 to 0.833333 |
| faradaic_efficiency_mae | 0.189296 | 0.353421 | 0.0614558 | 0.335504 | 3/3 | 0.250127 | 0.16364 | 0.0614558 to 0.353421 |
| recommendation_score | 0.593299 | 0.280734 | 0.598356 | 0.100564 | 3/3 | 0.326551 | 0.252039 | 0.100564 to 0.598356 |
| score_coverage80 | 0.833333 | 0.5 | 0.75 | 0.5 | 3/3 | 0.583333 | 0.144338 | 0.5 to 0.75 |
| score_mae | 0.0906425 | 0.279932 | 0.112741 | 0.254463 | 3/3 | 0.215712 | 0.0900798 | 0.112741 to 0.279932 |
| selective_product_yield_coverage80 | 0.833333 | 0.166667 | 0.25 | 0.333333 | 3/3 | 0.25 | 0.0833333 | 0.166667 to 0.333333 |
| selective_product_yield_mae | 0.0392888 | 0.0989415 | 0.0694415 | 0.0999415 | 3/3 | 0.0894415 | 0.0173277 | 0.0694415 to 0.0999415 |
| transport_efficiency_coverage80 | 0.5 | 0.333333 | 0.916667 | 0.5 | 3/3 | 0.583333 | 0.300463 | 0.333333 to 0.916667 |
| transport_efficiency_mae | 0.200448 | 0.368166 | 0.0610567 | 0.337704 | 3/3 | 0.255642 | 0.169203 | 0.0610567 to 0.368166 |

## EC-optimization

| Metric | Previous | R1 | R2 | R3 | n/3 | Mean | SD | Min-max |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| electrochemical_selectivity_coverage80 | 1 | 0.916667 | 0.916667 | 0.5 | 3/3 | 0.777778 | 0.240563 | 0.5 to 0.916667 |
| electrochemical_selectivity_mae | 0.0380328 | 0.0635398 | 0.0999822 | 0.147141 | 3/3 | 0.103554 | 0.0419151 | 0.0635398 to 0.147141 |
| energy_efficiency_coverage80 | 0.416667 | 0.916667 | 0.75 | 0.166667 | 3/3 | 0.611111 | 0.393818 | 0.166667 to 0.916667 |
| energy_efficiency_mae | 0.258261 | 0.110247 | 0.136069 | 0.443067 | 3/3 | 0.229794 | 0.18515 | 0.110247 to 0.443067 |
| faradaic_efficiency_coverage80 | 0.666667 | 0.833333 | 0.916667 | 0.0833333 | 3/3 | 0.611111 | 0.458964 | 0.0833333 to 0.916667 |
| faradaic_efficiency_mae | 0.194616 | 0.0900174 | 0.103128 | 0.391838 | 3/3 | 0.194994 | 0.170597 | 0.0900174 to 0.391838 |
| recommendation_score | 0.831125 | 0.66899 | 0.919517 | 0.463137 | 3/3 | 0.683881 | 0.228554 | 0.463137 to 0.919517 |
| score_coverage80 | 0.75 | 0.833333 | 0.916667 | 0.166667 | 3/3 | 0.638889 | 0.411074 | 0.166667 to 0.916667 |
| score_mae | 0.100479 | 0.0471846 | 0.0867263 | 0.281219 | 3/3 | 0.138377 | 0.125275 | 0.0471846 to 0.281219 |
| selective_product_yield_coverage80 | 0.833333 | 0.833333 | 0.833333 | 0.583333 | 3/3 | 0.75 | 0.144338 | 0.583333 to 0.833333 |
| selective_product_yield_mae | 0.0421456 | 0.0469875 | 0.0419806 | 0.0939331 | 3/3 | 0.0609671 | 0.028659 | 0.0419806 to 0.0939331 |
| transport_efficiency_coverage80 | 0.666667 | 0.833333 | 0.916667 | 0 | 3/3 | 0.583333 | 0.506897 | 0 to 0.916667 |
| transport_efficiency_mae | 0.21748 | 0.110777 | 0.108162 | 0.423 | 3/3 | 0.213979 | 0.181021 | 0.108162 to 0.423 |

## EQ-Sol

| Metric | Previous | R1 | R2 | R3 | n/3 | Mean | SD | Min-max |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| acid_dissociation_fraction_coverage80 | 1 | 1 | 1 | 1 | 3/3 | 1 | 0 | 1 to 1 |
| acid_dissociation_fraction_mae | 0.09057 | 0.013956 | 0.0143667 | 0.0138727 | 3/3 | 0.0140651 | 0.000264505 | 0.0138727 to 0.0143667 |
| acid_dissociation_fraction_mean_width80 | 0.267167 | 0.141583 | 0.15675 | 0.17525 | 3/3 | 0.157861 | 0.0168608 | 0.141583 to 0.17525 |
| all_twelve_coverage80 | 0.966667 | 0.972222 | 0.994444 | 0.983333 | 3/3 | 0.983333 | 0.0111111 | 0.972222 to 0.994444 |
| all_twelve_coverage_denominator | 180 | 180 | 180 | 180 | 3/3 | 180 | 0 | 180 to 180 |
| all_twelve_covered | 174 | 175 | 179 | 177 | 3/3 | 177 | 2 | 175 to 179 |
| all_twelve_macro_mae | 0.0402979 | 0.0105883 | 0.00904557 | 0.0119871 | 3/3 | 0.0105403 | 0.00147136 | 0.00904557 to 0.0119871 |
| lowest_three_coverage80 | 1 | 1 | 1 | 1 | 3/3 | 1 | 0 | 1 to 1 |
| lowest_three_coverage_denominator | 45 | 45 | 45 | 45 | 3/3 | 45 | 0 | 45 to 45 |
| lowest_three_covered | 45 | 45 | 45 | 45 | 3/3 | 45 | 0 | 45 to 45 |
| lowest_three_macro_mae | 0.120622 | 0.0133214 | 0.0145308 | 0.012877 | 3/3 | 0.0135764 | 0.000855917 | 0.012877 to 0.0145308 |
| minimum_positive_concentration_M | 0.1 | 0.0625 | 0.05 | 0.0625 | 3/3 | 0.0583333 | 0.00721688 | 0.05 to 0.0625 |
| pH_normalized_coverage80 | 1 | 1 | 1 | 0.966667 | 3/3 | 0.988889 | 0.019245 | 0.966667 to 1 |
| pH_normalized_mae | 0.0142292 | 0.00317847 | 0.0052186 | 0.00344439 | 3/3 | 0.00394715 | 0.0011091 | 0.00317847 to 0.0052186 |
| pH_normalized_mean_width80 | 0.0850833 | 0.0387083 | 0.058 | 0.03875 | 3/3 | 0.0451528 | 0.011126 | 0.0387083 to 0.058 |
| precipitation_signal_coverage80 | 0.9 | 0.916667 | 0.983333 | 0.983333 | 3/3 | 0.961111 | 0.03849 | 0.916667 to 0.983333 |
| precipitation_signal_mae | 0.0160946 | 0.0146303 | 0.00755135 | 0.0186443 | 3/3 | 0.0136086 | 0.00561659 | 0.00755135 to 0.0186443 |
| precipitation_signal_mean_width80 | 0.0891667 | 0.06125 | 0.0579167 | 0.0855 | 3/3 | 0.0682222 | 0.0150555 | 0.0579167 to 0.0855 |
| remaining_nine_coverage80 | 0.955556 | 0.962963 | 0.992593 | 0.977778 | 3/3 | 0.977778 | 0.0148148 | 0.962963 to 0.992593 |
| remaining_nine_coverage_denominator | 135 | 135 | 135 | 135 | 3/3 | 135 | 0 | 135 to 135 |
| remaining_nine_covered | 129 | 130 | 134 | 132 | 3/3 | 132 | 2 | 130 to 134 |
| remaining_nine_macro_mae | 0.0135234 | 0.0096772 | 0.00721714 | 0.0116905 | 3/3 | 0.00952828 | 0.00224039 | 0.00721714 to 0.0116905 |
| sampled_below_1mM | 0 | 0 | 0 | 0 | 3/3 | 0 | 0 | 0 to 0 |

## EQ-Astra

| Metric | Previous | R1 | R2 | R3 | n/3 | Mean | SD | Min-max |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| acid_dissociation_fraction_coverage80 | 0.633333 | 0.983333 | 1 | 0.983333 | 3/3 | 0.988889 | 0.0096225 | 0.983333 to 1 |
| acid_dissociation_fraction_mae | 0.0766053 | 0.00344075 | 0.00216889 | 0.0033486 | 3/3 | 0.00298608 | 0.000709201 | 0.00216889 to 0.00344075 |
| acid_dissociation_fraction_mean_width80 | 0.037 | 0.0441667 | 0.0575833 | 0.0466667 | 3/3 | 0.0494722 | 0.00713478 | 0.0441667 to 0.0575833 |
| all_twelve_coverage80 | 0.661111 | 0.994444 | 0.972222 | 0.955556 | 3/3 | 0.974074 | 0.0195105 | 0.955556 to 0.994444 |
| all_twelve_coverage_denominator | 180 | 180 | 180 | 180 | 3/3 | 180 | 0 | 180 to 180 |
| all_twelve_covered | 119 | 179 | 175 | 172 | 3/3 | 175.333 | 3.51188 | 172 to 179 |
| all_twelve_macro_mae | 0.0434307 | 0.0029614 | 0.00282347 | 0.00363233 | 3/3 | 0.00313907 | 0.000432708 | 0.00282347 to 0.00363233 |
| lowest_three_coverage80 | 0 | 1 | 0.911111 | 0.888889 | 3/3 | 0.933333 | 0.0587945 | 0.888889 to 1 |
| lowest_three_coverage_denominator | 45 | 45 | 45 | 45 | 3/3 | 45 | 0 | 45 to 45 |
| lowest_three_covered | 0 | 45 | 41 | 40 | 3/3 | 42 | 2.64575 | 40 to 45 |
| lowest_three_macro_mae | 0.16267 | 0.00611347 | 0.00606813 | 0.0064408 | 3/3 | 0.00620747 | 0.000203341 | 0.00606813 to 0.0064408 |
| minimum_positive_concentration_M | 0.00555556 | 1.85185e-05 | 1.85185e-05 | 1.25e-05 | 3/3 | 1.65123e-05 | 3.47479e-06 | 1.25e-05 to 1.85185e-05 |
| pH_normalized_coverage80 | 0.616667 | 1 | 0.983333 | 0.966667 | 3/3 | 0.983333 | 0.0166667 | 0.966667 to 1 |
| pH_normalized_mae | 0.0160914 | 0.00113761 | 0.00138342 | 0.00134307 | 3/3 | 0.00128803 | 0.000131826 | 0.00113761 to 0.00138342 |
| pH_normalized_mean_width80 | 0.01375 | 0.013 | 0.0171667 | 0.0155833 | 3/3 | 0.01525 | 0.00210324 | 0.013 to 0.0171667 |
| precipitation_signal_coverage80 | 0.733333 | 1 | 0.933333 | 0.916667 | 3/3 | 0.95 | 0.0440959 | 0.916667 to 1 |
| precipitation_signal_mae | 0.0375956 | 0.00430586 | 0.0049181 | 0.00620533 | 3/3 | 0.0051431 | 0.000969516 | 0.00430586 to 0.00620533 |
| precipitation_signal_mean_width80 | 0.0390833 | 0.04 | 0.044 | 0.0463333 | 3/3 | 0.0434444 | 0.00320301 | 0.04 to 0.0463333 |
| remaining_nine_coverage80 | 0.881481 | 0.992593 | 0.992593 | 0.977778 | 3/3 | 0.987654 | 0.00855334 | 0.977778 to 0.992593 |
| remaining_nine_coverage_denominator | 135 | 135 | 135 | 135 | 3/3 | 135 | 0 | 135 to 135 |
| remaining_nine_covered | 119 | 134 | 134 | 132 | 3/3 | 133.333 | 1.1547 | 132 to 134 |
| remaining_nine_macro_mae | 0.00368444 | 0.00191072 | 0.00174192 | 0.00269617 | 3/3 | 0.00211627 | 0.000509253 | 0.00174192 to 0.00269617 |
| sampled_below_1mM | 0 | 1 | 1 | 1 | 3/3 | 1 | 0 | 1 to 1 |

## C-12

| Metric | Previous | R1 | R2 | R3 | n/3 | Mean | SD | Min-max |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Q07_fines_prediction | 0.36 | 0.25 | 0.41 | 0.48 | 3/3 | 0.38 | 0.117898 | 0.25 to 0.48 |
| Q07_predicted_feasible | 1 | 1 | 1 | 1 | 3/3 | 1 | 0 | 1 to 1 |
| Q08_fines_prediction | 0.46 | 0.68 | 0.86 | 0.58 | 3/3 | 0.706667 | 0.141892 | 0.58 to 0.86 |
| Q08_predicted_feasible | 1 | 0 | 0 | 0 | 3/3 | 0 | 0 | 0 to 0 |
| crystal_fines_fraction_coverage80 | 0.333333 | 0.416667 | 0.666667 | 0.0833333 | 3/3 | 0.388889 | 0.292657 | 0.0833333 to 0.666667 |
| crystal_fines_fraction_mae | 0.331565 | 0.257945 | 0.226565 | 0.368231 | 3/3 | 0.284247 | 0.0744057 | 0.226565 to 0.368231 |
| crystal_purity_coverage80 | 0.0833333 | 0.666667 | 0.833333 | 0.0833333 | 3/3 | 0.527778 | 0.393818 | 0.0833333 to 0.833333 |
| crystal_purity_mae | 0.089449 | 0.0311156 | 0.0361156 | 0.086949 | 3/3 | 0.0513934 | 0.0308933 | 0.0311156 to 0.086949 |
| crystal_size_coverage80 | 0.916667 | 0.75 | 0.833333 | 0.833333 | 3/3 | 0.805556 | 0.0481125 | 0.75 to 0.833333 |
| crystal_size_mae | 0.0197462 | 0.0471589 | 0.0221401 | 0.0187462 | 3/3 | 0.0293484 | 0.0155174 | 0.0187462 to 0.0471589 |
| crystal_yield_coverage80 | 0.833333 | 1 | 1 | 0.916667 | 3/3 | 0.972222 | 0.0481125 | 0.916667 to 1 |
| crystal_yield_mae | 0.0791949 | 0.0414418 | 0.0581949 | 0.0397387 | 3/3 | 0.0464584 | 0.0101997 | 0.0397387 to 0.0581949 |
| quality_correct_of_12 | 7 | 8 | 10 | 7 | 3/3 | 8.33333 | 1.52753 | 7 to 10 |
| recommendation_fines_margin | 0.186467 | -0.499936 | -0.0935371 | 0.141099 | 3/3 | -0.150792 | 0.32433 | -0.499936 to 0.141099 |
| recommendation_true_crystal_fines_fraction | 0.313533 | 0.999936 | 0.593537 | 0.358901 | 3/3 | 0.650792 | 0.32433 | 0.358901 to 0.999936 |
| recommendation_true_crystal_purity | 0.988558 | 0.989628 | 0.989166 | 0.990764 | 3/3 | 0.989853 | 0.000822522 | 0.989166 to 0.990764 |
| recommendation_true_crystal_yield | 0.518086 | 0.471009 | 0.447632 | 0.509885 | 3/3 | 0.476175 | 0.0314462 | 0.447632 to 0.509885 |
| thermal_fines_absolute_delta_error | 0.638545 | 0.308545 | 0.288545 | 0.638545 | 3/3 | 0.411879 | 0.196554 | 0.288545 to 0.638545 |
| thermal_fines_direction_correct | 1 | 1 | 1 | 0 | 3/3 | 0.666667 | 0.57735 | 0 to 1 |
| thermal_fines_predicted_delta | 0.1 | 0.43 | 0.45 | 0.1 | 3/3 | 0.326667 | 0.196554 | 0.1 to 0.45 |
| thermal_fines_true_delta | 0.738545 | 0.738545 | 0.738545 | 0.738545 | 3/3 | 0.738545 | 0 | 0.738545 to 0.738545 |

## C-24

| Metric | Previous | R1 | R2 | R3 | n/3 | Mean | SD | Min-max |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Q07_fines_prediction | 0.39 | 0.47 | 0.34 | 0.34 | 3/3 | 0.383333 | 0.0750555 | 0.34 to 0.47 |
| Q07_predicted_feasible | 1 | 1 | 1 | 1 | 3/3 | 1 | 0 | 1 to 1 |
| Q08_fines_prediction | 0.69 | 0.37 | 0.53 | 0.6 | 3/3 | 0.5 | 0.117898 | 0.37 to 0.6 |
| Q08_predicted_feasible | 0 | 1 | 0 | 0 | 3/3 | 0.333333 | 0.57735 | 0 to 1 |
| crystal_fines_fraction_coverage80 | 0.5 | 0.25 | 0.416667 | 0.5 | 3/3 | 0.388889 | 0.127294 | 0.25 to 0.5 |
| crystal_fines_fraction_mae | 0.252398 | 0.321565 | 0.350731 | 0.233231 | 3/3 | 0.301842 | 0.0611824 | 0.233231 to 0.350731 |
| crystal_purity_coverage80 | 0.916667 | 1 | 1 | 1 | 3/3 | 1 | 0 | 1 to 1 |
| crystal_purity_mae | 0.039449 | 0.0124425 | 0.0210985 | 0.0164939 | 3/3 | 0.0166783 | 0.00433096 | 0.0124425 to 0.0210985 |
| crystal_size_coverage80 | 0.5 | 0.916667 | 0.25 | 0.583333 | 3/3 | 0.583333 | 0.333333 | 0.25 to 0.916667 |
| crystal_size_mae | 0.0612029 | 0.0375755 | 0.0899529 | 0.0665767 | 3/3 | 0.0647017 | 0.026239 | 0.0375755 to 0.0899529 |
| crystal_yield_coverage80 | 0.916667 | 0.75 | 0.25 | 0.25 | 3/3 | 0.416667 | 0.288675 | 0.25 to 0.75 |
| crystal_yield_mae | 0.0515063 | 0.0828487 | 0.182432 | 0.162432 | 3/3 | 0.142571 | 0.0526788 | 0.0828487 to 0.182432 |
| quality_correct_of_12 | 10 | 9 | 8 | 11 | 3/3 | 9.33333 | 1.52753 | 8 to 11 |
| recommendation_fines_margin | 0.0182891 | 0.0126486 | 0.219146 | 0.0554485 | 3/3 | 0.0957477 | 0.108988 | 0.0126486 to 0.219146 |
| recommendation_true_crystal_fines_fraction | 0.481711 | 0.487351 | 0.280854 | 0.444551 | 3/3 | 0.404252 | 0.108988 | 0.280854 to 0.487351 |
| recommendation_true_crystal_purity | 0.985541 | 0.989483 | 0.989828 | 0.984381 | 3/3 | 0.987897 | 0.00305041 | 0.984381 to 0.989828 |
| recommendation_true_crystal_yield | 0.557549 | 0.451154 | 0.648357 | 0.561044 | 3/3 | 0.553518 | 0.0988169 | 0.451154 to 0.648357 |
| thermal_fines_absolute_delta_error | 0.438545 | 0.838545 | 0.548545 | 0.478545 | 3/3 | 0.621879 | 0.190875 | 0.478545 to 0.838545 |
| thermal_fines_direction_correct | 1 | 0 | 1 | 1 | 3/3 | 0.666667 | 0.57735 | 0 to 1 |
| thermal_fines_predicted_delta | 0.3 | -0.1 | 0.19 | 0.26 | 3/3 | 0.116667 | 0.190875 | -0.1 to 0.26 |
| thermal_fines_true_delta | 0.738545 | 0.738545 | 0.738545 | 0.738545 | 3/3 | 0.738545 | 0 | 0.738545 to 0.738545 |

## Direction recurrence

Round labels organize comparisons; they do not pair provider sampling randomness.

| Comparison | Metric | Test | Holds / planned | Observed / planned |
| --- | --- | --- | ---: | ---: |
| EC-optimization vs EC-discovery | recommendation_score | second > first | 3/3 | 3/3 |
| EC-optimization vs EC-discovery | score_mae | second < first | 2/3 | 3/3 |
| C-24 vs C-12 | quality_correct_of_12 | second > first | 2/3 | 3/3 |
| C-24 vs C-12 | crystal_yield_mae | second < first | 0/3 | 3/3 |
| C-24 vs C-12 | crystal_purity_mae | second < first | 3/3 | 3/3 |
| C-24 vs C-12 | crystal_size_mae | second < first | 1/3 | 3/3 |
| C-24 vs C-12 | crystal_fines_fraction_mae | second < first | 1/3 | 3/3 |

## Accounting and retained failures

```json
{
  "terminal_sources": 18,
  "completed_sources": 17,
  "completed_batches": 252,
  "completed_posttests": 58,
  "source_operations": 3019,
  "source_rollbacks": 486,
  "laboratory_tool_failures": 1,
  "notebook_tool_failures": 7,
  "source_provider_process_attempts": 18,
  "recommendation_retest_batches": 12,
  "recommendation_retest_operations": 149,
  "recommendation_retests_replayed": 12,
  "source_replays_verified": 18,
  "notebook_versions": 65,
  "notebook_read_calls": 0,
  "token_accounting_complete_cases": 17,
  "observed_input_plus_output_tokens": 19205936
}
```

- repeat-01/EQ-Astra/K2: provider_failure
- repeat-01/EQ-Astra/EQS: not executed/recorded

Full errors, notebook citation checks, resource accounts and unchanged model text are retained in each repeat's exports. Missing values are not zeros. No significance test, population stability threshold or causal notebook effect is claimed.
