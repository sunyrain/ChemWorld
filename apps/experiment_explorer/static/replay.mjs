// Pure replay projections. Seeking reads snapshots; it never executes an action.
export const MODE_NAMES = {
  development: "开发",
  formal: "正式",
  historical: "历史",
  unspecified: "未声明",
};
export const LABELS = {
  purity: "纯度",
  recovery: "回收率",
  yield: "产率",
  score: "记录得分",
  cost: "归一化费用",
  safety_risk: "风险",
  conversion: "转化率",
  selectivity: "选择性",
  crystal_fines_fraction: "细粉比例",
  crystal_size: "晶体尺寸",
  crystal_purity: "晶体纯度",
  crystal_yield: "晶体产率",
  crystal_csd_quality: "粒径质量",
  physical_cost: "物理费用",
  process_time_s: "过程时间 (s)",
  sample_consumed_L: "取样消耗 (L)",
  operation_attempts: "操作尝试",
  nonfinal_instrument_uses: "非终检测量",
  final_assays: "终检次数",
  planned: "计划",
  attempted: "已尝试",
  completed: "已完成",
  failed: "失败",
  not_started: "未启动",
  interrupted: "中断",
  recorded_operations: "记录动作",
  verified_trajectories: "原报告重放通过",
  checked_steps: "已核对步数",
  max_abs_error: "最大绝对误差",
  replay_verified: "原报告重放通过",
  agent_attempted: "Agent 已尝试",
  agent_planned: "Agent 计划",
  agent_final_assays: "Agent 终检",
  agent_execution_failures: "Agent 执行失败",
  agent_valid_successes: "Agent 有效成功",
  all_reference_attempts: "参考条件尝试",
  all_reference_final_assays: "参考条件终检",
  current_reference_candidates: "当前参考条件",
  current_reference_witnesses: "当前可达见证",
  temperature_K: "实际温度 (K)",
  target_temperature_K: "目标温度 (K)",
  duration_s: "持续时间 (s)",
  amount_mol: "投料 (mol)",
  volume_L: "体积 (L)",
  stirring_speed_rpm: "搅拌 (rpm)",
  instrument: "仪器",
  catalyst: "催化剂",
  catalyst_amount_mol: "催化剂量 (mol)",
  solvent: "溶剂",
  task: "任务",
  task_id: "任务",
  cell: "条件",
  condition: "条件",
  kind: "角色",
  status: "状态",
  quality_passed: "质量达标",
  witness: "可达见证",
  leaderboard_score: "终态评分",
  operations: "动作数",
  final_metrics: "终检观测",
  resources: "资源",
};
export const ACTIONS = {
  add_reagent: "加入反应物",
  add_solvent: "加入溶剂",
  add_catalyst: "加入催化剂",
  heat: "加热",
  cool: "冷却",
  wait: "等待",
  measure: "测量",
  quench: "淬灭",
  add_phase: "加入液相",
  add_extractant: "加入萃取剂",
  mix: "混合",
  settle: "静置",
  separate_phase: "分相",
  wash: "洗涤",
  dry: "干燥",
  concentrate: "浓缩",
  transfer: "转移",
  terminate: "终止实验",
  cool_crystallize: "冷却结晶",
  seed_crystals: "播种",
  filter_crystals: "过滤晶体",
  distill: "蒸馏",
  collect_fraction: "收集馏分",
  start_experiment: "开始批次",
};
export const label = (key) => LABELS[key] || key.replaceAll("_", " ");
export function finite(value) {
  return typeof value === "number" && Number.isFinite(value);
}
export function format(value) {
  if (
    value === null ||
    value === undefined ||
    (typeof value === "number" && !Number.isFinite(value))
  )
    return "—";
  if (typeof value === "boolean") return value ? "是" : "否";
  if (typeof value === "number")
    return Number.isInteger(value)
      ? value.toLocaleString("zh-CN")
      : Math.abs(value) > 0 && Math.abs(value) < 0.0001
        ? value.toExponential(3)
        : value.toLocaleString("zh-CN", { maximumFractionDigits: 5 });
  if (Array.isArray(value)) return `[${value.length} 项]`;
  if (typeof value === "object") return `{${Object.keys(value).length} 项}`;
  return String(value);
}
export function parseLocal(text, name) {
  text = text.replace(/^\uFEFF/, "");
  if (name.toLowerCase().endsWith(".jsonl")) {
    const records = [],
      errors = [];
    for (const [i, line] of text.split(/\r?\n/).entries()) {
      if (!line.trim()) continue;
      try {
        const row = JSON.parse(line);
        if (
          !row ||
          typeof row.action !== "object" ||
          !row.action ||
          Array.isArray(row.action)
        )
          throw Error("缺少 action 对象");
        records.push(row);
      } catch (error) {
        errors.push({ line: i + 1, error: error.message });
        break;
      }
    }
    if (!records.length)
      throw Error(`文件没有可回放轨迹：${errors[0]?.error || "空文件"}`);
    return { kind: "trajectory", records, errors };
  }
  const data = JSON.parse(text);
  const records = Array.isArray(data)
    ? data
    : data?.records || data?.trajectory;
  if (
    Array.isArray(records) &&
    records.length &&
    records.every(
      (r) =>
        r &&
        typeof r.action === "object" &&
        r.action &&
        !Array.isArray(r.action),
    )
  )
    return { kind: "trajectory", records, errors: [] };
  if (!data || typeof data !== "object")
    throw Error("JSON 文件应包含报告对象或轨迹数组");
  return { kind: "report", report: Array.isArray(data) ? { data } : data };
}
export function observations(row) {
  const source =
    row.agent_visible_observation?.observation ||
    row.observation ||
    row.environment_outcome?.observation ||
    {};
  const mask = row.observed_mask || {};
  return Object.fromEntries(
    Object.entries(source).map(([k, v]) => [
      k,
      mask[k] === false || !finite(v) ? null : v,
    ]),
  );
}
export function snapshot(records, index) {
  const i = Math.max(0, Math.min(records.length - 1, index));
  const row = records[i];
  if (!row) return null;
  const views = row.agent_visible_observation?.views || row.agent_view || {};
  const report = views.lab_report || {};
  const campaign = report.campaign_state?.campaign_resources || {};
  const state = campaign.state || {};
  return {
    row,
    index: i,
    action: row.action || {},
    observations: observations(row),
    status:
      row.transaction_status ||
      row.environment_outcome?.transaction_status ||
      "unknown",
    resources: state.report_only || {},
    remaining: state.remaining || {},
    operational:
      views.tool_json?.operational_state ||
      report.operational_state ||
      report.public_operational_state ||
      {},
    delta: row.state_delta_summary || {},
    method: row.method_resources || {},
    completed: row.terminated === true || row.truncated === true,
  };
}
export function metricSeries(records, key, through = records.length - 1) {
  return records.map((row, i) => ({
    step: i + 1,
    value: i <= through ? (observations(row)[key] ?? null) : null,
  }));
}

