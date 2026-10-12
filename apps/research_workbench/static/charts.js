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
    H = container.id === "explore-chart"
      ? Math.max(120, Math.min(245, container.clientHeight || 220))
      : W < 450 ? 220 : 270,
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
      operation: "vessel", lines: ["容量 " + v.capacity_L + " L"],
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
      operation: e.action?.operation, instrument: e.action?.instrument,
      lines: actionLines(e.action || {}),
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

export function icon(name) {
  const paths = {
    flask: '<path d="M9 3h6M10 3v6l-5 9a2 2 0 0 0 2 3h10a2 2 0 0 0 2-3l-5-9V3M8 15h8"/>',
    book: '<path d="M12 5v16M3 4c4-1 6 0 9 2 3-2 5-3 9-2v15c-4-1-6 0-9 2-3-2-5-3-9-2Z"/>',
    records: '<rect x="5" y="3" width="14" height="18" rx="2"/><path d="M9 7h6M9 11h6M9 15h3"/>',
    settings: '<path d="m10 3-1 3-3 1-3 3 2 2-1 4 3 1 2 4h4l2-3 4-1 2-4-2-3V6l-4-1-2-2Z"/><circle cx="12" cy="12" r="3"/>',
    wrench: '<path d="m14 6 4-4a6 6 0 0 1-7 8L4 19a2 2 0 0 0 3 3l8-9a6 6 0 0 0 7-7l-4 4Z"/>',
    chart: '<rect x="3" y="3" width="18" height="18" rx="3"/><path d="m5 16 3-1 3-9 3 12 3-7 2 4"/>',
    network: '<circle cx="12" cy="4" r="3"/><circle cx="4" cy="19" r="3"/><circle cx="20" cy="19" r="3"/><path d="m10 7-5 9m9-9 5 9M7 19h10"/>',
    target: '<circle cx="12" cy="12" r="8"/><circle cx="12" cy="12" r="4"/><path d="m12 12 8-9"/>',
    fit: '<path d="M9 3H3v6m12-6h6v6M3 15v6h6m12-6v6h-6"/>',
    clock: '<circle cx="12" cy="12" r="9"/><path d="M12 6v6l4 2"/>',
    agent: '<path d="m12 3 1 4 4 1-4 2-1 4-2-4-4-2 4-1Z"/><path d="M5 13v7h14v-7M8 17h1m6 0h1M19 3v5m-2-2h4"/>',
    compare: '<path d="M4 20V8m8 12V3m8 17V12"/>',
    sun: '<circle cx="12" cy="12" r="4"/><path d="M12 1v3m0 16v3M1 12h3m16 0h3M4 4l2 2m12 12 2 2M4 20l2-2M18 6l2-2"/>',
    moon: '<path d="M21 13A9 9 0 0 1 11 3 9 9 0 1 0 21 13Z"/>',
  };
  return '<svg class="ui-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + (paths[name] || paths.flask) + '</svg>';
}

export function actionLines(action) {
  const fmt = n => Number(n.toPrecision(4)).toString();
  if (action.operation === 'heat') return [
    Number.isFinite(action.target_temperature_K) ? fmt(action.target_temperature_K - 273.15) + ' °C' : '温度未提供',
    Number.isFinite(action.duration_s) ? fmt(action.duration_s / 60) + ' min' : '时长未提供',
  ];
  if (action.instrument) return [action.instrument === 'final_assay' ? '终检数据包' : action.instrument.toUpperCase(), '实际仪器观测'];
  const fields = [['volume_L',1000,'mL'],['amount_mol',1000,'mmol'],['catalyst_amount_mol',1000,'mmol'],['duration_s',1/60,'min'],['flow_rate_mL_min',1,'mL/min']];
  const values = fields.filter(([key])=>Number.isFinite(action[key])).map(([key,scale,unit])=>fmt(action[key]*scale)+' '+unit);
  if (action.solvent !== undefined) values.push('溶剂 '+action.solvent);
  if (action.catalyst !== undefined) values.push('催化剂 '+action.catalyst);
  return values.slice(0,2).length ? values.slice(0,2) : ['已保存操作'];
}

