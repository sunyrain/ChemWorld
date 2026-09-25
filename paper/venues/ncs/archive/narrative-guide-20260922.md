# ChemWorld — NCS Narrative & Paper Structure README

> Archived editorial snapshot. For the current manuscript and figure order, use
> [the NCS entry](../README.md). Relative links below reflect its former location.

2026-09-22 ???????????????????? EQ/P ????????? [Article](article.md)?Methods ??????? C.4?? 4 ?????????????? 5 ?? C ????????????????? PDF ? 23 ??????????? 2,214 ???? 143 ???????

?????????????????????????????????????????????????????/????????????????????????????????????????????EQ ?????????? Aligned ?????????? Opaque ?????? MisIndexed ???K1????? Q ? K2 ???????????????????????????????????????????????????????????

> 本 README 用于统一 ChemWorld 当前论文的主故事、章节逻辑、Figure 组织与写作边界。
> 核心目标不是按体系罗列结果，而是围绕一个单一科学问题组织全部实验。

---

## 1. Core Scientific Question

ChemWorld 不是在回答：

- LLM agent 在六类化学任务中表现怎么样？
- prior / budget / optimization 分别有什么影响？

而是回答：

> **Can an autonomous scientist determine which experimentally learned relationships remain valid under new interventions?**

即：

> **自主科学家能否判断：从已有实验中学到的规律，在新的干预条件下什么时候应该保持，什么时候应该修改？**

这个问题应该贯穿：

**Title → Abstract → Introduction → Results → Discussion**

---

## 2. Central Story

整篇文章的主线应当是：

**Successful operation does not imply scientific generalization**

↓

**More evidence can help, but does not solve every failure**

↓

**Correct prior information can help, but its value depends on the regime**

↓

**The deeper challenge is judging the applicability of learned relationships**

↓

**Two complementary failures emerge**

- **EQ:** the relationship should change, but the agent preserves it.
- **Crystallization:** the relationship remains stable, but the agent revises it.

↓

> **Scientific generalization requires learning not only empirical relationships, but their domains of validity.**

---

## 3. Recommended Title Direction

### Current preferred title

**Controlled chemical worlds reveal limits of generalization in autonomous scientific research**

This framing combines:

- experimental instrument
- scientific question
- scientific finding

### Stronger conceptual alternative

**Controlled chemical worlds reveal failures to preserve and revise empirical relationships in autonomous science**

Use this stronger title only if the preserve/revise analysis is made sufficiently systematic.

---

## 4. Abstract Logic

The abstract should follow five steps.

### 4.1 Scientific problem

Autonomous science should do more than find a productive recipe. It should learn relationships that remain useful under new interventions.

### 4.2 Why this is difficult to evaluate

In physical laboratories:

- mechanisms are often unknown;
- agents select their own evidence;
- matched counterfactual worlds are difficult to reproduce;
- prior information changes experimental acquisition.

### 4.3 What ChemWorld enables

ChemWorld separates and controls:

- private physical laws;
- public observations;
- supplied information;
- persistent experimental state.

It separately evaluates:

- operational achievement;
- withheld-condition prediction;
- uncertainty.

### 4.4 Main results

First establish the broad result:

> **Operational success and predictive knowledge diverge.**

Then highlight the two deepest complementary findings:

- **EQ:** a plateau is preserved beyond its applicable regime;
- **Crystallization:** stable purity is unnecessarily revised.

### 4.5 Conceptual implication

End on:

> **Scientific generalization requires judging the applicability of learned empirical relationships.**

---

## 5. Introduction Structure

Use a compact four-paragraph Introduction.

### Paragraph 1 — What should an autonomous scientist learn?

Core distinction:

> **Finding a productive condition is not the same as learning knowledge that transfers to new interventions.**

Optimization may require only finding a high-performing condition.
Scientific understanding requires knowing **where a relationship remains valid**.

### Paragraph 2 — Why current evaluation cannot answer this

Separate three stages:

**evidence acquisition**

→ **inference / model formation**

→ **generalization to interventions**

A failed prediction can come from:

- insufficient or poorly chosen experiments;
- unresolved identifiability;
- incorrect extrapolation despite available evidence.

### Paragraph 3 — What ChemWorld makes controllable

Position ChemWorld as:

