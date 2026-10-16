# 先提出严重度不足并检验，失败的X0流程也确实降低后续预测中的先验权重

`repeat-02/P-W03-B12-optimization-E-MisIndexed`

阅读覆盖：同一分析智能体完整阅读笔记/差异、全部公开操作测量及K1/Q/K2；非独立双人编码。

[完整公开记录](../sessions/repeat-02__P-W03-B12-optimization-E-MisIndexed.json)

## 问题与先验

研究同时追求纯度≥0.80和回收。错配资料将X0描述为有利萃取剂；第一次完整处理纯度0.742但回收为零，随后六次短条件反应筛选显示转化均低。首次处理还包含洗涤、干燥和浓缩，不能把零回收单独归因于X0。

## 预期与实验

v2/cursor64在新实验前明确提出时间/温度不足，预测C1/S0由350 K、1200 s改为400 K、7200 s将提高转化；第8批转化由第5批0.084升至0.721，回收0.0465升至0.335。随后同一严重度下比较S0–S3，S2最终纯度/回收0.576/0.432最优，S3为0.353/0.232。温度和时间共同改变，因此只建立严重度方向，不能分别识别两者作用。

## 实际证据

第12批重复较优C1/S2上游，处理前HPLC纯度/回收0.578/0.421，X0分相、0.040 L洗涤和干燥后降为0.325/0.038；末端近一转化仅属于保留相。v3因此否定资料可直接预测完整反应混合物。两次X0流程的洗量、反应组成及浓缩均不同，仍不能识别损失步骤，更不能从未测X2推断真实X0/X2排名。

## 修订

这是实际具有事前预测和后续检验的认识修订：低转化→提出严重度限制→更强条件显著提高转化；另一路为有利X0先验→两次流程失败→撤回直接可迁移的判断。K1明确列出基质依赖、错配、洗涤损失等替代解释，K2提出在分相后、洗干后分阶段测量来区分原因，但该实验尚未执行。

## 后续采用

Q确实降低X0纯度预测并扩大不确定性，没有继续机械维持X0优势。其低催化剂组回收仅0.004–0.017，低投料但恢复催化剂比例组为0.110–0.155，表明反应阶段认识进入预测；这些催化剂/稀释规律从未实测。Q仍预计洗涤提高纯度，而实际失败处理未拆分，故该方向保留了未经识别的通用假设。推荐选纯度最高但回收零的第1批，K1/K2均明说不合格，不能把推荐存在或回放成功当作成功工艺。

## 未解决问题及解释限制

所有配方只做一次；催化剂剂量、相比例和其他X类别均无实验覆盖。成功形成的是局部严重度与选择性关系，以及完整X0流程不能直接由资料解释的认识；没有得到普遍动力学常数、真正分配系数或单一失败原因。

## 已核验引文与事件锚点

v2 / cursor {'event_count': 64, 'last_event_id': 'runner-operation-0064'}

> Low conversion across categories suggests residence time/temperature, rather than category alone, is limiting.

事件：runner-operation-0072

v3 / cursor {'event_count': 111, 'last_event_id': 'runner-operation-0111'}

> The dossier's X0 organic-extraction prior did not transfer reliably to the tested reaction mixtures.

事件：runner-operation-0101, runner-operation-0111

Q

> X0 receives a lower and much less certain purity prediction because the two observed X0 workups