function apparatus(kind, id) {
  const liquid = kind === 'add_solvent' ? '#a278ed' : '#41bdec';
  const defs = '<defs><linearGradient id="glass-'+id+'"><stop stop-color="#6e94ae" stop-opacity=".8"/><stop offset=".28" stop-color="#e1f4ff" stop-opacity=".8"/><stop offset=".52" stop-color="#96b5c8" stop-opacity=".1"/><stop offset="1" stop-color="#6289a4" stop-opacity=".65"/></linearGradient><linearGradient id="liquid-'+id+'" x2="1" y2="1"><stop stop-color="'+liquid+'" stop-opacity=".95"/><stop offset="1" stop-color="'+liquid+'" stop-opacity=".3"/></linearGradient></defs>';
  const glass = 'url(#glass-'+id+')', fill = 'url(#liquid-'+id+')';
  let drawing;
  if (kind === 'measure') {
    drawing = '<rect x="5" y="12" width="47" height="49" rx="6" fill="var(--device-face)" stroke="#95aac3" stroke-width="1.5"/><rect x="10" y="18" width="37" height="33" rx="3" fill="var(--canvas)"/><path d="m12 42 5 0 4-20 4 21 5-8 3 9 4-3 8 0" fill="none" stroke="#a899ff" stroke-width="2.5"/><circle cx="29" cy="56" r="2" fill="#98a3bb"/>';
  } else if (['heat','run_flow','set_flow_rate','advance_flow'].includes(kind)) {
    drawing = '<path d="M20 23h18l6 25H14Z" fill="'+glass+'" stroke="#9faec2"/><path d="m18 39-2 7h26l-2-7Z" fill="'+fill+'"/><path d="M21 5c-6 7 5 7-1 13m10-13c-6 7 5 7-1 13m10-13c-6 7 5 7-1 13" fill="none" stroke="#b8c8db" stroke-width="1.5"/><rect x="9" y="49" width="39" height="13" rx="3" fill="#56687b" stroke="#b0bed1"/><rect x="13" y="52" width="16" height="5" fill="#0e1c2b"/><circle cx="39" cy="55" r="3" fill="#d5ddeb"/>';
  } else if (['sample','quench','terminate','filter_crystals','cool_crystallize'].includes(kind)) {
    drawing = '<path d="M20 12h18v45a9 9 0 0 1-18 0Z" fill="'+glass+'" stroke="#acbfd3"/><path d="M23 31h12v26a6 6 0 0 1-12 0Z" fill="'+fill+'"/><rect x="18" y="5" width="22" height="11" rx="2" fill="#556883" stroke="#b7c9e4"/><path d="M25 20v32" stroke="white" stroke-opacity=".65" stroke-width="2"/>';
  } else {
    drawing = '<rect x="21" y="3" width="16" height="14" rx="2" fill="#41526b" stroke="#a9b8cb"/><path d="M22 17v5l-9 6v35q0 3 4 3h26q4 0 4-3V28l-10-6v-5Z" fill="'+glass+'" stroke="#afc3d6" stroke-width="1.2"/><path d="M16 39h28v24H16Z" fill="'+fill+'"/><path d="M20 29v31" stroke="white" stroke-opacity=".65" stroke-width="2"/><path d="M16 34h28" stroke="#c9e4f2" stroke-opacity=".6"/>';
  }
  return defs + drawing;
}

