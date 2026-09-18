import {
  MODE_NAMES,
  LABELS,
  ACTIONS,
  label,
  finite,
  format,
  parseLocal,
  observations,
  snapshot,
  metricSeries,
  scalarColumns,
  datasets,
  numericMetrics,
  csv,
  classify,
} from "./replay.mjs";
import { mountReplay, mountRecordingList } from "./viewer.mjs";

const $ = (id) => document.getElementById(id);
const state = {
  catalog: null,
  entries: [],
  imports: new Map(),
  category: "all",
  page: 0,
  selected: null,
  request: 0,
  trajectoryRequest: 0,
  playback: null,
  timer: null,
  tab: "overview",
  verifyBusy: false,
  recordingMeta: new Map(),
};
const PAGE = 30;
function syncFocusLabel() {
  $("focusWorkspace").textContent = document
    .querySelector(".workspace")
    .classList.contains("focused")
    ? "显示实验目录"
    : "扩展工作区";
}
$("focusWorkspace").onclick = () => {
  document.querySelector(".workspace").classList.toggle("focused");
  syncFocusLabel();
};
const titles = {
  w2_61_codex_open_action_donor: "GPT · 多轮实验与决策记录",
  w2_50_open_action: "先验三臂 · 多轮自主实验",
  w2_105_full_process_iteration: "完整流程 · 开发迭代总览",
  w2_105d_crystal_seed_continuity: "结晶过程 · 晶种与交付连续性",
  w2_105c_crystal_thermal_continuity: "结晶过程 · 热历史连续性",
  w2_105b_process_continuity: "完整流程 · 过程连续性",
  w2_105_phase_resolved_process: "完整流程 · 分相与测量",
  w2_104_full_process_diagnostic: "完整流程 · 可达性与接口诊断",
  w2_103_astra_full_process_trial: "Astra · 完整流程单轮实验",
  w2_100_astra_state_resolved_pilot: "Astra · 实际温度解析试跑",
  w2_99_astra_single_trial: "Astra · 首轮开发试跑",
  w2_72_m1_replication: "M1 · 知识交付与独立复现",
  w2_69_m3_portability: "M3 · 知识可迁移性",
  w2_77_final_diagnostic: "结构理解与行动 · 最终诊断",
};
function displayTitle(entry) {
  for (const binding of entry.bindings || [])
    for (const part of binding.split("."))
      if (titles[part]) return titles[part];
  return entry.title;
}
function el(tag, attrs = {}, ...children) {
  const node = document.createElement(tag);
  for (const [key, value] of Object.entries(attrs)) {
    if (key.startsWith("on")) node.addEventListener(key.slice(2), value);
    else if (key === "class") node.className = value;
    else if (key === "text") node.textContent = value;
    else if (value !== false && value !== null && value !== undefined)
      node.setAttribute(key, value === true ? "" : String(value));
  }
  for (const child of children.flat(Infinity)) {
    if (child !== null && child !== undefined && child !== false)
      node.append(
        child instanceof Node ? child : document.createTextNode(String(child)),
      );
  }
  return node;
}
function button(text, handler, cls = "button secondary", attrs = {}) {
  return el("button", { class: cls, onclick: handler, ...attrs }, text);
}
function pill(text, type = "") {
  return el("span", { class: `pill ${type}` }, text);
}
function notice(message) {
  $("notice").hidden = !message;
  $("notice").textContent = message;
}
function errorPanel(message) {
  return el("div", { class: "alert error", role: "alert" }, message);
}
function empty(message) {
  return el("div", { class: "empty" }, message);
}
async function api(path, body) {
  const response = await fetch(
    path,
    body === undefined
      ? {}
      : {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(body),
        },
  );
  const payload = await response.json();
  if (!response.ok) throw Error(payload.error || `HTTP ${response.status}`);
  return payload;
}
function download(name, value, type = "application/json") {
  const text =
    typeof value === "string" ? value : JSON.stringify(value, null, 2);
  const url = URL.createObjectURL(new Blob([text], { type }));
  const a = el("a", { href: url, download: name });
  document.body.append(a);
  a.click();
  a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 5000);
}
function stopPlayback() {
  if (state.timer) clearInterval(state.timer);
  state.timer = null;
  if (state.playback?.playButton)
    state.playback.playButton.textContent = "▶ 播放";
}
function safeAction(fn) {
  return async () => {
    try {
      await fn();
    } catch (error) {
      notice(error.message);
    }
  };
}
function metricLabel(key) {
  return key.split(".").map(label).join(" · ");
}
function metricsView(metrics, limit = 12) {
  const box = el("div", { class: "summary-metrics" });
  for (const metric of metrics.slice(0, limit))
    box.append(
      el(
        "div",
        { class: "metric-box" },
        el("span", { title: metric.key }, metricLabel(metric.key)),
        el("strong", {}, format(metric.value)),
      ),
    );
  return box;
}
function showInspector(title, value) {
  $("inspectorTitle").textContent = title;
  $("inspectorBody").replaceChildren(jsonTree(value));
  $("inspector").showModal();
}
$("closeInspector").onclick = () => $("inspector").close();
function jsonTree(value) {
  const root = el("div", { class: "json-tree" });
  function item(key, data) {
    if (data === null || typeof data !== "object")
      return el(
        "div",
        { class: "leaf" },
        el("b", {}, `${key}: `),
        String(data),
      );
    const count = Object.keys(data).length;
    const d = el(
      "details",
      {},
      el(
        "summary",
        {},
        `${key} ${Array.isArray(data) ? "[" : "{"}${count} 项${Array.isArray(data) ? "]" : "}"}`,
      ),
    );
    let loaded = false;
    d.addEventListener("toggle", () => {
      if (!d.open || loaded) return;
      loaded = true;
      const entries = Object.entries(data);
      let offset = 0;
      const more = button("显示后续 100 项", append, "");
      function append() {
        more.remove();
        for (const [k, v] of entries.slice(offset, offset + 100))
          d.append(item(k, v));
        offset += 100;
        if (offset < entries.length) d.append(more);
      }
      append();
    });
    return d;
  }
  for (const [key, data] of Object.entries(value || {}))
    root.append(item(key, data));
  return root;
}