> **an experimental instrument for controlled studies of autonomous scientific inference**

Key capabilities:

- law ↔ observation ↔ information separation;
- persistent physical state;
- matched worlds;
- autonomous experiment selection;
- sealed recommendation;
- withheld interventions;
- exact research-history reconstruction.

### Paragraph 4 — What we find

Do not introduce results by system.

Instead summarize:

1. operational success does not guarantee predictive knowledge;
2. more evidence and correct information sometimes help;
3. neither uniformly resolves generalization;
4. two complementary preserve/revise failures emerge;
5. applicability of learned relationships becomes the central object of evaluation.

---

# 6. Results Structure

The main text should use **five result-driven sections**.

---

## Result 1 — A programmable experimental instrument separates laws, evidence and information

### Purpose

Establish that the scientific questions studied later are measurable.

### Logic

**world construction**

→ persistent physical state / finite resources

→ information conditions

→ autonomous experiment selection

→ evidence accumulation

→ sealed recommendation + scientific assessment

→ matched comparisons

→ 240 campaigns across six chemical systems

### Figure 1

Use Figure 1 to show the full ChemWorld research instrument and assessment protocol.

### Do not discuss here

- which arm performs best;
- which system fails;
- which prior helps.

This section should establish the **instrument**, not the findings.

### Transition

> **This design allows operational achievement, predictive generalization and evidence use to be measured separately under matched experimental worlds.**

---

## Result 2 — Operational achievement does not imply predictive generalization

### Scientific question

Why is a successful autonomous experiment not sufficient evidence of scientific understanding?

### Main evidence: Electrochemistry

Optimization vs discovery:

- recommendation retest improves in **26/30** pairs;
- score prediction improves in only **14/30**;
- **13/30** pairs show better operation but worse prediction.

### Boundary: Reaction processing

RX prevents the reader from interpreting the EC result as a universal optimization–prediction trade-off.

The correct interpretation is:

> **Operational achievement and predictive generalization are distinct dimensions of autonomous scientific performance.**

### Supporting result: Purification

High recovered fraction does not necessarily satisfy purity constraints.

Operational success is itself multi-objective.

### Figure 2

Matched operation-versus-prediction comparisons, led by EC with RX as a boundary case.

### Transition

> **If successful operation does not guarantee generalizable knowledge, a natural possibility is that the agent simply lacks sufficient evidence.**

---

## Result 3 — Additional evidence improves generalization selectively

### Scientific question

Are the failures simply caused by insufficient experimental evidence?

### Positive result: EC

Increasing the research envelope from 12 to 24 batches improves predictive performance across multiple EC responses.

### Strong positive control: PA

PA is important because it shows that the agent **can** turn more evidence into better generalization.

Key pattern:

- MAE decreases strongly;
- 13/15 matched pairs improve;
- process-choice accuracy improves;
- intervals narrow while coverage increases.

### Boundary: Crystallization

More resources improve some responses, but:

- some response-specific errors remain;
- calibration can remain poor;
- delivery does not uniformly improve.

### Main conclusion

> **Evidence quantity matters, but does not fully explain when learned relationships generalize.**

### Figure 3

Budget / research-envelope effects.

### Transition

> **If more evidence is not sufficient, the next question is whether better prior knowledge resolves the problem.**

---

## Result 4 — Prior information helps within some regimes but fails across others

### Scientific question

Does supplying correct scientific information improve autonomous generalization?

### Positive control: RX/P

Aligned information improves prediction in the reaction parameter study.

This establishes:

> **Correct prior information can help.**

### EQ/P overall reversal

Opaque performs better overall than Aligned.

Do not stop at:

> “correct information hurts.”

Instead ask:

> **Where does the reversal occur?**

### Regime-specific analysis

For the other nine queries:

- Aligned performs better.

For the three most dilute queries:

- Aligned performs worse in all five worlds;
- interval coverage collapses.

All source campaigns remain above the dilute test regime.

### Deeper insight

> **A locally useful relationship can be extended beyond the regime supported by acquired evidence.**

### Input coverage ≠ response-regime coverage

The 90× versus 4× concentration-range example supports a broader point:

> **Broad exploration in input space is not equivalent to acquiring discriminating evidence across distinct response regimes.**

This can be expressed as:

> **parameter coverage ≠ mechanistic / discriminating coverage**

