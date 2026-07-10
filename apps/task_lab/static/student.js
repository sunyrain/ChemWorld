const lab = {
  tasks: [],
  session: null,
  affordance: null,
  spectrum: null,
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
  const latestSpectrum = [...history].reverse().find((item) => item.spectrum?.available)?.spectrum;
  lab.spectrum?.render(latestSpectrum);
  $("#studentSpectrumInstrument").textContent = latestSpectrum?.instrument || latestSpectrum?.kind || "No signal";
  const report = session.lab_report || {};
  if (report.text) $("#labFeedback").textContent = report.text;
  const instrument = report.instrument_summary?.instrument;
  $("#reportInstrument").textContent = instrument || "No instrument";
}

function updateDigitalTwin(latest) {
  const operation = latest?.action?.operation || "idle";
  $("#twinStage").dataset.operation = operation;
  $("#twinOperation").textContent = operation;
  $("#twinStatus").textContent = latest ? latest.status || "operation applied" : "Ready for setup";
  const materialSteps = (lab.session?.history || []).filter((item) => ["add_solvent", "add_reagent", "add_phase", "add_extractant"].includes(item.action.operation)).length;
  const top = Math.max(25, 58 - materialSteps * 7);
  $("#vesselLiquid").style.inset = `${top}% 4px 4px`;
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
  $("#operationFields").innerHTML = fields.map((field) => fieldControl(field)).join("");
  document.querySelectorAll("[data-action-field]").forEach((input) => input.addEventListener("input", updatePreview));
  updatePreview();
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
  $("#studentHistory").innerHTML = history.length ? history.map((item) => `<tr><td>${item.step}</td><td><code>${esc(item.action.operation)}</code></td><td>${esc(item.status)}</td><td>${fmt(item.reward)}</td><td>${fmt(item.leaderboard_score)}</td><td>${esc(Object.entries(item.visible_metrics || {}).map(([key, value]) => `${key}=${fmt(value, 3)}`).join(" · "))}</td></tr>`).join("") : '<tr><td colspan="6"><div class="empty-table">尚未开始实验</div></td></tr>';
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
