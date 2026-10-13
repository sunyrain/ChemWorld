# EC-discovery — sealed model reports

Model-authored answers in their original sequence. These were written after the source campaign, separately from its contemporary notebook. No reference answers were supplied during these stages.

## K1

Mechanistic account

1. Experimental scope

All 12 batches used the same charge: 0.020 mol limiting reagent in 0.040 L solvent. Thus reagent loading and concentration were not varied. Potential, current cap, electrolysis duration, solvent label, and electrolyte label were varied. All material labels are anonymous benchmark identities, so the conclusions concern S0–S3 and E0–E3 only and should not be mapped onto real chemicals.

The strongest interpretation is that target formation is a cathodic, negative-potential process with competing loss pathways. Potential controls which electrochemical branch is active; time controls accumulated conversion; the current cap trades throughput against faradaic and transport efficiency; and solvent/electrolyte alter transport, acid/base state, and precipitation.

2. Polarity and potential dependence

The clearest causal result is the matched polarity comparison. Batch 1 used S0/E0, +1.5 V, 100 mA, and 600 s. Its final assay gave conversion 0.0080, selectivity 0.0103, faradaic efficiency 0.0245, transport efficiency 0, energy efficiency 0.0053, and zero reported selective-product yield. Batch 2 changed only the potential to -1.5 V. It gave selectivity 0.5601, faradaic efficiency 0.3136, transport efficiency 0.3398, energy efficiency 0.1074, and yield 0.0117. The large polarity-dependent efficiency and selectivity differences greatly exceed the stated instrumental uncertainties. I therefore infer that the target-producing electron-transfer branch is enabled by negative polarization, while positive polarization predominantly leaves reagent unproductively transformed or inactive.

Potential magnitude is nonmonotonic. At -0.8 V and 600 s, batch 3 gave especially favorable efficiencies—faradaic 0.4022, transport 0.4188, and energy 0.3568—but conversion 0.0011 and yield at the reporting floor. At -2.2 V, batch 4 gave lower selectivity (0.4412), faradaic efficiency (0.2572), transport efficiency (0.2257), energy efficiency (0.0120), and yield 0.0025. Thus stronger negative polarization is not uniformly beneficial. A plausible explanation is an activation window followed by parasitic reduction, polarization loss, or transport limitation at excessive magnitude. The data locate a favorable efficiency region somewhere between roughly -0.8 and -1.5 V, but do not locate the long-duration yield optimum because the potential sweep was performed only at 600 s.

3. Time and accumulated product

At S0/E0, -1.5 V, and a 100 mA cap, batch 5 ran for 60 s and gave conversion 0.0039 and yield 0.0087. Batch 2 ran for 600 s and gave yield 0.0117. Batch 6 ran for 2400 s and gave conversion 0.0217 and yield 0.0211. Its selectivity (0.5543), faradaic efficiency (0.3378), and transport efficiency (0.3131) were similar to those of batch 2. The numerical trend supports accumulation of target with time while the instantaneous branching efficiencies remain approximately stable.

Because the conversion and yield signals are near their approximately 0.01 assay-noise scales and there were no replicates, I would not infer a precise rate constant. A useful provisional process equation is

  dR/dt = -k_total(V,I,S,E) R,
  dP/dt = s(V,I,S,E) k_total R - k_loss P,

or, before appreciable depletion,

  X(t) approximately 1 - exp[-k_total t],
  Y_P(t) approximately s X(t),

with the important warning that the independently calibrated reported conversion, selectivity, and yield channels do not obey this identity exactly near their detection floor. For example, batch 2 reported zero conversion but nonzero yield. That is better interpreted as clipping and independent measurement noise than as literal negative mass balance.

Extrapolation: at the same moderate negative potential and current cap, extending time beyond 2400 s should initially increase conversion and product, followed eventually by a plateau or degradation regime. That plateau was not observed and its location is unknown.

4. Current-cap tradeoff

Batches 7, 6, and 8 compared 10, 100, and 400 mA caps, respectively, at S0/E0, -1.5 V, and 2400 s. Their measured conversions were 0.0123, 0.0217, and 0.0443, suggesting greater gross consumption with increasing current allowance. However, the 400 mA condition reduced faradaic efficiency to 0.2062, transport efficiency to 0.1997, ohmic efficiency to 0.9599, and energy efficiency to 0.0728. The 100 mA values were 0.3378, 0.3131, 0.9857, and 0.1154. Selective-product yield was nonmonotonic: 0.0084 at 10 mA, 0.0211 at 100 mA, and 0.0067 at 400 mA.

