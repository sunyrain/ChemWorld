const app = {
  tasks: [],
  quickTasks: [],
  results: [],
  series: {},
  currentTask: null,
  eventCount: 0,
  job: null,
  spectrum: null,
  spectrumHistory: [],
  spectrumHistoryIndex: -1,
  spectrumHistoryKeys: new Set(),
};

const $ = (selector) => document.querySelector(selector);
const all = (selector) => [...document.querySelectorAll(selector)];
const fmt = (value, digits = 4) => value === null || value === undefined ? "—" : Number(value).toFixed(digits);
const esc = (value) => String(value ?? "").replaceAll("&", "&amp;").replaceAll("<", "&lt;").replaceAll(">", "&gt;").replaceAll('"', "&quot;").replaceAll("'", "&#039;");

document.addEventListener("DOMContentLoaded", async () => {
  wireControls();
  drawLineChart([]);
  app.spectrum = ChemWorldSpectra.mount({ canvas: $("#agentSpectrum"), tabs: $("#agentSpectrumTabs"), peaks: $("#agentSpectrumPeaks"), empty: $("#agentSpectrumEmpty"), meta: $("#agentSpectrumMeta"), theme: "dark" });
  try {
    const [payload, runtime] = await Promise.all([api("/api/tasks"), api("/api/status")]);
    app.tasks = payload.tasks;
    app.quickTasks = payload.quick_tasks;
    renderTaskChecklist();
    applyPreset("all");
    updateBackendControls();
    showDossier(app.tasks[0]);
    renderRuntimeStatus(runtime);
  } catch (error) {
    $("#apiState").textContent = `Runtime error: ${error.message}`;
  }
});

function wireControls() {
  all(".preset").forEach((button) => button.addEventListener("click", () => applyPreset(button.dataset.preset)));
  $("#taskSearch").addEventListener("input", filterTasks);
  $("#toggleTasks").addEventListener("click", invertTasks);
  $("#startRun").addEventListener("click", startRun);
  $("#exportResults").addEventListener("click", exportResults);
  $("#agentBackend").addEventListener("change", updateBackendControls);
  $("#budgetMultiplier").addEventListener("change", updateContractNotice);
  $("#campaignOverride").addEventListener("change", updateContractNotice);
  $("#spectrumHistoryPrev").addEventListener("click", () => showSpectrumSnapshot(app.spectrumHistoryIndex - 1));
  $("#spectrumHistoryNext").addEventListener("click", () => showSpectrumSnapshot(app.spectrumHistoryIndex + 1));
  $("#agentSpectrumHistory").addEventListener("change", (event) => showSpectrumSnapshot(Number(event.target.value)));
}

function renderTaskChecklist() {
  $("#taskChecklist").innerHTML = app.tasks.map((task) => `
    <label class="task-check" data-task-id="${esc(task.task_id)}" data-compatible="${task.classic_active_learning_compatible ? "true" : "false"}" data-search="${esc(`${task.task_id} ${task.title}`.toLowerCase())}">
      <input type="checkbox" name="taskScope" value="${esc(task.task_id)}">
      <span><strong>${esc(task.title)}</strong><small>${esc(task.task_id)}</small></span>
      <em>${esc(task.physics_maturity)}</em>
    </label>`).join("");
  all('input[name="taskScope"]').forEach((input) => {
    input.addEventListener("change", updateSelectedCount);
    input.closest(".task-check").addEventListener("mouseenter", () => showDossier(taskById(input.value)));
  });
}

function applyPreset(name) {
  const classic = $("#agentBackend")?.value !== "deepseek";
  all(".preset").forEach((button) => button.classList.toggle("active", button.dataset.preset === name));
  all('input[name="taskScope"]').forEach((input) => {
    const task = taskById(input.value);
    const matches = name === "all" || (name === "quick" && app.quickTasks.includes(input.value)) ||
      (name === "serious" && task.suite_memberships.includes("serious"));
    input.checked = matches && (!classic || task.classic_active_learning_compatible);
  });
  updateSelectedCount();
}

