# Appendix G. Response contributions and purity-error diagnosis

## G.1 Equilibrium reversal by response

This exploratory decomposition retains all fifteen parameter-prior campaigns and all 540 response predictions. It uses the existing three-lowest-concentration grouping. MAE first averages queries within a campaign and response, then the five worlds. Averaging the three response MAEs exactly recovers Table 1. The same worlds recur across arms; queries and responses are not independent replicates.

**Table G1. Original prediction MAE by response and concentration group.**

| Response | Group | Opaque | Aligned | MisIndexed | Lower / higher |
| :--- | :--- | ---: | ---: | ---: | :--- |
| pH / 14 | Other nine | 0.00261 | 0.00269 | 0.00254 | 2 / 3 of 5 |
| pH / 14 | Dilute three | 0.00448 | 0.05576 | 0.05230 | 0 / 5 of 5 |
| Dissociation fraction | Other nine | 0.00839 | 0.00709 | 0.00660 | 3 / 2 of 5 |
| Dissociation fraction | Dilute three | 0.02640 | 0.28229 | 0.23861 | 0 / 5 of 5 |
| Precipitation signal | Other nine | 0.01923 | 0.00417 | 0.00403 | 5 / 0 of 5 |
| Precipitation signal | Dilute three | 0.02411 | 0.13783 | 0.14099 | 0 / 5 of 5 |

The final column counts worlds with lower/higher Aligned MAE than Opaque. Signed response differences divided by three sum to the macro-error difference. They quantify the contribution on the declared normalized scales; they do not establish a shared failure mechanism or physical comparability of targets.

\clearpage

## G.2 Separating purity offset from variation error

For each of thirty campaigns, let $p_i$ and $y_i$ be its original prediction and retained noiseless reference for the twelve queries. Define $b=\overline{p-y}$ and $c_i=(p_i-\bar p)-(y_i-\bar y)$. Then

$$\operatorname{MSE}=b^2+\frac{1}{12}\sum_{i=1}^{12}c_i^2.$$

The first term measures the common offset; the second measures mismatched variation across conditions. Centred RMSE is the square root of the second term. Reference and prediction standard deviations use denominator twelve. All calculations retain the source-assay shortfall. Demeaning uses withheld references only for diagnosis; it is not an available predictor or a corrected performance result. MAE has no analogous additive decomposition.

**Table G2. Purity offset and variation diagnostics.**

| Batches | Arm | N | Bias | cRMSE | Ref. SD | Pred. SD | Offset share |
| ---: | :--- | ---: | ---: | ---: | ---: | ---: | ---: |
| Both | All | 30 | -4.289 | 1.889 | 0.598 | 1.968 | 87.6% |
| 12 | Opaque | 5 | -0.806 | 0.970 | 0.598 | 1.031 | 45.3% |
| 12 | Aligned | 5 | -4.920 | 1.837 | 0.598 | 1.791 | 89.8% |
| 12 | MisIndexed | 5 | -9.166 | 2.843 | 0.598 | 2.977 | 91.3% |
| 24 | Opaque | 5 | -1.816 | 1.682 | 0.598 | 1.649 | 57.4% |
| 24 | Aligned | 5 | -3.948 | 1.797 | 0.598 | 1.983 | 85.6% |
| 24 | MisIndexed | 5 | -5.080 | 2.206 | 0.598 | 2.376 | 85.3% |

N is the campaign count; cRMSE denotes centred RMSE. Bias, cRMSE and both standard deviations are campaign means in percentage points. Offset share is the ratio of summed squared campaign biases to summed campaign MSEs, with equal query counts; it is not the mean campaign fraction. The median campaign fraction is 77.6%. Mean bias is negative in 30 of 30 campaigns. Centred RMSE exceeds reference SD in 29 of 30. These comparisons describe forecast outputs and do not identify an internal revision process. No new agent or simulator calls were made.