### Figure 4

Regime-specific EQ reversal, prediction error, interval coverage, and selected trajectory illustration.

### Transition

At this point the reader may suspect the agent is simply too conservative and preserves observed relationships too often.

Result 5 should immediately present the opposite failure.

---

## Result 5 — Autonomous generalization fails by both preserving and revising the wrong relationships

This is the conceptual climax of the paper.

### 5.1 Crystallization gives the opposite failure

Crystallization purity is relatively stable across source and withheld conditions.

Yet the agent systematically predicts lower purity.

Key evidence:

- public observation mean beats the agent on purity in **30/30** campaigns;
- **335/360** purity predictions are too low;
- the same agent still beats the mean on recovery in **26/30** campaigns.

Therefore the problem is selective rather than a general inability to use data.

Interpretation:

> **response-selective over-revision**

### 5.2 Mirror-image synthesis

#### EQ

**True relationship changes → agent preserves it**

#### Crystallization

**True relationship remains stable → agent revises it**

The deeper question is not:

> Can the agent extrapolate?

It is:

> **Can the agent determine when extrapolation is warranted?**

### 5.3 Purification as supporting evidence

Some purification interventions have very small true effects.

This provides supporting evidence that:

> **Predicting invariance is itself a scientific capability.**

### 5.4 Uncertainty is part of the same problem

EQ dilute conditions show:

- large prediction error;
- narrow intervals;
- very poor coverage.

A crystallization case shows that verbal acknowledgment of limited evidence does not guarantee appropriate numerical uncertainty.

Safe formulation:

> **Stating a limitation is not equivalent to propagating that limitation into quantitative uncertainty.**

Avoid claims that:

- the model “knew it was wrong”;
- report compression caused the failure.

### 5.5 Conceptual synthesis

> **Together, equilibrium and crystallization reveal two complementary scope errors: extending a relationship beyond its supported regime, and abandoning a relationship that remains empirically stable.**

Final conceptual statement:

> **Scientific generalization requires inference over the applicability of relationships, not merely estimation of the relationships themselves.**

---

# 7. Preserve–Revise Conceptual Analysis

A useful conceptual figure or diagnostic can organize interventions into a 2×2 map:

| | Agent preserves | Agent revises |
|---|---|---|
| **World remains stable** | Correct preservation | **Over-revision** — crystallization purity |
| **World changes** | **Over-extension / under-revision** — EQ dilute | Correct revision |

Possible supporting examples:

- EQ dilute regime;
- crystallization purity;
- purification small-effect interventions.

This figure should become a conceptual object of the paper rather than another performance plot.

---

# 8. Discussion Structure

Keep the Discussion compact and conceptual.

## Paragraph 1 — Main finding

ChemWorld shows that:

- operational achievement;
- predictive generalization;
- warranted uncertainty

can diverge.

Then elevate the main point:

> **The central challenge is not whether agents can fit observations, but whether they can infer the domain over which learned relationships remain applicable.**

## Paragraph 2 — Deeper interpretation

Reject two overly simple strategies:

- always trust empirical stability;
- always extrapolate mechanistically.

The desired capability is:

**evidence**

→ **relationship**

→ **applicability**

→ **prediction**

## Paragraph 3 — What has not been established

Do not claim that the current study proves:

- prior anchoring;
- report compression;
- a causal separation of evidence acquisition and inference;
- selected trajectories represent population frequency;
- a universal limitation of all language models.

Important boundaries:

- one agent configuration;
- five reused worlds per study;
- correlated readouts;
- some analyses are post hoc;
- no wet-laboratory validation.

## Paragraph 4 — Implication for autonomous-science evaluation

Future autonomous-science evaluation should ask:

**Did it find something useful?**

**What did it learn?**

**Where does it think that relationship applies?**

**Does uncertainty reflect the available evidence?**

The final implication should connect:

> **acquired evidence → claimed applicability → predictions under intervention**

---

# 9. Methods Structure

Keep Methods descriptive rather than story-driven.

## World construction and execution

- physical state;
- process components;
- operations;
- instruments;
- resources;
- replay.

## Platform qualification

- execution-domain checks;
- boundary and invalid-action tests;
- interface consistency;
- generated compositions.

## Study units and scientific objectives

- six chemical system families;
- eight study blocks;
- budgets;
- scientific objectives.