export function isFinalAssay(row) {
  return (
    row?.action?.instrument === "final_assay" &&
    (row.transaction_status || row.environment_outcome?.transaction_status) ===
      "committed"
  );
}

export function experiments(records) {
  // Lifecycle indices are identities, not assumed 0/1-based display ordinals.
  const groups = [];
  for (let i = 0; i < records.length; i++) {
    const row = records[i],
      previous = records[i - 1];
    const changed =
      !previous ||
      ["campaign_id", "experiment_index"].some(
        (k) => row[k] != null && previous[k] != null && row[k] !== previous[k],
      ) ||
      isFinalAssay(previous);
    if (changed)
      groups.push({
        ordinal: groups.length + 1,
        start: i,
        end: i,
        identity: row.experiment_index ?? null,
        campaign: row.campaign_id ?? null,
        indices: [],
        finalIndex: null,
        failed: 0,
        measurements: 0,
        cost: null,
        time: null,
        decisionNotes: 0,
      });
    const group = groups.at(-1);
    group.end = i;
    group.indices.push(i);
    const status =
      row.transaction_status || row.environment_outcome?.transaction_status;
    if (status && !["committed", "unknown"].includes(status)) group.failed++;
    if (row.action?.operation === "measure") group.measurements++;
    if (isFinalAssay(row)) group.finalIndex = i;
    const delta = row.state_delta_summary || {};
    for (const [key, field] of [
      ["cost", "delta_cost"],
      ["time", "delta_time_s"],
    ])
      if (finite(delta[field])) group[key] = (group[key] ?? 0) + delta[field];
    const audit = stepIO(records, i).audit;
    if (audit) group.decisionNotes++;
  }
  for (const group of groups) {
    group.metrics =
      group.finalIndex === null ? {} : observations(records[group.finalIndex]);
    const last = records[group.end];
    const outcome = last.explanation?.outcome || {};
    group.status =
      group.finalIndex !== null
        ? "assayed"
        : outcome.batch_discarded ||
            last.action?.operation === "discard_experiment"
          ? "discarded"
          : "prefix";
    group.steps = group.indices.length;
  }
  return groups;
}

