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
  const offset = 0;
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
      status: committed ? "已执行" : e.transaction_status === "rolled_back" ? "已回滚" : "未执行",
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

export function graphLayout(graph, saved = {}, viewport = {width:1000,height:630}) {
  let columns=1,best=0;
  for(let count=1;count<=Math.min(6,graph.nodes.length);count++) {
    const scale=Math.min((viewport.width-56)/(208+(count-1)*264),(viewport.height-56)/(134+(Math.ceil(graph.nodes.length/count)-1)*168));
    if(scale>best){best=scale;columns=count;}
  }
  return new Map(graph.nodes.map((node, i) => {
    const row = Math.floor(i / columns), column = i % columns;
    const point = saved[node.id];
    return [node.id, point && Number.isFinite(point.x) && Number.isFinite(point.y)
      ? { ...point } : { x: 32 + (row % 2 ? columns - 1 - column : column) * 264, y: 32 + row * 168 }];
  }));
}

export function drawExplorationGraph(container, graph, onSelect, options = {}) {
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
    container.replaceChildren(empty);
    return { fit() {}, resetLayout() {}, zoomBy() {}, focusLatest() {}, dispose() {}, interacting: false };
  }
  const nodeWidth=208, nodeHeight=134;
  let manualLayout=options.saved?.manualLayout || false;
  let positions = graphLayout(graph,manualLayout?options.saved?.positions:{},{width:container.clientWidth,height:container.clientHeight});
  const svg=make('svg',{role:'group',tabindex:0,'aria-label':graph.title+'。拖动空白平移，滚轮缩放，方向键平移，Home 适应画布。'});
  const scene=make('g',{class:'graph-scene'}), nodeElements=new Map(), edgeElements=[];
  const defs=make('defs');
  const marker=make('marker',{id:'graph-arrow',viewBox:'0 0 10 10',refX:8,refY:5,markerWidth:6,markerHeight:6,orient:'auto-start-reverse'});
  marker.append(make('path',{d:'M 2 1 L 7 5 L 2 9',fill:'none',stroke:'var(--graph-link)','stroke-width':1.5}));
  defs.append(marker);svg.append(defs,scene);
  graph.edges.forEach(edge=>{
    const path=make('path',{class:'network-edge '+graph.kind,'marker-end':'url(#graph-arrow)'});
    const port=make('circle',{r:4.5,class:'network-port'});
    edgeElements.push({edge,path,port});scene.append(path,port);
  });
  function drawEdges() {
    edgeElements.forEach(({edge,path,port})=>{
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
      path.setAttribute('d',d);port.setAttribute('cx',x1);port.setAttribute('cy',y1);
    });
  }
  graph.nodes.forEach((n,i)=>{
    const p=positions.get(n.id),interactive=n.eventIndex!==undefined;
    const selected = graph.selectedId === n.id || (!graph.selectedId && interactive && i===graph.nodes.length-1);
    const g=make('g',{transform:`translate(${p.x} ${p.y})`,class:'network-node '+n.state+(selected?' selected':''),
      ...(interactive?{role:'button',tabindex:0,'aria-label':n.label+'，'+n.status+'，查看事件'}:{role:'group','aria-label':n.label+'，'+n.status})});
    g.append(make('rect',{width:nodeWidth,height:nodeHeight,rx:7,class:'node-card'}));
    g.dataset.nodeId=n.id;
    if(interactive) g.append(make('text',{x:194,y:18,'text-anchor':'end',class:'node-index'},String(n.eventIndex+1).padStart(2,'0')));
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
      g.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();onSelect(n.eventIndex);}});
    }
    scene.append(g);nodeElements.set(n.id,g);
  });
  container.replaceChildren(svg);
  drawEdges();
  let width=options.saved?.viewport?.width || 0,height=options.saved?.viewport?.height || 0,drag=null;
  let camera={x:0,y:0,scale:1,autoFit:true,...options.saved?.camera};
  const emit=()=>options.onChange?.({camera:{...camera},positions:Object.fromEntries(positions),viewport:{width,height},manualLayout});
  function paint() {
    scene.setAttribute('transform',`translate(${camera.x} ${camera.y}) scale(${camera.scale})`);
    emit();
  }
  function fit() {
    const points=[...positions.values()];
    const left=Math.min(...points.map(p=>p.x)),top=Math.min(...points.map(p=>p.y));
    const w=Math.max(...points.map(p=>p.x))+nodeWidth-left;
    const h=Math.max(...points.map(p=>p.y))+nodeHeight-top;
    const scale=Math.min(1.2,(width-40)/w,(height-40)/h);
    camera={scale:Math.max(.02,scale),x:(width-w*scale)/2-left*scale,y:(height-h*scale)/2-top*scale,autoFit:true};
    paint();
  }
  function resize() {
    const oldWidth=width,oldHeight=height;
    width=Math.max(1,container.clientWidth);height=Math.max(1,container.clientHeight);
    svg.setAttribute('viewBox',`0 0 ${width} ${height}`);
    if(camera.autoFit) {if(!manualLayout) arrange();fit();}
    else { if(oldWidth) {camera.x+=(width-oldWidth)/2;camera.y+=(height-oldHeight)/2;} paint(); }
  }
  function arrange() {
    positions=graphLayout(graph,{}, {width,height});
    positions.forEach((p,id)=>nodeElements.get(id).setAttribute('transform',`translate(${p.x} ${p.y})`));drawEdges();
  }
  function resetLayout() {manualLayout=false;arrange();fit();}
  function zoomBy(factor, anchor={x:width/2,y:height/2}) {
    const scale=Math.max(.02,Math.min(3,camera.scale*factor)),ratio=scale/camera.scale;
    camera={x:anchor.x-(anchor.x-camera.x)*ratio,y:anchor.y-(anchor.y-camera.y)*ratio,scale,autoFit:false};paint();
  }
  function focusLatest() {
    const point=positions.get(graph.nodes.at(-1).id),scale=Math.max(.8,camera.scale);
    camera={scale,x:width/2-(point.x+nodeWidth/2)*scale,y:height/2-(point.y+nodeHeight/2)*scale,autoFit:false};paint();
  }
  const point=e=>{const box=svg.getBoundingClientRect();return {x:e.clientX-box.left,y:e.clientY-box.top};};
  svg.addEventListener('wheel',e=>{
    e.preventDefault();zoomBy(Math.exp(-Math.max(-120,Math.min(120,e.deltaY))*.0025),point(e));
  },{passive:false});
  svg.addEventListener('pointerdown',e=>{
    if(drag || ![0,1].includes(e.button)) return;
    const node=e.button===0?e.target.closest('.network-node'):null;
    const id=node?.dataset.nodeId;
    drag={pointer:e.pointerId,start:point(e),camera:{...camera},id,
      position:id?{...positions.get(id)}:null,moved:false};
    svg.setPointerCapture(e.pointerId);svg.classList.add('is-dragging');e.preventDefault();
  });
  svg.addEventListener('pointermove',e=>{
    if(!drag || drag.pointer!==e.pointerId) return;
    const p=point(e),dx=p.x-drag.start.x,dy=p.y-drag.start.y;
    if(!drag.moved && Math.hypot(dx,dy)<5) return;
    drag.moved=true;camera.autoFit=false;
    if(drag.id) {
      manualLayout=true;
      const position={x:drag.position.x+dx/camera.scale,y:drag.position.y+dy/camera.scale};
      positions.set(drag.id,position);nodeElements.get(drag.id).setAttribute('transform',`translate(${position.x} ${position.y})`);drawEdges();
    } else {camera.x=drag.camera.x+dx;camera.y=drag.camera.y+dy;}
    paint();
  });
  function release(e) {
    if(!drag || drag.pointer!==e.pointerId) return;
    const gesture=drag;drag=null;svg.classList.remove('is-dragging');
    if(svg.hasPointerCapture(e.pointerId)) svg.releasePointerCapture(e.pointerId);
    if(e.type==='pointerup' && !gesture.moved && gesture.id) {
      const node=graph.nodes.find(n=>n.id===gesture.id);
      if(node.eventIndex!==undefined) onSelect(node.eventIndex);
    }
    emit();
  }
  svg.addEventListener('pointerup',release);svg.addEventListener('pointercancel',release);
  svg.addEventListener('lostpointercapture',release);
  svg.addEventListener('keydown',e=>{
    const delta={ArrowLeft:[40,0],ArrowRight:[-40,0],ArrowUp:[0,40],ArrowDown:[0,-40]}[e.key];
    if(delta) {e.preventDefault();camera.x+=delta[0];camera.y+=delta[1];camera.autoFit=false;paint();}
    if(e.key==='Home') {e.preventDefault();fit();}
    if(e.key==='+' || e.key==='=') {e.preventDefault();zoomBy(1.2);}
    if(e.key==='-') {e.preventDefault();zoomBy(1/1.2);}
  });
  resize();
  const observer=new ResizeObserver(resize);observer.observe(container);
  return {fit,resetLayout,zoomBy,focusLatest,get interacting(){return Boolean(drag);},dispose(){observer.disconnect();}};
}

