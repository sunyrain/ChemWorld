# Mechanism 协议

Mechanism schema 描述任务背后的反应网络、物种、参数、观测接口和约束。它是隐藏世界
与可执行 runtime 之间的合同。

## 合同

一个 mechanism 至少应描述：

- species；
- reaction steps；
- kinetic 或 proxy kinetic 参数；
- phase/partition 信息；
- safety/cost 参数；
- instrument mapping；
- maturity metadata。

这些字段不一定全部公开给 agent，但必须足够支持 replay、审计和任务卡生成。

## 编译期产物

Mechanism compiler 应把 schema 转成 runtime 可用的 kernel、ledger 初始化信息和
instrument model。编译产物需要版本化，避免同一任务在不同机器上解释不一致。

## 回放

Replay 使用相同 mechanism、scenario、seed 和 action 序列，应该得到一致的关键结果。
如果结果漂移，优先检查随机数、浮点容忍度、ledger transaction 和 instrument noise。

## 参考阅读

未来的 professional-candidate 版本应逐步接入经过文献或开源工具校准的反应/物性模块。
在此之前，schema 中必须明确 proxy 和 lite 边界。