export function stepIO(records, index) {
  const row = records[index],
    explanation = row.explanation || {};
  const trace = Array.isArray(row.agent_trace) ? row.agent_trace : [];
  const sameAction = (t) =>
    JSON.stringify(t.action) === JSON.stringify(row.action);
  const matched = trace.filter(
    (t) =>
      t &&
      row.step != null &&
      (t.expected_step === row.step || t.step === row.step),
  );
  const unnumbered = trace.filter(
    (t) => t && t.expected_step == null && t.step == null,
  );
  const current =
    matched.at(-1) ||
    unnumbered.filter(sameAction).at(-1) ||
    (trace.length === 1 && unnumbered.length === 1 && !trace[0].action
      ? trace[0]
      : null);
  let audit = current?.decision_audit || explanation.decision_audit;
  if (
    !audit &&
    current &&
    (current.expected_effect || current.diagnostic_target)
  )
    audit = current;
  if (
    !audit ||
    audit.status === "not_provided" ||
    !(
      audit.expected_effect ||
      audit.diagnostic_target ||
      audit.rationale ||
      audit.reasoning ||
      audit.belief_update_rule
    )
  )
    audit = null;
  const request = current?.request || row.model_input;
  const messages =
    current?.messages ||
    current?.input_messages ||
    row.input_messages ||
    request?.messages;
  const prompt = current?.user_prompt || current?.prompt || row.prompt;
  const context = explanation.decision_context || null;
  let input = messages || request || prompt || context;
  let inputKind =
    messages || request || prompt
      ? "recorded_request"
      : context
        ? "decision_context"
        : "missing";
  if (!input && index > 0) {
    const before = records[index - 1];
    if (
      before.campaign_id === row.campaign_id &&
      before.experiment_index === row.experiment_index &&
      !isFinalAssay(before)
    ) {
      input = before.agent_visible_observation || {
        observation: observations(before),
      };
      inputKind = "previous_observation";
    }
  }
  const output =
    current?.response ||
    current?.model_output ||
    current?.completion ||
    (current
      ? { action: current.action || row.action, decision_audit: audit }
      : null);
  const tool = current?.outcome ||
    explanation.outcome ||
    row.environment_outcome || {
      observation: observations(row),
      transaction_status: row.transaction_status,
      reward: row.reward,
    };
  const metadata = row.agent_metadata || {};
  const usage = row.method_resources?.agent_usage || {};
  const provenance = usage.model_provenance || metadata.model_provenance || {};
  return {
    step: row.step ?? index + 1,
    action: row.action,
    input,
    inputKind,
    output,
    audit,
    tool,
    trace: current,
    model:
      metadata.provider_model ||
      metadata.model ||
      provenance.model ||
      metadata.agent_name ||
      "未声明控制器",
    scripted:
      metadata.requires_online_model === false ||
      (metadata.interaction_capabilities?.adapts_within_experiment === false &&
        !trace.length),
    exactPrompt: Boolean(messages || request || prompt),
    requestId: current?.request_id || current?.provider_request_id || null,
    sessionId: current?.session_id || null,
  };
}