// Public-event summaries never infer an observation from an unexecuted request.
export function eventSummary(event) {
  const committed=event.transaction_status==='committed',rollback=event.transaction_status==='rolled_back';
  const action=event.action || {};
  const reasons=event.validation?.invalid_reasons || event.report?.failure_summary?.failed_preconditions || [];
  const reasonText=reason=>({
    seed_crystals_requires_current_reaction_assay:'添加晶种前，需要对当前反应液做一次测定。',
    filter_crystals_requires_current_slurry_assay:'过滤前，需要对当前浆料做一次测定。',
    measure_final_requires_terminated:'终检前需要先终止反应。',
    run_flow_requires_flow_setup:'运行前需要先配置流动条件。',
  })[reason] || (reason.startsWith('payload_bounds:')
    ? ({duration_s:'请求时长不在当时允许的范围内。',target_temperature_K:'请求温度不在当时允许的范围内。'}[reason.split(':')[1]] || '请求参数超出当时允许的范围。')
    : '当前实验状态不满足这一步的执行条件。');
  const measured=committed && action.operation==='measure';
  const labels={yield:'产率',selectivity:'选择性',conversion:'转化率',crystal_yield:'晶体回收',crystal_purity:'晶体纯度',flow_conversion:'流动转化率',purity:'纯度',recovery:'回收率',crystal_fines_fraction:'细粉比例'};
  const source=event.observation || event.report?.visible_metrics || {};
  const metrics=measured?Object.entries(labels).filter(([key])=>Number.isFinite(source[key]) && event.observed_mask?.[key]!==false).map(([key,label])=>({key,label,value:source[key]})):[];
  const summary=rollback?'环境一致性检查未通过，这次操作已回滚，未产生新的有效实验结果。'
    : !committed?[...new Set(reasons.map(reasonText))].join(' ') || '这次请求未执行，实验记录已保留。'
    : measured?action.instrument==='final_assay'?'已完成终检，以下为这次实际测得的结果。':'已完成仪器测量，以下为这次实际观测。'
    : action.operation==='terminate'?'已终止反应；是否完成实验仍以终检记录为准。':'操作已执行，参数和资源变化已保存。';
  return {status:committed?'已执行':rollback?'已回滚':'未执行',summary,metrics,
    parameters:Object.entries(action).filter(([key])=>key!=='operation'),
    resourceDelta:event.delta || null,
    caveat:rollback?'回滚后仍可能保留虚拟成本；详见记录的资源变化。':!committed?'请求参数不代表已经实际执行。':measured?'虚拟仪器观测；未测指标不会显示为零。':action.residence_time_s!==undefined?'停留时间为请求值，实际值由容器体积和流量决定。':null};
}
