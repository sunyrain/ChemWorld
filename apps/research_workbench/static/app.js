import { drawChart, explorationGraph, drawExplorationGraph } from "./charts.js";

const $ = (id) => document.getElementById(id);
const esc = (s) =>
  String(s ?? "").replace(
    /[&<>"']/g,
    (c) =>
      ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[
        c
      ],
  );
const pretty = (value) => JSON.stringify(value, null, 2);
const state = {
  catalog: null,
  runs: [],
  run: null,
  page: "home",
  tab: "explore",
  graphMode: "events",
  graphZoom: 1,
  previewEpoch: 0,
  noteCache: new Map(),
  author: "model",
  selected: new Set(),
  polling: false,
  navigation: 0,
  notebookVersion: 0,
};
const statuses = {
  ready: "待操作",
  running: "运行中",
  completed: "已终检",
  truncated: "预算终止",
  failed: "运行失败",
  stopped: "已停止",
  cancelled: "已取消",
  cancelling: "取消中",
  interrupted: "已中断",
};
const names = {
  "reaction-to-assay": "反应与表征",
  "reaction-to-crystallization": "反应与结晶",
  "flow-reaction-optimization": "连续流反应",
  "reaction-to-purification": "反应与纯化",
  "reaction-to-distillation": "反应与蒸馏",
  "electrochemical-conversion": "电化学转化",
};
const operations = {
  add_solvent: "加入溶剂",
  add_reagent: "加入试剂",
  add_catalyst: "加入催化剂",
  heat: "加热反应",
  wait: "等待",
  measure: "仪器测量",
  terminate: "终止反应",
  quench: "淬灭",
  sample: "取样",
  cool_crystallize: "冷却结晶",
  seed_crystals: "加入晶种",
  filter: "过滤",
  run_flow: "运行连续流",
  set_flow: "设置流量",
  distill: "蒸馏",
  collect_fraction: "收集馏分",
};
const fieldNames = {
  volume_L: "体积 (L)",
  amount_mol: "物质的量 (mol)",
  catalyst_amount_mol: "催化剂用量 (mol)",
  target_temperature_K: "目标温度 (K)",
  duration_s: "持续时间 (s)",
  stirring_speed_rpm: "搅拌转速 (rpm)",
  solvent: "溶剂",
  catalyst: "催化剂",
  instrument: "仪器",
  sample_volume_L: "取样体积 (L)",
};
const taskName = (design) =>
  names[design.task_id] ||
  design.task_id ||
  design.composition?.composition_id ||
  "自定义组合";
const date = (value) =>
  new Date(value).toLocaleString("zh-CN", {
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
  });
const number = (v, digits = 3) =>
  v === null || v === undefined || !Number.isFinite(Number(v))
    ? "—"
    : Number(v).toLocaleString("zh-CN", { maximumFractionDigits: digits });
const badge = (status) =>
  `<span class="badge ${esc(status)}">${esc(statuses[status] || status)}</span>`;
function toast(message) {
  $("toast").textContent = message;
  $("toast").hidden = false;
  clearTimeout(toast.timer);
  toast.timer = setTimeout(() => ($("toast").hidden = true), 6500);
}
async function api(path, body) {
  const response = await fetch(path, {
    method: body === undefined ? "GET" : "POST",
    headers: body === undefined ? {} : { "Content-Type": "application/json" },
    body: body === undefined ? undefined : JSON.stringify(body),
  });
  const data = await response.json();
  if (!response.ok) throw new Error(data.error || `HTTP ${response.status}`);
  return data;
}
async function refreshRuns() {
  state.runs = (await api("/api/runs")).runs;
  renderSidebar();
}
function renderSidebar() {
  $("run-count").textContent = state.runs.length;
  $("compare-count").textContent = state.selected.size;
  $("recent-runs").innerHTML =
    state.runs
      .slice(0, 15)
      .map(
        (r) =>
          `<button class="recent-run ${state.run?.id === r.id && state.page === "run" ? "active" : ""}" data-run="${r.id}"><span class="mini-dot ${r.status}"></span><span>${esc(r.name)}</span></button>`,
      )
      .join("") || '<p class="fineprint">配置目标，开始自主探索</p>';
  document
    .querySelectorAll("[data-nav]")
    .forEach((b) =>
      b.classList.toggle(
        "active",
        b.dataset.nav === (state.page === "run" ? (state.tab === "notebook" ? "notes" : "home") : state.page === "home" ? "records" : state.page),
      ),
    );
  $("breadcrumb").textContent =
    state.page === "run"
      ? "实验记录"
      : state.page === "compare"
        ? "结果比较"
        : "实验工作台";
}
function renderHome() {
  state.navigation++;
  state.page = "home";
  state.run = null;
  renderSidebar();
  const completed = state.runs.filter((r) => r.final_assay_count > 0).length;
  const working = state.runs.filter((r) =>
    ["running", "cancelling"].includes(r.status),
  ).length;
  const projects = new Set(state.runs.map((r) => r.project)).size;
  $("main").innerHTML =
    `<section class="intro"><div><div class="eyebrow">YOUR RESEARCH, IN MOTION</div><h1>让 Agent 探索虚拟实验室。</h1><p>配置研究目标、模型和预算，观察 Agent 选择操作、读取观测与维护研究记录。</p></div><div class="intro-tag">CHEMWORLD / 本机试用</div></section>
  <section class="stats" aria-label="工作空间概览">${[
    [projects, "研究项目", "个"],
    [state.runs.length, "独立实验", "批"],
    [working, "后台运行", "批"],
    [completed, "已完成终检", "批"],
  ]
    .map(
      ([v, l, u]) =>
        `<div class="stat"><div class="stat-label">${l}<span>↗</span></div><div class="stat-value">${v}<span class="stat-unit">${u}</span></div></div>`,
    )
    .join("")}</section>
  <div class="section-heading"><h2>选择一个起点</h2><span>虚拟环境 · 当前核心执行</span></div><section class="template-grid">
  ${[
    [
      "reaction-to-assay",
      "⌁",
      "01 / REACTION",
      "反应与表征",
      "从投料、控温到色谱测量，探索反应过程与结果。",
      "HPLC · GC · UV–Vis",
    ],
    [
      "reaction-to-crystallization",
      "◇",
      "02 / CRYSTALLIZATION",
      "反应与结晶",
      "连接上游反应与冷却结晶，观察产物回收及粒度。",
      "结晶 · 过滤 · 终检",
    ],
    [
      "flow-reaction-optimization",
      "⇌",
      "03 / CONTINUOUS FLOW",
      "连续流实验",
      "调整流量与操作条件，研究连续过程的响应。",
      "流量 · 停留时间 · 表征",
    ],
  ]
    .map(
      ([id, symbol, kicker, title, copy, tools]) =>
        `<button class="template-card" data-template="${id}"><div class="template-top"><span class="template-symbol">${symbol}</span><span>${kicker}</span></div><h3>${title}</h3><p>${copy}</p><div class="template-bottom"><span>${tools}</span><b>开始设计 ↗</b></div></button>`,
    )
    .join("")}</section>
  <div class="section-heading"><h2>实验记录</h2><span>运行、未完成与失败，一并保留</span></div><section class="panel">${runTable(state.runs)}</section>`;
}
function runTable(runs) {
  if (!runs.length)
    return '<div class="empty"><div class="empty-icon">⌬</div>还没有实验记录<br>选择上方模板，几步完成你的第一次实验。</div>';
  return `<div class="table-wrap"><table><thead><tr><th>实验 / 项目</th><th>执行方式</th><th>状态</th><th>动作提交</th><th>创建时间</th><th>比较</th></tr></thead><tbody>${runs.map((r) => `<tr><td><button class="run-name" data-run="${r.id}">${esc(r.name)}</button><div class="subline">${esc(r.project)} · ${esc(taskName(r.design))}</div></td><td>${esc(r.actor === "reference" ? "离线参考流程" : r.actor === "manual" ? "手动实验" : r.actor)}</td><td>${badge(r.status)}</td><td>${r.submitted_steps}<span class="muted"> / ${r.design.budget}</span></td><td class="muted">${date(r.created_at)}</td><td><label class="compare-check"><input type="checkbox" data-compare="${r.id}" ${state.selected.has(r.id) ? "checked" : ""}> 加入</label></td></tr>`).join("")}</tbody></table></div>`;
}
async function openRun(id) {
  const navigation = ++state.navigation;
  const run = await api(`/api/runs/${id}`);
  if (navigation !== state.navigation) return;
  state.run = run;
  state.page = "run";
  renderRun();
}
function renderRun() {
  const r = state.run;
  const viewport = $("graph-viewport");
  const graphScroll = viewport ? { x: viewport.scrollLeft, y: viewport.scrollTop } : null;
  state.previewEpoch++;
  renderSidebar();
  const active = ["ready", "running", "cancelling"].includes(r.status);
  $("main").innerHTML =
    `<section class="run-heading"><div><div class="eyebrow">${esc(r.project)} / EXPERIMENT</div><h1>${esc(r.name)}</h1>${badge(r.status)} <span class="muted compact">${esc(taskName(r.design))} · seed ${r.design.seed} · ${date(r.created_at)}</span><p>${esc(r.question || "")}</p></div><div class="row-actions"><button class="button secondary small" id="clone-run">新建同条件实验</button>${active ? '<button class="button danger small" id="cancel-run">' + (r.status === "ready" ? "关闭实验" : "取消运行") + "</button>" : ""}<button class="button secondary small" id="replay-run" ${["running", "cancelling"].includes(r.status) ? "disabled" : ""}>精确回放</button><a class="button secondary small" href="/api/runs/${r.id}/export">导出 ZIP ↗</a></div></section>
  ${r.message && (state.tab !== "explore" || ["failed", "interrupted", "truncated", "cancelled"].includes(r.status)) ? `<div class="notice ${["failed", "interrupted", "truncated"].includes(r.status) ? "warning" : ""}">${esc(r.message)}</div>` : ""}
  ${r.replay ? `<div class="notice">${r.replay.verified ? "✓ 精确回放通过" : "回放未通过"} · 检查 ${r.replay.checked_steps} 步 · 最大绝对误差 ${number(r.replay.max_abs_error, 8)}</div>` : ""}
  <div class="executor-strip"><span class="executor-icon">◇</span><strong>${esc(executorLabel(r))}</strong><span>虚拟实验室</span><span class="executor-help">${r.actor === "reference" ? "固定配方 · 非自主 Agent" : r.actor === "manual" ? "手动实验 · 独立可选模式" : "模型自主选择操作 · 记录按实际执行更新"}</span></div>
  <div class="tabs" role="tablist">${[
    ["explore", "探索画布"],
    ["timeline", "操作记录"],
    ["spectra", "仪器观测"],
    ["notebook", "研究笔记"],
    ["report", "设计与报告"],
  ]
    .map(
      ([id, name]) =>
        `<button role="tab" aria-selected="${state.tab === id}" class="tab ${state.tab === id ? "active" : ""}" data-tab="${id}">${name}</button>`,
    )
    .join("")}</div><div id="run-panel"></div>`;
  if (state.tab === "explore") renderExplorer(graphScroll);
  if (state.tab === "timeline") renderTimeline();
  if (state.tab === "spectra") renderSpectra();
  if (state.tab === "notebook") renderNotebook();
  if (state.tab === "report") renderReport();
  $("clone-run").onclick = () => openDesign(r.design.task_id || "custom", r);
  if ($("cancel-run"))
    $("cancel-run").onclick = () =>
      perform(async () => {
        state.run = await api(`/api/runs/${r.id}/cancel`, {});
        renderRun();
        await refreshRuns();
      });
  $("replay-run").onclick = () =>
    perform(async () => {
      toast("正在用当前核心重新执行轨迹…");
      await api(`/api/runs/${r.id}/replay`, {});
      await openRun(r.id);
      toast("回放检查已完成");
    });
}


function applyTheme(theme) {
  document.documentElement.dataset.theme = theme;
  const dark = theme === "dark";
  $("theme-toggle").textContent = dark ? "☀ 浅色模式" : "☾ 深色模式";
  $("theme-toggle").setAttribute("aria-label", dark ? "切换为浅色模式" : "切换为深色模式");
  $("theme-toggle").setAttribute("aria-pressed", String(dark));
}
let initialTheme = globalThis.matchMedia?.("(prefers-color-scheme: dark)").matches ? "dark" : "light";
try {
  const saved = globalThis.localStorage?.getItem("chemworld.theme");
  if (saved === "dark" || saved === "light") initialTheme = saved;
} catch { /* System preference is sufficient when storage is unavailable. */ }
applyTheme(initialTheme);
$("theme-toggle").onclick = () => {
  const theme = document.documentElement.dataset.theme === "dark" ? "light" : "dark";
  applyTheme(theme);
  try { globalThis.localStorage?.setItem("chemworld.theme", theme); } catch {}
};
function executorLabel(r) {
  if (r.actor === "reference") return "离线参考流程";
  if (r.actor === "manual") return "手动实验";
  return "Agent · " + (r.model_configuration?.requested_model || r.actor);
}
function observationSeries(r) {
  return [...r.events].reverse().find((e) => e.measurement && e.series?.length);
}
function renderExplorer(savedScroll = null) {
  const r = state.run;
  const epoch = ++state.previewEpoch;
  const previousGraph = $("graph-viewport");
  const scroll = savedScroll || (previousGraph ? { x: previousGraph.scrollLeft, y: previousGraph.scrollTop } : { x: 0, y: 0 });
  const isModel = !["reference", "manual"].includes(r.actor);
  const hasNetwork = Boolean(r.view?.component_network?.vessels?.length);
  const graph = explorationGraph(r, hasNetwork ? state.graphMode : "events", { ...operations, ...fieldNames });
  const measured = observationSeries(r);
  const latest = r.events.at(-1);
  const revisions = r.model_notebook?.revisions || [];
  const revision = revisions[0]?.revision ?? 0;
  const noteKey = r.id + ":" + revision;
  const actions = r.events.slice(-5);
  const usage = r.model_calls ? number((r.usage?.input_tokens || 0) + (r.usage?.output_tokens || 0), 0) + (r.usage?.complete ? "" : " · 不完整") : "未调用";
  $("run-panel").innerHTML =
    '<div class="explorer-layout"><section class="panel network-panel">' +
    '<div class="network-heading"><div><h2>' + esc(graph.title) + '</h2><p>' +
    (graph.kind === "network" ? '环境公开组件 · 只读' : '来自实际提交记录 · 最近 ' + graph.nodes.length + ' / ' + graph.total + ' 条') +
    '</p></div><div class="graph-tools">' +
    (hasNetwork ? '<select id="graph-mode" aria-label="选择网络视图"><option value="events">执行轨迹</option><option value="network">组件网络</option></select>' : '') +
    '<button class="button secondary small" id="graph-fit">适应画布</button><button class="button secondary small" id="graph-minus" aria-label="缩小画布">−</button><span id="graph-scale">100%</span><button class="button secondary small" id="graph-plus" aria-label="放大画布">＋</button></div></div>' +
    '<div class="graph-viewport" id="graph-viewport"><div id="network-graph" class="network-graph"></div></div>' +
    '<div class="graph-legend"><span class="line-key"></span>' + esc(graph.legend) + '<span>' + (graph.kind === "events" ? '点击操作查看原始事件' : '当前容器以高亮边框标记') + '</span></div></section>' +
    '<aside class="explorer-inspector"><section class="panel"><div class="panel-header"><h3>' + (isModel ? 'Agent 研究状态' : '执行状态') + '</h3>' + badge(r.status) + '</div><div class="panel-body">' +
    '<div class="research-label">研究目标</div><p class="research-question">' + esc(r.question || "未填写目标") + '</p>' +
    '<div class="metric"><span>执行者</span><strong>' + esc(executorLabel(r)) + '</strong></div>' +
    '<hr class="metric-separator"><div class="research-label">最近提交</div><p class="current-operation">' + esc(latest ? operations[latest.action.operation] || latest.action.operation : "尚无操作") +
    '</p><span class="muted compact">' + esc(latest ? (latest.transaction_status === "committed" ? "已提交" : "已拒绝 / 回滚") + " · " + latest.event_id : "等待执行记录") + '</span></div></section>' +
    '<section class="panel observation-preview"><div class="panel-header"><h3>环境观测</h3><button class="text-button" data-tab="spectra">全部观测 ↗</button></div>' +
    (measured ? '<div id="explore-chart" class="chart"></div><div class="chart-note">' + esc(measured.action.instrument || "测量") + ' · ' + esc(measured.event_id) + ' · 虚拟仪器数据</div>' : '<div class="empty">尚无可绘制的仪器信号<br>测量后显示实际观测</div>') + '</section>' +
    '<section class="panel notebook-preview"><div class="panel-header"><h3>Agent 研究笔记</h3><button class="text-button" data-agent-notes>查看版本 ↗</button></div><div class="panel-body"><div id="agent-note-preview" class="note-excerpt">' +
    esc(state.noteCache.get(noteKey) || (revisions.length ? "正在读取模型记录…" : "Agent 尚未主动提交研究笔记。")) +
    '</div><p class="fineprint">模型主动写下的记录 · ' + revisions.length + ' 个版本</p></div></section></aside></div>' +
    '<section class="panel execution-dock"><div class="panel-header"><h3>执行事件</h3><button class="text-button" data-tab="timeline">查看全部 ' + r.events.length + ' 条 ↗</button></div>' +
    '<div class="execution-events">' + (actions.map((e, i) => '<button class="execution-chip ' + (e.transaction_status === "committed" ? "" : "rejected") + '" data-event="' + (r.events.length - actions.length + i) + '"><span>' + esc(e.event_id) + '</span><strong>' + esc(operations[e.action.operation] || e.action.operation) + '</strong><small>' + (e.transaction_status === "committed" ? "已提交" : "拒绝 / 回滚") + '</small></button>').join("") || '<p class="muted compact">执行后，操作与拒绝记录会显示在这里。</p>') +
    '</div><div class="resource-strip"><span>操作提交 <strong>' + r.submitted_steps + '</strong></span><span>剩余操作预算 <strong>' + esc(r.view?.campaign_state?.remaining_budget ?? "—") +
    '</strong></span><span>模型调用 <strong>' + r.model_calls + ' / ' + esc(r.limits?.call_limit ?? "—") + '</strong></span><span>Token <strong>' + esc(usage) +
    '</strong></span><span>运行用时 <strong>' + ([ "running", "cancelling" ].includes(r.status) ? "运行中" : number(r.wall_time_s) + " s") +
    '</strong></span><span>终检 <strong>' + (r.final_assay_count ? "已完成" : "未完成") + '</strong></span></div></section>';
  drawExplorationGraph($("network-graph"), graph, (i) => showDetail("公开事件详情", r.events[i]));
  const zoom = (value) => {
    state.graphZoom = Math.max(0.6, Math.min(1.8, value));
    $("network-graph").className = "network-graph zoom-" + Math.round(state.graphZoom * 10);
    $("graph-scale").textContent = Math.round(state.graphZoom * 100) + "%";
  };
  zoom(state.graphZoom);
  $("graph-viewport").scrollLeft = scroll.x;
  $("graph-viewport").scrollTop = scroll.y;
  $("graph-fit").onclick = () => { zoom(1); $("graph-viewport").scrollLeft = 0; };
  $("graph-plus").onclick = () => zoom(state.graphZoom + 0.2);
  $("graph-minus").onclick = () => zoom(state.graphZoom - 0.2);
  if ($("graph-mode")) {
    $("graph-mode").value = state.graphMode;
    $("graph-mode").onchange = () => { state.graphMode = $("graph-mode").value; renderExplorer(); };
  }
  document.querySelector("[data-agent-notes]").onclick = () => { state.author = "model"; state.tab = "notebook"; renderRun(); };
  if (measured) drawChart($("explore-chart"), measured.series[0]);
  if (revisions.length && !state.noteCache.has(noteKey)) {
    api("/api/runs/" + r.id + "/notebook", { author: "model", operation: "read", arguments: { revision, limit: 1400 } }).then((note) => {
      if (state.noteCache.size > 30) state.noteCache.clear();
      state.noteCache.set(noteKey, note.text || "记录为空。");
      if (state.run?.id === r.id && state.tab === "explore" && state.previewEpoch === epoch && $("agent-note-preview"))
        $("agent-note-preview").textContent = note.text || "记录为空。";
    }).catch(() => {
      if (state.run?.id === r.id && state.tab === "explore" && state.previewEpoch === epoch && $("agent-note-preview"))
        $("agent-note-preview").textContent = "读取失败，可在研究笔记页重试。";
    });
  }
}

function metrics(r) {
  const obs = r.view?.lab_report?.visible_metrics || {};
  const camp = r.view?.campaign_state || {};
  return `<div class="metric-list">${[
    ["当前批次终检", r.final_assay_count ? "已完成" : "尚未完成"],
    ["已提交动作", r.submitted_steps],
    ["拒绝 / 回滚", r.rejected_steps],
    ["剩余操作预算", camp.remaining_budget ?? "—"],
    ["模型调用", r.model_calls],
    [
      "模型 token",
      r.model_calls
        ? number(
            (r.usage?.input_tokens || 0) + (r.usage?.output_tokens || 0),
            0,
          ) + (r.usage?.complete ? "" : "（不完整）")
        : "未调用",
    ],
    ["模型费用", "未知 / 以厂商账单为准"],
  ]
    .map(
      ([k, v]) =>
        `<div class="metric"><span>${k}</span><strong>${esc(v)}</strong></div>`,
    )
    .join("")}</div><hr class="metric-separator"><div class="metric-list">${
    Object.entries(obs)
      .slice(0, 12)
      .map(
        ([k, v]) =>
          `<div class="metric"><span>${esc(k)}</span><strong class="good">${number(v, 4)}</strong></div>`,
      )
      .join("") ||
    '<span class="muted compact">尚无公开测量值。缺测不填零。</span>'
  }</div>`;
}
function renderTimeline() {
  const r = state.run;
  const actions = r.view?.available_actions || [];
  $("run-panel").innerHTML =
    `<div class="workspace-grid"><section class="panel"><div class="panel-header"><h3>实验操作</h3><span class="event-ref">${r.status === "ready" ? "MANUAL" : "OBSERVE"}</span></div><div class="panel-body">${r.status === "ready" ? `<form class="operation-form" id="action-form"><label>选择操作<select id="operation-select">${actions.map((a) => `<option value="${esc(a.operation)}">${esc(operations[a.operation] || a.operation)}</option>`).join("")}</select></label><div id="action-fields"></div><button class="button primary" type="submit">提交操作 →</button></form>${r.events.length === 0 ? '<button id="reference-start" class="button secondary small">运行离线参考流程</button>' : ""}` : `<p class="muted compact">${["running", "cancelling"].includes(r.status) ? "后台正在运行，操作将在此实时显示。" : "此批次已结束。复制设计可开始新实验，原始记录继续保留。"}</p>`}<p class="fineprint">操作字段来自核心的当前合法动作。仪器测量可能消耗时间、样品与预算。</p></div></section>
  <section class="panel"><div class="panel-header"><h3>操作时间线</h3><span class="muted compact">${r.events.length} 次提交 · 按发生顺序</span></div><div class="timeline">${
    r.events
      .map(
        (e, i) =>
          `<article class="event ${e.transaction_status === "committed" ? "" : "rejected"}"><div class="event-head"><span>${String(i + 1).padStart(2, "0")} &nbsp; ${esc(operations[e.action.operation] || e.action.operation)}${e.action.instrument ? " · " + esc(e.action.instrument.toUpperCase()) : ""}</span><small>${e.transaction_status === "committed" ? "已提交" : "已拒绝 / 回滚"}</small></div><p>${
            esc(
              Object.entries(e.action)
                .filter(([k]) => !["operation", "instrument"].includes(k))
                .map(
                  ([k, v]) =>
                    `${fieldNames[k] || k}: ${typeof v === "object" ? JSON.stringify(v) : v}`,
                )
                .join(" · "),
            ) || esc(e.report?.text || "操作已记录")
          }</p><span class="event-ref">${e.event_id}</span> &nbsp; <button data-event="${i}">查看详情 ↗</button>${e.measurement ? ` &nbsp; <button data-tab="spectra">仪器数据 ↗</button>` : ""}</article>`,
      )
      .join("") ||
    '<div class="empty"><div class="empty-icon">⌁</div>等待第一次操作<br>左侧选择操作，或运行参考流程。</div>'
  }</div></section>
  <aside class="panel resource-panel"><div class="panel-header"><h3>状态与资源</h3></div><div class="panel-body">${metrics(r)}</div></aside></div>`;
  if ($("operation-select")) {
    $("operation-select").onchange = renderActionFields;
    renderActionFields();
    $("action-form").onsubmit = (event) => {
      event.preventDefault();
      perform(async () => {
        const action = { operation: $("operation-select").value };
        document.querySelectorAll("[data-field]").forEach((input) => {
          if (input.value !== "")
            action[input.dataset.field] =
              input.dataset.numeric === "yes"
                ? Number(input.value)
                : input.value;
        });
        const button = event.target.querySelector("button[type=submit]");
        button.disabled = true;
        try {
          state.run = await api(`/api/runs/${r.id}/step`, {
            action,
            expected_step: r.events.length,
          });
          renderRun();
          await refreshRuns();
        } finally {
          button.disabled = false;
        }
      });
    };
  }
  if ($("reference-start"))
    $("reference-start").onclick = () =>
      perform(async () => {
        state.run = await api(`/api/runs/${r.id}/start`, { mode: "reference" });
        renderRun();
      });
}
function renderActionFields() {
  const entry = state.run.view.available_actions.find(
    (a) => a.operation === $("operation-select").value,
  );
  const schema = entry?.schema || entry || {};
  $("action-fields").innerHTML = (schema.fields || [])
    .filter((f) => f.field !== "operation")
    .map((f) => {
      const name = f.field;
      const required = (schema.required_fields || []).includes(name);
      const range = f.bounds || f.recommended_range;
      const numeric =
        range || ["number", "integer", "float", "int"].includes(f.type);
      const hint = range ? `${range.low} – ${range.high}` : f.description || "";
      let control;
      if (f.choices?.length)
        control = `<select data-field="${esc(name)}" data-numeric="${typeof f.choices[0] === "number" ? "yes" : "no"}">${required ? "" : '<option value="">默认</option>'}${f.choices.map((v) => `<option value="${esc(v)}">${esc(f.choice_labels?.[v] || v)}</option>`).join("")}</select>`;
      else
        control = `<input data-field="${esc(name)}" data-numeric="${numeric ? "yes" : "no"}" type="${numeric ? "number" : "text"}" ${numeric ? 'step="any"' : ""} ${range ? `min="${range.low}" max="${range.high}"` : ""} ${required ? "required" : ""} value="${esc(f.default ?? (required && range ? Number(((range.low + range.high) / 2).toPrecision(6)) : ""))}" placeholder="${required ? "必填" : "留空使用默认值"}">`;
      return `<label>${esc(fieldNames[name] || name)}${control}<span class="schema-hint">${esc(hint).slice(0, 240)}</span></label>`;
    })
    .join("");
}
function renderSpectra() {
  const entries = state.run.events.filter((e) => e.measurement);
  $("run-panel").innerHTML =
    `<div class="notice">谱图来自仪器实际返回的公开数据。移动指针查看数值；显示降采样时可下载完整原始信号。</div><div class="chart-grid">${entries.flatMap((e) => (e.series?.length ? e.series.map((s, i) => `<section class="panel chart-card"><div class="panel-header"><h3>${esc(s.label.toUpperCase())}</h3><a href="/api/runs/${state.run.id}/measurement?event=${e.event_id}" target="_blank" rel="noopener">${e.event_id} · 原始数据 ↗</a></div><div class="chart" id="chart-${e.event_id}-${i}"></div><div class="chart-note">${s.original_points} 个原始点${s.downsampled ? " · 显示 1,500 点" : ""} · ${date(e.recorded_at)}</div></section>`) : [`<section class="panel"><div class="panel-body"><h3>${esc(e.action.instrument)}</h3><p class="muted compact">此测量返回数值或当前未适配的信号格式，没有生成示意曲线。</p><a href="/api/runs/${state.run.id}/measurement?event=${e.event_id}" target="_blank" rel="noopener">查看完整公开数据 ↗</a></div></section>`])).join("") || '<section class="panel"><div class="empty">尚未进行仪器测量。<br>执行测量后，实际数据会显示在这里。</div></section>'}</div>`;
  entries.forEach((e) =>
    (e.series || []).forEach((s, i) =>
      drawChart($(`chart-${e.event_id}-${i}`), s),
    ),
  );
}
async function renderNotebook() {
  const r = state.run;
  const notebookVersion = ++state.notebookVersion;
  const revisions =
    (state.author === "model" ? r.model_notebook : r.human_notebook)
      ?.revisions || [];
  $("run-panel").innerHTML =
    `<div class="notice">人工笔记与模型笔记分别保存。版本带有当时的事件游标；恢复旧文字会新增版本，实验记录保持不变。</div><div class="row-actions"><button class="button ${state.author === "human" ? "primary" : "secondary"} small" data-author="human">我的研究笔记</button><button class="button ${state.author === "model" ? "primary" : "secondary"} small" data-author="model">模型笔记 · 只读</button></div><br><div class="notebook-layout"><section class="panel"><div class="panel-header"><h3>版本记录</h3><span class="muted compact">${revisions.length} 个</span></div>${revisions.map((v) => `<button class="revision" data-revision="${v.revision}">v${v.revision} · ${esc(v.message || v.kind || "更新")}<small>${date(v.recorded_at)} · 事件 ${v.public_cursor?.event_count ?? "—"}</small></button>`).join("") || '<div class="empty">尚无提交版本</div>'}</section><section class="panel"><div class="panel-header"><h3 id="notebook-title">${state.author === "human" ? "我的研究笔记" : "模型主动记录的笔记"}</h3><button class="button secondary small" id="notebook-diff">最近版本差异</button></div><textarea class="notebook-editor" id="notebook-text" aria-label="研究笔记正文" maxlength="16000" ${state.author === "model" ? "readonly" : ""} placeholder="问题 / 假设 / 预测 / 观测 / 证据 / 下一步…"></textarea><div class="notebook-controls"><span class="muted compact" id="notebook-version"></span>${state.author === "human" ? '<button class="button primary small" id="save-notebook">保存为新版本</button>' : ""}<span class="fineprint">Markdown 原文 · 正文按需读取</span></div></section></div>`;
  try {
    const note = await api(`/api/runs/${r.id}/notebook`, {
      author: state.author,
      operation: "read",
      arguments: { limit: 16000 },
    });
    if (
      state.tab !== "notebook" ||
      state.run?.id !== r.id ||
      state.notebookVersion !== notebookVersion
    )
      return;
    $("notebook-text").value = note.text;
    $("notebook-version").textContent =
      `v${note.revision} · ${note.total_characters} 字符`;
  } catch (error) {
    toast(error.message);
  }
  if ($("save-notebook"))
    $("save-notebook").onclick = () =>
      perform(async () => {
        const text = $("notebook-text").value;
        await api(`/api/runs/${r.id}/notebook`, {
          author: "human",
          operation: "write",
          arguments: { text, message: "人工研究记录" },
        });
        await openRun(r.id);
        toast("已保存新版本");
      });
  if ($("notebook-diff"))
    $("notebook-diff").onclick = () =>
      perform(async () => {
        const diff = await api(`/api/runs/${r.id}/notebook`, {
          author: state.author,
          operation: "diff",
          arguments: { limit: 16000 },
        });
        showDetail("笔记版本差异", diff.text);
      });
}
function renderReport() {
  const r = state.run;
  $("run-panel").innerHTML =
    `<div class="chart-grid"><section class="panel"><div class="panel-header"><h3>保存的实验设计</h3></div><div class="panel-body"><pre class="document document-code">${esc(pretty({ design: r.design, actor: r.actor, limits: r.limits, model: r.model_configuration }))}</pre></div></section><section class="panel"><div class="panel-header"><h3>实验报告</h3><span class="muted compact">公开记录</span></div><div class="panel-body"><p class="document">${esc(r.view?.lab_report?.text || "尚无报告。")}</p><hr class="metric-separator"><h3>模型提交的最终报告</h3><p class="document">${esc(r.model_report || "模型尚未主动提交最终报告。")}</p><hr class="metric-separator"><p class="fineprint">${r.submitted_steps} 次提交，${r.rejected_steps} 次拒绝或回滚，${r.final_assay_count} 次终检。保存了全部已提交事件；未终检不等于零产率。环境 seed 不保证不同厂商模型输出相同。</p></div></section></div><div class="section-heading"><h2>物料与设备公开状态</h2></div><section class="panel"><div class="panel-body"><pre class="document document-code">${esc(pretty({ samples: r.view?.sample_inventory, network: r.view?.component_network, routing: r.view?.material_routing, process: r.view?.process_control }))}</pre></div></section>`;
}
async function renderCompare() {
  const navigation = ++state.navigation;
  state.page = "compare";
  state.run = null;
  renderSidebar();
  $("main").innerHTML =
    `<div class="intro"><div><div class="eyebrow">COMPARE EXPERIMENTS</div><h1>并排看结果，也看过程。</h1><p>选择同一设计下的实验进行比较。操作、仪器和预算条件不同会影响结果，单次运行不构成模型排名。</p></div></div><div class="compare-options">${state.runs.map((r) => `<label><input type="checkbox" data-compare="${r.id}" ${state.selected.has(r.id) ? "checked" : ""}>${esc(r.name)}</label>`).join("")}</div><div id="comparison-content" class="panel"><div class="empty">${state.selected.size ? "正在读取实验…" : "请从实验列表选择 2–6 个实验。"}</div></div>`;
  const ids = [...state.selected].slice(0, 6);
  if (!ids.length) return;
  const runs = await Promise.all(ids.map((id) => api(`/api/runs/${id}`)));
  if (state.page !== "compare" || navigation !== state.navigation) return;
  const designKey = (r) => pretty(r.design);
  const matched = runs.every((r) => designKey(r) === designKey(runs[0]));
  const metricsKeys = [
    ...new Set(
      runs.flatMap((r) =>
        Object.keys(r.view?.lab_report?.visible_metrics || {}),
      ),
    ),
  ];
  const rows = [
    ["世界", (r) => taskName(r.design)],
    ["seed", (r) => r.design.seed],
    ["操作预算", (r) => r.design.budget],
    ["执行方式", (r) => r.actor],
    ["状态", (r) => statuses[r.status]],
    ["终检", (r) => (r.final_assay_count ? "已完成" : "未完成")],
    ["动作提交", (r) => r.submitted_steps],
    ["拒绝 / 回滚", (r) => r.rejected_steps],
    ["模型调用", (r) => r.model_calls],
    [
      "输入 token",
      (r) =>
        r.model_calls
          ? number(r.usage.input_tokens, 0) +
            (r.usage.complete ? "" : "（不完整）")
          : "未调用",
    ],
    [
      "输出 token",
      (r) =>
        r.model_calls
          ? number(r.usage.output_tokens, 0) +
            (r.usage.complete ? "" : "（不完整）")
          : "未调用",
    ],
    [
      "实际返回模型",
      (r) =>
        [...new Set((r.model_receipts || []).map((x) => x.model))].join(", ") ||
        "—",
    ],
    ["用时 (墙钟 s)", (r) => number(r.wall_time_s)],
    ["模型费用", () => "未知"],
    [
      "精确回放",
      (r) => (r.replay ? (r.replay.verified ? "通过" : "未通过") : "未检查"),
    ],
    ...metricsKeys.map((k) => [
      k,
      (r) => number(r.view?.lab_report?.visible_metrics?.[k], 5),
    ]),
  ];
  $("comparison-content").innerHTML =
    `<div class="panel-body"><div class="notice ${matched ? "" : "warning"}">${matched ? "所选运行的保存设计相同。仍需核对执行方式、模型工具格式、资源上限及重复次数。" : "所选实验的世界、seed 或预算不同：此表仅并列展示，不作公平模型排名。"}</div></div><div class="table-wrap"><table><thead><tr><th>对照项</th>${runs.map((r) => `<th><button class="run-name" data-run="${r.id}">${esc(r.name)}</button></th>`).join("")}</tr></thead><tbody>${rows.map(([label, value]) => `<tr><td class="muted">${esc(label)}</td>${runs.map((r) => `<td>${esc(value(r))}</td>`).join("")}</tr>`).join("")}</tbody></table></div>`;
}
function showDetail(title, content) {
  $("detail-title").textContent = title;
  $("detail-content").textContent =
    typeof content === "string" ? content : pretty(content);
  $("detail-dialog").showModal();
}
async function perform(work) {
  try {
    await work();
  } catch (error) {
    toast(error.message);
  }
}
function openDesign(task = "reaction-to-assay", clone = null, mode = "model") {
  const form = $("design-form");
  form.reset();
  form.elements.mode.value = mode;
  $("form-error").textContent = "";
  $("validation-result").textContent = "";
  form.elements.name.value = clone
    ? `${clone.name} · 新批次`
    : names[task] || "新实验";
  form.elements.project.value = clone?.project || "我的研究";
  form.elements.question.value = clone?.question || "";
  form.elements.seed.value = clone?.design.seed ?? 0;
  form.elements.budget.value =
    clone?.design.budget ??
    Math.max(
      24,
      state.catalog.tasks.find((t) => t.task_id === task)?.budget || 24,
    );
  $("design-task").value = task;
  if (clone?.design.composition)
    $("composition-json").value = pretty(clone.design.composition);
  else $("composition-json").value = pretty(state.catalog.templates[0]);
  changeTask();
  changeMode();
  changeProvider();
  $("design-dialog").showModal();
}
function changeTask() {
  const custom = $("design-task").value === "custom";
  $("composition-fields").hidden = !custom;
  $("task-description").textContent = custom
    ? "编辑已声明组件与兼容域内的组合。创建前由真实构造器校验。"
    : state.catalog.tasks.find((t) => t.task_id === $("design-task").value)
        ?.description || "";
}
function changeMode() {
  const mode = $("design-form").elements.mode.value;
  $("design-title").textContent = mode === "model"
    ? "开始 Agent 自主探索"
    : mode === "manual" ? "创建手动实验" : "运行离线参考流程";
  $("provider-fields").hidden = mode !== "model";
  $("model-input").required = mode === "model";
  $("api-key").required = mode === "model";
  $("create-button").textContent =
    mode === "manual"
      ? "创建手动实验 →"
      : mode === "model"
        ? "创建并调用模型 →"
        : "创建并运行参考流程 →";
}
function changeProvider() {
  const p = state.catalog.providers.find(
    (p) => p.id === $("provider-select").value,
  );
  $("model-input").value = p.suggested_model;
  $("provider-note").textContent =
    `请求目标：${p.url}。请使用该服务可用的模型与 key；提交实验会产生厂商费用。`;
}
function designPayload() {
  const f = $("design-form");
  return {
    seed: Number(f.elements.seed.value),
    budget: Number(f.elements.budget.value),
    ...($("design-task").value === "custom"
      ? { composition: JSON.parse($("composition-json").value) }
      : { task_id: $("design-task").value }),
  };
}
document.addEventListener("click", (e) => {
  const b = e.target.closest("button");
  if (!b) return;
  if (b.dataset.run)
    perform(() => {
      state.tab = "explore";
      return openRun(b.dataset.run);
    });
  if (b.dataset.template) openDesign(b.dataset.template);
  if (b.dataset.nav) {
    if (b.dataset.nav === "home") {
      const latest = state.runs.find((r) => r.status === "running" && r.actor !== "reference") || state.runs[0];
      if (latest) { state.tab = "explore"; perform(() => openRun(latest.id)); }
      else renderHome();
    } else if (b.dataset.nav === "records") renderHome();
    else if (b.dataset.nav === "notes") {
      const id = state.run?.id || state.runs[0]?.id;
      if (id) { state.tab = "notebook"; state.author = "model"; perform(() => openRun(id)); }
      else toast("先开始一个实验，Agent 提交的记录会保存在这里。");
    } else perform(renderCompare);
  }
  if (b.dataset.tab) {
    state.tab = b.dataset.tab;
    renderRun();
  }
  if (b.dataset.event)
    showDetail("公开事件详情", state.run.events[Number(b.dataset.event)]);
  if (b.dataset.author) {
    state.author = b.dataset.author;
    renderNotebook();
  }
  if (b.dataset.revision)
    perform(async () => {
      const note = await api(`/api/runs/${state.run.id}/notebook`, {
        author: state.author,
        operation: "read",
        arguments: { revision: Number(b.dataset.revision), limit: 16000 },
      });
      $("notebook-text").value = note.text;
      $("notebook-version").textContent =
        `正在查看 v${note.revision}${state.author === "human" ? "，保存会新增一个版本" : ""}`;
    });
});
document.addEventListener("change", (e) => {
  if (e.target.dataset.compare) {
    const id = e.target.dataset.compare;
    if (e.target.checked) {
      if (state.selected.size >= 6) {
        e.target.checked = false;
        toast("每次最多比较 6 个实验");
        return;
      }
      state.selected.add(id);
    } else state.selected.delete(id);
    renderSidebar();
    if (state.page === "compare") perform(renderCompare);
  }
});
$("new-run").onclick = () => openDesign();
$("manual-entry").onclick = () => openDesign("reaction-to-assay", null, "manual");
document.querySelectorAll(".close-dialog").forEach(
  (b) =>
    (b.onclick = () => {
      $("api-key").value = "";
      $("design-dialog").close();
    }),
);
$("design-dialog").addEventListener("close", () => ($("api-key").value = ""));
$("close-detail").onclick = () => $("detail-dialog").close();
$("design-task").onchange = changeTask;
$("composition-template").onchange = () => {
  $("composition-json").value = pretty(
    state.catalog.templates[Number($("composition-template").value)],
  );
};
$("provider-select").onchange = changeProvider;
document
  .querySelectorAll("[name=mode]")
  .forEach((r) => (r.onchange = changeMode));
$("validate-design").onclick = () =>
  perform(async () => {
    await api("/api/design/validate", designPayload());
    $("validation-result").textContent = " ✓ 组合校验通过";
  });
$("design-form").onsubmit = async (event) => {
  event.preventDefault();
  const f = event.target;
  const button = $("create-button");
  button.disabled = true;
  $("form-error").textContent = "";
  let created = null;
  try {
    const mode = f.elements.mode.value;
    const job = {
      mode,
      provider: f.elements.provider.value,
      model: f.elements.model.value,
      api_key: f.elements.api_key.value,
      call_limit: Number(f.elements.call_limit.value),
      token_limit: Number(f.elements.token_limit.value),
      max_output: Number(f.elements.max_output.value),
    };
    created = await api("/api/runs", {
      name: f.elements.name.value,
      project: f.elements.project.value,
      question: f.elements.question.value,
      design: designPayload(),
    });
    if (mode !== "manual") {
      try {
        await api(`/api/runs/${created.id}/start`, job);
      } finally {
        job.api_key = "";
        $("api-key").value = "";
      }
    }
    $("design-dialog").close();
    state.tab = "explore";
    await refreshRuns();
    await openRun(created.id);
    toast("实验已创建，记录将自动保存。");
  } catch (error) {
    $("form-error").textContent = error.message;
    if (created) {
      $("design-dialog").close();
      await refreshRuns();
      await openRun(created.id);
      toast(`实验已保留，但未启动：${error.message}`);
    }
  } finally {
    $("api-key").value = "";
    button.disabled = false;
  }
};
async function poll() {
  if (state.polling || !state.catalog) return;
  state.polling = true;
  try {
    const active =
      state.runs.some((r) => ["running", "cancelling"].includes(r.status)) ||
      ["running", "cancelling"].includes(state.run?.status);
    if (active) {
      await refreshRuns();
      if (
        state.page === "run" &&
        ["running", "cancelling"].includes(state.run?.status)
      ) {
        const id = state.run.id;
        const navigation = state.navigation;
        const updated = await api(`/api/runs/${id}`);
        if (
          state.run?.id === id &&
          state.page === "run" &&
          state.navigation === navigation
        ) {
          state.run = updated;
          if (state.tab !== "notebook") renderRun();
        }
      } else if (state.page === "home") renderHome();
    }
    $("connection").textContent = "已连接";
  } catch {
    $("connection").textContent = "连接中断";
  } finally {
    state.polling = false;
  }
}
async function init() {
  try {
    state.catalog = await api("/api/catalog");
    $("design-task").innerHTML =
      state.catalog.tasks
        .map(
          (t) =>
            `<option value="${esc(t.task_id)}">${esc(names[t.task_id] || t.task_id)}</option>`,
        )
        .join("") + '<option value="custom">自定义组件组合…</option>';
    $("composition-template").innerHTML = state.catalog.templates
      .map((t, i) => `<option value="${i}">${esc(t.composition_id)}</option>`)
      .join("");
    $("provider-select").innerHTML = state.catalog.providers
      .map((p) => `<option value="${p.id}">${esc(p.label)}</option>`)
      .join("");
    await refreshRuns();
    $("connection").textContent = "已连接";
    const latest = state.runs.find((r) => r.status === "running") || state.runs[0];
    if (latest) await openRun(latest.id);
    else renderHome();
    setInterval(poll, 1800);
  } catch (error) {
    $("main").textContent = `无法连接本机服务：${error.message}`;
    $("connection").textContent = "未连接";
  }
}
init();