export function changedConditions(records, group, previous) {
  const conditions = (g) => {
    const result = {};
    for (const i of g?.indices || [])
      for (const [key, value] of Object.entries(records[i].action || {}))
        if (
          !["operation", "instrument"].includes(key) &&
          value !== null &&
          typeof value !== "object"
        )
          (result[`${records[i].action.operation}.${key}`] ||= []).push(value);
    return result;
  };
  const current = conditions(group),
    before = conditions(previous);
  return [...new Set([...Object.keys(current), ...Object.keys(before)])]
    .filter(
      (k) =>
        !previous || JSON.stringify(before[k]) !== JSON.stringify(current[k]),
    )
    .map((key) => ({
      key,
      value: current[key] ?? null,
      previous: before[key] ?? null,
    }));
}
export function classify(value, categories) {
  const found = new Set();
  const patterns = categories.map((c) => [
    c.id,
    c.tasks.map((task) => new RegExp(`(^|[^a-z])${task}([^a-z]|$)`)),
  ]);
  function visit(v) {
    if (v && typeof v === "object" && !Array.isArray(v) && v.action) {
      visit([
        v.task_id,
        v.benchmark_task_id,
        v.explanation?.decision_context?.task_id,
      ]);
      return;
    }
    if (typeof v === "string") {
      for (const [id, tests] of patterns)
        if (tests.some((re) => re.test(v))) found.add(id);
    } else if (Array.isArray(v)) v.forEach(visit);
    else if (v && typeof v === "object")
      for (const [key, child] of Object.entries(v)) {
        visit(key);
        visit(child);
      }
  }
  visit(value);
  return found.size
    ? categories.filter((c) => found.has(c.id)).map((c) => c.id)
    : ["other"];
}

export function scalarColumns(row, prefix = "", depth = 0) {
  if (!row || typeof row !== "object" || Array.isArray(row)) return {};
  const result = {};
  for (const [key, value] of Object.entries(row)) {
    const path = prefix ? `${prefix}.${key}` : key;
    if (
      value === null ||
      ["number", "string", "boolean"].includes(typeof value)
    )
      result[path] = value;
    else if (!Array.isArray(value) && depth < 2)
      Object.assign(result, scalarColumns(value, path, depth + 1));
  }
  return result;
}
export function datasets(report) {
  const output = [];
  function visit(value, path, depth) {
    if (depth > 4 || !value || typeof value !== "object") return;
    if (Array.isArray(value)) {
      if (
        value.length &&
        value.some((x) => x && typeof x === "object" && !Array.isArray(x))
      )
        output.push({
          name: path,
          rows: value.filter(
            (x) => x && typeof x === "object" && !Array.isArray(x),
          ),
        });
      return;
    }
    for (const [key, child] of Object.entries(value))
      visit(child, path ? `${path}.${key}` : key, depth + 1);
  }
  visit(report, "", 0);
  return output;
}
export function numericMetrics(report) {
  const result = [];
  for (const [key, value] of Object.entries(report)) {
    if (finite(value)) result.push({ key, value });
    else if (
      ["counts", "denominators", "physical_runs", "model_calls"].includes(key)
    ) {
      for (const [k, v] of Object.entries(scalarColumns(value, key)))
        if (finite(v)) result.push({ key: k, value: v });
    }
  }
  return result;
}
export function csv(rows, columns) {
  const cell = (v) => `"${String(v ?? "").replaceAll('"', '""')}"`;
  return (
    "\uFEFF" +
    [
      columns.map(cell).join(","),
      ...rows.map((row) => columns.map((k) => cell(row[k])).join(",")),
    ].join("\r\n")
  );
}