I therefore distinguish gross reaction rate from productive rate. A possible representation is

  r_total proportional to I_effective,
  s or FE approximately s0(V,S,E) / [1 + alpha(V,S,E) I_effective^n],
  r_product = r_total × s × FE_transport,

where the commanded current is only a cap; actual current and charge were not measured publicly. Moderate current can maximize productive output even if a high cap maximizes reagent consumption. The yield differences are not individually decisive given assay uncertainty, but the coherent fall across several independent efficiency channels supports a real high-current loss regime.

5. Solvent and electrolyte coupling

Batch 9 changed only S0 to S1 relative to batch 6, retaining E0, -1.5 V, 100 mA, and 2400 s. It gave yield 0.0265, selectivity 0.5351, energy efficiency 0.1594, faradaic efficiency 0.2659, and transport efficiency 0.2868. The apparent yield increase over batch 6 is smaller than the combined yield uncertainty and should not be called established. The lower faradaic efficiency and higher energy efficiency, however, indicate that solvent can alter different loss terms rather than simply scaling every metric together.

Batch 10 changed only electrolyte E0 to E1 in S0. Its pH-normalized signal shifted from 0.2312 in batch 6 to 0.1978, and precipitation fell from 0.9975 to 0.8540. These changes are far larger than the respective assay uncertainties. Conversion was 0.0340, selectivity 0.5638, and yield 0.0077. I infer that electrolyte strongly controls acid/base or ionic speciation and phase behavior, while its direct effect on target selectivity is smaller in this comparison.

Batch 11 used S2/E2 jointly. It had pH-normalized 0.1669, precipitation 0.0052, selectivity 0.4058, faradaic efficiency 0.2274, and transport efficiency 0.2345. Batch 12 used S3/E3 jointly and had pH-normalized 0.2848, zero reported precipitation, selectivity 0.4782, faradaic efficiency 0.1944, and transport efficiency 0.2156. These large phase and pH changes establish material dependence, but solvent and electrolyte contributions are inseparable in batches 11 and 12. It is plausible that precipitation removes a species from solution or reports a change in ionic environment, but the data do not identify whether the precipitate is reagent, target, byproduct, or spectator material. The fact that batch 12 retained yield 0.0181 with zero precipitation shows that precipitation is not simply identical to target formation.

A compact coupled model would therefore use material-dependent terms:

  k_total = k0(S,E) f(V) g(I),
  selectivity = s0(S,E) q(V) h(I),
  transport efficiency = T(S,E,I),
  ohmic efficiency = O(S,E,I),
  pH and precipitation = equilibrium_state(S,E,extent),
  productive rate proportional to k_total × selectivity × FE × T.

This is a conceptual factorization, not a fitted law. Interactions are expected: conductivity changes the realized polarization and current, while pH or precipitation may alter reactant availability and electrode interfaces.

6. How the explanation changed during the campaign

Batches 1–2 established that potential sign, rather than time alone, switches the productive branch. Batches 3–4 replaced a simple 'more negative is better' idea with a bounded operating-window hypothesis. Batches 5–6 supported time-dependent accumulation without a large change in selectivity. Batches 7–8 then showed that greater current allowance can increase gross conversion while degrading efficiencies and selective yield, motivating the parallel productive/parasitic pathway model. Batches 9–12 showed that materials affect different observables independently and introduced acid/base and phase-equilibrium coupling into the account.

The observed balanced scores are consistent with this interpretation: batch 6 scored 0.2596, batch 9 scored 0.2542, whereas the high-current batch 8 scored 0.0740 and the positive-potential batch 1 scored 0. Batch 6 was therefore the sealed recommendation, although score was treated as a secondary aggregate observation rather than mechanistic proof.

7. Scope and unresolved alternatives

The study has no true zero-electrolysis control, no replicated batches, no actual current-time traces, and no direct charge measurement. Concentration, reagent amount, and solvent volume were fixed. Potential and duration were not crossed fully: magnitude was tested at 600 s, whereas the principal duration/current comparisons used -1.5 V. Consequently, a potential-by-time interaction remains unresolved.

S2/E2 and S3/E3 are confounded pairs. Even the apparently clean S1 and E1 comparisons were performed once, so smaller differences may be noise. The anonymous identities prevent molecular assignments. The public signals do not determine electron stoichiometry, electrode kinetics, whether conversion represents target plus byproducts, or the composition of the precipitate.

