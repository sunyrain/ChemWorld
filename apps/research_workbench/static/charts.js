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
  const W = 640,
    H = 270,
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
    dot = el("circle", { r: 3, fill: "#5251c9", visibility: "hidden" }),
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
