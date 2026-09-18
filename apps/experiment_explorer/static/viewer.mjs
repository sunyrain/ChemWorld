import {
  ACTIONS,
  label,
  format,
  finite,
  observations,
  snapshot,
  metricSeries,
  experiments,
  stepIO,
  changedConditions,
} from "./replay.mjs";

const PHASE = {
  add_reagent: "prepare",
  add_solvent: "prepare",
  add_catalyst: "prepare",
  add_phase: "prepare",
  heat: "process",
  cool: "process",
  quench: "process",
  cool_crystallize: "process",
  distill: "process",
  measure: "measure",
  terminate: "close",
  discard_experiment: "close",
  separate_phase: "separate",
  wash: "separate",
  dry: "separate",
  filter_crystals: "separate",
  collect_fraction: "separate",
};
const STATUS = {
  assayed: "已完成终检",
  discarded: "已弃批",
  prefix: "未记录终检",
};
const INPUT_KIND = {
  recorded_request: "保存的模型请求",
  decision_context: "操作前上下文快照",
  previous_observation: "前一步公开返回（参考）",
  missing: "未留存输入",
};

export function mountRecordingList(detail, host, ui) {
  const { el, button, pill, empty, api, state, loadTrajectory, openPlayback } =
    ui;
  host.replaceChildren();
  if (detail.localPayload) {
    openPlayback(detail.localPayload, host);
    return;
  }
  const files = [...detail.trajectories].sort(
    (a, b) =>
      Number(b.path.includes("/campaigns/")) -
      Number(a.path.includes("/campaigns/")),
  );
  if (!files.length) {
    host.append(
      empty("没有关联的轨迹。可搜索本地实验批次，或导入 JSON / JSONL 文件。"),
    );
    return;
  }
  const search = el("input", {
    type: "search",
    placeholder: "搜索任务、条件或会话路径",
    "aria-label": "搜索实验会话",
  });
  const count = el("span", { class: "muted" }),
    grid = el("div", { class: "recording-cards" }),
    status = el("div", { class: "inline-status", "aria-live": "polite" });
  let page = 0,
    revision = 0;
  const prev = button(
      "←",
      () => {
        page--;
        draw();
      },
      "",
      { "aria-label": "上一页会话" },
    ),
    next = button(
      "→",
      () => {
        page++;
        draw();
      },
      "",
      { "aria-label": "下一页会话" },
    ),
    position = el("span");
  host.append(
    el(
      "div",
      { class: "panel-heading" },
      el("h3", {}, "选择完整实验组或单次记录"),
      count,
    ),
    el(
      "p",
      { class: "recording-list-note" },
      "同一连续会话中的多轮实验支持整组回放。模型一次规划、分别保存的方案独立展示，保留各自矩阵与方案标识。打开记录可查看每步输入、输出与工具反馈。",
    ),
    el("label", { class: "search-field" }, el("span", {}, "⌕"), search),
    status,
    grid,
    el("div", { class: "pagination" }, prev, position, next),
  );
  search.oninput = () => {
    page = 0;
    draw();
  };
  async function draw() {
    const version = ++revision,
      filtered = files.filter((f) =>
        f.path.toLowerCase().includes(search.value.toLowerCase()),
      ),
      pages = Math.max(1, Math.ceil(filtered.length / 12));
    page = Math.max(0, Math.min(page, pages - 1));
    const visible = filtered.slice(page * 12, (page + 1) * 12);
    count.textContent = `${filtered.length} 份会话记录`;
    prev.disabled = page === 0;
    next.disabled = page >= pages - 1;
    position.textContent = `${page + 1} / ${pages}`;
    const cards = new Map();
    grid.replaceChildren();
    for (const file of visible) {
      const card = button(
        "",
        () =>
          loadTrajectory(file, host, () =>
            mountRecordingList(detail, host, ui),
          ),
        "recording-card trajectory-item",
      );
      cards.set(file.id, card);
      grid.append(card);
      paint(file, card);
    }
    if (!visible.length) grid.append(empty("没有匹配的会话记录。"));
    const pending = visible.filter((f) => !state.recordingMeta.has(f.id));
    if (!pending.length) {
      status.textContent = "按记录中的实际小实验数量展示";
      return;
    }
    status.textContent = `正在读取本页 ${pending.length} 份会话的分组与 IO 覆盖…`;
    try {
      const meta = await api(
        "/api/recordings?" +
          pending.map((f) => "id=" + encodeURIComponent(f.id)).join("&"),
      );
      for (const [id, value] of Object.entries(meta))
        state.recordingMeta.set(id, value);
      if (version !== revision || !grid.isConnected) return;
      for (const file of visible) paint(file, cards.get(file.id));
      status.textContent = "分组来自实验索引与成功终检边界；数字为已记录数量。";
    } catch (error) {
      if (version === revision)
        status.textContent = `摘要读取失败：${error.message}。仍可直接打开原始轨迹。`;
    }
  }
  function paint(file, card) {
    const m = state.recordingMeta.get(file.id);
    card.replaceChildren(
      el("h4", {}, file.name.replace("/trajectory.jsonl", "")),
      el(
        "div",
        { class: "recording-model" },
        m?.planning?.model || m?.model || "读取控制器与实验分组…",
      ),
      el(
        "div",
        { class: "recording-meta" },
        pill(
          m?.experiments > 1
            ? `完整实验组 · ${m.experiments} 次`
            : m?.experiments === 1
              ? "单次实验"
              : "待识别分组",
          m?.experiments > 1 ? "success" : "",
        ),
        m?.planning ? pill("一次规划 · 分文件执行", "planned") : null,
        m?.steps !== undefined ? pill(`${m.steps} 个操作`) : null,
        m?.error ? pill("包含读取错误", "failure") : null,
      ),
      el("p", {}, file.path),
      m?.planning
        ? el(
            "div",
            { class: "planning-identity" },
            `${m.planning.source} / round ${m.planning.round + 1} / ${m.planning.member}`,
          )
        : null,
      el(
        "div",
        { class: "recording-card-footer" },
        el(
          "span",
          {},
          m?.steps !== undefined
            ? `终检 ${m.final_assays} · 决策说明 ${m.decision_notes}/${m.steps}`
            : "打开查看原始记录",
        ),
        el("span", {}, "进入回放 →"),
      ),
    );
  }
  draw();
}

