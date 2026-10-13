import { drawChart, explorationGraph, drawExplorationGraph, icon, eventSummary } from "./charts.js";

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
const hasModelUsage = (r) => Boolean(r.model_calls || r.provider);
const modelCallCount = (r) => r.model_calls ?? "未提供";
const modelUsageText = (r, key) => hasModelUsage(r)
  ? number(key ? r.usage?.[key] || 0 : (r.usage?.input_tokens || 0) + (r.usage?.output_tokens || 0), 0) + (r.usage?.complete ? "" : "（不完整）")
  : "未调用";
const state = {
  catalog: null,
  runs: [],
  run: null,
  page: "home",
  tab: "explore",
  graphMode: "events",
  graphViews: new Map(),
  inspectorTab: "event",
  eventSelection: new Map(),
  canvasExpanded: false,
  previewRevision: null,
  graphController: null,
  previewSignal: null,
  chartObserver: null,
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
  "equilibrium-characterization": "平衡表征",
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
  filter_crystals: "过滤晶体",
  run_flow: "运行连续流",
  set_flow: "设置流量",
  set_flow_rate: "设置流量",
  set_potential: "设置电位",
  electrolyze: "电解",
  add_component: "加入组分",
  create_container: "创建容器",
  transfer: "转移物料",
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
  flow_rate_mL_min: "流量 (mL/min)",
  residence_time_s: "请求停留时间 (s)",
  reagent: "试剂",
  seed_mass_g: "晶种质量 (g)",
  cooling_rate_K_min: "降温速率 (K/min)",
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
  document.body.classList.toggle("explore-mode", state.page === "run" && state.tab === "explore");
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
  disposeExplorer();
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
    [state.runs.length, "实验记录", "组"],
    [working, "后台运行", "组"],
    [completed, "含终检记录", "组"],
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
  if (state.run?.id !== run.id) state.previewRevision = null;
  state.run = run;
  state.page = "run";
  history.replaceState(null, "", "?run=" + encodeURIComponent(id));
  renderRun();
}
function disposeExplorer() {
  state.graphController?.dispose();
  state.graphController = null;
  state.chartObserver?.disconnect();
  state.chartObserver = null;
}
function runMessage(r) {
  if (r.archive_only && r.message) return r.message;
  const rollback = r.events.findLast(e => e.transaction_status === "rolled_back");
  if (r.status === "failed" && rollback) return eventSummary(rollback).summary;
  if (r.message === "Native model report saved.") return r.status === "failed" ? "实验未完成，请查看操作记录和模型报告。" : "模型报告已保存。";
  return r.message;
}
function renderRun() {
  const r = state.run;
  const inspectorScroll=document.querySelector(".inspector-body")?.scrollTop || 0;
  disposeExplorer();
  state.previewEpoch++;
  renderSidebar();
  const active = ["ready", "running", "cancelling"].includes(r.status);
  $("main").innerHTML = state.tab === "explore" ? renderExploreHeader(r) + `<div id="run-panel"></div>` :
    `<section class="run-heading"><div><div class="eyebrow">${esc(r.project)} / EXPERIMENT</div><h1>${esc(r.name)}</h1>${badge(r.status)} <span class="muted compact">${esc(taskName(r.design))} · seed ${r.design.seed} · ${date(r.created_at)}</span><p>${esc(r.question || "")}</p></div><div class="row-actions"><button class="button secondary small" id="clone-run">新建同条件实验</button>${active ? '<button class="button danger small" id="cancel-run">' + (r.status === "ready" ? "关闭实验" : "取消运行") + "</button>" : ""}<button class="button secondary small" id="replay-run" ${["running", "cancelling"].includes(r.status) ? "disabled" : ""}>精确回放</button><a class="button secondary small" href="/api/runs/${r.id}/export">导出 ZIP ↗</a></div></section>
  ${r.message && (state.tab !== "explore" || ["failed", "interrupted", "truncated", "cancelled"].includes(r.status)) ? `<div class="notice ${["failed", "interrupted", "truncated"].includes(r.status) ? "warning" : ""}">${esc(runMessage(r))}</div>` : ""}
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
  if (state.tab === "explore") {
    if (active) {
      const stop = document.createElement("button");
      stop.id = "cancel-run"; stop.className = "button secondary explore-stop";
      stop.textContent = r.status === "cancelling" ? "停止中…" : "■ 停止";
      stop.disabled = r.status === "cancelling";
      document.querySelector(".explore-title-line").append(stop);
    }
    renderExplorer();
    document.querySelector(".inspector-body").scrollTop=inspectorScroll;
  }
  if (state.tab === "timeline") renderTimeline();
  if (state.tab === "spectra") renderSpectra();
  if (state.tab === "notebook") renderNotebook();
  if (state.tab === "report") renderReport();
  archiveControls(r);
  if ($("cancel-run"))
    $("cancel-run").onclick = () =>
      perform(async () => {
        state.run = await api(`/api/runs/${r.id}/cancel`, {});
        renderRun();
        await refreshRuns();
      });

}


function applyTheme(theme) {
  document.documentElement.dataset.theme = theme;
  const dark = theme === "dark";
  $("theme-toggle").innerHTML = icon(dark ? "sun" : "moon") + `<span>${dark ? "浅色模式" : "深色模式"}</span>`;
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
function archiveControls(r) {
  if(!r.archive_only) return;
  if($('clone-run')) { $('clone-run').disabled=true; $('clone-run').title='多批论文协议不能直接复制为网页单批实验'; }
  if($('replay-run')) { $('replay-run').disabled=true; $('replay-run').textContent=r.replay?.verified?'执行时回放已通过':'查看原回放记录'; }
}
function renderExploreHeader(r) {
  const isModel = !['manual','reference'].includes(r.actor);
  return `<header class="explore-title"><div class="explore-title-line"><h1>${esc(r.batch_count?r.name:taskName(r.design))}</h1>${badge(r.status)}<span class="environment-tag">${isModel?'Agent 自主探索':r.actor==='reference'?'固定参考流程':'手动实验'}</span><span class="run-title-name" title="${esc(r.name)}">${esc(r.batch_count?r.batch_count+' 批 · 开发复跑':r.name)}</span></div><p>${esc(r.question || '尚未设置研究目标')}</p></header>`;
}
function formatDuration(seconds) {
  if (!Number.isFinite(seconds)) return '—';
  if (seconds < 60) return number(seconds,1)+' s';
  return number(seconds/60,1)+' min';
}
function renderExplorer() {
  const r=state.run;
  const hasNetwork=Boolean(r.view?.component_network?.vessels?.length);
  const eventIndex=state.eventSelection.get(r.id) ?? r.events.length-1;
  const batch=r.batch_count?r.events[eventIndex]?.batch:null;
  const graph=explorationGraph(r,hasNetwork?state.graphMode:'events',{...operations,...fieldNames},batch);
  graph.selectedId=r.events[eventIndex]?.event_id;
  const consumed=r.view?.campaign_state?.operation_count ?? r.executed_steps;
  const elapsed=Number.isFinite(r.wall_time_s)?r.wall_time_s:null;
  const sim=r.events.reduce((sum,e)=>sum+(e.delta?.delta_time_s || 0),0);
  $('run-panel').innerHTML=`<div class="explorer-layout ${state.canvasExpanded?'canvas-expanded':''}">
    <section class="network-panel panel" aria-label="实验执行画布">
      <div class="network-heading"><div class="graph-heading-label"><h2>${graph.kind==='network'?'组件网络':'实验轨迹'} <span>${graph.total} 个节点</span></h2>${r.batch_count?`<select id="graph-batch" aria-label="选择实验批次">${Array.from({length:r.batch_count},(_,i)=>`<option value="${i+1}" ${batch===i+1?'selected':''}>第 ${i+1} / ${r.batch_count} 批</option>`).join('')}</select>`:''}</div>
        <div class="graph-tools">${hasNetwork?'<select id="graph-mode" aria-label="选择网络视图"><option value="events">执行轨迹</option><option value="network">组件网络</option></select>':''}
          <button class="button secondary small" id="graph-reset" title="恢复自动排布并显示全部节点">重新排布</button>
          <button class="button secondary small" id="graph-fit" title="保持节点位置，显示全部">${icon('fit')}全图</button>
          <div class="zoom-control"><button id="graph-minus" aria-label="缩小画布">−</button><span id="graph-scale">100%</span><button id="graph-plus" aria-label="放大画布">＋</button></div>
          <button class="button secondary small" id="graph-follow" title="定位最近操作">${icon('target')}最近</button>
          <button class="button secondary small" id="graph-expand" aria-pressed="${state.canvasExpanded}">${state.canvasExpanded?'显示详情':'展开画布'}</button>
        </div>
      </div>
      <div class="graph-viewport" id="graph-viewport"><div id="network-graph" class="network-graph"></div></div>
      <div class="graph-legend ${graph.kind}"><span class="line-key"></span>${esc(graph.legend)}<span>拖动平移 / 排布 · 滚轮缩放</span></div>
    </section>
    <aside class="explorer-inspector panel" aria-label="实验详情"><div id="inspector-content"></div></aside>
  </div>
  <section class="execution-dock" aria-label="运行资源"><button class="text-button" data-tab="timeline">${icon('records')} ${r.events.length} 次提交 <span class="muted">/ ${r.rejected_steps} 次拒绝或回滚</span></button><span>操作预算 <strong>${consumed} / ${r.design.budget}</strong></span><span>模拟时间 <strong>${formatDuration(sim)}</strong></span><span>墙钟 <strong>${formatDuration(elapsed)}</strong></span><span>Token <strong>${modelUsageText(r)}</strong></span></section>`;
  const viewKey=r.id+':'+graph.kind+':'+(batch ?? 'all');
  const controller=drawExplorationGraph($('network-graph'),graph,selectEvent,{
    saved:state.graphViews.get(viewKey),
    onChange:view=>{state.graphViews.set(viewKey,view);$('graph-scale').textContent=Math.round(view.camera.scale*100)+'%';},
  });
  state.graphController=controller;
  $('graph-reset').onclick=()=>controller.resetLayout();
  $('graph-fit').onclick=()=>controller.fit();
  $('graph-plus').onclick=()=>controller.zoomBy(1.2);$('graph-minus').onclick=()=>controller.zoomBy(1/1.2);
  $('graph-follow').onclick=()=>{selectEvent(graph.nodes.at(-1)?.eventIndex ?? r.events.length-1);controller.focusLatest();};
  if($('graph-batch')) $('graph-batch').onchange=()=>{
    state.eventSelection.set(r.id,r.events.findLastIndex(e=>e.batch===Number($('graph-batch').value)));
    state.inspectorTab='event';state.previewSignal=null;renderRun();
  };
  $('graph-expand').onclick=()=>{state.canvasExpanded=!state.canvasExpanded;document.querySelector('.explorer-layout').classList.toggle('canvas-expanded',state.canvasExpanded);$('graph-expand').textContent=state.canvasExpanded?'显示详情':'展开画布';$('graph-expand').setAttribute('aria-pressed',String(state.canvasExpanded));};
  if($('graph-mode')) {$('graph-mode').value=state.graphMode;$('graph-mode').onchange=()=>{state.graphMode=$('graph-mode').value;renderRun();};}
  renderInspector();
}

function selectEvent(index) {
  if(index<0 || index>=state.run.events.length) return;
  const previous=state.eventSelection.get(state.run.id) ?? state.run.events.length-1;
  state.eventSelection.set(state.run.id,index);state.inspectorTab='event';
  if(state.run.batch_count && state.run.events[previous]?.batch!==state.run.events[index].batch) {renderRun();return;}
  document.querySelectorAll('.network-node').forEach(node=>node.classList.toggle('selected',Number(node.dataset.eventIndex)===index));
  if(state.canvasExpanded) $('graph-expand').click();
  renderInspector();
  if(innerWidth<900) document.querySelector('.explorer-inspector').scrollIntoView({block:'nearest',behavior:'smooth'});
}

function noteMarkup(text) {
  return esc(text).split(/\n\s*\n/).map(block=>{
    const rows=block.split('\n');
    if(rows.length>1 && rows[0].trim().startsWith('|') && /^\s*\|[\s:|\-]+\|\s*$/.test(rows[1])) {
      const cells=line=>line.trim().replace(/^\||\|$/g,'').split('|').map(s=>s.trim());
      return `<div class="table-wrap"><table><thead><tr>${cells(rows[0]).map(c=>`<th>${c}</th>`).join('')}</tr></thead><tbody>${rows.slice(2).map(row=>`<tr>${cells(row).map(c=>`<td>${c}</td>`).join('')}</tr>`).join('')}</tbody></table></div>`;
    }
    if(/^#{1,3} /.test(block)) {
      const [heading,...body]=block.split('\n');
      return `<h3>${heading.replace(/^#+ /,'')}</h3>${body.length?`<p>${body.join('\n')}</p>`:''}`;
    }
    return `<p>${block}</p>`;
  }).join('').replace(/\*\*([^*]+)\*\*/g,'<strong>$1</strong>');
}