function filterTasks() {
  const query = $("#taskSearch").value.trim().toLowerCase();
  all(".task-check").forEach((label) => label.classList.toggle("hidden", query && !label.dataset.search.includes(query)));
}

function invertTasks() {
  all('.task-check:not(.hidden) input[name="taskScope"]:not(:disabled)').forEach((input) => { input.checked = !input.checked; });
  updateSelectedCount();
}

function updateSelectedCount() {
  $("#selectedCount").textContent = selectedTasks().length;
}

function selectedTasks() {
  return all('input[name="taskScope"]:checked').map((input) => input.value);
}

async function startRun() {
  const tasks = selectedTasks();
  if (!tasks.length) return setStatus("ERROR", "Select at least one task");
  resetRun(tasks.length);
  const button = $("#startRun");
  button.disabled = true;
  try {
    const payload = {
      tasks,
      agent_backend: $("#agentBackend").value,
      mode: $("#runMode").value,
      model: $("#modelName").value.trim(),
      max_steps: Number($("#maxSteps").value),
      budget_multiplier: Number($("#budgetMultiplier").value),
      campaign_override: $("#campaignOverride").checked,
      thinking: $("#thinkingMode").checked,
      reasoning_effort: $("#reasoningEffort").value,
      spectrum_disclosure: $("#spectrumDisclosure").value,
    };
    if ($("#runSeed").value !== "") payload.seed = Number($("#runSeed").value);
    app.job = await api("/api/runs", { method: "POST", body: payload });
    setStatus("RUNNING", app.job.model);
    const source = new EventSource(`/api/runs/${app.job.job_id}/events`);
    source.onmessage = (message) => handleEvent(JSON.parse(message.data), source, button);
    source.onerror = () => {
      if (source.readyState === EventSource.CLOSED) button.disabled = false;
    };
  } catch (error) {
    setStatus("ERROR", $("#modelName").value);
    addTelemetry("error", "启动失败", error.message);
    button.disabled = false;
  }
}

function resetRun(taskCount) {
  app.results = [];
  app.series = {};
  app.currentTask = null;
  app.eventCount = 0;
  app.spectrumHistory = [];
  app.spectrumHistoryIndex = -1;
  app.spectrumHistoryKeys = new Set();
  app.spectrum?.render(null);
  $("#agentSpectrumContext").textContent = "Awaiting signal";
  $("#agentSpectrumInstrument").textContent = "No signal";
  $("#liveVessel").textContent = "Awaiting task";
  renderSpectrumHistoryControls();
  renderDecisionAudit(null);
  $("#agentTimeline").innerHTML = "";
  $("#scoreTable").innerHTML = '<tr><td colspan="10"><div class="empty-table">评测运行中...</div></td></tr>';
  $("#kpiCompleted").textContent = `0 / ${taskCount}`;
  $("#kpiCoverage").textContent = "0% coverage";
  $("#kpiAverage").textContent = "—";
  $("#kpiTokens").textContent = "0";
  $("#kpiCalls").textContent = "0 model calls";
  $("#kpiValidity").textContent = "—";
  $("#exportResults").disabled = true;
  updateEventCount();
}

