const lab = {
  tasks: [],
  session: null,
  affordance: null,
  spectrum: null,
  spectrumHistory: [],
  spectrumHistoryIndex: -1,
};

const $ = (selector) => document.querySelector(selector);
const fmt = (value, digits = 4) => value === null || value === undefined ? "—" : Number(value).toFixed(digits);
const esc = (value) => String(value ?? "").replaceAll("&", "&amp;").replaceAll("<", "&lt;").replaceAll(">", "&gt;").replaceAll('"', "&quot;").replaceAll("'", "&#039;");

document.addEventListener("DOMContentLoaded", async () => {
  wireLab();
  drawLearningCurve([]);
  lab.spectrum = ChemWorldSpectra.mount({ canvas: $("#studentSpectrum"), tabs: $("#studentSpectrumTabs"), peaks: $("#studentSpectrumPeaks"), empty: $("#studentSpectrumEmpty"), meta: $("#studentSpectrumMeta"), theme: "light" });
  try {
    const payload = await api("/api/tasks");
    lab.tasks = payload.tasks;
    $("#studentTask").innerHTML = lab.tasks.map((task) => `<option value="${esc(task.task_id)}">${esc(task.title)}</option>`).join("");
    previewMission(currentTask());
    const sessionId = new URLSearchParams(window.location.search).get("session");
    if (sessionId) {
      const session = await api(`/api/student-sessions/${encodeURIComponent(sessionId)}`);
      $("#studentTask").value = session.task_id;
      $("#studentSeed").value = session.seed;
  renderSession(session);
    }
  } catch (error) {
    showValidation(false, error.message);
  }
});

function wireLab() {
  $("#studentTask").addEventListener("change", () => previewMission(currentTask()));
  $("#createSession").addEventListener("click", createSession);
  $("#operationSelect").addEventListener("change", renderOperationFields);
  $("#submitAction").addEventListener("click", submitAction);
  $("#downloadNotebook").addEventListener("click", downloadNotebook);
  $("#studentSpectrumHistoryPrev").addEventListener("click", () => showStudentSpectrumSnapshot(lab.spectrumHistoryIndex - 1));
  $("#studentSpectrumHistoryNext").addEventListener("click", () => showStudentSpectrumSnapshot(lab.spectrumHistoryIndex + 1));
  $("#studentSpectrumHistory").addEventListener("change", (event) => showStudentSpectrumSnapshot(Number(event.target.value)));
}

function currentTask() {
  return lab.tasks.find((task) => task.task_id === $("#studentTask").value) || lab.tasks[0];
}

function previewMission(task) {
  if (!task) return;
  $("#missionMaturity").textContent = task.physics_maturity;
  $("#studentBackground").innerHTML = `<h3>${esc(task.title)}</h3><p>${esc(task.background)}</p><p><strong>学习目标</strong><br>${esc(task.student_goal)}</p><p><strong>评分口径</strong><br>${esc(task.score_note)}</p>`;
}

async function createSession() {
  const button = $("#createSession");
  button.disabled = true;
  try {
    const session = await api("/api/student-sessions", {
      method: "POST",
      body: { task_id: $("#studentTask").value, seed: Number($("#studentSeed").value || 0) },
    });
    renderSession(session);
    showValidation(true, "实验已创建。系统只展示当前状态下可执行的合法操作。");
  } catch (error) {
    showValidation(false, error.message);
  } finally {
    button.disabled = false;
  }
}

async function submitAction() {
  if (!lab.session) return;
  const button = $("#submitAction");
  button.disabled = true;
  try {
    const result = await api(`/api/student-sessions/${lab.session.session_id}/actions`, {
      method: "POST",
      body: { action: buildAction() },
    });
    if (result.accepted) {
      showValidation(true, "动作通过验证并已执行。公开观测和实验状态已经更新。");
      if (result.feedback?.message) $("#labFeedback").textContent = result.feedback.message;
    } else {
      showValidation(false, `${result.feedback.message}\n${result.feedback.recovery_suggestion || ""}`);
    }
    renderSession(result.state);
  } catch (error) {
    showValidation(false, error.message);
  } finally {
    if (!lab.session?.done) button.disabled = false;
  }
}