function renderInspector() {
  state.chartObserver?.disconnect();state.chartObserver=null;
  const r=state.run,epoch=++state.previewEpoch;
  const index=state.eventSelection.get(r.id) ?? r.events.length-1,event=r.events[index];
  const tabs=[['event','操作'],['observation','观测'],['notebook','笔记'],['archive','档案']];
  const measurements=r.events.flatMap((e,eventIndex)=>(e.series || []).map((series,seriesIndex)=>({event:e,eventIndex,series,key:eventIndex+':'+seriesIndex})));
  const selected=measurements.find(item=>r.id+':'+item.key===state.previewSignal) || measurements.findLast(item=>item.eventIndex===index) || measurements.at(-1);
  const revisions=r.model_notebook?.revisions || [],revision=state.previewRevision ?? revisions[0]?.revision ?? 0;
  const noteKey=r.id+':model:'+revision;
  let content='';
  if(state.inspectorTab==='event') content=event?`<div class="inspector-step"><button class="button secondary small" data-select-event="${index-1}" ${index===0?'disabled':''} aria-label="上一步">←</button><span>第 ${index+1} / ${r.events.length} 步</span><button class="button secondary small" data-select-event="${index+1}" ${index===r.events.length-1?'disabled':''} aria-label="下一步">→</button></div><h2 class="inspector-operation">${esc(event.action.instrument==='final_assay'?'终检结果':operations[event.action.operation] || event.action.operation)}</h2>${eventDetailHTML(index)}`:'<div class="empty">等待 Agent 的第一条操作。</div>';
  if(state.inspectorTab==='observation') content=`<h2>仪器观测</h2><p class="inspector-help">来自虚拟仪器的已保存测量</p>${selected?`<select id="preview-spectrum" aria-label="选择观测通道">${measurements.map(item=>`<option value="${esc(item.key)}" ${item===selected?'selected':''}>第 ${item.eventIndex+1} 步 · ${esc(item.series.label)}</option>`).join('')}</select><div id="explore-chart" class="chart"></div><p class="inspector-help" id="preview-source">第 ${selected.eventIndex+1} 步 · 已记录的仪器信号</p>`:'<p class="empty">尚无仪器信号，缺测不代表零。</p>'}<button class="button secondary small" data-tab="spectra">查看全部观测 ↗</button>`;
  if(state.inspectorTab==='notebook') content=`<h2>Agent 研究笔记</h2><p class="inspector-help">模型主动记录 · ${revisions.length} 个版本 · 只读</p>${revisions.length?`<select id="preview-revision" aria-label="选择笔记版本">${revisions.map(item=>`<option value="${item.revision}" ${item.revision===revision?'selected':''}>版本 ${item.revision}${item.event_count!=null?' · '+item.event_count+' 条事件后':''}</option>`).join('')}</select><div id="agent-note-preview" class="note-reader">${noteMarkup(state.noteCache.get(noteKey) || '正在读取记录…')}</div>`:'<p class="empty">Agent 尚未提交研究笔记。</p>'}<button class="button secondary small" data-agent-notes>完整笔记与版本差异 ↗</button>`;
  if(state.inspectorTab==='archive') content=`<h2>实验档案</h2><p class="inspector-help">${esc(executorLabel(r))}</p><dl class="event-fields">${[['实验',r.name],['世界',taskName(r.design)],['状态',statuses[r.status]],['终检',r.final_assay_count?'已完成':'未完成'],['精确回放',r.replay?(r.replay.verified?'已验证':'未通过'):'未检查'],['环境 seed',r.design.seed],['模型调用',modelCallCount(r)],['工具请求',r.model_tool_calls ?? '—']].map(([k,v])=>`<div><dt>${k}</dt><dd>${esc(v)}</dd></div>`).join('')}</dl>${runMessage(r)?`<p class="inspector-help">${esc(runMessage(r))}</p>`:''}<div class="archive-actions"><button class="button secondary small" data-tab="report">研究报告 ↗</button><button class="button secondary small" id="clone-run">新建同条件实验</button><button class="button secondary small" id="replay-run" ${['running','cancelling'].includes(r.status)?'disabled':''}>精确回放</button><a class="button secondary small" href="/api/runs/${r.id}/export">导出 ZIP ↗</a></div>`;
  $('inspector-content').innerHTML=`<div class="inspector-heading"><span>研究详情</span><span class="model-pill" title="${esc(executorLabel(r))}">${esc(r.model_configuration?.requested_model || r.actor)}</span></div><div class="inspector-tabs" role="tablist" aria-label="选择详情内容">${tabs.map(([id,label])=>`<button role="tab" aria-selected="${state.inspectorTab===id}" data-inspector-tab="${id}">${label}${id==='notebook'&&revisions.length?`<small>${revisions.length}</small>`:''}</button>`).join('')}</div><div class="inspector-body">${content}</div>`;
  archiveControls(r);
  document.querySelectorAll('[data-inspector-tab]').forEach(button=>button.onclick=()=>{state.inspectorTab=button.dataset.inspectorTab;renderInspector();});
  document.querySelectorAll('[data-select-event]').forEach(button=>button.onclick=()=>selectEvent(Number(button.dataset.selectEvent)));
  if($('preview-revision')) $('preview-revision').onchange=()=>{state.previewRevision=Number($('preview-revision').value);renderInspector();};
  if(document.querySelector('[data-agent-notes]')) document.querySelector('[data-agent-notes]').onclick=()=>{state.author='model';state.tab='notebook';renderRun();};
  if(state.inspectorTab==='observation'&&selected) {
    const chart=$('explore-chart');drawChart(chart,selected.series);
    $('preview-spectrum').onchange=()=>{state.previewSignal=r.id+':'+$('preview-spectrum').value;renderInspector();};
    state.chartObserver=new ResizeObserver(()=>drawChart(chart,selected.series));state.chartObserver.observe(chart);
  }
  if(state.inspectorTab==='notebook'&&revisions.length&&!state.noteCache.has(noteKey)) {
    api('/api/runs/'+r.id+'/notebook',{author:'model',operation:'read',arguments:{revision,limit:16000}}).then(note=>{
      state.noteCache.set(noteKey,note.text || '记录为空。');
      if(state.run?.id===r.id&&state.previewEpoch===epoch&&$('agent-note-preview'))$('agent-note-preview').innerHTML=noteMarkup(note.text || '记录为空。');
    }).catch(()=>{if(state.previewEpoch===epoch&&$('agent-note-preview'))$('agent-note-preview').textContent='读取失败，请重试。';});
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
    ["模型调用", modelCallCount(r)],
    ["模型工具请求", r.model_tool_calls ?? "—"],
    ["模型 token", modelUsageText(r)],
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
          `<article class="event ${e.transaction_status === "committed" ? "" : "rejected"}"><div class="event-head"><span>${String(i + 1).padStart(2, "0")} &nbsp; ${esc(operations[e.action.operation] || e.action.operation)}${e.action.instrument ? " · " + esc(e.action.instrument.toUpperCase()) : ""}</span><small>${eventSummary(e).status}</small></div><p>${
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
  if(r.sealed_reports?.length) {
    const failures=r.retained_failures || {};
    $('run-panel').innerHTML=`<div class="notice">${r.final_assay_count} / ${r.batch_count} 批终检完成 · ${r.submitted_steps} 次物理操作 · ${r.model_notebook.total} 版同期笔记。以下为实验结束后的模型报告，与同期笔记分开保存。笔记工具错误 ${failures.notebook_tool_errors ?? '—'} 次，实验工具响应错误 ${failures.laboratory_tool_errors ?? '—'} 次，均保留在原记录中。</div><section class="panel"><div class="panel-header"><h3>封闭后测 · 模型原文</h3><select id="sealed-stage" aria-label="选择后测报告">${r.sealed_reports.map((s,i)=>`<option value="${i}">${s.stage} · ${esc(s.title)}</option>`).join('')}</select></div><div class="panel-body report-reader" id="sealed-report-text"></div></section>`;
    const show=()=>{
      const report=r.sealed_reports[Number($('sealed-stage').value)];
      $('sealed-report-text').innerHTML=noteMarkup(report.text)+`<details class="event-raw"><summary>原始回答 JSON · 完整数值与质量判断</summary><pre class="document document-code">${esc(pretty(report.payload))}</pre></details>`;
    };
    $('sealed-stage').onchange=show;show();return;
  }
  const designFields=[['实验世界',taskName(r.design)],['执行方式',executorLabel(r)],['环境 seed',r.design.seed],['操作预算',r.design.budget],['终检',r.final_assay_count?'已完成':'未完成']];
  $("run-panel").innerHTML =
    `<div class="chart-grid"><section class="panel"><div class="panel-header"><h3>实验设计</h3></div><div class="panel-body"><p class="document">${esc(r.question || '未填写研究目标')}</p><dl class="event-fields">${designFields.map(([label,value])=>`<div><dt>${label}</dt><dd>${esc(value)}</dd></div>`).join('')}</dl><details class="event-raw"><summary>完整设计 JSON</summary><pre class="document document-code">${esc(pretty({ design: r.design, actor: r.actor, limits: r.limits, model: r.model_configuration }))}</pre></details></div></section><section class="panel"><div class="panel-header"><h3>实验报告</h3><span class="muted compact">公开记录</span></div><div class="panel-body"><p class="document">${esc(r.view?.lab_report?.text || "尚无报告。")}</p><hr class="metric-separator"><h3>模型提交的最终报告</h3><p class="document">${esc(r.model_report || "模型尚未主动提交最终报告。")}</p><hr class="metric-separator"><p class="fineprint">${r.submitted_steps} 次提交，${r.rejected_steps} 次拒绝或回滚，${r.final_assay_count} 次终检。保存了全部已提交事件；未终检不等于零产率。环境 seed 不保证不同厂商模型输出相同。</p></div></section></div><section class="panel"><div class="panel-body"><details class="event-raw"><summary>物料与设备的公开原始状态</summary><pre class="document document-code">${esc(pretty({ samples: r.view?.sample_inventory, network: r.view?.component_network, routing: r.view?.material_routing, process: r.view?.process_control }))}</pre></details></div></section>`;
}
async function renderCompare() {
  disposeExplorer();
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
    ["模型调用", modelCallCount],
    ["模型工具请求", (r) => r.model_tool_calls ?? "—"],
    ["输入 token", (r) => modelUsageText(r, "input_tokens")],
    ["输出 token", (r) => modelUsageText(r, "output_tokens")],
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
  $("detail-content").innerHTML = `<pre>${esc(typeof content === "string" ? content : pretty(content))}</pre>`;
  $("detail-dialog").showModal();
}
function eventDetailHTML(index) {
  const event=state.run.events[index], detail=eventSummary(event);

  const fields=detail.parameters.map(([key,value])=>`<div><dt>${esc(fieldNames[key] || key)}</dt><dd>${esc(key==='instrument'?(value==='final_assay'?'终检数据包':String(value).toUpperCase()):typeof value==='object'?pretty(value):value)}</dd></div>`).join('');
  const delta=detail.resourceDelta;
  const costs=[['模拟时间',delta?.delta_time_s,'s'],['虚拟成本',delta?.delta_cost,'环境单位'],['样品体积变化',Number.isFinite(delta?.delta_volume_L)?delta.delta_volume_L*1000:null,'mL']].filter(([,value])=>Number.isFinite(value));
  return `<div class="event-meta"><span class="event-status ${event.transaction_status==='committed'?'success':'failure'}">${detail.status}</span><span>第 ${index+1} 步${event.recorded_at?' · '+esc(date(event.recorded_at)):''}</span></div>
    <p class="event-summary">${esc(detail.summary)}</p>
    ${detail.metrics.length?`<div class="event-metrics">${detail.metrics.map(metric=>`<div><span>${esc(metric.label)}</span><strong>${number(metric.value*metric.scale,3)}<small>${metric.unit}</small></strong></div>`).join('')}</div>`:''}
    ${fields?`<section class="event-section"><h3>请求参数</h3><dl class="event-fields">${fields}</dl></section>`:''}
    ${costs.length?`<section class="event-section"><h3>记录的资源变化</h3><dl class="event-fields">${costs.map(([name,value,unit])=>`<div><dt>${name}</dt><dd>${number(value,3)} ${unit}</dd></div>`).join('')}</dl></section>`:''}
    ${detail.caveat?`<p class="event-caveat">${esc(detail.caveat)}</p>`:''}
    ${event.series?.length && event.transaction_status==='committed'?'<button data-tab="spectra" class="button secondary small">查看仪器观测 ↗</button>':''}
    <details class="event-raw"><summary>原始记录 JSON</summary><pre>${esc(pretty(event))}</pre></details>`;

}
function showEventDetail(index) {
  const event=state.run.events[index];
  $("detail-title").textContent=event.action.instrument==='final_assay'?'终检结果':operations[event.action.operation] || event.action.operation;
  $("detail-content").innerHTML=eventDetailHTML(index);
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
  if (b.id === "clone-run") openDesign(state.run.design.task_id || "custom",state.run);
  if (b.id === "replay-run") perform(async()=>{const id=state.run.id;toast("正在精确回放…");await api(`/api/runs/${id}/replay`,{});await openRun(id);toast("回放检查已完成");});
  if (b.dataset.run)
    perform(() => {
      state.tab = "explore";
      return openRun(b.dataset.run);
    });
  if (b.dataset.template) openDesign(b.dataset.template);
  if (b.dataset.nav) {
    if (b.dataset.nav === "home") {
      const latest = state.run || state.runs.find((r) => r.status === "running" && r.actor !== "reference") || state.runs[0];
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
    $("detail-dialog").close();
    state.tab = b.dataset.tab;
    renderRun();
  }
  if (b.dataset.event)
    showEventDetail(Number(b.dataset.event));
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
          if (state.tab !== "notebook" && !state.graphController?.interacting && !document.querySelector('dialog[open], .event-raw[open]') && !document.activeElement?.matches('.network-panel select, .explorer-inspector select, .network-node, #network-graph svg')) renderRun();
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
    const navIcons = { home: "flask", records: "records", notes: "book", compare: "compare" };
    const navLabels = { home: "探索", records: "实验", notes: "研究记录", compare: "结果比较" };
    document.querySelectorAll("[data-nav]").forEach(button => {
      const label = navLabels[button.dataset.nav];
      button.setAttribute("aria-label", label);
      button.title = label;
      const count = button.querySelector("#compare-count");
      button.innerHTML = icon(navIcons[button.dataset.nav]) + label;
      if (count) button.append(count);
    });
    document.querySelector(".sidebar nav").append(document.querySelector("[data-nav=compare]"));
    $("manual-entry").innerHTML = icon("wrench") + "<span>手动实验<small>（可选）</small></span>";
    $("manual-entry").setAttribute("aria-label", "手动实验（可选）");
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
    const requested = new URLSearchParams(location.search).get("run");
    const latest = state.runs.find((r) => r.id === requested) || state.runs.find((r) => r.status === "running") || state.runs[0];
    if (new URLSearchParams(location.search).get('view')==='records') renderHome();
    else if (latest) await openRun(latest.id);
    else renderHome();
    setInterval(poll, 1800);
  } catch (error) {
    $("main").textContent = `无法连接本机服务：${error.message}`;
    $("connection").textContent = "未连接";
  }
}
init();