## Agent and information conditions

- Opaque;
- Aligned;
- MisIndexed;
- agent settings;
- tools and resource contracts.

## Sealed assessment protocol

- recommendation;
- independent retest;
- K1;
- Q;
- K2.

## Outcome definitions and empirical references

- MAE;
- coverage;
- width;
- system-specific reference targets;
- empirical baselines.

## Matched comparisons and sensitivity analyses

- goal pairs;
- budget pairs;
- information-arm comparisons;
- repeated world structure.

## Protocol deviations and retained failures

- source-assay shortfalls;
- infrastructure recovery;
- parser/evaluator corrections;
- retained failures.

---

# 10. Supplementary Information Structure

Organize Supplementary Information by the logic of the paper.

1. **ChemWorld construction and qualification**
2. **Complete autonomous study design**
3. **Prediction targets and assessment protocol**
4. **Complete operational–prediction comparisons**
5. **Budget effects**
6. **Information-arm effects**
7. **Regime-specific equilibrium analysis**
8. **Crystallization empirical references**
9. **Purification intervention-response analysis**
10. **Selected research trajectories**
11. **Protocol variation, failures and evaluator corrections**

---

# 11. Recommended Main-Figure Logic

## Figure 1 — ChemWorld as an experimental instrument

Show:

- programmable chemical world;
- autonomous experiment loop;
- persistent physical state;
- controlled information / research envelope / matched worlds;
- evidence accumulation;
- sealed operational retest;
- unseen-condition prediction and uncertainty;
- six-system study scope.

Do not place numerical results in Figure 1.

## Figure 2 — Operation versus predictive knowledge

Use EC as the main result and RX as a boundary condition.

## Figure 3 — What additional evidence repairs

Use 12 vs 24 research-envelope comparisons.

## Figure 4 — Regime-dependent value of prior information

Lead with EQ/P regime reversal and uncertainty collapse.

## Figure 5 — Preserve versus revise

Use crystallization as the opposite failure and synthesize EQ + crystallization into the preserve/revise conceptual framework.

---

# 12. Claims to Avoid

Do **not** currently claim:

- experimental insufficiency has been ruled out;
- correct prior information is generally harmful;
- wrong prior information is generally helpful;
- report writing causes systematic information loss;
- the agent knew it was wrong;
- simple empirical baselines prove no mechanism was learned;
- the agent systematically fails across all chemistry;
- selected trajectory examples estimate prevalence;
- current data identify a single psychological or cognitive mechanism.

Prefer precise formulations such as:

- benefits depend on response and regime;
- acquired evidence and predictive use can diverge;
- locally useful relationships can fail outside their supported regime;
- stable empirical relationships can be revised unnecessarily;
- verbal limitations do not guarantee calibrated numerical uncertainty.

---

# 13. Final Paper Outline

## Introduction

## Results

### A programmable experimental instrument separates laws, evidence and information

### Operational achievement does not imply predictive generalization

### Additional evidence improves generalization selectively

### Prior information helps within some regimes but fails across others

### Autonomous generalization fails by both preserving and revising the wrong relationships

## Discussion

## Methods

### World construction and execution

### Platform qualification

### Study units and scientific objectives

### Agent and information conditions

### Sealed assessment protocol

### Outcome definitions and empirical references

### Matched comparisons and sensitivity analyses

### Protocol deviations and retained failures

---

# 14. One-Sentence Story

> **ChemWorld uses controlled chemical worlds to show that successful autonomous experimentation is not sufficient for scientific generalization: agents must learn not only empirical relationships, but when those relationships should persist or change under new interventions.**

---

## 15. Narrative in Six Questions

The paper should feel like the reader is being led through six increasingly precise questions:

1. **成功操作是否等于学会了规律？**
   → No.

2. **是不是实验数据太少？**
   → Sometimes, but not enough to explain all failures.

3. **是不是缺少正确先验？**
   → Correct prior can help, but its value is regime-dependent.

4. **真正缺的是什么？**
   → Judging the applicability of learned relationships.

5. **最直接的证据是什么？**
   → EQ preserves a relationship that should change; crystallization revises one that remains stable.

6. **因此 autonomous science 应该评估什么？**
   → Not only task success, but scope-aware generalization and warranted uncertainty.
