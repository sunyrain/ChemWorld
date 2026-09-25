# Appendix H. Executed process models and information conditions

## H.1 Equilibrium response model

The parameter-prior study uses a bounded monoprotic acid-base model followed by a precipitation calculation. These are the process relations used for the retained campaigns and references. They are distinct from explanations proposed by the agents. In particular, an agent's proposed active-pool cap is not the implemented source of the dissociation plateau.

Let $n$ be the current ledger amount of the initial reactant, $V$ the current sample volume and $C=n/V$. The background-ion amounts are $n_+=\min(0.020,0.15n)$ and $n_-=\min(0.020,0.08n)$, in moles. With $H=[\mathrm{H}^+]$, $K_a=10^{-\mathrm{p}K_a}$ and activity-ratio factor $g$, the solver obtains

$$[\mathrm{A}^-]=\frac{CK_a}{K_a+gH},\qquad [\mathrm{OH}^-]=\frac{K_w(T)}{H},$$

subject to charge balance,

$$H+\frac{n_+}{V}-\frac{K_w(T)}{H}-[\mathrm{A}^-]-\frac{n_-}{V}=0.$$

The reported responses are $\mathrm{pH}/14=-\log_{10}(H)/14$ and dissociation fraction $\alpha=[\mathrm{A}^-]/C$, clipped to the public unit interval. In the uncapped background-ion range, charge balance implies $\alpha=0.07+H/C-K_w/(HC)$. At sufficiently high concentration the last two terms are small, giving a local plateau near 7%; dilution makes their contribution appreciable. The plateau and departure therefore arise under the same fixed equations. The five effective pKa values span 4.6594 to 5.3794 in increments of 0.18; the default activity-ratio factor is one.

Precipitation is calculated sequentially from effective ion inventories $a=n_++0.10n_{\mathrm{A}^-}$ and $b=n_-+0.08n_{\mathrm{HA}}$. When supersaturated, a 1:1 removal $x$, bounded by the limiting inventory, satisfies $(a-x)(b-x)/V^2=K_{sp}$, with default $K_{sp}=1.8\times10^{-10}$. The public signal is $x/n$, clipped to $[0,1]$. This hook does not feed precipitation back into the acid-base solution. Thus the three public responses are related but should not be interpreted as three independent measurements of one failure mechanism.

The concentration in Figure 5 is a recipe descriptor: total nominal reagent additions divided by total solvent additions. The solver instead uses the ledger state at measurement, after any sample consumption and other operations. The scatterplot combines distinct recipes and histories; it is not a controlled one-dimensional titration curve. The three most dilute test recipes have nominal concentrations of approximately $1.33\times10^{-4}$, $1.33\times10^{-5}$ and $1.67\times10^{-4}$ M. No source assay in these fifteen campaigns reaches those concentrations.

## H.2 A concrete three-arm information example

Table H1 reproduces the numerical content of the first equilibrium world's public prior from the frozen configuration and input serializer. It is a formatted input excerpt, not a reconstruction of agent dialogue. All three arms retain the same public operations, general task background, resource contract and physical world. Opaque receives no instance-specific initial world model. The other two arms receive the same schema and wording; MisIndexed substitutes the configured fifth world's claim.

**Table H1. Public prior content in one matched physical world.**

| Supplied field | Opaque | Aligned | MisIndexed |
| :--- | :--- | :--- | :--- |
| Effective pKa interval (80%) | Absent | [4.6094, 4.7094] | [5.3294, 5.4294] |
| Dilution change in pH/14 | Absent | +0.003494987 | +0.000875889 |
| Dilution change in dissociation | Absent | +0.008187416 | +0.001884676 |
| Nominal confidence | Absent | 0.8 | 0.8 |

The common dilution anchor is 0.001 mol acid at 298.15 K, with volume increasing from 0.018 to 0.054 L. Both supplied records identify the source as an “independent bounded archival fit” and qualify the claim as a “local effective relationship; not a universal aqueous-chemistry law”. The pKa intervals above are rounded for display; the input contains their full precision. Aligned therefore supplies correct partial local information, not the evaluator's complete process equations, query answers or an instruction to enter the most dilute test region. The experiment contrasts the resulting complete research processes, including possible changes to evidence acquisition and interpretation.

\clearpage

## H.3 Crystallization response model

The retained crystallization block composes upstream reaction, thermal operations, seeding, crystal nucleation and growth, filtration and measurement. It uses the latent-material process family and its linear supersaturation-dependent impurity transfer. Solid product, solid impurity and the particle population persist across operations; dissolved and solid inventories are accounted for separately.

The temperature-dependent solubility follows

$$c^*(T)=c^*_{\mathrm{ref}}\exp\!\left[-\frac{\Delta H}{R}\left(\frac{1}{T}-\frac{1}{T_{\mathrm{ref}}}\right)\right],$$

with $T_{\mathrm{ref}}=298.15$ K, $\Delta H=20{,}000$ J mol$^{-1}$ and a declared temperature domain of 250-430 K. World and solvent properties scale the reference solubility and kinetics. For relative supersaturation $s=\max(C/c^*-1,0)$, primary nucleation scales as $B=k_b s^2$ and linear growth as $G=k_g s$. Before world and solvent multipliers, the coefficients are $2\times10^7$ L$^{-1}$ s$^{-1}$ for nucleation and $2\times10^{-8}$ m s$^{-1}$ for growth. Nucleation and growth consume available dissolved target and update the population distribution; they are not independent score adjustments.

Each crystallized target increment transfers impurity according to

$$\Delta n_{I,s}=\min\!\left(n_{I,l},\;\Delta n_{P,s}\,k_{\mathrm{occ}}(1+0.5s)\right),$$

where $k_{\mathrm{occ}}=0.02$ times the solvent's occlusion multiplier. The four nominal solvent multipliers are 1.20, 0.80, 0.65 and 1.05; world-fixed material residuals further modulate these properties. Filtration retains 96% of target solids and 92% of impurity solids. The final-assay purity is the solid-target mole fraction $n_{P,s}/(n_{P,s}+n_{I,s})$. Seed contributes to target purity but is subtracted in the full-process recovery numerator; final-assay recovery is normalized by the initial reagent charge.

These relations allow thermal and seeding histories to alter the amount and size distribution of crystals while impurity incorporation remains modest. They explain how recovery and particle responses can vary without requiring a comparable purity change. The approximately 98.5% purity level is an empirical property of the retained source and query conditions, not a hard-coded value or a universal invariant of the model. The present analysis does not isolate individual process contributions to that stability. Appendix G separately tests whether the forecasts preserve the level and variation of the retained purity references.

## H.4 Scope of this reconstruction

The equations and input excerpt were checked against the execution-version source and retained configuration bindings. Later equilibrium adapters and alternative crystallization impurity laws are not used to explain these observations. This documentation and the error decompositions use existing source records, predictions and references only; they add no agent or simulator calls. Internal source identities are retained with the analysis records for the archival package.
