(() => {
  const finite = (value) => Number.isFinite(Number(value));
  const escapeHtml = (value) => String(value ?? "").replaceAll("&", "&amp;").replaceAll("<", "&lt;").replaceAll(">", "&gt;").replaceAll('"', "&quot;").replaceAll("'", "&#039;");

  function mount({ canvas, tabs, peaks, empty, meta, theme = "dark" }) {
    let payload = null;
    let selected = 0;

    function render(nextPayload) {
      payload = nextPayload?.available ? nextPayload : null;
      selected = 0;
      paint();
    }

    function paint() {
      const series = payload?.series || [];
      tabs.innerHTML = series.map((item, index) => `<button class="spectrum-tab ${index === selected ? "active" : ""}" data-index="${index}">${escapeHtml(item.label)}</button>`).join("");
      tabs.querySelectorAll("button").forEach((button) => button.addEventListener("click", () => {
        selected = Number(button.dataset.index);
        paint();
      }));
      const current = series[selected];
      empty.classList.toggle("hidden", Boolean(current));
      canvas.classList.toggle("hidden", !current);
      if (!current) {
        peaks.innerHTML = '<span class="spectrum-empty-chip">运行测量操作后显示公开仪器曲线</span>';
        meta.textContent = "No public signal";
        clearCanvas(canvas);
        return;
      }
      meta.textContent = `${current.x_label} (${current.x_unit}) · ${current.y_label} (${current.y_unit})`;
      peaks.innerHTML = current.peaks?.length ? current.peaks.slice(0, 8).map((peak) => `<span><b>${escapeHtml(peak.group)}</b>${Number(peak.center).toFixed(2)} · ${escapeHtml(peak.label)}</span>`).join("") : '<span class="spectrum-empty-chip">该信号未提供公开峰指认</span>';
      draw(canvas, current, theme);
    }

    render(null);
    return { render };
  }

  function clearCanvas(canvas) {
    canvas.getContext("2d").clearRect(0, 0, canvas.width, canvas.height);
  }

  function draw(canvas, series, theme) {
    const context = canvas.getContext("2d");
    const width = canvas.width;
    const height = canvas.height;
    const pad = { left: 58, right: 20, top: 22, bottom: 38 };
    const x = (series.x || []).map(Number);
    const y = (series.y || []).map(Number);
    const points = Math.min(x.length, y.length);
    clearCanvas(canvas);
    if (!points) return;
    const xMin = Math.min(...x.slice(0, points));
    const xMax = Math.max(...x.slice(0, points));
    const yMinRaw = Math.min(...y.slice(0, points));
    const yMaxRaw = Math.max(...y.slice(0, points));
    const yPadding = Math.max((yMaxRaw - yMinRaw) * 0.08, 0.01);
    const yMin = Math.min(0, yMinRaw - yPadding);
    const yMax = yMaxRaw + yPadding;
    const dark = theme === "dark";
    const grid = dark ? "rgba(153,207,215,.10)" : "rgba(18,74,72,.10)";
    const text = dark ? "#63808a" : "#718487";
    const lineA = dark ? "#53e0ca" : "#079b86";
    const lineB = dark ? "#42bdf5" : "#27aee2";
    const chartWidth = width - pad.left - pad.right;
    const chartHeight = height - pad.top - pad.bottom;
    const xPosition = (value) => {
      const fraction = (value - xMin) / Math.max(xMax - xMin, Number.EPSILON);
      return pad.left + (series.reverse_x ? 1 - fraction : fraction) * chartWidth;
    };
    const yPosition = (value) => pad.top + (1 - (value - yMin) / Math.max(yMax - yMin, Number.EPSILON)) * chartHeight;

    context.strokeStyle = grid;
    context.lineWidth = 1;
    context.font = "11px system-ui";
    context.fillStyle = text;
    for (let index = 0; index <= 4; index += 1) {
      const yy = pad.top + index * chartHeight / 4;
      const value = yMax - index * (yMax - yMin) / 4;
      context.beginPath(); context.moveTo(pad.left, yy); context.lineTo(width - pad.right, yy); context.stroke();
      context.fillText(value.toFixed(value >= 10 ? 1 : 3), 6, yy + 4);
    }
    const leftValue = series.reverse_x ? xMax : xMin;
    const rightValue = series.reverse_x ? xMin : xMax;
    context.fillText(leftValue.toFixed(1), pad.left, height - 12);
    context.textAlign = "right"; context.fillText(rightValue.toFixed(1), width - pad.right, height - 12); context.textAlign = "left";

    const gradient = context.createLinearGradient(pad.left, 0, width - pad.right, 0);
    gradient.addColorStop(0, lineA); gradient.addColorStop(1, lineB);
    context.strokeStyle = gradient;
    context.lineWidth = 2.4;
    context.beginPath();
    for (let index = 0; index < points; index += 1) {
      if (!finite(x[index]) || !finite(y[index])) continue;
      const px = xPosition(x[index]);
      const py = yPosition(y[index]);
      index ? context.lineTo(px, py) : context.moveTo(px, py);
    }
    context.stroke();

    context.strokeStyle = dark ? "rgba(245,185,66,.55)" : "rgba(216,137,29,.62)";
    context.fillStyle = dark ? "#d8a947" : "#a76b16";
    context.font = "10px system-ui";
    (series.peaks || []).filter((peak) => finite(peak.center)).slice(0, 8).forEach((peak, index) => {
      const px = xPosition(Number(peak.center));
      context.beginPath(); context.moveTo(px, pad.top); context.lineTo(px, height - pad.bottom); context.stroke();
      if (index < 5) context.fillText(String(peak.group || "peak"), Math.min(px + 4, width - 75), pad.top + 12 + (index % 2) * 13);
    });
  }

  window.ChemWorldSpectra = { mount };
})();