function renderSession(session) {
  lab.session = session;
  const task = lab.tasks.find((item) => item.task_id === session.task_id);
  const campaign = session.campaign_state;
  const history = session.history || [];
  const latest = history.at(-1);
  const visible = latest?.visible_metrics || session.lab_report?.visible_metrics || {};
  previewMission(task);
  $("#sessionCode").textContent = session.session_id.slice(0, 8).toUpperCase();
  $("#sessionState").textContent = session.done ? "Episode completed" : `${task.title} · seed ${session.seed}`;
  $("#experimentBadge").textContent = `Experiment ${campaign.experiment_index + 1}`;
  $("#studentStep").textContent = `${campaign.operation_count} / ${campaign.budget}`;
  $("#studentProgress").style.width = `${campaign.operation_count / Math.max(campaign.budget, 1) * 100}%`;
  $("#remainingBudget").textContent = `${campaign.remaining_budget} remaining`;
  $("#studentBest").textContent = fmt(campaign.best_score);
  $("#studentRisk").textContent = fmt(visible.safety_risk);
  $("#studentCost").textContent = fmt(visible.cost);
  $("#studentAssays").textContent = campaign.final_assay_count ?? 0;
  $("#twinScore").textContent = fmt(campaign.best_score);
  $("#historyCount").textContent = `${history.length} operations`;
  $("#downloadNotebook").disabled = history.length === 0;
  updateDigitalTwin(latest);
  renderActions(session.available_actions, session.done);
  renderMetrics(visible);
  renderHistory(history);
  drawLearningCurve(history.map((item) => Number(item.best_score ?? item.reward ?? 0)));
  renderStudentSpectrumHistory(history);
  const report = session.lab_report || {};
  if (report.text) $("#labFeedback").textContent = report.text;
  const instrument = report.instrument_summary?.instrument;
  $("#reportInstrument").textContent = instrument || "No instrument";
}

function renderStudentSpectrumHistory(history) {
  lab.spectrumHistory = history.filter((item) => item.spectrum?.available).map((item) => ({
    step: Number(item.step || 0),
    experimentIndex: Number(item.experiment_index || 0),
    instrument: item.spectrum.instrument || item.spectrum.kind || "Public signal",
    spectrum: item.spectrum,
  }));
  const select = $("#studentSpectrumHistory");
  if (!lab.spectrumHistory.length) {
    lab.spectrumHistoryIndex = -1;
    lab.spectrum?.render(null);
    $("#studentSpectrumInstrument").textContent = "No signal";
    select.innerHTML = '<option value="">尚无谱图</option>';
    select.disabled = true;
    $("#studentSpectrumHistoryPrev").disabled = true;
    $("#studentSpectrumHistoryNext").disabled = true;
    $("#studentSpectrumHistoryCount").textContent = "0 / 0";
    return;
  }
  select.disabled = false;
  select.innerHTML = lab.spectrumHistory.map((entry, index) => `<option value="${index}">E${entry.experimentIndex + 1} · Step ${entry.step} · ${esc(entry.instrument)}</option>`).join("");
  showStudentSpectrumSnapshot(lab.spectrumHistory.length - 1);
}

function showStudentSpectrumSnapshot(index) {
  if (!lab.spectrumHistory.length) return;
  const bounded = Math.max(0, Math.min(lab.spectrumHistory.length - 1, Number(index)));
  const entry = lab.spectrumHistory[bounded];
  lab.spectrumHistoryIndex = bounded;
  lab.spectrum?.render(entry.spectrum);
  $("#studentSpectrumInstrument").textContent = entry.instrument;
  $("#studentSpectrumHistory").value = String(bounded);
  $("#studentSpectrumHistoryCount").textContent = `${bounded + 1} / ${lab.spectrumHistory.length}`;
  $("#studentSpectrumHistoryPrev").disabled = bounded === 0;
  $("#studentSpectrumHistoryNext").disabled = bounded === lab.spectrumHistory.length - 1;
}

