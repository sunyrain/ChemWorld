# 世界律

世界律是 ChemWorld 的统一规则层。它定义物质、相、反应、分离、测量、安全、成本和
评分之间的关系。任务只是世界律上的不同切片。

## 世界律合同

当前世界律标识：

```text
chemworld-physical-chemistry
```

所有正式任务都应声明该字段或明确声明自己使用的其他 world law。相同 world law 下的
任务应共享基本操作语义、ledger 规则和 observation boundary。

## 共享模块

- ontology；
- mechanism schema；
- physical constitution；
- runtime transaction；
- instrument model；
- safety/cost model；
- scoring interface。

## 设计规则

不要为了单个任务偷偷改变底层世界规则。如果某个任务需要特殊物理或特殊观测，应把差异
写入 task card、scenario 或 backend，而不是让 agent 面对隐式不一致。