function handleEvent(event, source, button) {
  app.eventCount += 1;
  updateEventCount();
  if (event.type === "run_started") {
    addTelemetry("run", "全局运行开始", `${event.tasks.length} tasks · ${event.agent_backend} · spectrum ${event.spectrum_disclosure} · ${event.budget_multiplier}× budget · campaign ${event.campaign_override ? "on" : "off"}`);
  } else if (event.type === "task_started") {
    app.currentTask = taskById(event.task_id);
    app.series[event.task_id] = [];
    $("#currentTask").textContent = event.background.title;
    $("#currentTaskId").textContent = event.task_id;
    $("#chartTask").textContent = event.task_id;
    $("#orbLimit").textContent = `/ ${event.step_limit} steps`;
    $("#currentAction").textContent = event.mode === "adaptive" ? "Reading observations" : "Generating baseline plan";
    $("#currentRationale").textContent = event.background.background;
    showDossier(app.currentTask);
    updateLiveProgress(0, event.step_limit, null, 0, event.budget);
    renderVesselState({ episode_mode: event.episode_mode, experiment_index: 0 });
    drawLineChart([]);
    const profile = event.contract_profile === "official" ? "official" : "extended research";
    addTelemetry("task", event.background.title, `seed ${event.seed} · ${profile} · budget ${event.official_budget} → ${event.budget}`);
  } else if (event.type === "plan_ready") {
    $("#currentAction").textContent = `${event.planned_action_count} operations planned`;
    $("#currentRationale").textContent = event.strategy_summary || "Plan accepted by orchestrator.";
    addTelemetry("plan", "规划已生成", `${event.planned_action_count} steps · ${event.strategy_summary || "ready"}`);
  } else if (event.type === "spectrum_requested") {
    $("#currentAction").textContent = "Requesting spectrum";
    $("#currentRationale").textContent = `模型主动请求 ${event.spectrum_id}`;
    addTelemetry("decision", `谱图请求 ${event.request_index}`, event.spectrum_id);
  } else if (event.type === "spectrum_retrieved") {
    recordSpectrumSnapshot({
      event,
      spectrum: event.spectrum,
      source: "model-input",
      context: `MODEL RETRIEVAL · DECISION ${event.step}`,
    });
    addTelemetry("decision", "谱图已按需提供", `${event.spectrum_id} · 未自动附带其他历史谱图`);
  } else if (event.type === "spectrum_unavailable") {
    addTelemetry("warn", "谱图请求无效", `${event.spectrum_id} 不在可获取目录中`);
  } else if (event.type === "decision_ready") {
    $("#currentAction").textContent = event.action.operation;
    $("#currentRationale").textContent = event.rationale;
    renderDecisionAudit(event);
    renderModelInputSpectrum(event);
    renderVesselState(event);
    const inputSeries = event.spectrum_input?.series?.length || 0;
    addTelemetry("decision", `Decision ${event.step} · ${event.action.operation}`, `${event.experiment_intent || "decision"} · ${inputSeries ? `${inputSeries} supplied signal channel(s)` : "no spectrum supplied"} · ${event.evidence?.[0] || "public evidence reviewed"} · uncertainty ${fmt(event.uncertainty, 2)}`);
  } else if (event.type === "surrogate_decision") {
    $("#currentAction").textContent = `${event.phase} · ${event.selected_policy}`;
    $("#currentRationale").textContent = event.rationale;
    renderDecisionAudit(event);
    const acquisition = event.acquisition_value === null || event.acquisition_value === undefined ? "initial design" : `acquisition ${fmt(event.acquisition_value, 5)}`;
    addTelemetry("decision", `${event.selected_policy} · recipe ${event.trained_recipe_count + 1}`, `${event.trained_recipe_count} learned experiments · ${acquisition}`);
  } else if (event.type === "experiment_learned") {
    const conditionCount = event.conditions?.length || 0;
    const design = event.design_audit?.classification || "baseline";
    const changed = event.design_audit?.changed_factors?.map((item) => item.factor).join(", ") || "initial conditions";
    addTelemetry("score", `Experiment ${event.experiment_index + 1} learned`, `score ${fmt(event.final_score)} · ${design} · ${changed} · ${conditionCount} conditions · best ${fmt(event.best_score)}`);
  } else if (event.type === "action_rejected") {
    addTelemetry("warn", "动作被验证器拒绝", `${event.action.operation} · ${(event.reasons || []).join(", ")}`);
  } else if (event.type === "action_skipped") {
    addTelemetry("error", "动作修正失败", `${event.action.operation} · ${(event.reasons || []).join(", ")}`);
  } else if (event.type === "decision_fallback") {
    addTelemetry("warn", "重复非法决策已熔断", `${event.action.operation} · ${event.reason}`);
  } else if (event.type === "decision_loop_stopped") {
    addTelemetry("error", "决策循环已停止", event.reason);
  } else if (event.type === "model_call_failed") {
    addTelemetry("warn", "模型调用失败，进入协议闭环", event.error);
  } else if (event.type === "closeout_action") {
    addTelemetry("plan", "评测闭环", `${event.action.operation} · ${event.reason}`);
  } else if (event.type === "step_completed") {
    const value = Number(event.best_score ?? event.leaderboard_score ?? event.reward ?? 0);
    app.series[event.task_id].push(value);
    $("#currentAction").textContent = event.action.operation;
    $("#currentRationale").textContent = event.rationale;
    if (event.spectrum?.available) {
      recordSpectrumSnapshot({
        event,
        spectrum: event.spectrum,
        source: "measurement",
        context: `MEASUREMENT OUTPUT · STEP ${event.step}`,
      });
    }
    renderVesselState(event);
    updateLiveProgress(event.step, event.step_limit, event.best_score, event.final_assay_count, event.remaining_budget);
    drawLineChart(app.series[event.task_id]);
    addTelemetry(event.status === "accepted" ? "step" : "warn", `Step ${event.step} · ${event.action.operation}`, `reward ${fmt(event.reward)} · best ${fmt(event.best_score)} · ${event.hypothesis}`);
  } else if (event.type === "task_completed") {
    app.results.push(event);
    renderResults();
    updateKpis();
    const score = event.official_score ?? event.research_score;
    addTelemetry(event.status.startsWith("scored") ? "score" : "warn", `${taskById(event.task_id).title} 完成`, `${event.contract_profile} ${fmt(score)} · ${event.experiment_count} experiments · ${event.steps} steps`);
  } else if (event.type === "run_completed") {
    setStatus("COMPLETED", app.job.model);
    addTelemetry("done", "全量评测完成", `${event.results.length} task results are replay verified.`);
    source.close();
    button.disabled = false;
    $("#exportResults").disabled = false;
  } else if (event.type === "run_failed") {
    setStatus("ERROR", app.job?.model || "runtime");
    addTelemetry("error", "运行失败", event.error);
    source.close();
    button.disabled = false;
  }
}