async function loadCatalog(refresh = false) {
  $("refresh").disabled = true;
  $("indexState").textContent = refresh ? "正在刷新索引" : "正在读取目录";
  try {
    const data = await api(
      refresh ? "/api/refresh" : "/api/catalog",
      refresh ? {} : undefined,
    );
    state.catalog = data;
    if (refresh) state.recordingMeta.clear();
    state.entries = data.entries;
    updateCounts();
    renderEntries();
    $("indexState").textContent = "本地索引就绪";
    $("indexTime").textContent = new Date(
      data.indexed_at * 1000,
    ).toLocaleString("zh-CN", { hour12: false });
    if (data.errors.length)
      notice(
        `目录提示：${data.errors.map((x) => `${x.path}: ${x.error}`).join("；")}`,
      );
    if (!state.selected) {
      const first =
        data.entries.find((e) =>
          e.bindings?.some((b) => b.includes("w2_61_codex_open_action_donor")),
        ) ||
        data.entries.find((e) =>
          e.bindings?.some((b) => b.includes("w2_105_full_process_iteration")),
        ) ||
        data.entries.find((e) => e.kind === "report") ||
        data.entries[0];
      if (first) await selectEntry(first);
    }
  } catch (error) {
    notice(`读取目录失败：${error.message}`);
    $("indexState").textContent = "连接失败";
    $("entryList").replaceChildren(
      empty("无法读取目录。请确认本地服务运行后点击刷新。"),
    );
  } finally {
    $("refresh").disabled = false;
  }
}
function updateCounts() {
  const c = state.catalog?.counts || {};
  $("statReports").textContent = format(c.reports);
  $("statRuns").textContent = format(c.runs);
  $("statTrajectories").textContent = format(c.trajectories);
  const entries = allEntries();
  $("categoryNav").replaceChildren(
    ...[
      { id: "all", label: "全部实验" },
      ...(state.catalog?.categories || []),
    ].map(
      (category) =>
        button(
          "",
          () => {
            state.category = category.id;
            state.page = 0;
            updateCounts();
            renderEntries();
            document.querySelector(".workspace").classList.remove("focused");
            syncFocusLabel();
          },
          `nav-button ${state.category === category.id ? "active" : ""}`,
          {
            "data-category": category.id,
            "aria-pressed": state.category === category.id,
          },
        ).appendChild(
          el(
            "span",
            { class: "category-nav-content" },
            el("span", {}, category.label),
            el(
              "span",
              {},
              category.id === "all"
                ? entries.length
                : entries.filter((e) => e.categories?.includes(category.id))
                    .length,
            ),
          ),
        ).parentNode,
    ),
  );
}
function categoryLabel(entry) {
  const labels = (state.catalog?.categories || [])
    .filter((c) => entry.categories?.includes(c.id))
    .map((c) => c.label);
  return labels.length > 2
    ? `${labels.slice(0, 2).join(" · ")} +${labels.length - 2}`
    : labels.join(" · ") || "综合与未分类";
}
function allEntries() {
  return [...[...state.imports.values()].map((x) => x.entry), ...state.entries];
}
function filteredEntries() {
  const query = $("search").value.trim().toLowerCase();
  const source = $("source").value,
    mode = $("mode").value;
  return allEntries().filter(
    (e) =>
      (source === "all" || e.kind === source) &&
      (state.category === "all" || e.categories?.includes(state.category)) &&
      (!mode || e.mode === mode) &&
      (!query ||
        `${displayTitle(e)} ${categoryLabel(e)} ${e.path} ${e.bindings?.join(" ")}`
          .toLowerCase()
          .includes(query)),
  );
}
function renderEntries() {
  const entries = filteredEntries();
  const pages = Math.max(1, Math.ceil(entries.length / PAGE));
  state.page = Math.min(state.page, pages - 1);
  $("resultCount").textContent = `${entries.length} 条`;
  $("entryPage").textContent = `${state.page + 1} / ${pages}`;
  $("prevEntries").disabled = state.page === 0;
  $("nextEntries").disabled = state.page >= pages - 1;
  const list = $("entryList");
  list.replaceChildren();
  for (const entry of entries.slice(
    state.page * PAGE,
    (state.page + 1) * PAGE,
  )) {
    const date = entry.modified
      ? new Date(entry.modified * 1000).toLocaleDateString("zh-CN")
      : "本地文件";
    list.append(
      button(
        "",
        () => selectEntry(entry),
        `entry ${state.selected?.id === entry.id ? "selected" : ""}`,
        { "aria-pressed": state.selected?.id === entry.id },
      ).appendChild(
        el(
          "div",
          {},
          el(
            "div",
            { class: "entry-top" },
            pill(categoryLabel(entry)),
            pill(MODE_NAMES[entry.mode] || entry.mode, entry.mode),
          ),
          el("div", { class: "entry-title" }, displayTitle(entry)),
          el(
            "div",
            { class: "entry-meta" },
            el(
              "span",
              {},
              entry.kind === "report"
                ? entry.available
                  ? "绑定报告"
                  : "源文件缺失"
                : entry.kind === "import"
                  ? "手动导入"
                  : `${format(entry.trajectory_count)} 条轨迹`,
            ),
            el("span", {}, date),
          ),
        ),
      ).parentNode,
    );
  }
  if (!entries.length)
    list.append(empty("没有匹配的实验。调整筛选，或导入本地文件。"));
}
for (const id of ["search", "source", "mode"])
  $(id).addEventListener(id === "search" ? "input" : "change", () => {
    state.page = 0;
    renderEntries();
  });