A plausible alternative to a distinct parasitic high-current chemistry is purely physical polarization or mass-transfer limitation: the same chemistry could operate, but reactant supply to the electrode and ohmic losses worsen at high current. Another alternative is that the potential dependence reflects a threshold in actual electrode potential caused by medium resistance rather than an intrinsic molecular redox window. Material-associated pH and precipitation could be spectator equilibria rather than causal controls on selectivity. The current data cannot distinguish these alternatives.

Overall, the most defensible predictive account is qualitative: use negative rather than positive potential; expect an intermediate potential window; expect product to accumulate with duration; avoid assuming that maximal current maximizes target yield; and treat solvent/electrolyte as coupled controls of transport, pH, precipitation, and efficiency. Quantitative predictions outside the tested loading, 60–2400 s duration range, -2.2 to +1.5 V range, or tested material combinations should carry substantial uncertainty.

## Q

| Query | Metric | Estimate | Lower 80% | Upper 80% |
| --- | --- | ---: | ---: | ---: |
| Q01 | electrochemical_selectivity | 0.63 | 0.58 | 0.68 |
| Q01 | energy_efficiency | 0.357 | 0.29 | 0.43 |
| Q01 | faradaic_efficiency | 0.402 | 0.35 | 0.46 |
| Q01 | score | 0.063 | 0 | 0.2 |
| Q01 | selective_product_yield | 0.004 | 0 | 0.018 |
| Q01 | transport_efficiency | 0.419 | 0.35 | 0.49 |
| Q02 | electrochemical_selectivity | 0.015 | 0 | 0.06 |
| Q02 | energy_efficiency | 0.005 | 0 | 0.04 |
| Q02 | faradaic_efficiency | 0.015 | 0 | 0.07 |
| Q02 | score | 0.005 | 0 | 0.06 |
| Q02 | selective_product_yield | 0.002 | 0 | 0.015 |
| Q02 | transport_efficiency | 0.005 | 0 | 0.06 |
| Q03 | electrochemical_selectivity | 0.62 | 0.55 | 0.69 |
| Q03 | energy_efficiency | 0.34 | 0.25 | 0.43 |
| Q03 | faradaic_efficiency | 0.4 | 0.32 | 0.48 |
| Q03 | score | 0.327 | 0.2 | 0.43 |
| Q03 | selective_product_yield | 0.035 | 0.008 | 0.078 |
| Q03 | transport_efficiency | 0.41 | 0.31 | 0.5 |
| Q04 | electrochemical_selectivity | 0.02 | 0 | 0.08 |
| Q04 | energy_efficiency | 0.006 | 0 | 0.05 |
| Q04 | faradaic_efficiency | 0.015 | 0 | 0.08 |
| Q04 | score | 0.013 | 0 | 0.08 |
| Q04 | selective_product_yield | 0.003 | 0 | 0.018 |
| Q04 | transport_efficiency | 0.006 | 0 | 0.07 |
| Q05 | electrochemical_selectivity | 0.63 | 0.53 | 0.71 |
| Q05 | energy_efficiency | 0.39 | 0.27 | 0.5 |
| Q05 | faradaic_efficiency | 0.37 | 0.27 | 0.47 |
| Q05 | score | 0.328 | 0.18 | 0.45 |
| Q05 | selective_product_yield | 0.028 | 0.003 | 0.072 |
| Q05 | transport_efficiency | 0.4 | 0.28 | 0.51 |
| Q06 | electrochemical_selectivity | 0.02 | 0 | 0.09 |
| Q06 | energy_efficiency | 0.008 | 0 | 0.06 |
| Q06 | faradaic_efficiency | 0.014 | 0 | 0.08 |
| Q06 | score | 0.013 | 0 | 0.09 |
| Q06 | selective_product_yield | 0.003 | 0 | 0.02 |
| Q06 | transport_efficiency | 0.006 | 0 | 0.07 |
| Q07 | electrochemical_selectivity | 0.53 | 0.36 | 0.66 |
| Q07 | energy_efficiency | 0.36 | 0.2 | 0.5 |
| Q07 | faradaic_efficiency | 0.24 | 0.11 | 0.39 |
| Q07 | score | 0.28 | 0.12 | 0.42 |
| Q07 | selective_product_yield | 0.025 | 0 | 0.075 |
| Q07 | transport_efficiency | 0.29 | 0.14 | 0.44 |
| Q08 | electrochemical_selectivity | 0.018 | 0 | 0.09 |
| Q08 | energy_efficiency | 0.006 | 0 | 0.06 |
| Q08 | faradaic_efficiency | 0.01 | 0 | 0.07 |
| Q08 | score | 0.009 | 0 | 0.08 |
| Q08 | selective_product_yield | 0.002 | 0 | 0.02 |
| Q08 | transport_efficiency | 0.005 | 0 | 0.07 |
| Q09 | electrochemical_selectivity | 0.56 | 0.39 | 0.68 |
| Q09 | energy_efficiency | 0.37 | 0.21 | 0.51 |
| Q09 | faradaic_efficiency | 0.32 | 0.18 | 0.45 |
| Q09 | score | 0.303 | 0.14 | 0.44 |
| Q09 | selective_product_yield | 0.028 | 0.001 | 0.078 |
| Q09 | transport_efficiency | 0.35 | 0.2 | 0.48 |
| Q10 | electrochemical_selectivity | 0.018 | 0 | 0.09 |
| Q10 | energy_efficiency | 0.006 | 0 | 0.06 |
| Q10 | faradaic_efficiency | 0.012 | 0 | 0.08 |
| Q10 | score | 0.009 | 0 | 0.09 |
| Q10 | selective_product_yield | 0.002 | 0 | 0.02 |
| Q10 | transport_efficiency | 0.006 | 0 | 0.08 |
| Q11 | electrochemical_selectivity | 0.6 | 0.47 | 0.7 |
| Q11 | energy_efficiency | 0.22 | 0.1 | 0.34 |
| Q11 | faradaic_efficiency | 0.25 | 0.12 | 0.38 |
| Q11 | score | 0.273 | 0.13 | 0.4 |
| Q11 | selective_product_yield | 0.025 | 0.002 | 0.072 |
| Q11 | transport_efficiency | 0.26 | 0.12 | 0.4 |
| Q12 | electrochemical_selectivity | 0.012 | 0 | 0.08 |
| Q12 | energy_efficiency | 0.003 | 0 | 0.05 |
| Q12 | faradaic_efficiency | 0.008 | 0 | 0.07 |
| Q12 | score | 0.012 | 0 | 0.1 |
| Q12 | selective_product_yield | 0.002 | 0 | 0.02 |
| Q12 | transport_efficiency | 0.003 | 0 | 0.07 |

