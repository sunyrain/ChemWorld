# 缺组分解释引入额外投料，后来撤回必需性并修复容量操作

`repeat-03/P-W04-B12-optimization-E-MisIndexed`

阅读覆盖：同一分析智能体完整阅读笔记/差异、全部公开操作测量及K1/Q/K2；非独立双人编码。

[完整公开记录](../sessions/repeat-03__P-W04-B12-optimization-E-MisIndexed.json)

## 问题与先验

错配资料选择X0；前四批低终态回收使v2/cursor65认为漏component使催化剂筛选无效，转而每批加0.04mol component。实际同命令共享投料，先前C1/C2/C3仍是有效无额外投料比较。

## 预期与实验

中途额外投料伴随温时变化，未隔离组分作用；批7—10的0.06L萃取超容量被拒，随后选空有机相，复加溶剂完成终检。末两批减至0.018L萃取并取消干燥浓缩，得到有效非零回收。

## 实际证据

批11/12无component的C1S3反应纯度0.647/0.651、产率0.226/0.205，X0无洗最终0.710/0.0308，X1加洗0.692/0.0234。无纯度合格批；首批0.79977且回收0被选为最近门槛候选。

## 修订

K1和K2明确component并非必需，恢复前四批内的局部催化剂比较；正确识别容量拒绝、空相而非无目标反应。仍把干燥/浓缩与零体积归因混在一起：批7浓缩0113因已无体积被拒，批8—10无浓缩，不能以这些批证明浓缩造成空相。

## 后续采用

Q仍以资料估算未测X2与X0，给X0纯度/回收均高；Q11/12浓缩后纯度0.88→0.91、回收0.085→0.075。K2承认有效600s浓缩从未隔离，却仍称多次干燥浓缩导致空样；操作时间顺序限制该解释。

## 未解决问题及解释限制

该场既有真实操作修复与假说撤回，也有失败来源混淆。不能把被拒提取当化学萃取反证；同样不能把0.79977和零回收当成功。后续时间序列只是提案。

## 已核验引文与事件锚点

v2 / cursor {'event_count': 65, 'last_event_id': 'runner-operation-0065'}

> Future batches will include 0.04 mol component-0.

K1

> Component-0 is not demonstrably required for target formation

K1

> Drying and especially a 300 s concentration step could reduce the selected liquid to zero.

K2

> the effect of a valid 600 s concentration step was never isolated.