function setStatus(status, model) {
  $("#runStatus").textContent = status;
  $("#runModel").textContent = model;
  $("#runModel").closest(".run-badge").classList.toggle("running", status === "RUNNING");
}

function updateLiveProgress(step, limit, best, assays, remaining) {
  const degrees = Math.min(360, step / Math.max(limit, 1) * 360);
  $("#progressOrb").style.setProperty("--progress", `${degrees}deg`);
  $("#orbStep").textContent = step;
  $("#liveBest").textContent = fmt(best);
  $("#liveAssays").textContent = assays ?? 0;
  $("#liveBudget").textContent = remaining ?? "—";
}

function addTelemetry(kind, title, detail) {
  const item = document.createElement("div");
  item.className = `telemetry-item ${kind === "warn" ? "warn" : kind === "error" ? "error" : ""}`;
  const symbol = { run: "R", task: "T", plan: "P", decision: "D", step: "→", score: "S", done: "✓", warn: "!", error: "×" }[kind] || "·";
  item.innerHTML = `<span class="event-symbol">${symbol}</span><div><strong>${esc(title)}</strong><p>${esc(detail)}</p><time>${new Date().toLocaleTimeString()}</time></div>`;
  $("#agentTimeline").prepend(item);
}

function renderDecisionAudit(event) {
  const analysis = event?.analysis || event || {};
  const evidence = analysis?.evidence?.length ? analysis.evidence : ["等待模型读取公开观测"];
  $("#decisionEvidence").innerHTML = evidence.map((item) => `<li>${esc(item)}</li>`).join("");
  $("#decisionSpectrum").textContent = analysis?.spectrum_interpretation || "尚无谱图解读。";
  $("#decisionHypothesis").textContent = analysis?.hypothesis || "尚未建立实验假设。";
  $("#decisionRationale").textContent = analysis?.rationale || "启动多轮评测后显示。";
  $("#decisionIntent").textContent = analysis?.experiment_intent || "尚未分类。";
  $("#decisionComparison").textContent = analysis?.comparison_to_prior || "尚无可比较实验。";
  $("#decisionOrigin").textContent = decisionOriginLabel(event?.decision_origin);
  const uncertainty = analysis?.uncertainty;
  $("#decisionUncertainty").textContent = uncertainty === undefined || uncertainty === null ? "—" : `${(Number(uncertainty) * 100).toFixed(0)}%`;
  $("#decisionUncertaintyBar").style.width = `${Math.max(0, Math.min(1, Number(uncertainty ?? 0))) * 100}%`;
  $("#decisionUncertaintyNote").textContent = analysis?.uncertainty_note || "模型将报告主要不确定性来源；隐藏逐字思维链不会被采集。";
}