$("prevEntries").onclick = () => {
  state.page--;
  renderEntries();
};
$("nextEntries").onclick = () => {
  state.page++;
  renderEntries();
};
$("refresh").onclick = () => loadCatalog(true);

async function selectEntry(entry) {
  stopPlayback();
  document.querySelector(".workspace").classList.remove("focused");
  $("detail").classList.remove("replay-open");
  syncFocusLabel();
  state.playback = null;
  state.selected = entry;
  const request = ++state.request;
  ++state.trajectoryRequest;
  renderEntries();
  const host = $("detail");
  host.replaceChildren(empty("正在读取实验记录…"));
  $("footerStatus").textContent = "按需读取记录";
  try {
    let detail;
    if (entry.kind === "import") {
      const imported = state.imports.get(entry.id);
      if (!imported.data)
        imported.data = parseLocal(
          await imported.file.text(),
          imported.file.name,
        );
      if (request !== state.request) return;
      entry.categories = classify(
        imported.data.records || imported.data.report,
        state.catalog?.categories || [],
      );
      updateCounts();
      renderEntries();
      if (imported.data.kind === "trajectory") {
        detail = {
          entry,
          report: { records: imported.data.records },
          metrics: [],
          trajectories: [],
          localPayload: {
            ...imported.data,
            name: imported.file.name,
            path: imported.file.name,
          },
        };
        renderDetail(detail);
        return;
      }
      detail = {
        entry,
        report: imported.data.report,
        metrics: numericMetrics(imported.data.report),
        trajectories: [],
      };
    } else
      detail = await api(`/api/experiment?id=${encodeURIComponent(entry.id)}`);
    if (request !== state.request) return;
    renderDetail(detail);
    $("footerStatus").textContent =
      `${entry.kind === "report" ? "当前绑定报告" : "本地记录"} · ${detail.trajectories.length} 条关联轨迹`;
  } catch (error) {
    if (request === state.request)
      host.replaceChildren(
        errorPanel(error.message),
        button("重试", () => selectEntry(entry)),
      );
  }
}
function renderDetail(detail) {
  const host = $("detail"),
    entry = detail.entry;
  host.replaceChildren(
    el(
      "div",
      { class: "detail-header" },
      el(
        "div",
        { class: "detail-kicker" },
        pill(categoryLabel(entry)),
        pill(MODE_NAMES[entry.mode] || entry.mode, entry.mode),
        pill(
          entry.kind === "report"
            ? "当前绑定"
            : entry.kind === "import"
              ? "本地导入"
              : "本地档案",
        ),
      ),
      el("h2", {}, displayTitle(entry)),
      el("div", { class: "source-path" }, entry.path),
    ),
  );
  if (detail.error) host.append(errorPanel(detail.error));
  const tabs = el("div", {
    class: "tabs",
    role: "tablist",
    "aria-label": "实验视图",
  });
  const content = el("div", { id: "tabContent", role: "tabpanel" });
  const views = [
    ["overview", "结果概览"],
    [
      "trajectories",
      `实验组与回放 ${detail.localPayload ? 1 : detail.trajectories.length || ""}`,
    ],
    ["source", "原始记录"],
  ];
  function activate(key) {
    stopPlayback();
    state.playback = null;
    ++state.trajectoryRequest;
    state.tab = key;
    for (const b of tabs.children) {
      b.classList.toggle("active", b.dataset.key === key);
      b.setAttribute("aria-selected", b.dataset.key === key);
    }
    content.replaceChildren();
    if (key === "overview") renderReport(detail, content);
    if (key === "trajectories") renderTrajectories(detail, content);
    if (key === "source")
      content.append(
        el(
          "p",
          { class: "footnote" },
          "按原文件展开字段；数值口径、失败与缺失值保持原记录。",
        ),
        button("下载报告 JSON", () =>
          download("experiment-report.json", detail.report),
        ),
        jsonTree(detail.report),
      );
  }
  for (const [key, text] of views)
    tabs.append(
      button(text, () => activate(key), "tab", {
        role: "tab",
        "data-key": key,
        "aria-selected": false,
      }),
    );
  host.append(tabs, content);
  activate(
    entry.kind === "run" ||
      detail.localPayload ||
      entry.bindings?.some((b) => b.includes("w2_61_codex_open_action_donor"))
      ? "trajectories"
      : "overview",
  );
}
function renderReport(detail, host) {
  const report = detail.report,
    metrics = detail.metrics.length ? detail.metrics : numericMetrics(report);
  if (metrics.length) {
    host.append(metricsView(metrics));
    if (metrics.length > 12)
      host.append(
        el(
          "details",
          { class: "analysis-block" },
          el("summary", {}, `全部计数与分母 (${metrics.length})`),
          metricsView(metrics, metrics.length),
        ),
      );
  }
  const notes = [
    report.interpretation,
    report.limits,
    report.stop_reason,
  ].filter((x) => typeof x === "string");
  for (const note of notes) host.append(el("p", { class: "footnote" }, note));
  const sets = datasets(report);
  if (!sets.length) {
    host.append(
      empty(
        Object.keys(report).length
          ? "此报告没有可自动绘图的条件表；可在原始记录中查看全部字段。"
          : "此批次按轨迹保存。选择“轨迹回放”浏览每一步操作。",
      ),
    );
    return;
  }
  sets.sort((a, b) => (b.name === "cells") - (a.name === "cells"));
  const selector = el("select", {
    class: "wide-select",
    "aria-label": "报告数据表",
  });
  for (const [i, set] of sets.entries())
    selector.append(
      el(
        "option",
        { value: i },
        `${metricLabel(set.name)} · ${set.rows.length} 行`,
      ),
    );
  const display = el("div");
  host.append(
    el("div", { class: "toolbar" }, el("h3", {}, "条件与结果"), selector),
    display,
  );
  selector.onchange = () =>
    renderDataset(sets[Number(selector.value)], display);
  renderDataset(sets[0], display);
}