Displayed values use six significant digits; the JSON record retains the original numeric values and particle/quality decisions.

Predictions anchor the 600 s S0/E0 cases to the matched campaign potential sweep, then extrapolate duration using the observed rise in product with time. Negative polarization is assigned high selectivity and efficiency, whereas positive polarization remains largely unproductive. E1, E3, S2, and 500 mA adjustments use the observed material and high-current efficiency shifts. Intervals widen substantially for 7200 s and for unseparated material effects because these require extrapolation beyond the campaign and some solvent/electrolyte effects were confounded. Score estimates apply the published weighted components and selective-yield gate, with allowance for unreported conversion and ohmic-efficiency uncertainty.

## K2

1. Claims and judgment changes

No instance-specific mechanistic prior or supplied law was provided. The only supplied information described anonymous materials, permitted operations, measurements, and scoring. The hypotheses and equations assessed below were therefore self-developed.

• Polarity law—negative polarization activates the productive pathway: strongly supported within S0/E0. Batch 1 (+1.5 V, 600 s) had selectivity 0.010, faradaic efficiency 0.025, zero transport efficiency, and zero selective yield. Changing only the sign in batch 2 (-1.5 V) raised these to 0.560, 0.314, 0.340, and 0.0117. This was the clearest evidence and changed polarity from an open possibility into the most secure part of the explanation.

• “More negative potential is better”: contradicted. Batch 4 at -2.2 V had lower selectivity and efficiencies than batch 2 at -1.5 V. Batch 3 at -0.8 V had the best efficiency channels but unresolved product. These results replaced a monotonic-potential picture with an intermediate operating-window hypothesis. The location of the long-duration yield optimum remains untested because the potential sweep used only 600 s.

