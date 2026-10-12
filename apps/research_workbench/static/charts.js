export function extent(points, index) {
  const values = points.map((p) => p[index]).filter(Number.isFinite);
  if (!values.length) return [0, 1];
  let lo = Math.min(...values),
    hi = Math.max(...values);
  if (lo === hi) {
    lo -= 0.5;
    hi += 0.5;
  }
  return [lo, hi];
}

export function drawChart(container, series) {
  const ns = "http://www.w3.org/2000/svg";
  const el = (tag, attrs = {}, text) => {
    const node = document.createElementNS(ns, tag);
    for (const [k, v] of Object.entries(attrs)) node.setAttribute(k, v);
    if (text !== undefined) node.textContent = text;
    return node;
  };
  const points = series.points.filter(
    (p) => p.length === 2 && p.every(Number.isFinite),
  );
  if (!points.length) {
    container.textContent = "没有可绘制的观测";
    return;
  }
  const [xmin, xmax] = extent(points, 0),
    [ymin, ymax] = extent(points, 1);
  const W = Math.max(320, Math.min(640, container.clientWidth || 640)),
    H = W < 450 ? 220 : 270,
    L = 65,
    R = 22,
    T = 25,
    B = 48;
  const X = (x) =>
    L +
    ((series.reverse_x ? xmax - x : x - xmin) / (xmax - xmin)) * (W - L - R);
  const Y = (y) => H - B - ((y - ymin) / (ymax - ymin)) * (H - B - T);
  const svg = el("svg", {
    viewBox: `0 0 ${W} ${H}`,
    role: "img",
    "aria-label": `${series.label}，${series.x_label} (${series.x_unit})，${series.y_label} (${series.y_unit})`,
  });
  const fmt = (n) =>
    Math.abs(n) < 0.001 && n !== 0
      ? n.toExponential(1)
      : Number(n.toPrecision(4)).toString();
  for (let i = 0; i < 5; i++) {
    const y = ymin + ((ymax - ymin) * i) / 4;
    svg.append(
      el("line", {
        x1: L,
        x2: W - R,
        y1: Y(y),
        y2: Y(y),
        class: "chart-gridline",
      }),
      el(
        "text",
        { x: L - 10, y: Y(y) + 3, "text-anchor": "end", class: "chart-axis" },
        fmt(y),
      ),
    );
  }
  for (let i = 0; i < 6; i++) {
    const x = xmin + ((xmax - xmin) * i) / 5;
    svg.append(
      el(
        "text",
        {
          x: X(x),
          y: H - B + 20,
          "text-anchor": "middle",
          class: "chart-axis",
        },
        fmt(x),
      ),
    );
  }
  svg.append(
    el(
      "text",
      { x: L, y: 12, class: "chart-axis" },
      `${series.y_label} · ${series.y_unit}`,
    ),
    el(
      "text",
      {
        x: (W + L - R) / 2,
        y: H - 6,
        "text-anchor": "middle",
        class: "chart-axis",
      },
      `${series.x_label} (${series.x_unit})`,
    ),
  );
  svg.append(
    el("path", {
      d: points
        .map(
          (p, i) =>
            `${i ? "L" : "M"}${X(p[0]).toFixed(2)},${Y(p[1]).toFixed(2)}`,
        )
        .join(" "),
      class: "chart-line",
    }),
  );
  const cross = el("line", {
      y1: T,
      y2: H - B,
      class: "chart-cross",
      visibility: "hidden",
    }),
    dot = el("circle", { r: 3, fill: "var(--teal)", visibility: "hidden" }),
    readout = el("text", {
      x: W - R,
      y: 13,
      "text-anchor": "end",
      class: "chart-readout",
    });
  svg.append(cross, dot, readout);
  svg.addEventListener("pointermove", (event) => {
    const b = svg.getBoundingClientRect();
    const x = ((event.clientX - b.left) * W) / b.width;
    const nearest = points.reduce(
      (a, p) => (Math.abs(X(p[0]) - x) < Math.abs(X(a[0]) - x) ? p : a),
      points[0],
    );
    cross.setAttribute("x1", X(nearest[0]));
    cross.setAttribute("x2", X(nearest[0]));
    cross.setAttribute("visibility", "visible");
    dot.setAttribute("cx", X(nearest[0]));
    dot.setAttribute("cy", Y(nearest[1]));
    dot.setAttribute("visibility", "visible");
    readout.textContent = `${fmt(nearest[0])} ${series.x_unit} / ${fmt(nearest[1])}`;
  });
  svg.addEventListener("pointerleave", () => {
    cross.setAttribute("visibility", "hidden");
    dot.setAttribute("visibility", "hidden");
    readout.textContent = "";
  });
  container.replaceChildren(svg);
}