function updateDigitalTwin(latest) {
  const vessel = lab.session?.public_vessel || {};
  const currentExperiment = Number(vessel.experiment_index || 0);
  const currentLatest = Number(latest?.experiment_index ?? -1) === currentExperiment ? latest : null;
  const effect = currentLatest?.state_effects || {};
  const operation = currentLatest?.action?.operation || (latest ? "reset" : "idle");
  const visual = effect.visual || (operation === "reset" ? "reset" : "idle");
  $("#twinStage").dataset.operation = operation;
  $("#twinStage").dataset.visual = visual;
  $("#twinStage").dataset.phase = vessel.phase_active ? "active" : "inactive";
  $("#twinStage").dataset.solid = vessel.solid_active ? "active" : "inactive";
  $("#twinOperation").textContent = operation;
  $("#twinStatus").textContent = currentLatest ? currentLatest.status || "operation applied" : latest ? "New vessel ready" : "Ready for setup";
  $("#twinInstrument").textContent = currentLatest?.spectrum?.instrument || currentLatest?.action?.instrument || "INSTRUMENT";
  const netVolume = Number(vessel.net_volume_delta_L || 0);
  const top = Math.max(22, Math.min(70, 64 - netVolume / 0.1 * 38));
  $("#vesselLiquid").style.inset = `${top}% 4px 4px`;
  $("#effectType").textContent = effect.label_zh || (latest ? "实验边界" : "等待操作");
  $("#effectTitle").textContent = effect.type ? effectTypeLabel(effect.type) : latest ? "新实验使用初始容器" : "当前实验尚未改变";
  $("#effectSummary").textContent = effect.summary_zh || (latest ? "上一实验已完成；当前动画已切换到新容器。" : "动画只反映公开动作与事务增量。");
  $("#effectDeltas").innerHTML = effect.type ? [
    `Δt ${signed(effect.delta_time_s, "s", 0)}`,
    `ΔV ${signed(effect.delta_volume_L, "L", 4)}`,
    `sample ${signed(-Number(effect.sample_delta_L || 0), "L", 4)}`,
    `Δrisk ${signed(effect.delta_risk, "", 3)}`,
  ].map((item) => `<span>${esc(item)}</span>`).join("") : "<span>Δt —</span><span>ΔV —</span><span>sample —</span>";
  $("#vesselRelation").textContent = vessel.vessel_relation === "cumulative" ? `E${currentExperiment + 1} · CUMULATIVE` : `E${currentExperiment + 1} · FRESH VESSEL`;
  $("#vesselLedgerSummary").textContent = `${Number(vessel.operation_count || 0)} actions · visible ΔV ${signed(netVolume, "L", 4)} · elapsed ${fmtDuration(vessel.elapsed_time_delta_s)} · sampled ${Number(vessel.sampled_volume_L || 0).toFixed(4)} L`;
}

function renderActions(actions, done) {
  const select = $("#operationSelect");
  select.innerHTML = actions.map((entry, index) => `<option value="${index}">${esc(entry.operation)}</option>`).join("");
  select.disabled = done || !actions.length;
  $("#submitAction").disabled = done || !actions.length;
  $("#validActionCount").textContent = `${actions.length} valid`;
  lab.session.available_actions = actions;
  renderOperationFields();
}

function renderOperationFields() {
  if (!lab.session) return;
  const index = Number($("#operationSelect").value || 0);
  lab.affordance = lab.session.available_actions[index];
  const fields = lab.affordance?.fields || [];
  renderOperationEffect(lab.affordance?.effect);
  $("#operationFields").innerHTML = fields.map((field) => fieldControl(field)).join("");
  document.querySelectorAll("[data-action-field]").forEach((input) => input.addEventListener("input", updatePreview));
  updatePreview();
}

function renderOperationEffect(effect) {
  const card = $("#operationEffect");
  if (!effect) {
    card.innerHTML = "<span>操作效果</span><strong>暂无可执行操作</strong><p>当前状态没有公开的动作语义。</p>";
    return;
  }
  card.innerHTML = `<span>${esc(effect.label_zh || "操作效果")}</span><strong>${esc(effectTypeLabel(effect.type))}</strong><p>${esc(effect.summary_zh || effect.summary || "更新当前实验状态。")}</p>`;
}

function fieldControl(field) {
  const choices = field.choices || field.allowed_values;
  const title = `${esc(field.field)}${field.required ? " *" : ""}`;
  if (Array.isArray(choices)) {
    const labels = field.choice_labels || {};
    return `<label class="field-label dark-label">${title}<select data-action-field="${esc(field.field)}">${choices.map((choice) => `<option value="${esc(choice)}">${esc(labels[String(choice)] || choice)}</option>`).join("")}</select></label>`;
  }
  const bounds = field.recommended_range || field.bounds || {};
  const low = bounds.low ?? "", high = bounds.high ?? "";
  const initial = low !== "" && high !== "" ? (Number(low) + Number(high)) / 2 : "";
  return `<label class="field-label dark-label">${title} ${esc(field.unit || "")}<input data-action-field="${esc(field.field)}" data-numeric="true" type="number" min="${esc(low)}" max="${esc(high)}" step="any" value="${esc(initial)}" ${field.required ? "required" : ""}></label>`;
}

function buildAction() {
  if (!lab.affordance) return {};
  const action = { operation: lab.affordance.operation };
  document.querySelectorAll("[data-action-field]").forEach((input) => {
    if (input.value === "") return;
    action[input.dataset.actionField] = input.dataset.numeric === "true" ? Number(input.value) : parseChoice(input.value);
  });
  return action;
}

function parseChoice(value) {
  return /^-?\d+(\.\d+)?$/.test(value) ? Number(value) : value;
}

function updatePreview() {
  $("#actionPreview").textContent = JSON.stringify(buildAction(), null, 2);
}

function showValidation(success, message) {
  const box = $("#actionValidation");
  box.className = `validation-card ${success ? "success" : "error"}`;
  box.innerHTML = `<span class="validation-icon">${success ? "✓" : "!"}</span><p>${esc(message)}</p>`;
}