function renderModelInputSpectrum(event) {
  const spectrum = event?.spectrum_input;
  if (spectrum?.available) {
    recordSpectrumSnapshot({
      event,
      spectrum,
      source: "model-input",
      context: `MODEL INPUT · DECISION ${event.step}`,
    });
    return;
  }
  app.spectrum?.render(null);
  $("#agentSpectrumContext").textContent = `MODEL INPUT · NO SPECTRUM · DECISION ${event.step}`;
  $("#agentSpectrumInstrument").textContent = "No signal supplied";
}

function recordSpectrumSnapshot({ event, spectrum, source, context }) {
  if (!spectrum?.available) return;
  const identity = spectrum.spectrum_id || `${event.index ?? app.eventCount}`;
  const key = `${event.task_id || app.currentTask?.task_id || "task"}:${identity}:${source}`;
  if (app.spectrumHistoryKeys.has(key)) return;
  app.spectrumHistoryKeys.add(key);
  app.spectrumHistory.push({
    key,
    taskId: event.task_id || app.currentTask?.task_id || "task",
    step: Number(event.step || 0),
    experimentIndex: Number(spectrum.provenance?.experiment_index ?? event.action_experiment_index ?? event.experiment_index ?? 0),
    source,
    context,
    instrument: spectrum.instrument || spectrum.kind || "Public signal",
    spectrum,
  });
  renderSpectrumHistoryControls();
  showSpectrumSnapshot(app.spectrumHistory.length - 1);
}

function showSpectrumSnapshot(index) {
  if (!app.spectrumHistory.length) return;
  const bounded = Math.max(0, Math.min(app.spectrumHistory.length - 1, Number(index)));
  const entry = app.spectrumHistory[bounded];
  app.spectrumHistoryIndex = bounded;
  app.spectrum?.render(entry.spectrum);
  $("#agentSpectrumContext").textContent = entry.context;
  $("#agentSpectrumInstrument").textContent = entry.instrument;
  $("#agentSpectrumHistory").value = String(bounded);
  $("#spectrumHistoryCount").textContent = `${bounded + 1} / ${app.spectrumHistory.length}`;
  $("#spectrumHistoryPrev").disabled = bounded === 0;
  $("#spectrumHistoryNext").disabled = bounded === app.spectrumHistory.length - 1;
}

function renderSpectrumHistoryControls() {
  const select = $("#agentSpectrumHistory");
  if (!app.spectrumHistory.length) {
    select.innerHTML = '<option value="">尚无谱图</option>';
    select.disabled = true;
    $("#spectrumHistoryPrev").disabled = true;
    $("#spectrumHistoryNext").disabled = true;
    $("#spectrumHistoryCount").textContent = "0 / 0";
    return;
  }
  select.disabled = false;
  select.innerHTML = app.spectrumHistory.map((entry, index) => {
    const source = entry.source === "model-input" ? "模型输入" : "测量输出";
    const experiment = `E${entry.experimentIndex + 1}`;
    return `<option value="${index}">${esc(entry.taskId)} · ${experiment} · Step ${entry.step} · ${source} · ${esc(entry.instrument)}</option>`;
  }).join("");
}

