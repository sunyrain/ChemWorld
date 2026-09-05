# Work II 最后诊断块：最小提交与公开数值工具

状态：**DRAFT / development design，未执行**。任务：W2-77。
本说明覆盖整个开发与后续诊断块，不建立额外readiness包；执行状态由
[TODO](WORK_II_TODOLIST.md)管理，论文角色与取舍见[矩阵](WORK_II_EXPERIMENT_MATRIX.md)。
模型/预算及下方技术缺项落实之前不能把本草案当作已冻结协议。

## 问题与预期用途

原B3有界可识别表面中，GPT有30/30完成和5/30 joint recovery，DeepSeek有17/30完成、
13/30 schema failures和0/30 joint recovery。新块问：在最小科学提交下，开放数值计算工具
是否改变结构恢复与后续选择？它补强F2，并记录受限的预测/规律承诺/行动读出。
它不复现完整C2、原纵向F4、主动取证或新条件迁移，不要求结果继续表现为失败。

已有科学范围由[GPT B3原note](WORK_II_AS_STUDY_B3_GPT56_SOL_MEDIUM_REPLICATION_EXPERIMENT_NOTE.md)
和[DeepSeek后继note](WORK_II_W263_DEEPSEEK_B3_FULL_REPLICATION_EXPERIMENT_NOTE.md)解释。
这些note中的旧授权、canary和重试规则只适用于旧块；本块使用新的固定设计，不能续跑旧目录。
原结果、schema失败、停止和未启动分母不变。

## 测试单位与固定覆盖候选

| 项目 | 设计 |
| --- | --- |
| 科学表面 | 原B3全部5个评分world、原三初始描述、公开evidence和8个scoring/action queries；不按结果挑world |
| 模型 | GPT-5.6-sol/medium、DeepSeek-v4-flash/high；第三家族/版本/渠道在启动前确定，当前未定 |
| 工具条件 | post无数值工具 / post可调用相同公开数值工具；两条件pre均无工具 |
| 重复与单位 | 每world×prior×model×tool为2个fresh sessions；session内pre→post保持同thread；独立world仍为原5个 |
| 双模型 | 5×3×2×2×2＝120 sessions、240轮；新增独立world为0 |
| 若预先加入第三模型 | 总量180 sessions、360轮；第三模型60 sessions不增加world分母 |
| 开发 | 原公开开发world中事先固定1个，与评分world不同；每prior×model×tool各1 session，共12或18，独立保存 |
| 物理与replay | 若封存包/评分完整可复用，则新增participant物理、truth/replay均为0；复用读取不算新执行 |

全部无工具条件也重新采集，不能用旧复杂schema组充当新最小schema对照。
正式顺序在第一次正式调用前生成，按world/prior/repeat平衡model和tool先后；不因早期结果改顺序。
第三模型可做固定接口的开发验证，但不按其科学得分调整提示、工具、任务或阈值。

## 参与者可见内容和工具

参与者在pre提交family、指数和逐query数值预测；post收到原公开证据后提交同样科学字段及候选query ID。
family/指数只提交一次，typed law用公开、固定的映射构建；该映射不拟合新参数，不访问truth。
删除重复stage/status、重复指数和runner可推导元数据；科学字段仍需合法、有限、完整且一致。
两个工具条件使用完全相同的最小schema，不在一个比较内同时改变schema与工具。

数值工具只处理参与者可见的表格与表达式，例如固定的表达式求值和最小二乘计算。
工具不得访问仓库、私有模拟器、候选评分、目标指数或封存结果；不能将旧B3特权资格器直接开放。
公开工具能否形成有效参考路径需要开发验证，不能从“内部资格器能恢复”推出“公开信息一定足够”。
工具引入的计算与消息交互一起构成系统干预；不将效果单独归因于Agent内部算术能力。
若最小接口结果与历史不同，只称跨协议边界，不称已随机识别schema修复效应。

## 测量、分析与判断

- 唯一primary候选：GPT/DeepSeek等权的tool-on minus tool-off failure-aware joint-recovery比例差；
  正值有利于工具条件。joint recovery沿用正确family且指数绝对误差≤0.10，失败计0。
  先在world内平均priors/repeats，再按world等权；报告5个配对world值及小样本近似95%区间。
- 第三模型单独报告同一效应；它是预先选择配置的复核，不是对Agent总体的随机抽样。
- Secondary：pre/post数值误差、family和指数误差、提交有效率、候选regret、Top-1、
  原行动机会定义下的useful gain，以及模型/初始描述异质性。报告连续读出和精确分母，
  不事后发明“低误差但不懂规律”的最优阈值。结构失败与提交失败分别列出。
- 原B3 action regret和机会定义继续使用原规则。若开发发现端点科学定义有缺陷，则在正式前
  明确修订为不同读出；保留原结果，不能静默更换分母或阈值。
- 其他探索性比较不作确认性显著性结论；如需确认性secondary，须在执行前固定其完整列表及校正。
  不以“一个模型显著、另一个不显著”判断交互，不以不显著证明等价。
- 科学结论分三类：差异仍存在、工具可缓解、在该条件下转化成功；三种均是有效终态。
  未支持预期效果不触发补样本，诊断论文不要求超越nearest。

## 开发验收与资源/停止规则

开发只验证真实输入→最小schema→工具权限→完整pre/post→离线评分的路径，以及已知合法输出
和公开参考计算。科学回答错误不是技术验收失败，不能要求开发Agent全部成功才进入正式块。
开发范围最多两个工作日和12/18个计入账本的sessions；无法完成则记录限制并暂缓，进入已有证据写作。

正式前固定每turn/session timeout、输入/输出与工具调用上限、总wall预算、模型版本和完整单元表。
这些数值由本块单executor开发观测确定；目前未知，不能套用旧并发B3或M3短选择调用的ETA。
现有两配置最多120正式sessions，三配置最多180；不以不同提供方的同名reasoning档位表示等算力。
每分钟至少报告阶段、完成/计划量、吞吐与ETA；分开记录所有turn、tokens、工具计算与失败成本。

每个科学单元仅尝试一次，不按得分、schema失败或模型身份重试；普通参与者失败不阻止后续独立单元。
公共/私有污染、输入漂移、未授权工具访问或真实平台缺陷暂停后续调用；保留已完成与未启动记录。
中断后保留完成单元，已开始却无终态的调用不能静默重发。平台修复影响正式执行语义时，
受影响的正式qualification块按AGENTS从首单元重跑，原块完整保留，不能拼接成更好结果。
如果预声明总资源上限触发，按已执行/失败/未启动分别收尾，不声称完整正式复核。

## 预期输出与当前技术缺项

新ignored run目录保存每个单元的尝试和终态、pre/post原始回执、公开输入、工具日志、资源及离线评分。
Git只收一个脱敏机器JSON和一份可读摘要，含完整scheduled/attempted/completed/failed/unstarted分母、
逐world主读出、全部失败和成本；不覆盖旧结果。原始provider payload与凭据不进Git。

当前待实现：新的最小schema映射；只读公开数值工具及其权限边界；120/180单元调度；
工具计费/停止计数；复用B3输入与评分的完整读取；新块分析和摘要。
现行W2-63/M1 runner硬绑定旧配置且禁止工具，**不是本块可直接运行的入口**。
完成这些开发项后再固定最小执行面并冻结一次；不为实现本块刷新旧全树hash或资格证书。

本说明是最后实验的准备草案；没有生成participant、physics或新的科学统计结果。