• Time-dependent accumulation: provisionally supported. At otherwise matched -1.5 V/100 mA/S0/E0 conditions, batches 5, 2, and 6 ran for 60, 600, and 2400 s. Selective yield increased numerically from 0.0087 to 0.0117 to 0.0211, while selectivity remained near 0.55. Batch 6 particularly strengthened the interpretation that product accumulates without a large change in branching efficiency. A precise kinetic law, saturation point, and degradation term were untested because the values were near measurement uncertainty and there were no replicates or longer runs.

• “Higher current gives more target”: contradicted as a simple law. Across batches 7, 6, and 8 at 10, 100, and 400 mA, gross conversion rose numerically, but 400 mA substantially reduced faradaic, transport, ohmic, and energy efficiencies; selective yield also fell from 0.0211 at 100 mA to 0.0067 at 400 mA. This evidence changed the explanation to a throughput-versus-loss tradeoff. Whether the loss is chemical side reaction, mass-transfer polarization, or both remains unresolved.

• Material-dependent transport and equilibrium: supported qualitatively. Changing only S0 to S1 in batch 9 altered the efficiency pattern relative to batch 6. Changing only E0 to E1 in batch 10 caused large pH-normalized and precipitation shifts. Batches 11 and 12 further showed large material-associated changes in precipitation, pH, selectivity, and efficiency. However, independent S2, S3, E2, and E3 effects and specific solvent–electrolyte interactions were untested because batches 11 and 12 changed both labels simultaneously.

• The provisional factorized law—rate and efficiency as functions of potential, current, solvent, and electrolyte—was useful descriptively but was not identified quantitatively. Electron stoichiometry, actual current, charge passed, rate constants, precipitate identity, and whether pH/precipitation are causal or spectator variables all remain untested.

2. One additional discriminating experiment

I would run one S0/E0 batch at the established loading, -0.8 V, 100 mA, and 7200 s, with a final assay. This crosses the high-efficiency potential from batch 3 with a duration well beyond the time series used in batches 5, 2, and 6.

The leading explanation predicts that -0.8 V activates the same productive negative-potential branch but at a lower accumulation rate; a long run should therefore produce clearly resolved target while retaining relatively high faradaic, transport, and energy efficiencies. If selective yield became clearly positive—roughly above the assay-floor region—and the strong efficiency pattern persisted, I would strengthen the common-pathway/time-accumulation account.

An important alternative is that -0.8 V lies below the target-forming activation threshold and that batch 3’s favorable efficiency proxies do not represent accumulated target formation. If the 7200 s result still had near-zero yield and conversion, I would favor this threshold or proxy-mismatch explanation and narrow the productive potential window toward -1.5 V. If product accumulated but the efficiency channels collapsed or precipitation changed strongly, I would instead add a time-dependent process such as electrode passivation, product degradation, or phase evolution. A single batch would not supply replication, but it would resolve the largest potential-by-time gap in the campaign.

3. Unused evidence, reliability, and goal effects

The raw final-assay spectra and most detailed characterization artifacts were not modeled; interpretation used processed estimates. Intermediate UV–visible measurements were inspected but not incorporated systematically into a fitted time-course model. Spectral peak shapes, mass-balance details, cost, and most safety-risk trajectories were also unused. pH and precipitation were used qualitatively, not through a quantitative equilibrium model. No replicate-based variance estimate was available.

The least reliable predictions are the 7200 s extrapolations, especially for selective yield; the isolated effects assigned to E3 and S2, because campaign batches 11 and 12 confounded solvent with electrolyte; and all positive-potential/high-current combinations, which were far from directly matched evidence. Predicted scores are additionally uncertain because score depends on conversion, ohmic efficiency, and a selective-yield gate, while not all of those quantities were requested as prediction outputs. Near-zero yield makes the gate highly sensitive to assay noise and clipping.

The recommendation of batch 6 is also less secure than its rank suggests. Its score of 0.2596 was only slightly above batch 9’s 0.2542, neither was replicated, and no condition combined the favorable -0.8 V efficiency with a long duration. Batch 6 is defensible as the best observed balanced result, not as a proven global optimum.

The assigned explanatory goal materially affected evidence collection. I prioritized broad contrasts in sign, potential magnitude, duration, current, solvent, and electrolyte rather than repeating the current leader or performing a dense local optimization. That improved mechanistic coverage but sacrificed replication and a full material factorial. There was no clear conflict between the explanatory goal and the final recommendation, although a purely score-maximizing campaign would likely have spent more batches refining batches 6 and 9 rather than screening distant or deliberately poor conditions.
