# Work II 最后诊断块：最小提交与公开数值工具

状态：**正式块于2026-09-06完成，120/120尝试，117有效完成、3失败保留**。任务：W2-77。
本说明覆盖整个开发与后续诊断块，不建立额外readiness包；执行状态由
[TODO](WORK_II_TODOLIST.md)管理，论文角色与取舍见[矩阵](WORK_II_EXPERIMENT_MATRIX.md)。
本轮固定GPT/DeepSeek双模型，第三模型暂缓；开发完成后冻结正式执行面，不重复请求已有执行授权。

终态报告：[可读摘要](reports/work-ii-final-diagnostic-20260905.md)及
[机器数据](reports/work-ii-final-diagnostic-20260905.json)，由current的w2_77_final_diagnostic绑定。
240轮全部尝试，零未启动、零补跑或替换；新增world、物理及replay均为0。
主差+0.01667，95%区间[−0.08333,+0.10000]，未支持明确工具可用性收益，亦不证明等价。
opaque/misindexed共80 scheduled、78有效，joint recovery为0；全部17次成功为aligned先验保持。
GPT开放工具30会话均未调用；DeepSeek在20/30会话共尝试63次，其中9次表达式拒绝。
3个失败为DeepSeek post提交校验、GPT传输中断和DeepSeek提供方输出上限各1例。
报告wall合计33,619秒；输入8,251,168、输出5,152,198 tokens，两次失败轮用量缺失，均为已知下界。
上述是终态记录，不改写以下执行前设计与原开发失败。

开发前固定：复用原B3公开开发seed 0，三prior×两模型×两工具各一次，共12 sessions，24轮；
每轮上限600秒，每session上限1200秒，整块上限4小时，无结果选择性重试。
post工具最多8次尝试（含错误请求）；表达式长度≤20,000，AST节点≤1,024，数组元素及输出≤4,096。
仅提供固定白名单的数组算术、log/exp/sqrt、归约、clip、linspace和最小二乘；无文件、网络或模拟器操作。
所有模型调用tokens按实际usage计数；CLI不能保证服务端严格输出token上限，因此采用wall-clock硬停止，
不虚构token硬限。开发记录与正式数据分开。正式预算已在开发结束后、首单元之前写定：
每轮600秒、每session 1200秒、整块64,800秒（18小时），HTTP/SSE内部重试均为0；
模型、提示、工具、coverage、读出和阈值不变，仍为120 sessions、240计划轮次。

## 问题与预期用途

原B3有界可识别表面中，GPT有30/30完成和5/30 joint recovery，DeepSeek有17/30完成、
13/30 schema failures和0/30 joint recovery。新块问：在最小科学提交下，开放数值计算工具
是否改变结构恢复与后续选择？它补强F2，并记录受限的预测/规律承诺/行动读出。
它不复现完整C2、原纵向F4、主动取证或新条件迁移，不要求结果继续表现为失败。

已有科学范围由[GPT B3原note](WORK_II_AS_STUDY_B3_GPT56_SOL_MEDIUM_REPLICATION_EXPERIMENT_NOTE.md)
和[DeepSeek后继note](WORK_II_W263_DEEPSEEK_B3_FULL_REPLICATION_EXPERIMENT_NOTE.md)解释。
这些note中的旧授权、canary和重试规则只适用于旧块；本块使用新的固定设计，不能续跑旧目录。
原结果、schema失败、停止和未启动分母不变。

## 测试单位与固定覆盖

| 项目 | 设计 |
| --- | --- |
| 科学表面 | 原B3全部5个评分world、原三初始描述、公开evidence和8个scoring/action queries；不按结果挑world |
| 模型 | GPT-5.6-sol/medium、DeepSeek-v4-flash/high；本轮不加入第三模型 |
| 工具条件 | post无数值工具 / post可调用相同公开数值工具；两条件pre均无工具 |
| 重复与单位 | 每world×prior×model×tool为2个fresh sessions；session内pre→post保持同thread；独立world仍为原5个 |
| 双模型 | 5×3×2×2×2＝120 sessions、240轮；新增独立world为0 |
| 开发 | 原公开开发seed 0，与评分world不同；每prior×model×tool各1 session，共12，独立保存 |
| 物理与replay | 若封存包/评分完整可复用，则新增participant物理、truth/replay均为0；复用读取不算新执行 |

全部无工具条件也重新采集，不能用旧复杂schema组充当新最小schema对照。
正式顺序在第一次正式调用前生成，按world/prior/repeat平衡model和tool先后；不因早期结果改顺序。
第三模型本轮暂缓，不改变上述设计。

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