export function mountReplay(payload, host, back, ui) {
  const {
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
  } = ui;
  stopPlayback();
  host.replaceChildren();
  const records = payload.records,
    groups = experiments(records),
    firstIO = stepIO(records, 0);
  const planning = payload.context?.planning;
  const controller = {
    payload,
    records,
    index: 0,
    groupIndex: 0,
    speed: 1,
    mode: groups.length > 1 ? "campaign" : "experiment",
    host,
  };
  state.playback = controller;
  const multi = groups.length > 1;
  const campaignIds = new Set(
    records.map((r) => r.campaign_id).filter(Boolean),
  );
  const header = el(
    "div",
    { class: "recording-heading" },
    el(
      "div",
      {},
      el("div", { class: "eyebrow" }, "RECORDED EXPERIMENT / REPLAY"),
      el(
        "h2",
        {},
        multi ? "从整组探索，走进每一次决策" : "沿着操作，理解这次实验",
      ),
      el(
        "div",
        { class: "detail-kicker" },
        pill(planning?.model || firstIO.model),
        pill(
          records[0].benchmark_task_id || records[0].task_id || "未声明任务",
        ),
        pill(`${groups.length} 次小实验`),
        pill(`${records.length} 个操作`),
      ),
    ),
    back
      ? button("← 会话列表", () => {
          stopPlayback();
          back();
        })
      : pill("本地导入"),
  );
  host.append(header);
  if (planning)
    host.append(
      el(
        "div",
        { class: "planning-banner" },
        el("strong", {}, "模型一次规划 · 分文件执行"),
        el(
          "p",
          {},
          `规划调用保存了 ${planning.planned} 个方案；当前独立展示 ${planning.source} / round ${planning.round + 1} / ${planning.member}。其他矩阵与方案不合并回放。`,
        ),
        el(
          "small",
          {},
          "下面的动作由脚本执行。已保存的模型方案见单次视图，未记录逐步模型请求。",
        ),
      ),
    );
  if (payload.errors?.length)
    host.append(
      el(
        "div",
        { class: "alert error" },
        `第 ${payload.errors[0].line} 行损坏，只展示此前连续记录：${payload.errors[0].error}`,
      ),
    );
  if (campaignIds.size > 1)
    host.append(
      el(
        "div",
        { class: "alert" },
        `此文件包含 ${campaignIds.size} 个不同 campaign 标识，分段显示，不视作同一连续研究会话。`,
      ),
    );
  const switcher = el("div", {
    class: "granularity-switch",
    role: "group",
    "aria-label": "回放粒度",
  });
  const campaignButton = button(
    `◫ 整组实验 · ${groups.length} 次`,
    () => switchMode("campaign"),
    "granularity",
  );
  const experimentButton = button(
    "⌁ 单次实验 · 操作与 IO",
    () => switchMode("experiment"),
    "granularity",
  );
  switcher.append(campaignButton, experimentButton);
  const exportButton = button(
    "导出本步 IO",
    () => download("recorded-step-io.json", stepIO(records, controller.index)),
    "button secondary compact",
  );
  host.append(el("div", { class: "viewer-controls" }, switcher, exportButton));
  const player = el("div", { class: "player modern-player" }),
    position = el("span", { class: "time-label" });
  const slider = el("input", {
    type: "range",
    min: 0,
    max: 0,
    value: 0,
    step: 1,
    "aria-label": "回放进度",
  });
  const play = button("▶ 播放", togglePlay, "primary-play");
  controller.playButton = play;
  const speed = el(
    "select",
    { "aria-label": "回放速度" },
    ...[0.5, 1, 2, 4].map((v) => el("option", { value: v }, `${v}×`)),
  );
  speed.value = "1";
  speed.onchange = () => {
    const was = !!state.timer;
    stopPlayback();
    controller.speed = Number(speed.value);
    if (was) togglePlay();
  };
  const scope = el("span", { class: "player-scope" });
  player.append(
    el(
      "div",
      { class: "player-main" },
      button("↤", () => seek(0), "", { "aria-label": "回到起点" }),
      button("‹", () => controller.nudge(-1), "", { "aria-label": "上一个" }),
      play,
      button("›", () => controller.nudge(1), "", { "aria-label": "下一个" }),
      position,
      scope,
      speed,
    ),
    slider,
  );
  slider.oninput = () => seek(Number(slider.value));
  host.append(player);
  const stage = el("div", { class: "replay-stage" });
  host.append(stage);
  const verification = el("div", {
    class: "inline-status",
    "aria-live": "polite",
  });
  const verifyButton = button("验证原始完整轨迹", async () => {
    try {
      await verifyTrajectory(controller, verification, verifyButton);
    } catch (error) {
      verification.textContent = error.message;
    }
  });
  verifyButton.disabled = !payload.id;
  host.append(
    el(
      "details",
      { class: "recording-provenance" },
      el("summary", {}, "记录来源、下载与精确验证"),
      el("p", { class: "source-path" }, payload.path || payload.name),
      el(
        "div",
        { class: "toolbar" },
        button("下载完整轨迹", () =>
          download("trajectory-records.json", records),
        ),
        verifyButton,
        button("查看附带记录", () =>
          showInspector("原文件附带记录", payload.context || {}),
        ),
      ),
      el(
        "p",
        { class: "footnote" },
        "播放只读取已存记录；精确验证始终使用完整原文件。单次视图是展示切片，不独立重算或改变原轨迹。",
      ),
      verification,
    ),
  );
  let metric = "score",
    operationMetric = "purity",
    ioTab = "io",
    activeStepNode = null;
  const terminals = groups.map((g) => g.metrics),
    available = [
      ...new Set(
        terminals.flatMap((r) => Object.keys(r).filter((k) => finite(r[k]))),
      ),
    ];
  if (!available.includes(metric)) metric = available[0] || "score";
  function cursor() {
    return controller.mode === "campaign"
      ? controller.groupIndex
      : controller.index - groups[controller.groupIndex].start;
  }
  function length() {
    return controller.mode === "campaign"
      ? groups.length
      : groups[controller.groupIndex].steps;
  }
  function togglePlay() {
    if (state.timer) {
      stopPlayback();
      return;
    }
    if (cursor() >= length() - 1) seek(0);
    play.textContent = "Ⅱ 暂停";
    state.timer = setInterval(() => {
      if (state.playback !== controller) {
        stopPlayback();
        return;
      }
      seek(cursor() + 1, false);
      if (cursor() >= length() - 1) stopPlayback();
    }, 1000 / controller.speed);
  }
  function seek(value, pause = true) {
    if (pause) stopPlayback();
    const index = Math.max(0, Math.min(length() - 1, value));
    if (controller.mode === "campaign") {
      controller.groupIndex = index;
      controller.index = groups[index].end;
    } else controller.index = groups[controller.groupIndex].start + index;
    draw();
  }
  controller.seek = seek;
  controller.nudge = (delta) => seek(cursor() + delta);
  function chooseGroup(index, open = false) {
    stopPlayback();
    controller.groupIndex = index;
    controller.index = groups[index].start;
    if (open) controller.mode = "experiment";
    draw();
  }
  function switchMode(mode) {
    stopPlayback();
    controller.mode = mode;
    if (mode === "campaign")
      controller.index = groups[controller.groupIndex].end;
    else controller.index = groups[controller.groupIndex].start;
    draw();
  }
  function stats(items) {
    return el(
      "div",
      { class: "viewer-stats" },
      items.map(([name, value, note]) =>
        el(
          "div",
          {},
          el("span", {}, name),
          el("strong", {}, format(value)),
          note ? el("small", {}, note) : null,
        ),
      ),
    );
  }
  function selectMetric(keys, value, handler, name) {
    const s = el("select", { "aria-label": name });
    for (const k of keys) s.append(el("option", { value: k }, label(k)));
    s.value = value;
    s.onchange = () => handler(s.value);
    return s;
  }
  function chipStatus(g) {
    return pill(
      STATUS[g.status],
      g.status === "assayed" ? "success" : "development",
    );
  }
  function actionName(row) {
    return ACTIONS[row.action?.operation] || row.action?.operation || "操作";
  }
  function section(title, subtitle, ...children) {
    return el(
      "section",
      { class: "viewer-section" },
      el(
        "div",
        { class: "section-head" },
        el(
          "div",
          {},
          el("h3", {}, title),
          subtitle ? el("p", {}, subtitle) : null,
        ),
      ),
      ...children,
    );
  }
  function rawDetails(title, value) {
    const details = el(
      "details",
      { class: "raw-fold" },
      el("summary", {}, title),
    );
    let loaded = false;
    details.addEventListener("toggle", () => {
      if (!details.open || loaded) return;
      loaded = true;
      details.append(
        typeof value === "string"
          ? el("pre", { class: "io-raw" }, value)
          : jsonTree(value || {}),
      );
    });
    return details;
  }

  function campaignView() {
    const current = groups[controller.groupIndex],
      completed = groups.filter((g) => g.status === "assayed").length;
    const auditCount = groups.reduce((n, g) => n + g.decisionNotes, 0),
      failed = groups.reduce((n, g) => n + g.failed, 0);
    stage.append(
      stats([
        ["已记录小实验", groups.length, "来自轨迹生命周期"],
        [
          "完成终检",
          `${completed} / ${groups.length}`,
          "终检完成不代表质量达标",
        ],
        ["保留失败操作", failed, "包括验证失败和回滚"],
        [
          "有决策说明的操作",
          `${auditCount} / ${records.length}`,
          "原模型明确提供的说明",
        ],
      ]),
    );
    const rail = el("div", { class: "batch-grid" });
    for (const [i, g] of groups.entries()) {
      const card = button(
        "",
        () => chooseGroup(i),
        "batch-card" + (i === controller.groupIndex ? " selected" : ""),
        {
          "aria-pressed": i === controller.groupIndex,
          "aria-label": `选择第 ${i + 1} 次小实验`,
        },
      );
      card.append(
        el(
          "div",
          { class: "batch-card-top" },
          el("span", { class: "batch-number" }, String(i + 1).padStart(2, "0")),
          chipStatus(g),
        ),
        el("strong", {}, format(g.metrics[metric])),
        el("span", { class: "batch-metric-label" }, label(metric)),
        el(
          "div",
          { class: "batch-mini-flow" },
          g.indices.map((j) =>
            el("span", {
              class: `phase-pip ${PHASE[records[j].action?.operation] || "other"}`,
              title: actionName(records[j]),
            }),
          ),
        ),
        el(
          "small",
          {},
          `${g.steps} 步 · ${g.measurements} 次测量${g.failed ? ` · ${g.failed} 次失败` : ""}`,
        ),
      );
      rail.append(card);
    }
    stage.append(
      section(
        "完整实验组",
        "每张卡片是一轮小实验。按实际实验索引分段，未完成与失败记录一起保留。",
        rail,
      ),
    );
    const plot = el(
      "div",
      { class: "chart-panel campaign-plot" },
      el(
        "div",
        { class: "chart-head" },
        el(
          "div",
          {},
          el("h3", {}, "跨小实验的终检变化"),
          el("p", {}, "显示所有已保存终检；游标标记当前查看的小实验。"),
        ),
        selectMetric(
          available,
          metric,
          (key) => {
            metric = key;
            draw();
          },
          "跨实验指标",
        ),
      ),
      chart(
        groups.map((g, i) => ({
          step: i + 1,
          value: g.metrics[metric] ?? null,
        })),
        {
          title: label(metric),
          unit: "次",
          current: controller.groupIndex,
          onSeek: (i) => chooseGroup(i),
        },
      ),
    );
    stage.append(plot);
    const selected = el(
      "div",
      { class: "selected-batch" },
      el(
        "div",
        {},
        el(
          "div",
          { class: "eyebrow" },
          `EXPERIMENT ${String(current.ordinal).padStart(2, "0")} / ${groups.length}`,
        ),
        el(
          "h3",
          {},
          `第 ${current.ordinal} 次小实验 · ${current.steps} 个操作`,
        ),
        el(
          "p",
          {},
          `原轨迹第 ${current.start + 1}–${current.end + 1} 条记录 · ${STATUS[current.status]}`,
        ),
      ),
      button("查看操作与模型 IO →", () => switchMode("experiment")),
    );
    stage.append(selected);
    const firstNote = current.indices
      .map((i) => stepIO(records, i).audit)
      .find(Boolean);
    if (firstNote)
      stage.append(
        el(
          "div",
          { class: "research-note" },
          el("span", {}, "模型记录的本次目标"),
          el(
            "p",
            {},
            firstNote.diagnostic_target ||
              firstNote.expected_effect ||
              firstNote.rationale ||
              "",
          ),
          el("small", {}, "摘自本次最早提供的决策说明"),
        ),
      );
    const changes = changedConditions(
      records,
      current,
      groups[controller.groupIndex - 1],
    );
    if (changes.length)
      stage.append(
        section(
          controller.groupIndex
            ? "相较前一次，操作参数发生了哪些变化"
            : "本次操作参数",
          "逐项比较记录的参数序列；这不自动构成因果对照。",
          el(
            "div",
            { class: "parameter-changes" },
            changes.slice(0, 12).map((c) =>
              el(
                "div",
                { class: "parameter-change" },
                el(
                  "span",
                  {},
                  c.key
                    .split(".")
                    .map((k) => ACTIONS[k] || label(k))
                    .join(" · "),
                ),
                el(
                  "strong",
                  {},
                  sequence(c.previous),
                  " → ",
                  sequence(c.value),
                ),
              ),
            ),
          ),
          changes.length > 12
            ? rawDetails(`查看全部 ${changes.length} 项差异`, { changes })
            : null,
        ),
      );
    stage.append(heatmap());
    const finals = finalOutputs(payload.context || {});
    if (finals.length)
      stage.append(
        section(
          "模型最终交付",
          "来自该会话已保存的最终输出。",
          ...finals.map((v, i) => rawDetails(`最终输出 ${i + 1}`, v)),
        ),
      );
    stage.append(
      el(
        "p",
        { class: "footnote" },
        multi
          ? "整组模式按小实验移动游标；切到单次模式可逐操作查看输入、输出与工具反馈。"
          : "此轨迹只记录一次小实验。不会为了凑足8–12次而拼接不同会话或参考条件。",
      ),
    );
  }
  function sequence(value) {
    if (value === null || value === undefined) return "未记录";
    return Array.isArray(value) ? value.map(format).join(" → ") : format(value);
  }
  function heatmap() {
    const operations = [
      ...new Set(records.map((r) => r.action?.operation).filter(Boolean)),
    ];
    const table = el("table", { class: "operation-matrix" }),
      head = el("tr", {}, el("th", {}, "小实验"));
    for (const op of operations)
      head.append(el("th", { title: op }, ACTIONS[op] || op));
    table.append(el("thead", {}, head));
    const body = el("tbody");
    for (const [i, g] of groups.entries()) {
      const counts = {};
      for (const j of g.indices)
        counts[records[j].action.operation] =
          (counts[records[j].action.operation] || 0) + 1;
      const tr = el(
        "tr",
        { class: i === controller.groupIndex ? "selected" : "" },
        el(
          "th",
          {},
          button(
            String(i + 1).padStart(2, "0"),
            () => chooseGroup(i, true),
            "matrix-row-button",
            { "aria-label": `打开第 ${i + 1} 次小实验` },
          ),
        ),
      );
      for (const op of operations) {
        const n = counts[op] || 0;
        tr.append(
          el(
            "td",
            {
              class: `heat-${Math.min(4, n)}`,
              title: `第 ${i + 1} 次 · ${ACTIONS[op] || op} · ${n} 次`,
            },
            n || "·",
          ),
        );
      }
      body.append(tr);
    }
    table.append(body);
    return section(
      "实验 × 操作覆盖",
      "颜色表示动作次数，点击实验编号进入操作回放。",
      el("div", { class: "matrix-scroll" }, table),
    );
  }
  function finalOutputs(context) {
    const output = [];
    function walk(value) {
      if (!value || typeof value !== "object") return;
      if (Array.isArray(value)) {
        value.forEach(walk);
        return;
      }
      for (const [k, v] of Object.entries(value)) {
        if (["final_payload", "provider_final"].includes(k) && v)
          output.push(v);
        else walk(v);
      }
    }
    walk(context);
    return output;
  }
  function experimentView() {
    const group = groups[controller.groupIndex],
      io = stepIO(records, controller.index),
      snap = snapshot(records, controller.index);
    const selector = el("select", { "aria-label": "选择小实验" });
    for (const [i, g] of groups.entries())
      selector.append(
        el(
          "option",
          { value: i },
          `第 ${i + 1} 次 · ${g.steps} 步 · ${STATUS[g.status]}`,
        ),
      );
    selector.value = controller.groupIndex;
    selector.onchange = () => chooseGroup(Number(selector.value), true);
    stage.append(
      el(
        "div",
        { class: "experiment-breadcrumb" },
        button("整组实验", () => switchMode("campaign"), "breadcrumb-button"),
        el("span", {}, "/"),
        selector,
        el(
          "span",
          { class: "breadcrumb-step" },
          `/ 操作 ${controller.index - group.start + 1} / ${group.steps}`,
        ),
      ),
    );
    const strip = el("div", {
      class: "operation-strip",
      "aria-label": "本次实验操作流程",
    });
    for (const i of group.indices) {
      const row = records[i],
        status = row.transaction_status;
      strip.append(
        button(
          "",
          () => {
            controller.index = i;
            stopPlayback();
            draw();
          },
          `operation-node ${PHASE[row.action?.operation] || "other"} ${i === controller.index ? "active" : ""} ${status && status !== "committed" ? "failed" : ""}`,
          {
            "aria-current": i === controller.index ? "step" : false,
            title: `原始步骤 ${row.step ?? i + 1}`,
          },
        ).appendChild(
          el(
            "span",
            {},
            el("small", {}, String(i - group.start + 1).padStart(2, "0")),
            el("strong", {}, actionName(row)),
            row.action?.instrument ? el("em", {}, row.action.instrument) : null,
          ),
        ).parentNode,
      );
    }
    stage.append(strip);
    const focus = el(
      "div",
      { class: "step-focus-heading" },
      el(
        "div",
        {},
        el(
          "span",
          { class: "eyebrow" },
          `OPERATION ${String(controller.index - group.start + 1).padStart(2, "0")}`,
        ),
        el("h3", {}, actionName(snap.row)),
      ),
      el(
        "div",
        {},
        pill(snap.status, snap.status === "committed" ? "success" : "failure"),
        pill(planning || io.scripted ? "脚本 / 规则控制器" : "记录的模型交互"),
      ),
    );
    stage.append(focus);
    const tabs = el("div", { class: "step-view-tabs" });
    for (const [id, title] of [
      ["io", "输入 · 决策 · 反馈"],
      ["state", "观测与资源"],
      ["record", "完整记录"],
    ])
      tabs.append(
        button(
          title,
          () => {
            ioTab = id;
            draw();
          },
          `step-view-tab ${ioTab === id ? "active" : ""}`,
          { "aria-pressed": ioTab === id },
        ),
      );
    stage.append(tabs);
    if (ioTab === "io") stage.append(ioView(io, snap));
    if (ioTab === "state") stage.append(stateView(snap, group));
    if (ioTab === "record") stage.append(jsonTree(snap.row));
    stage.append(
      el(
        "div",
        { class: "viewer-bottom-navigation" },
        button(
          "← 上一次小实验",
          () => chooseGroup(Math.max(0, controller.groupIndex - 1), true),
          "button secondary",
          { disabled: controller.groupIndex === 0 },
        ),
        el(
          "span",
          {},
          `小实验 ${controller.groupIndex + 1} / ${groups.length}`,
        ),
        button(
          "下一次小实验 →",
          () =>
            chooseGroup(
              Math.min(groups.length - 1, controller.groupIndex + 1),
              true,
            ),
          "button secondary",
          { disabled: controller.groupIndex === groups.length - 1 },
        ),
      ),
    );
  }
  function ioView(io, snap) {
    const grid = el("div", { class: "io-grid" }),
      context = snap.row.explanation?.decision_context || {};
    const input = el(
      "article",
      { class: "io-pane input-pane" },
      paneHeading(
        "01",
        "INPUT",
        planning ? "执行前的记录" : "模型操作前看到了什么",
        INPUT_KIND[io.inputKind],
      ),
    );
    if (io.input) {
      if (io.inputKind === "decision_context") {
        input.append(
          keyValues({
            task_id: context.task_id,
            decision_stage: context.decision_stage,
            remaining_operations: context.remaining_operations,
          }),
        );
        const visible = context.visible_metrics || {};
        input.append(el("h4", {}, "决策前已知读数"), readings(visible));
        if (context.available_operations?.length)
          input.append(
            el("h4", {}, "当时可用操作"),
            el(
              "div",
              { class: "operation-tags" },
              context.available_operations.map((op) =>
                el("span", {}, ACTIONS[op] || op),
              ),
            ),
          );
      } else if (typeof io.input === "string")
        input.append(el("pre", { class: "io-message-preview" }, io.input));
      else if (Array.isArray(io.input))
        input.append(
          ...io.input.map((message) =>
            el(
              "div",
              { class: "saved-message" },
              el("strong", {}, message.role || "message"),
              el(
                "pre",
                {},
                typeof message.content === "string"
                  ? message.content
                  : JSON.stringify(message.content, null, 2),
              ),
            ),
          ),
        );
      else input.append(jsonTree(io.input));
      input.append(rawDetails("展开保存的输入字段", io.input));
    } else
      input.append(
        el("p", { class: "missing-record" }, "此步没有保存模型输入。"),
      );
    input.append(
      el(
        "p",
        { class: "io-boundary" },
        planning
          ? "这些是执行时的记录，不是组级规划时的模型输入；原规划请求未随轨迹保存。"
          : io.exactPrompt
            ? "按文件中保留的请求呈现；没有补写未保存的消息。"
            : io.inputKind === "previous_observation"
              ? "这是上一操作的反馈参考，不能视为本步完整提示词。"
              : "保存的是决策前公开上下文。完整提示词 / 消息历史未留存。",
      ),
    );
    const output = el(
      "article",
      { class: "io-pane output-pane" },
      paneHeading(
        "02",
        "MODEL OUTPUT",
        "为什么这样操作",
        io.audit
          ? "已保存决策说明"
          : planning || io.scripted
            ? "程序控制"
            : "未提供决策说明",
      ),
    );
    if (planning)
      output.append(
        el(
          "div",
          { class: "saved-plan" },
          el("h4", {}, "模型为本次生成的方案（规划输出）"),
          el("p", {}, `${planning.model || "模型"} · ${planning.member}`),
          el(
            "pre",
            { class: "io-raw" },
            JSON.stringify(planning.plan, null, 2),
          ),
        ),
      );
    if (io.audit) {
      for (const [name, value] of [
        ["实验目的", io.audit.diagnostic_target],
        ["预期效果", io.audit.expected_effect],
        ["模型说明", io.audit.rationale || io.audit.reasoning],
      ])
        if (value)
          output.append(
            el(
              "div",
              { class: "decision-statement" },
              el("h4", {}, name),
              el("p", {}, value),
            ),
          );
      const rules = io.audit.belief_update_rule;
      if (rules)
        output.append(
          el(
            "div",
            { class: "belief-branches" },
            rules.if_supported
              ? el(
                  "div",
                  {},
                  el("span", {}, "若得到支持"),
                  el("p", {}, rules.if_supported),
                )
              : null,
            rules.if_not_supported
              ? el(
                  "div",
                  {},
                  el("span", {}, "若不支持"),
                  el("p", {}, rules.if_not_supported),
                )
              : null,
          ),
        );
      if (finite(io.audit.uncertainty))
        output.append(
          el(
            "p",
            { class: "io-confidence" },
            `模型声明的不确定性：${format(io.audit.uncertainty)}`,
          ),
        );
    } else
      output.append(
        el(
          "div",
          { class: "missing-record" },
          planning || io.scripted
            ? "此步由脚本 / 规则执行，没有模型逐步说明。"
            : "模型没有为此步提供决策说明；保留动作，不推测原因。",
        ),
      );
    output.append(
      el(
        "div",
        { class: "tool-call" },
        el(
          "div",
          {},
          el("span", {}, "实际提交的操作"),
          el("code", {}, snap.action.operation || "action"),
        ),
        el("pre", {}, JSON.stringify(snap.action, null, 2)),
      ),
    );
    if (io.output) output.append(rawDetails("展开保存的模型输出", io.output));
    output.append(
      el(
        "p",
        { class: "io-boundary" },
        "展示模型明确提供的实验目标和解释，不代表未保存的内部推理。",
      ),
    );
    const tool = el(
      "article",
      { class: "io-pane feedback-pane" },
      paneHeading("03", "TOOL RETURN", "操作后返回了什么", snap.status),
    );
    const changed = Object.entries(snap.observations).filter(([, v]) =>
      finite(v),
    );
    tool.append(
      el(
        "div",
        { class: "feedback-readings" },
        changed.map(([key, value]) => {
          const before = context.visible_metrics?.[key];
          return el(
            "div",
            {},
            el("span", {}, label(key)),
            el("strong", {}, format(value)),
            finite(before) && value !== before
              ? el("small", {}, `此前 ${format(before)}`)
              : null,
          );
        }),
      ),
    );
    if (!changed.length)
      tool.append(
        el("p", { class: "missing-record" }, "此步没有已知数值观测。"),
      );
    const reason = snap.row.rollback_reason || io.tool.error_message;
    if (reason)
      tool.append(
        el(
          "div",
          { class: "alert error" },
          typeof reason === "string" ? reason : JSON.stringify(reason),
        ),
      );
    if (Object.keys(snap.delta).length)
      tool.append(rawDetails("本步过程与费用变化", snap.delta));
    tool.append(
      rawDetails("展开完整工具返回", io.tool),
      el(
        "p",
        { class: "io-boundary" },
        "读数来自本步返回，可能沿用历史测量；终检读数与过程估计不混用。",
      ),
    );
    grid.append(input, output, tool);
    return grid;
  }
  function paneHeading(number, en, title, sub) {
    return el(
      "header",
      {},
      el("div", { class: "io-pane-kicker" }, el("span", {}, number), en),
      el("h3", {}, title),
      el("small", {}, sub),
    );
  }
  function readings(values) {
    const pairs = Object.entries(values).filter(([, v]) => finite(v));
    return pairs.length
      ? el(
          "div",
          { class: "input-readings" },
          pairs.map(([k, v]) =>
            el(
              "div",
              {},
              el("span", {}, label(k)),
              el("strong", {}, format(v)),
            ),
          ),
        )
      : el("p", { class: "missing-record" }, "尚无已知数值读数");
  }
  function stateView(snap, group) {
    const root = el("div"),
      subset = records.slice(group.start, group.end + 1);
    const keys = [
      ...new Set(
        subset.flatMap((r) =>
          Object.entries(observations(r))
            .filter(([, v]) => finite(v))
            .map(([k]) => k),
        ),
      ),
    ];
    if (!keys.includes(operationMetric)) operationMetric = keys[0] || "score";
    root.append(
      stats([
        ["物理费用（账本累计）", snap.resources.physical_cost],
        ["过程秒数（账本累计）", snap.resources.process_time_s],
        ["取样体积 / L", snap.resources.sample_consumed_L],
        ["当前记录得分", snap.observations.score],
      ]),
    );
    root.append(
      el(
        "div",
        { class: "chart-panel" },
        el(
          "div",
          { class: "chart-head" },
          el("h3", {}, "本次实验的逐步观测"),
          selectMetric(
            keys,
            operationMetric,
            (k) => {
              operationMetric = k;
              draw();
            },
            "操作观测指标",
          ),
        ),
        chart(
          metricSeries(subset, operationMetric, controller.index - group.start),
          {
            current: controller.index - group.start,
            title: label(operationMetric),
            onSeek: seek,
          },
        ),
        el(
          "p",
          { class: "footnote" },
          "只显示当前操作及此前已知读数。跨小实验的累计资源保留原始账本口径。",
        ),
      ),
    );
    root.append(
      section(
        "公开操作状态",
        "",
        Object.keys(snap.operational).length
          ? jsonTree(snap.operational)
          : empty("该记录未保存公开操作状态"),
      ),
      section("剩余资源", "", jsonTree(snap.remaining)),
      rawDetails("模型资源与完整性标记", snap.method),
    );
    return root;
  }
  function draw() {
    campaignButton.classList.toggle("active", controller.mode === "campaign");
    experimentButton.classList.toggle(
      "active",
      controller.mode === "experiment",
    );
    campaignButton.setAttribute("aria-pressed", controller.mode === "campaign");
    experimentButton.setAttribute(
      "aria-pressed",
      controller.mode === "experiment",
    );
    slider.max = length() - 1;
    slider.value = cursor();
    position.textContent = `${cursor() + 1} / ${length()}`;
    scope.textContent =
      controller.mode === "campaign" ? "小实验 / 整组" : "操作 / 当前小实验";
    exportButton.hidden = controller.mode === "campaign";
    stage.replaceChildren();
    if (controller.mode === "campaign") campaignView();
    else experimentView();
    const active = stage.querySelector(".operation-node.active");
    if (active && activeStepNode !== controller.index) {
      active.scrollIntoView?.({
        block: "nearest",
        inline: "nearest",
        behavior: "instant",
      });
      activeStepNode = controller.index;
    }
  }
  if (controller.mode === "campaign") controller.index = groups[0].end;
  draw();
  return controller;
}
