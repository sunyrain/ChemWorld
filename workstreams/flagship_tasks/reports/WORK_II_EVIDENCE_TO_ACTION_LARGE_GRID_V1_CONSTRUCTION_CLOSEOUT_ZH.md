# Work II evidence-to-action large-grid v1.0 construction 收口

状态：**PASSED / 仅授权全新 prospective qualification / 不授权 provider**
日期：2026-08-24

large-grid v1.0 将每个 task-world 的 outcome-blind grid 从 `32 global + 64 neighborhood = 96`
扩大为 `64 global + 256 neighborhood = 320`，即每个八候选单元约有 `32` 个局部点。ExtraTrees
预测器及全部超参数保持 v0.4 不变，因此该 block 隔离检验 grid coverage。

修复 typed-law `evidence_ids` schema 缺陷后，restart1 从第一个单元完整重跑并通过 `7/7` exposed
construction units：

| task | seed | 角色 | 旧 rho | 320-grid rho | Top-1 |
|---|---:|---|---:|---:|---|
| electrochemical | 762707071 | v0.2 retained failure | 0.785714 | 0.904762 | yes |
| electrochemical | 241995082 | v0.4 retained failure | 0.785714 | 0.904762 | no |
| electrochemical | 2 | low-margin control | 0.833333 | 0.857143 | yes |
| crystallization | 836245547 | original W2-51 retained failure | 0.738095 | 0.928571 | yes |
| crystallization | 468887863 | v0.3 retained failure | 0.595238 | 0.928571 | no |
| crystallization | 2 | low-margin control | 0.809524 | 0.976190 | no |
| reaction-safety | 3 | low-margin control | 0.809524 | 1.000000 | yes |

总计完成 grid truth/replay `2240/2240`、registered truth/replay `112/112`，即总 truth/replay
`2352/2352`；全部 candidate design rank 为 `8`，最大 typed-law 蒸馏误差为 `9.09e-13`，
fit/candidate overlap 为 `0`，candidate outcomes read 为 `0`，provider calls 为 `0`。最低
`rho=0.857143`，高于冻结门槛 `0.80`。

这证明扩大 grid 能在已暴露 construction worlds 上修复四个已知失败且没有使三项低裕量控制
跌破门槛，但不能证明对新 world 泛化。该结果只授权按完全相同的 320-grid/ExtraTrees 设计运行
已冻结的五个全新 qualification seeds；它不回写原始 W2-51，不把旧失败改成通过，也不授权
participant 或 formal execution。

机器收口：`work-ii-evidence-to-action-large-grid-v1.0-construction-closeout.json`。