- 唯一primary：GPT/DeepSeek等权的tool-on minus tool-off failure-aware joint-recovery比例差；
  正值有利于工具条件。joint recovery沿用正确family且指数绝对误差≤0.10，失败计0。
  先在world内平均priors/repeats，再按world等权；报告5个配对world值及小样本近似95%区间。
  固定world cluster bootstrap 20,000次、随机种子90770、百分位[2.5%,97.5%]；不把120 sessions当作独立world。
  另列两模型逐world描述性效应；不是对Agent总体的随机抽样。
- 对齐先验已提供正确family/指数，该层的joint recovery表示知识保持；opaque/misindexed才涉及恢复。
  三prior各自列出完整分母，不能把对齐组保持率统称从证据发现规律。
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
开发范围最多12个计入账本的sessions及上述4小时；无法完成则记录限制并暂缓，进入已有证据写作。

正式前固定每turn/session timeout、输入/输出与工具调用上限、总wall预算、模型版本和完整单元表。
这些数值由本块单executor开发观测确定；开发12会话合计3501.736秒，最长轮次576.109秒。
按开发平均值估计正式约9–10小时；不套用旧并发B3或M3短选择调用的ETA。
现有两配置最多120正式sessions；不以不同提供方的同名reasoning档位表示等算力。
每分钟至少报告阶段、完成/计划量、吞吐与ETA；分开记录所有turn、tokens、工具计算与失败成本。

每个科学单元仅尝试一次，不按得分、schema失败或模型身份重试；普通参与者失败不阻止后续独立单元。
公共/私有污染、输入漂移、未授权工具访问或真实平台缺陷暂停后续调用；保留已完成与未启动记录。
中断后保留完成单元，已开始却无终态的调用不能静默重发。平台修复影响正式执行语义时，
受影响的正式qualification块按AGENTS从首单元重跑，原块完整保留，不能拼接成更好结果。
如果预声明总资源上限触发，按已执行/失败/未启动分别收尾，不声称完整正式复核。

## 执行入口与预期输出

新ignored run目录保存每个单元的尝试和终态、pre/post原始回执、公开输入、工具日志、资源及离线评分。
Git只收一个脱敏机器JSON和一份可读摘要，含完整scheduled/attempted/completed/failed/unstarted分母、
逐world主读出、全部失败和成本；不覆盖旧结果。原始provider payload与凭据不进Git。

入口为`uv run --no-sync python -m scripts.run_work_ii_final_diagnostic`，配置为
`configs/benchmark/work_ii_final_diagnostic_20260905.json`。先prepare development，再run/analyze；
开发结束后固定formal预算、提交执行面、prepare formal、freeze一次，再run/analyze。
复用原B3 `work-ii-as-study-b3-identifiable-law-action-v0.2-20260827-restart1` 的manifest和固定roster；
开发证据由其既有seed 0 linear/power truth按相同roster读取。无新物理或replay。
运行输出必须保存在ignored runs；不覆盖已存在输入或终态，不重发已有attempt标记的单元。
工具超过8次尝试计资源失败；禁止工具、缺少thread或执行器异常暂停后续单元。
输入token随固定公开包/schema及最多8次工具响应有界，实际输入/输出及可用cache/reasoning usage保留；
缺失usage显式计数，不视为零消耗。近最优沿用raw regret≤0.01，useful gain沿用≥0.02及原机会标记。
对未启动单元保留计划分母，失败感知joint=0/regret=1仅表示未取得成功，不宣称它们是模型作答。
不为实现本块刷新旧全树hash或资格证书。

上述开发设计已在首次participant调用前登记。开发结果不进入正式科学分母；原始回执独立保留。

开发校准记录：第6、7会话的DeepSeek post各收到`max_output_tokens`未完成响应，CLI各自动重连一次；
执行器按既定规则将整会话记为provider failure，未把恢复后的答案计作成功。开发块维持原设置和固定12单元。
正式预算同时固定provider内部重试为0（HTTP及SSE），避免隐藏恢复；
该设置已由[官方配置文档](https://developers.openai.com/codex/config-reference/)核实，
并以本地HTTP 503及未完成SSE假服务验证每轮仅发出一次请求，未调用真实模型。
记录的tokens为CLI提供的用量；错误、中断或恢复后的回执可能缺少部分消耗，相关组只报告已知下界。

开发终态：12/12尝试、24/24调用，10有效完成、2 provider failures、0未启动；
GPT 6/6完成，DeepSeek 4/6完成。3次公开计算全部返回，零越权工具、零单元重跑或替换。
全部pre/post同thread、12个fresh threads。报告输入1,238,133、输出417,422 tokens；
两次错误轮用量可能不完整。开发只有原seed 0，不作world不确定性推断，不进入正式结论。
见[开发摘要](reports/work-ii-final-diagnostic-development-20260905.md)及其同名机器JSON。