function svgNode(tag, attrs = {}, text) {
  const node = document.createElementNS("http://www.w3.org/2000/svg", tag);
  for (const [k, v] of Object.entries(attrs)) node.setAttribute(k, String(v));
  if (text !== undefined) node.textContent = text;
  return node;
}
function chart(
  points,
  {
    current = null,
    bars = false,
    title = "指标",
    onSeek = null,
    unit = "步",
  } = {},
) {
  const w = 700,
    h = 230,
    pad = { l: 52, r: 18, t: 15, b: 34 };
  const svg = svgNode("svg", {
    viewBox: `0 0 ${w} ${h}`,
    class: "chart",
    role: "img",
    "aria-label": title,
  });
  svg.append(svgNode("title", {}, title));
  const values = points.map((p) => p.value).filter(finite);
  if (!values.length) {
    svg.append(
      svgNode(
        "text",
        { x: w / 2, y: h / 2, "text-anchor": "middle" },
        "此范围内没有已观测的数值",
      ),
    );
    return svg;
  }
  let min = Math.min(...values),
    max = Math.max(...values);
  if (bars) min = Math.min(0, min);
  if (min === max) {
    min -= Math.abs(min) * 0.1 || 0.1;
    max += Math.abs(max) * 0.1 || 0.1;
  }
  const range = max - min;
  const y = (v) => h - pad.b - ((v - min) / range) * (h - pad.t - pad.b);
  const x = (i) =>
    pad.l +
    (points.length === 1 ? 0.5 : i / (points.length - 1)) * (w - pad.l - pad.r);
  for (let i = 0; i < 5; i++) {
    const value = min + (range * i) / 4,
      yy = y(value);
    svg.append(
      svgNode("line", {
        x1: pad.l,
        x2: w - pad.r,
        y1: yy,
        y2: yy,
        class: "grid",
      }),
      svgNode(
        "text",
        { x: pad.l - 9, y: yy + 4, "text-anchor": "end" },
        Math.abs(value) >= 10000
          ? value.toExponential(1)
          : Number(value.toPrecision(3)).toString(),
      ),
    );
  }
  if (bars) {
    const bw = Math.max(
      1,
      ((w - pad.l - pad.r) / Math.max(points.length, 1)) * 0.62,
    );
    points.forEach((p, i) => {
      if (!finite(p.value)) return;
      const zero = y(Math.max(min, Math.min(max, 0)));
      const rect = svgNode("rect", {
        x: x(i) - bw / 2,
        y: Math.min(y(p.value), zero),
        width: bw,
        height: Math.max(1, Math.abs(zero - y(p.value))),
        class: `bar ${p.failed ? "failed" : ""}`,
      });
      rect.append(
        svgNode("title", {}, `${p.name || p.step}: ${format(p.value)}`),
      );
      svg.append(rect);
    });
  } else {
    let path = "",
      connected = false;
    points.forEach((p, i) => {
      if (!finite(p.value)) {
        connected = false;
        return;
      }
      path += `${connected ? "L" : "M"}${x(i)},${y(p.value)} `;
      connected = true;
    });
    svg.append(svgNode("path", { d: path, class: "curve" }));
    for (let i = 0; i < points.length; i++) {
      const p = points[i];
      if (finite(p.value)) {
        const dot = svgNode("circle", {
          cx: x(i),
          cy: y(p.value),
          r: points.length > 250 ? 1.5 : 3,
          class: "dot",
        });
        dot.append(svgNode("title", {}, `第 ${p.step} 步: ${format(p.value)}`));
        svg.append(dot);
      }
    }
  }
  for (const i of new Set([
    0,
    Math.floor((points.length - 1) / 2),
    points.length - 1,
  ]))
    svg.append(
      svgNode(
        "text",
        { x: x(i), y: h - 10, "text-anchor": "middle" },
        bars ? `${i + 1}` : `${i + 1} ${unit}`,
      ),
    );
  if (current !== null)
    svg.append(
      svgNode("line", {
        x1: x(current),
        x2: x(current),
        y1: pad.t,
        y2: h - pad.b,
        class: "cursor",
      }),
    );
  if (onSeek) {
    svg.setAttribute("tabindex", "0");
    svg.setAttribute("aria-label", `${title}；左右键切换步骤，点击选择步骤`);
    svg.addEventListener("click", (e) => {
      const rect = svg.getBoundingClientRect();
      const vx = ((e.clientX - rect.left) / rect.width) * w;
      onSeek(
        Math.max(
          0,
          Math.min(
            points.length - 1,
            Math.round(
              ((vx - pad.l) / (w - pad.l - pad.r)) * (points.length - 1),
            ),
          ),
        ),
      );
    });
    svg.addEventListener("keydown", (e) => {
      if (["ArrowLeft", "ArrowRight"].includes(e.key)) {
        e.preventDefault();
        onSeek((current || 0) + (e.key === "ArrowRight" ? 1 : -1));
      }
    });
  }
  return svg;
}
function renderDataset(set, host) {
  host.replaceChildren();
  const rows = set.rows.map((r) => scalarColumns(r));
  const keys = [...new Set(rows.flatMap((r) => Object.keys(r)))];
  const preferred = [
    "cell",
    "task",
    "task_id",
    "condition",
    "kind",
    "status",
    "quality_passed",
    "witness",
    "final_metrics.purity",
    "final_metrics.recovery",
    "final_metrics.crystal_fines_fraction",
    "leaderboard_score",
    "operations",
    "replay.verified",
  ];
  const selected = [
    ...preferred.filter((k) => keys.includes(k)),
    ...keys.filter((k) => !preferred.includes(k)),
  ]
    .filter((k) => !/(sha256|hash|source_commit|seed|path|prompt)/i.test(k))
    .slice(0, 10);
  const numeric = keys.filter(
    (k) => rows.some((r) => finite(r[k])) && !/(seed|hash)/i.test(k),
  );
  if (numeric.length) {
    const panel = el("div", { class: "chart-panel" });
    const select = el("select", {
      "aria-label": "图表指标",
      class: "wide-select",
    });
    for (const key of numeric)
      select.append(el("option", { value: key }, metricLabel(key)));
    select.value = numeric.includes("final_metrics.purity")
      ? "final_metrics.purity"
      : numeric[0];
    const graph = el("div");
    const meta = el("p", { class: "footnote" });
    panel.append(
      el("div", { class: "chart-head" }, el("h3", {}, "条件读数"), select),
      graph,
      meta,
    );
    function draw() {
      const key = select.value;
      const shown = rows.slice(0, 80);
      graph.replaceChildren(
        chart(
          shown.map((r, i) => ({
            step: i + 1,
            name: r.cell || r.condition || i + 1,
            value: r[key] ?? null,
            failed: r.quality_passed === false || !!set.rows[i].failure,
          })),
          { bars: true, title: metricLabel(key) },
        ),
      );
      meta.textContent = `${rows.length > 80 ? `显示前 80 / ${rows.length} 条；` : `显示 ${rows.length} 条；`}每列对应原表一行，悬停查看数值。缺失不计零，红色表示原记录质量未通过或执行失败。`;
    }
    select.onchange = draw;
    draw();
    host.append(panel);
  }
  const tableHost = el("div");
  let page = 0;
  const pages = Math.max(1, Math.ceil(rows.length / 50));
  const prev = button(
      "←",
      () => {
        page--;
        drawTable();
      },
      "",
      { "aria-label": "上一页结果" },
    ),
    next = button(
      "→",
      () => {
        page++;
        drawTable();
      },
      "",
      { "aria-label": "下一页结果" },
    ),
    pageText = el("span");
  host.append(
    el(
      "div",
      { class: "toolbar" },
      button("导出完整表 CSV", () =>
        download(
          "experiment-table.csv",
          csv(rows, keys),
          "text/csv;charset=utf-8",
        ),
      ),
      button("查看全部字段", () => showInspector(set.name, { rows: set.rows })),
    ),
    tableHost,
    el("div", { class: "pagination" }, prev, pageText, next),
  );
  function drawTable() {
    const table = el("table", { class: "data-table" });
    table.append(
      el(
        "thead",
        {},
        el(
          "tr",
          {},
          el("th", {}, "#"),
          selected.map((k) => el("th", { title: k }, metricLabel(k))),
          el("th", {}, "记录"),
        ),
      ),
    );
    const body = el("tbody");
    rows.slice(page * 50, (page + 1) * 50).forEach((row, i) => {
      const index = page * 50 + i;
      body.append(
        el(
          "tr",
          {},
          el("td", {}, index + 1),
          selected.map((k) =>
            el("td", { title: String(row[k] ?? "") }, format(row[k])),
          ),
          el(
            "td",
            {},
            button(
              "展开",
              () => showInspector(`第 ${index + 1} 条记录`, set.rows[index]),
              "row-button",
            ),
          ),
        ),
      );
    });
    table.append(body);
    tableHost.replaceChildren(el("div", { class: "data-table-wrap" }, table));
    prev.disabled = page === 0;
    next.disabled = page >= pages - 1;
    pageText.textContent = `${page + 1} / ${pages} · 共 ${rows.length} 行`;
  }
  drawTable();
  host.append(
    el(
      "p",
      { class: "footnote" },
      "表格保留原报告的行与计数；报告可能是汇总或包含重复测量，这里不将行数解释为独立样本数。",
    ),
  );
}

