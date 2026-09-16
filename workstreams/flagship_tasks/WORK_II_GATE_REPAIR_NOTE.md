# W2-118：五体系合同修复与固定覆盖验证

2026-09-16，development，单executor。问题：修正W2-117的资料入口、观测对象及饱和/低响应选点后，五卡能否取得可测差异，使局部错误先验可被反驳？保留W2-117；不改物理常数、不降低原信噪阈值、不调用provider；Agent自由机理形式不变。

## 修复与固定覆盖

新增opt-in `research_brief`承载定制委托、共同背景和一条局部实例资料，不套旧材料白名单、不改权限/物理/native score。O无实例提示，A/M格式/范围/不确定性相同，无臂名或正确性标记。公开理想温度、压力、体积/时钟与流程配置；组分仍需付费。批次结束后区分新批当前状态与旧批终检。PA使用已有 `PARTITION_S0_EXTRACTION_EFFICIENCY_V3`固定初始目标物分母，终检前不弃相；不全局改写旧默认合同。

**23个campaign、75个计划化学批次**：基础标定5组/28批；EQ/PA/FL变化世界3组/17批；五卡O/A/M双批真实入口15组/30批。每条件一次。实例及观测seed写ignored plan；基础/变化世界同初始化；标定与三臂复测噪声namespace不同，三臂之间相同。

| 卡 | 基础标定批次顺序 | 每批操作 | 操作预算 | 主通道/对比（1-based） |
| --- | --- | --- | --- | --- |
| RX | 催化剂0.00002、0.00025mol各配1/5/30/300s，共8批；335K边界 | solvent2/0.028L、reagent0.010mol、catalyst1、heat、terminate、final，6步 | 48 | yield；2↔4及6↔8 |
| EQ | 体积0.020、0.060L各配投料0.00001/0.010mol，共4批 | solvent0、reagent、pH、terminate、final，5步 | 24 | acid_dissociation_fraction；1↔2及3↔4 |
| BC | 1/30/600s，共3批；335K边界 | RX同投料，catalyst1/0.00025mol，6步 | 18 | yield；1↔3；另报中间点 |
| PA | extractant体积0.006、0.030L各配索引0/3，共4批 | solvent0/0.025L、水相0.018L、extractant、mix240s/750rpm、settle360s、terminate、final，7步 | 48 | product_in_organic；1↔2及3↔4 |
| FL | residence900/3600/7200s各配340/390/430K，共9批；flow1.2mL/min | solvent2/0.026L、reagent0.010mol、catalyst1/0.00022mol、配置、run_flow(2×residence)、terminate、final，7步 | 72 | flow_conversion；4↔6及7↔9 |

这是参考覆盖，不限定Agent探索。RX扩大辨识预算，BC保留18步约束；FL的V=Qτ改变设备几何，边界温度不当实际流体温度，不把名义throughput当产品。不同任务不作等预算比较。

变化世界：EQ为pKa轴extrapolation severity=1；PA为constitutive_law_family severity=1（分配系数幂响应）；FL为kinetics轴extrapolation severity=1。RX/BC结构干预属可选后续，本块不新增。

主响应阈值仍为`max(0.02,3√2 σ_final)`；pH副指标最低0.01。每卡全部主对比须越阈值，方向不预设。S2要求同一通道至少2个对应条件越阈值，EQ用pH，其他用主通道。

## 固定两阶段资料生成与三臂验证

资料规则在标定前固定，不按结果换点：RX目标第4批/反事实第2批；EQ第2/1批；BC第3/1批；PA第2/1批；FL第9/1批。

A用基础标定目标条件的付费终检值；M把指定反事实条件的值错标到同一目标条件。两者只含目标操作、主通道、6位估计值及相同半宽`max(0.02,3√2 σ_final)`；解释为可修订的局部档案估计，不是全部世界规律。O不给此条。A是带噪局部参考，必须验证独立噪声复测相容性，不能称隐藏参数真值。

每卡三臂执行同样的“目标→反事实”两批。记录Agent reset真正收到的task_info及逐步tool_json，验证O无先验、A/M送达且不泄漏臂名；不传标定全表/评价端状态。验收15/15入口贯通、三臂对应物理观测及资源相同、A复测在所给区间内、M区间被同一新测量排除。无标定终检时相应三臂位记未启动/上游缺失，不换点。未来Q不能把已提示坐标当盲测。本轮无LLM，不测试自主决策。

## 资源、失败与输出

各campaign共用账本：容器/终检数=计划批数；EQ非终检数=批数，其余0；操作上限见表，三臂双批同卡相同预算。每批stock上限：reagent0.04mol、solvent0.08L、catalyst0.005mol、phase/extractant各0.06L；过程时间14400s/批。不刷新额度；重放与原执行分账。

FL示例可行标准保持conversion≥0.50、yield≥0.10、risk≤0.35，至少各1个可行/不可行点才称边界覆盖；温压另报，不冒充完整设备安全窗口。PA终检两相和须在0.90—1.05（容纳采样/噪声），评价端核对当前目标库存+已记录样品损失=初始库存（绝对误差≤1e-8mol）；评价信息不回流。

单campaign非法事务即终态，独立campaign继续；不重试、不按当轮结果加点/放宽阈值。平台语义修改后另立固定块；汇总错误只重算保留数据。每条轨迹精确重放一次（tolerance=0）；每20秒输出阶段、完成/23、动作活性、吞吐/ETA。

输出：ignored `runs/development/work-ii-gate-repair-20260916/` 保存计划、公开输入、轨迹、资源、评价记录与重放；reports内生成JSON/中文报告并绑定current。预计参考/重放5—20分钟。逐卡报告运行、响应、局部先验反证及物料/窗口检查；完整G-S/G-R、K1/Q/K2和评审仍须另验证。