function renderVesselState(event) {
  const experiment = Number(event?.experiment_index ?? 0) + 1;
  const fresh = event?.experiment_transition === "reset_for_next_experiment";
  const mode = event?.episode_mode === "campaign" ? "campaign" : "single";
  $("#liveVessel").textContent = `E${experiment} · ${fresh ? "fresh vessel" : "cumulative"} · ${mode}`;
}

function decisionOriginLabel(origin) {
  return {
    online_model: "MODEL RESPONSE",
    online_model_repair: "MODEL REPAIR",
    model_plan: "MODEL PLAN",
    protocol_closeout: "PROTOCOL CLOSEOUT",
    protocol_closeout_after_model_failure: "MODEL FAILURE · CLOSEOUT",
    protocol_fallback_after_invalid_model: "INVALID MODEL · FALLBACK",
  }[origin] || "AWAITING MODEL";
}

function renderRuntimeStatus(runtime) {
  const configured = Boolean(runtime?.deepseek_configured);
  $("#apiState").textContent = configured
    ? `Local runtime · DeepSeek ready (${runtime.credential_source})`
    : "Local runtime · DeepSeek key missing";
}

function updateEventCount() {
  $("#eventCount").textContent = `${app.eventCount} events`;
}

function updateKpis() {
  const target = selectedTasks().length;
  const official = app.results.filter((result) => result.official_score !== null);
  const research = app.results.filter((result) => result.research_score !== null);
  const scored = official.length ? official : research;
  const scoreKey = official.length ? "official_score" : "research_score";
  const average = scored.length ? scored.reduce((sum, item) => sum + Number(item[scoreKey]), 0) / scored.length : null;
  const tokens = app.results.reduce((sum, item) => sum + Number(item.usage?.total_tokens || 0), 0);
  const calls = app.results.reduce((sum, item) => sum + Number(item.model_call_count || 0), 0);
  const valid = app.results.length ? app.results.filter((item) => item.invalid_plan_actions === 0).length / app.results.length : null;
  $("#kpiCompleted").textContent = `${app.results.length} / ${target}`;
  $("#kpiCoverage").textContent = `${Math.round(app.results.length / Math.max(target, 1) * 100)}% coverage`;
  $("#kpiAverage").textContent = fmt(average);
  $("#kpiScoreLabel").textContent = official.length ? "平均 Official" : "平均 Research";
  $("#kpiScoreNote").textContent = official.length ? "官方任务契约" : "扩展结果与官方榜单隔离";
  $("#kpiTokens").textContent = tokens.toLocaleString();
  $("#kpiCalls").textContent = `${calls} model calls`;
  $("#kpiValidity").textContent = valid === null ? "—" : `${(valid * 100).toFixed(0)}%`;
}

function renderResults() {
  const ranked = [...app.results].sort((a, b) => Number(b.official_score ?? b.research_score ?? -1) - Number(a.official_score ?? a.research_score ?? -1));
  $("#scoreTable").innerHTML = ranked.map((result, index) => {
    const task = taskById(result.task_id);
    const valid = result.invalid_plan_actions === 0;
    return `<tr data-task-id="${esc(result.task_id)}"><td>${index + 1}</td><td><span class="task-cell"><strong>${esc(task.title)}</strong><small>${esc(result.task_id)}</small></span></td><td><span class="score-value">${fmt(result.official_score)}</span></td><td><span class="score-value">${fmt(result.research_score)}</span></td><td>${fmt(result.total_score)}</td><td>${result.experiment_count ?? result.final_assay_count}</td><td>${result.steps}</td><td>${Number(result.usage?.total_tokens || 0).toLocaleString()}</td><td>${valid ? "100%" : `${result.invalid_plan_actions} rejected`}</td><td><span class="status-chip ${result.status.startsWith("scored") ? "" : "warn"}">${esc(result.status)}</span></td></tr>`;
  }).join("");
  all("#scoreTable tr").forEach((row) => row.addEventListener("mouseenter", () => showDossier(taskById(row.dataset.taskId))));
}