function renderTrajectories(detail, host) {
  return mountRecordingList(detail, host, {
    el,
    button,
    pill,
    empty,
    api,
    state,
    loadTrajectory,
    openPlayback,
  });
}
async function loadTrajectory(item, host, back) {
  const request = ++state.trajectoryRequest;
  stopPlayback();
  host.replaceChildren(empty("正在读取轨迹…"));
  try {
    const payload = await api(`/api/trajectory?id=${item.id}`);
    if (request !== state.trajectoryRequest) return;
    openPlayback(payload, host, () => {
      stopPlayback();
      state.playback = null;
      host.replaceChildren();
      back();
    });
  } catch (error) {
    if (request === state.trajectoryRequest)
      host.replaceChildren(
        errorPanel(error.message),
        button("返回轨迹列表", () => {
          host.replaceChildren();
          back();
        }),
      );
  }
}
function keyValues(value) {
  const pairs = Object.entries(value).filter(
    ([, v]) => v === null || typeof v !== "object",
  );
  return el(
    "dl",
    { class: "kv" },
    pairs.flatMap(([k, v]) => [
      el("dt", {}, label(k)),
      el("dd", {}, format(v)),
    ]),
  );
}
function openPlayback(payload, host, back) {
  document.querySelector(".workspace").classList.add("focused");
  document.getElementById("detail").classList.add("replay-open");
  syncFocusLabel();
  const returnToList = back
    ? () => {
        document.querySelector(".workspace").classList.remove("focused");
        document.getElementById("detail").classList.remove("replay-open");
        syncFocusLabel();
        back();
      }
    : null;
  return mountReplay(payload, host, returnToList, {
    el,
    button,
    pill,
    empty,
    keyValues,
    jsonTree,
    showInspector,
    chart,
    download,
    stopPlayback,
    state,
    verifyTrajectory,
  });
}
async function verifyTrajectory(playback, status, buttonNode) {
  if (state.verifyBusy) throw Error("已有精确重算正在进行，请等待结果。");
  state.verifyBusy = true;
  buttonNode.disabled = true;
  const start = Date.now();
  status.textContent = "正在启动精确重算…";
  try {
    const job = await api("/api/verify", { id: playback.payload.id });
    while (true) {
      const result = await api(`/api/verification?id=${job.id}`);
      if (result.status === "done") {
        const r = result.result;
        status.replaceChildren(
          pill(
            r.verified ? "当前版本精确重算通过" : "当前版本重算存在失配",
            r.verified ? "success" : "failure",
          ),
          el(
            "span",
            {},
            ` ${r.checked_steps} 步 · 最大误差 ${format(r.max_abs_error)} · ${r.mismatches.length} 处失配 `,
          ),
          button(
            "查看核对详情",
            () => showInspector("精确重算结果", r),
            "row-button",
          ),
        );
        break;
      }
      if (result.status === "error") {
        status.replaceChildren(
          errorPanel(
            `无法完成当前版本验证：${result.error}。原始文件和历史验证结果保持不变。`,
          ),
        );
        break;
      }
      status.textContent = `正在按原动作精确重算 · ${Math.round((Date.now() - start) / 1000)} 秒 · 已检查步数等待原生验证器返回`;
      await new Promise((resolve) => setTimeout(resolve, 1000));
    }
  } finally {
    state.verifyBusy = false;
    buttonNode.disabled = false;
  }
}
document.addEventListener("keydown", (event) => {
  if (
    !state.playback ||
    $("inspector").open ||
    ["INPUT", "SELECT", "TEXTAREA", "BUTTON"].includes(event.target.tagName)
  )
    return;
  if ([" ", "ArrowLeft", "ArrowRight"].includes(event.key)) {
    event.preventDefault();
    if (event.key === " ") state.playback.playButton.click();
    else state.playback.nudge(event.key === "ArrowRight" ? 1 : -1);
  }
});
document.addEventListener("visibilitychange", () => {
  if (document.hidden) stopPlayback();
});
async function importFiles(files) {
  const accepted = [...files].filter((f) => /\.jsonl?$/i.test(f.name));
  const rejected = [];
  let first = null;
  for (const file of accepted) {
    if (file.size > 128 * 1024 * 1024) {
      rejected.push(`${file.name} 超过 128 MiB`);
      continue;
    }
    const id = crypto.randomUUID();
    const entry = {
      id,
      title: file.name,
      path: file.name,
      kind: "import",
      mode: "unspecified",
      categories: ["other"],
      modified: file.lastModified / 1000,
      available: true,
      bindings: [],
    };
    state.imports.set(id, { entry, file });
    first ||= entry;
  }
  state.category = "all";
  updateCounts();
  $("source").value = "import";
  state.page = 0;
  $("search").value = "";
  $("mode").value = "";
  renderEntries();
  notice(
    rejected.length
      ? rejected.join("；")
      : accepted.length
        ? ""
        : "请选择 JSON 或 JSONL 文件",
  );
  if (first) await selectEntry(first);
}
$("fileInput").onchange = (event) => {
  importFiles(event.target.files);
  event.target.value = "";
};
const drop = $("dropzone");
for (const name of ["dragenter", "dragover"])
  drop.addEventListener(name, (event) => {
    event.preventDefault();
    drop.classList.add("dragging");
  });
for (const name of ["dragleave", "drop"])
  drop.addEventListener(name, (event) => {
    event.preventDefault();
    drop.classList.remove("dragging");
  });
drop.addEventListener("drop", (event) => importFiles(event.dataTransfer.files));
window.addEventListener("dragover", (e) => e.preventDefault());
window.addEventListener("drop", (e) => {
  e.preventDefault();
  if (!drop.contains(e.target)) importFiles(e.dataTransfer.files);
});
loadCatalog();