function renderMetrics(metrics) {
  const entries = Object.entries(metrics).filter(([, value]) => Number.isFinite(Number(value))).slice(0, 10);
  $("#visibleMetricBars").innerHTML = entries.map(([key, value]) => `<div class="metric-bar-light"><span>${esc(key)}</span><div class="metric-track-light"><i style="width:${Math.max(0, Math.min(100, Number(value) * 100))}%"></i></div><strong>${fmt(value, 3)}</strong></div>`).join("");
}

function renderHistory(history) {
  $("#studentHistory").innerHTML = history.length ? history.map((item) => {
    const effect = item.state_effects || {};
    const delta = `Δt ${signed(effect.delta_time_s, "s", 0)} · ΔV ${signed(effect.delta_volume_L, "L", 4)}${Number(effect.sample_delta_L || 0) ? ` · sample −${Number(effect.sample_delta_L).toFixed(4)} L` : ""}`;
    return `<tr><td>${item.step}</td><td>E${Number(item.experiment_index || 0) + 1}</td><td><code>${esc(item.action.operation)}</code></td><td><span class="effect-table-label">${esc(effect.label_zh || item.status)}</span><small>${esc(delta)}</small></td><td>${fmt(item.reward)}</td><td>${fmt(item.leaderboard_score)}</td><td>${esc(Object.entries(item.visible_metrics || {}).map(([key, value]) => `${key}=${fmt(value, 3)}`).join(" · "))}</td></tr>`;
  }).join("") : '<tr><td colspan="7"><div class="empty-table">尚未开始实验</div></td></tr>';
}

function effectTypeLabel(type) {
  return ({
    additive_charge: "物料进入当前容器",
    cumulative_process: "从当前状态继续演化",
    destructive_withdrawal: "从当前库存扣除",
    destructive_measurement: "取样后获得观测",
    destructive_transfer: "转移并保留损失",
    configuration_update: "更新设备配置",
    inventory_selection: "切换工作库存",
    inventory_split: "拆分当前库存",
    state_change: "更新当前状态",
  })[type] || "更新当前状态";
}

function signed(value, unit = "", digits = 3) {
  const number = Number(value || 0);
  const sign = number > 0 ? "+" : number < 0 ? "−" : "";
  return `${sign}${Math.abs(number).toFixed(digits)}${unit ? ` ${unit}` : ""}`;
}

function fmtDuration(value) {
  const seconds = Number(value || 0);
  return seconds >= 3600 ? `${(seconds / 3600).toFixed(2)} h` : `${seconds.toFixed(0)} s`;
}

function downloadNotebook() {
  if (!lab.session) return;
  const payload = { session_id: lab.session.session_id, task_id: lab.session.task_id, seed: lab.session.seed, background: lab.session.background, history: lab.session.history };
  const url = URL.createObjectURL(new Blob([JSON.stringify(payload, null, 2)], { type: "application/json" }));
  const link = document.createElement("a");
  link.href = url; link.download = `${lab.session.task_id}-student-notebook.json`; link.click(); URL.revokeObjectURL(url);
}

function drawLearningCurve(values) {
  const canvas = $("#studentChart"), context = canvas.getContext("2d");
  const width = canvas.width, height = canvas.height;
  context.clearRect(0, 0, width, height);
  context.strokeStyle = "rgba(17,66,66,.09)"; context.lineWidth = 1;
  for (let i = 1; i < 5; i += 1) { const y = i * height / 5; context.beginPath(); context.moveTo(38, y); context.lineTo(width - 16, y); context.stroke(); }
  context.fillStyle = "#829496"; context.font = "11px system-ui"; context.fillText("1.0", 8, 18); context.fillText("0.0", 8, height - 13);
  if (!values.length) return;
  const gradient = context.createLinearGradient(0, 0, width, 0); gradient.addColorStop(0, "#0ca78e"); gradient.addColorStop(1, "#42bdf5");
  context.strokeStyle = gradient; context.lineWidth = 3; context.beginPath();
  values.forEach((value, index) => { const x = 38 + index / Math.max(values.length - 1, 1) * (width - 60); const y = height - 18 - Math.max(0, Math.min(1, value)) * (height - 37); index ? context.lineTo(x, y) : context.moveTo(x, y); });
  context.stroke();
}

async function api(url, options = {}) {
  const response = await fetch(url, { method: options.method || "GET", headers: { "Content-Type": "application/json" }, body: options.body === undefined ? undefined : JSON.stringify(options.body) });
  const payload = await response.json();
  if (!response.ok) throw new Error(payload.error || `HTTP ${response.status}`);
  return payload;
}