function showDossier(task) {
  if (!task) return;
  $("#dossierTitle").textContent = task.title;
  $("#dossierMaturity").textContent = task.physics_maturity;
  $("#dossierBackground").textContent = task.background;
  $("#dossierGoal").textContent = task.student_goal;
  $("#dossierChallenge").textContent = task.challenge;
  $("#dossierScore").textContent = task.score_note;
  $("#dossierMetrics").innerHTML = task.success_metrics.map((metric) => `<span>${esc(metric)}</span>`).join("");
}

function exportResults() {
  const payload = {
    generated_at: new Date().toISOString(),
    job: app.job,
    results: app.results,
    spectrum_history: app.spectrumHistory,
  };
  const url = URL.createObjectURL(new Blob([JSON.stringify(payload, null, 2)], { type: "application/json" }));
  const link = document.createElement("a");
  link.href = url;
  link.download = `chemworld-agent-results-${Date.now()}.json`;
  link.click();
  URL.revokeObjectURL(url);
}

function drawLineChart(values) {
  const canvas = $("#agentChart");
  const context = canvas.getContext("2d");
  const width = canvas.width, height = canvas.height;
  context.clearRect(0, 0, width, height);
  context.strokeStyle = "rgba(153,207,215,.09)";
  context.lineWidth = 1;
  for (let i = 1; i < 5; i += 1) { const y = i * height / 5; context.beginPath(); context.moveTo(35, y); context.lineTo(width - 15, y); context.stroke(); }
  context.fillStyle = "#557681"; context.font = "11px system-ui"; context.fillText("1.0", 6, 17); context.fillText("0.0", 6, height - 12);
  if (!values.length) return;
  const gradient = context.createLinearGradient(0, 0, width, 0); gradient.addColorStop(0, "#19c6ab"); gradient.addColorStop(1, "#42bdf5");
  context.strokeStyle = gradient; context.lineWidth = 3; context.beginPath();
  values.forEach((value, index) => { const x = 35 + index / Math.max(values.length - 1, 1) * (width - 55); const y = height - 18 - Math.max(0, Math.min(1, value)) * (height - 35); index ? context.lineTo(x, y) : context.moveTo(x, y); });
  context.stroke();
}

function taskById(taskId) { return app.tasks.find((task) => task.task_id === taskId); }

function updateBackendControls() {
  const classic = $("#agentBackend").value !== "deepseek";
  $("#runMode").disabled = classic;
  $("#modelName").disabled = classic;
  $("#thinkingMode").disabled = classic;
  $("#reasoningEffort").disabled = classic;
  all(".task-check").forEach((label) => {
    const incompatible = classic && label.dataset.compatible !== "true";
    label.classList.toggle("incompatible", incompatible);
    const input = label.querySelector('input[name="taskScope"]');
    input.disabled = incompatible;
    if (incompatible) input.checked = false;
  });
  updateSelectedCount();
  updateContractNotice();
}

function updateContractNotice() {
  const multiplier = Number($("#budgetMultiplier").value);
  const campaign = $("#campaignOverride").checked;
  const extended = multiplier > 1 || campaign;
  $("#contractNotice").textContent = extended
    ? `EXTENDED RESEARCH · ${multiplier}× budget · campaign ${campaign ? "on" : "off"} · non-official score`
    : "OFFICIAL CONTRACT · frozen budget and episode semantics";
}

async function api(url, options = {}) {
  const response = await fetch(url, { method: options.method || "GET", headers: { "Content-Type": "application/json" }, body: options.body === undefined ? undefined : JSON.stringify(options.body) });
  const payload = await response.json();
  if (!response.ok) throw new Error(payload.error || `HTTP ${response.status}`);
  return payload;
}