// Build only from saved public facts. Chronology is never presented as material flow.
export function explorationGraph(run, mode = "events", labels = {}) {
  const network = run.view?.component_network;
  if (mode === "network" && network?.vessels?.length) {
    const nodes = network.vessels.map((v) => ({
      id: v.id,
      label: v.id,
      detail: "容量 " + v.capacity_L + " L",
      state: v.id === network.active_vessel ? "active" : "neutral",
      status: v.id === network.active_vessel ? "当前容器" : "容器",
    }));
    const ids = new Set(nodes.map((n) => n.id));
    return {
      kind: "network", title: "组件网络", legend: "公开连接 · 不代表本次已转移物料",
      total: nodes.length, nodes,
      edges: (network.connections || [])
        .filter((e) => ids.has(e.source_vessel) && ids.has(e.target_vessel))
        .map((e) => ({ source: e.source_vessel, target: e.target_vessel })),
    };
  }
  const events = run.events || [];
  const offset = Math.max(0, events.length - 12);
  const nodes = events.slice(offset).map((e, i) => {
    const committed = e.transaction_status === "committed";
    const parameters = Object.entries(e.action || {})
      .filter(([key]) => key !== "operation")
      .map(([key, value]) => (labels[key] || key) + ": " + (typeof value === "object" ? JSON.stringify(value) : value));
    return {
      id: e.event_id, eventIndex: offset + i,
      label: labels[e.action?.operation] || e.action?.operation || "操作",
      detail: parameters.join(" · ") || "已保存公开事件",
      state: committed ? "committed" : "rejected",
      status: committed ? "已提交" : "拒绝 / 回滚",
    };
  });
  return {
    kind: "events", title: "执行轨迹", legend: "箭头仅表示提交顺序",
    total: events.length, nodes,
    edges: nodes.slice(1).map((n, i) => ({ source: nodes[i].id, target: n.id })),
  };
}

export function drawExplorationGraph(container, graph, onSelect) {
  const ns = "http://www.w3.org/2000/svg";
  const make = (tag, attrs = {}, text) => {
    const n = document.createElementNS(ns, tag);
    for (const [k, v] of Object.entries(attrs)) n.setAttribute(k, v);
    if (text !== undefined) n.textContent = text;
    return n;
  };
  if (!graph.nodes.length) {
    const empty = document.createElement("div");
    empty.className = "graph-empty";
    empty.textContent = "等待第一条操作记录。执行轨迹将随实验展开。";
    container.replaceChildren(empty);
    return;
  }
  const columns = 3, width = 900, nodeWidth = 218, nodeHeight = 108;
  const rows = Math.ceil(graph.nodes.length / columns);
  const height = Math.max(440, rows * 158 + 76);
  const positions = new Map(graph.nodes.map((n, i) => {
    const row = Math.floor(i / columns), col = i % columns;
    return [n.id, { x: 35 + (row % 2 ? columns - 1 - col : col) * 295, y: 40 + row * 158 }];
  }));
  const svg = make("svg", { viewBox: "0 0 " + width + " " + height, role: "group", "aria-label": graph.title + "，" + graph.legend });
  const defs = make("defs");
  const marker = make("marker", { id: "graph-arrow", viewBox: "0 0 10 10", refX: 9, refY: 5, markerWidth: 5, markerHeight: 5, orient: "auto-start-reverse" });
  marker.append(make("path", { d: "M 1 1 L 9 5 L 1 9", fill: "none", stroke: "var(--teal)", "stroke-width": 1.5 }));
  defs.append(marker); svg.append(defs);
  for (const edge of graph.edges) {
    const a = positions.get(edge.source), b = positions.get(edge.target);
    const forward = b.x > a.x, sameRow = a.y === b.y;
    const x1 = sameRow ? a.x + (forward ? nodeWidth : 0) : a.x + nodeWidth / 2;
    const y1 = sameRow ? a.y + nodeHeight / 2 : a.y + nodeHeight;
    const x2 = sameRow ? b.x + (forward ? 0 : nodeWidth) : b.x + nodeWidth / 2;
    const y2 = sameRow ? b.y + nodeHeight / 2 : b.y;
    const path = sameRow
      ? "M " + x1 + " " + y1 + " C " + (x1 + x2) / 2 + " " + y1 + " " + (x1 + x2) / 2 + " " + y2 + " " + x2 + " " + y2
      : "M " + x1 + " " + y1 + " C " + x1 + " " + (y1 + y2) / 2 + " " + x2 + " " + (y1 + y2) / 2 + " " + x2 + " " + y2;
    svg.append(make("path", { d: path, class: "network-edge", "marker-end": "url(#graph-arrow)" }));
  }
  graph.nodes.forEach((n, i) => {
    const p = positions.get(n.id), interactive = n.eventIndex !== undefined;
    const g = make("g", { transform: "translate(" + p.x + " " + p.y + ")", class: "network-node " + n.state,
      ...(interactive ? { role: "button", tabindex: 0, "aria-label": n.label + "，" + n.status + "，查看事件" } : { role: "group", "aria-label": n.label + "，" + n.status }) });
    g.append(make("rect", { width: nodeWidth, height: nodeHeight, rx: 10, class: "node-card" }));
    g.append(make("text", { x: 18, y: 27, class: "node-index" }, String(n.eventIndex !== undefined ? n.eventIndex + 1 : i + 1).padStart(2, "0")));
    g.append(make("text", { x: 48, y: 27, class: "node-label" }, n.label.length > 14 ? n.label.slice(0, 13) + "…" : n.label));
    g.append(make("text", { x: 18, y: 53, class: "node-detail" }, n.detail.length > 25 ? n.detail.slice(0, 24) + "…" : n.detail));
    g.append(make("circle", { cx: 23, cy: 83, r: 4, class: "node-status-dot" }));
    g.append(make("text", { x: 36, y: 87, class: "node-status" }, n.status));
    g.append(make("title", {}, n.label + "\n" + n.detail + "\n" + n.status));
    if (interactive) {
      g.addEventListener("click", () => onSelect(n.eventIndex));
      g.addEventListener("keydown", (e) => {
        if (e.key === "Enter" || e.key === " ") { e.preventDefault(); onSelect(n.eventIndex); }
      });
    }
    svg.append(g);
  });
  container.replaceChildren(svg);
}