export function drawExplorationGraph(container, graph, onSelect) {
  const ns = 'http://www.w3.org/2000/svg';
  const make = (tag, attrs = {}, text) => {
    const n = document.createElementNS(ns, tag);
    for (const [k,v] of Object.entries(attrs)) n.setAttribute(k,v);
    if (text !== undefined) n.textContent = text;
    return n;
  };
  if (!graph.nodes.length) {
    const empty = document.createElement('div'); empty.className = 'graph-empty';
    empty.textContent = '等待第一条操作记录。执行轨迹将随实验展开。';
    container.replaceChildren(empty); return;
  }
  const nodeWidth=184, nodeHeight=134, width=1000, height=630;
  const feeds = graph.kind === 'events' ? graph.nodes.findIndex(n=>!['add_solvent','add_reagent','add_catalyst'].includes(n.operation)) : 0;
  const feedCount = feeds > 0 && feeds <= 3 ? feeds : 0;
  const positions = new Map(graph.nodes.map((n,i)=>{
    let x,y;
    if(feedCount && i<feedCount) { x=26; y=95+i*180; }
    else if(feedCount) {
      const j=i-feedCount, row=Math.floor(j/3), col=j%3;
      x=276+(row%2?2-col:col)*248; y=graph.nodes.length<=6?275:185+row*185;
      if(graph.nodes.length-feedCount>6) y=75+row*185;
    } else {
      const row=Math.floor(i/4),col=i%4;
      x=25+(row%2?3-col:col)*249; y=110+row*180;
    }
    return [n.id,{x,y}];
  }));
  const svg=make('svg',{viewBox:`0 0 ${width} ${height}`,role:'group','aria-label':graph.title+'，'+graph.legend});
  const defs=make('defs');
  const marker=make('marker',{id:'graph-arrow',viewBox:'0 0 10 10',refX:8,refY:5,markerWidth:6,markerHeight:6,orient:'auto-start-reverse'});
  marker.append(make('path',{d:'M 2 1 L 7 5 L 2 9',fill:'none',stroke:'var(--graph-link)','stroke-width':1.5}));
  defs.append(marker);svg.append(defs);
  graph.edges.forEach(edge=>{
    const a=positions.get(edge.source),b=positions.get(edge.target);
    const sameColumn=a.x===b.x,forward=b.x>a.x;
    const x1=sameColumn?a.x+nodeWidth/2:a.x+(forward?nodeWidth:0);
    const y1=sameColumn?a.y+nodeHeight:a.y+nodeHeight/2;
    const x2=sameColumn?b.x+nodeWidth/2:b.x+(forward?0:nodeWidth);
    const y2=sameColumn?b.y:b.y+nodeHeight/2;
    let d;
    if(sameColumn) d=`M ${x1} ${y1} V ${y2}`;
    else {
      const mid=(x1+x2)/2;
      d=`M ${x1} ${y1} C ${mid} ${y1} ${mid} ${y2} ${x2} ${y2}`;
    }
    svg.append(make('path',{d,class:'network-edge '+graph.kind,'marker-end':'url(#graph-arrow)'}));
    svg.append(make('circle',{cx:x1,cy:y1,r:4.5,class:'network-port'}));
  });
  graph.nodes.forEach((n,i)=>{
    const p=positions.get(n.id),interactive=n.eventIndex!==undefined;
    const selected = graph.selectedId === n.id || (!graph.selectedId && interactive && i===graph.nodes.length-1);
    const g=make('g',{transform:`translate(${p.x} ${p.y})`,class:'network-node '+n.state+(selected?' selected':''),
      ...(interactive?{role:'button',tabindex:0,'aria-label':n.label+'，'+n.status+'，查看事件'}:{role:'group','aria-label':n.label+'，'+n.status})});
    g.append(make('rect',{width:nodeWidth,height:nodeHeight,rx:7,class:'node-card'}));
    const device=make('g',{transform:'translate(9 24) scale(.85)',class:'apparatus-icon'});
    device.innerHTML=apparatus(n.operation,'node'+i);g.append(device);
    const label=n.label==='仪器测量'?(n.instrument==='final_assay'?'终检':'测量'):n.label;
    g.append(make('text',{x:65,y:31,class:'node-label'},label.length>8?label.slice(0,8)+'…':label));
    const lines=n.lines || [n.detail];
    lines.slice(0,2).forEach((line,j)=>g.append(make('text',{x:65,y:56+j*21,class:'node-detail'},line.length>16?line.slice(0,15)+'…':line)));
    g.append(make('circle',{cx:24,cy:111,r:8,class:'node-status-dot'}));
    g.append(make('path',{d:n.state==='rejected'?'M20 107l8 8m0-8-8 8':'M20 111l3 3 5-6',class:'node-check'}));
    g.append(make('text',{x:40,y:115,class:'node-status'},n.status));
    g.append(make('title',{},n.label+'\n'+n.detail+'\n'+n.status));
    if(interactive) {
      g.dataset.eventIndex=n.eventIndex;
      g.addEventListener('click',()=>onSelect(n.eventIndex));
      g.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();onSelect(n.eventIndex);}});
    }
    svg.append(g);
  });
  container.replaceChildren(svg);
}
