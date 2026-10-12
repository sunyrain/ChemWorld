"use strict";
const designs = [
  {
    "id": "01",
    "name": "白色仪器台",
    "focus": "日常实验与实时观察",
    "file": "01-instrument-console.png"
  },
  {
    "id": "02",
    "name": "暗色运行观测站",
    "focus": "长程 Agent 运行监控",
    "file": "02-live-observatory.png"
  },
  {
    "id": "03",
    "name": "研究记录本",
    "focus": "假设、证据与版本化记录",
    "file": "03-research-notebook.png"
  },
  {
    "id": "04",
    "name": "实验编排画布",
    "focus": "组件组合与样品流转",
    "file": "04-experiment-canvas.png"
  },
  {
    "id": "05",
    "name": "空间实验室",
    "focus": "空间理解与设备观察",
    "file": "05-spatial-laboratory.png"
  },
  {
    "id": "06",
    "name": "模型对照台",
    "focus": "相同条件下比较过程与成本",
    "file": "06-matched-comparison.png"
  },
  {
    "id": "07",
    "name": "谱图分析室",
    "focus": "仪器信号与测量历史",
    "file": "07-spectrum-studio.png"
  },
  {
    "id": "08",
    "name": "研究演化图",
    "focus": "长程研究轨迹与假设修订",
    "file": "08-research-map.png"
  },
  {
    "id": "09",
    "name": "实验启动台",
    "focus": "建实验、接模型与临时密钥",
    "file": "09-experiment-launchpad.png"
  },
  {
    "id": "10",
    "name": "开放研究展厅",
    "focus": "社区入口、成果展示与可复现浏览",
    "file": "10-research-showcase.png"
  }
];
const viewer = document.getElementById("viewer");
let selected = 0;
function display(index) {
  selected = (index + designs.length) % designs.length;
  const design = designs[selected];
  document.getElementById("viewer-title").textContent = design.id + " · " + design.name + " — " + design.focus;
  const image = document.getElementById("viewer-image");
  image.src = design.file;
  image.alt = design.name + "：" + design.focus;
  document.getElementById("original").href = design.file;
  if (!viewer.open) { viewer.showModal(); document.body.classList.add("viewing"); }
}
document.querySelectorAll(".preview").forEach(button => button.addEventListener("click", () => display(Number(button.dataset.index))));
document.getElementById("previous").addEventListener("click", () => display(selected - 1));
document.getElementById("next").addEventListener("click", () => display(selected + 1));
document.getElementById("close").addEventListener("click", () => viewer.close());
viewer.addEventListener("close", () => document.body.classList.remove("viewing"));
viewer.addEventListener("keydown", event => {
  if (event.key === "ArrowLeft") { event.preventDefault(); display(selected - 1); }
  if (event.key === "ArrowRight") { event.preventDefault(); display(selected + 1); }
});
