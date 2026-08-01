# G0 来源与数据发布审计

## 结论

G0 的“多历史 commit”不是科学证据失效。四个被正式摘要引用的执行 commit 都存在，并且都是当前 `origin/main` 的祖先，因此代码来源可由 Git 历史不可变地取回。B4 来源绑定可以关闭；真正未解决的是 B5 数据发布：四个本地 raw roots 共 1,441 个文件、约 17.7 GB，仍只有本地副本，没有外部持久存档、公开哈希索引和 data card。

## 不重复的科学计数

- classic baselines：27,300 次物理实验；
- opaque / nominal / misindexed participant：2,280 次；
- opaque 的 760 次同时出现在 v1.0 和 v1.2 摘要中，只计一次；
- G0 总计：29,580 次。

## 来源 commit

| 角色 | commit | `origin/main` 可达 |
|---|---|---:|
| v1.0 baseline execution | `4a72320585166f4f063749e7d06068b42f7b7b68` | 是 |
| v1.0 opaque participant / postrun | `555896ce3f6b6d6455ab9e0605e01063057889da` | 是 |
| v1.1 nominal participant | `52d317e49887d4b918eb65319d57542126c6bb17` | 是 |
| v1.2 misindexed participant | `5f5d8b51bb7b987a3de5ac57e1890abcdc4ff0f2` | 是 |

## 本地 raw roots

| 数据根 | 文件数 | 字节数 | campaign index SHA-256 |
|---|---:|---:|---|
| v1.0 baselines | 1,133 | 16,239,891,581 | `9451f67a…c0238` |
| v1.0 opaque | 105 | 494,951,408 | `5b8acfce…9e8` |
| v1.1 nominal | 102 | 495,504,956 | `744a9de8…e511` |
| v1.2 misindexed | 101 | 495,376,658 | `8cedb86a…fb3` |

前两个 index 哈希与 v1.0 正式摘要中声明的哈希逐字节一致。后两个正式摘要记录了根目录和 source commit，但没有声明 index 哈希；上表是本次从本地字节重新计算的值，不能冒充当时预声明的哈希。

## 发布策略

Git 仓库只应承载：正式摘要、派生表、协议、源码 commit 列表、数据卡和完整文件哈希索引。约 17.7 GB raw roots 应进入带 DOI 或同等级持久标识的外部存档。第一版可同时发布一个紧凑可复核包，至少包含每个 cell 的配置、摘要、推荐、postrun audit、execution index 和必要轨迹；大体积 provider workspace archive 可单独分层。

机器可读明细见 `reports/g0-source-and-data-provenance-v0.1.json`。
