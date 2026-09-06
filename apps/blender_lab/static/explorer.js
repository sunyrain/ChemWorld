import * as THREE from "three";
import { OrbitControls } from "./vendor/controls/OrbitControls.js";
import { GLTFLoader } from "./vendor/loaders/GLTFLoader.js";

const $ = (id) => document.getElementById(id);
const esc = (s) =>
  String(s ?? "").replace(
    /[&<>"']/g,
    (c) =>
      ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[
        c
      ],
  );
const labels = {
  add_solvent: "加入溶剂",
  add_reagent: "加入反应物",
  add_catalyst: "加入催化剂",
  heat: "加热与搅拌",
  sample: "取样",
  measure: "仪器测量",
  terminate: "终止反应",
  start: "启动",
  stop: "停止",
  inspect: "检查",
  quench: "淬灭",
  navigate: "导航",
  pick: "抓取",
  place: "放置",
  home: "归位",
  estop: "虚拟急停",
  reset_estop: "复位",
  set_visible: "显示",
  select: "选择",
  move: "移动",
  weigh: "称量",
  tare: "去皮",
  dispense: "分装",
};
const titleOf = (f) =>
  f?.instrument === "final_assay"
    ? "终点检测"
    : f?.instrument === "uvvis"
      ? "UV–Vis 测量"
      : labels[f?.operation] || f?.operation || "实验开始";
const state = {
  mode: "recorded",
  index: 0,
  frames: [],
  demo: null,
  assets: [],
  evidence: null,
  study: "m3",
  timer: null,
  selected: "reactor_01",
  liveFrames: [],
  transport: null,
};
let renderer,
  camera,
  controls,
  scene,
  lab,
  dirty = true;
const roots = new Map();
const selectedBox = new THREE.Box3Helper(new THREE.Box3(), 0x267f78);
selectedBox.visible = false;

async function api(path, data) {
  const response = await fetch(path, {
    method: data === undefined ? "GET" : "POST",
    headers: data === undefined ? {} : { "Content-Type": "application/json" },
    body: data === undefined ? undefined : JSON.stringify(data),
  });
  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.error || `HTTP ${response.status}`);
  }
  return response.json();
}
function notice(message) {
  $("notice").textContent = message;
  $("notice").hidden = false;
  clearTimeout(notice.timer);
  notice.timer = setTimeout(() => ($("notice").hidden = true), 7000);
}
function save(blob, name) {
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = name;
  a.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}
function showPage(page) {
  $("lab-page").hidden = page !== "lab";
  $("evidence-page").hidden = page !== "evidence";
  document
    .querySelectorAll("[data-page]")
    .forEach((b) => b.classList.toggle("active", b.dataset.page === page));
  if (page === "evidence") {
    pause();
    drawEvidence();
  } else {
    resize();
    dirty = true;
  }
}
document
  .querySelectorAll("[data-page]")
  .forEach((b) => (b.onclick = () => showPage(b.dataset.page)));
$("open-evidence").onclick = () => showPage("evidence");

function setView(view) {
  if (!camera) return;
  const views = {
    overview: [
      [9, 8.5, 10.5],
      [0, 0.8, 0],
    ],
    reaction: [
      [-0.5, 4.8, 4],
      [-2.8, 1.3, -1.7],
    ],
    analysis: [
      [4, 4.5, 2],
      [1, 1.1, -2.3],
    ],
    preparation: [
      [4, 4.4, 5],
      [0.5, 0.9, 1],
    ],
    top: [
      [0, 14, 0.01],
      [0, 0, 0],
    ],
  };
  const [position, target] = views[view];
  camera.position.fromArray(position);
  controls.target.fromArray(target);
  controls.update();
  document
    .querySelectorAll("[data-view]")
    .forEach((b) => b.classList.toggle("active", b.dataset.view === view));
  dirty = true;
}
document
  .querySelectorAll("[data-view]")
  .forEach((b) => (b.onclick = () => setView(b.dataset.view)));
function resize() {
  if (!renderer) return;
  const { width, height } = $("viewport").getBoundingClientRect();
  if (!width || !height) return;
  renderer.setSize(width, height);
  camera.aspect = width / height;
  camera.updateProjectionMatrix();
  dirty = true;
}
async function setupScene() {
  try {
    renderer = new THREE.WebGLRenderer({
      antialias: true,
      alpha: true,
      preserveDrawingBuffer: true,
    });
    renderer.setPixelRatio(Math.min(devicePixelRatio, 1.5));
    renderer.outputColorSpace = THREE.SRGBColorSpace;
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.25;
    $("viewport").append(renderer.domElement);
    scene = new THREE.Scene();
    camera = new THREE.PerspectiveCamera(38, 1, 0.1, 100);
    controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.12;
    controls.minDistance = 2;
    controls.maxDistance = 25;
    controls.maxPolarAngle = Math.PI * 0.49;
    controls.addEventListener("change", () => (dirty = true));
    scene.add(new THREE.HemisphereLight(0xe6f3ff, 0x8d9b8c, 2.5));
    for (const [p, intensity] of [
      [[5, 9, 6], 3],
      [[-5, 5, -3], 1.4],
      [[2, 4, -6], 1],
    ]) {
      const light = new THREE.DirectionalLight(0xfffaf0, intensity);
      light.position.fromArray(p);
      scene.add(light);
    }
    const gltf = await new GLTFLoader().loadAsync(
      "/explorer/chemlab.glb",
      (e) => {
        if (e.total)
          $("loading").textContent =
            `载入实验室 · ${Math.round((e.loaded / e.total) * 100)}%`;
      },
    );
    lab = gltf.scene;
    scene.add(lab);
    scene.add(selectedBox);
    lab.traverse((o) => {
      const id = o.userData.lab_id;
      if (id && o.parent?.userData.lab_id !== id) roots.set(id, o);
      if (o.isMesh) {
        const mats = Array.isArray(o.material) ? o.material : [o.material];
        for (const m of mats) {
          m.metalness = Math.min(m.metalness || 0, 0.25);
          m.roughness = Math.max(m.roughness || 0, 0.38);
          if (m.transmission > 0) {
            m.transmission = 0;
            m.transparent = true;
            m.opacity = 0.2;
            m.depthWrite = false;
          }
        }
      }
    });
    $("scene-count").textContent = `${roots.size} 个场景资产`;
    $("loading").hidden = true;
    setView("overview");
    resize();
    selectAsset(state.selected, false);
    let down = null;
    renderer.domElement.addEventListener(
      "pointerdown",
      (e) => (down = [e.clientX, e.clientY]),
    );
    renderer.domElement.addEventListener("pointerup", (e) => {
      if (!down || Math.hypot(e.clientX - down[0], e.clientY - down[1]) > 5)
        return;
      const rect = renderer.domElement.getBoundingClientRect();
      const ray = new THREE.Raycaster();
      ray.setFromCamera(
        new THREE.Vector2(
          ((e.clientX - rect.left) / rect.width) * 2 - 1,
          (-(e.clientY - rect.top) / rect.height) * 2 + 1,
        ),
        camera,
      );
      const hit = ray
        .intersectObject(lab, true)
        .find((h) => h.object.userData.lab_id);
      if (hit) selectAsset(hit.object.userData.lab_id, false);
    });
    new ResizeObserver(resize).observe($("viewport"));
    function animate() {
      requestAnimationFrame(animate);
      if (document.hidden || $("lab-page").hidden) return;
      controls.update();
      if (dirty) {
        renderer.render(scene, camera);
        dirty = false;
      }
    }
    animate();
  } catch (error) {
    $("loading").textContent =
      "三维视图未能载入。仍可使用设备列表、轨迹与证据图表。";
    $("snapshot").disabled = true;
    notice(`场景载入失败：${error.message}`);
  }
}
function selectAsset(id, focus = false) {
  state.selected = id;
  const asset = state.assets.find((a) => a.id === id);
  if (!asset) return;
  $("asset-select").value = id;
  $("asset-name").textContent = asset.name;
  const mapped = ["uvvis_01", "ftir_01", "ph_01"].includes(id);
  $("asset-kind").textContent =
    `${asset.label} · ${mapped ? "已连接对应 Core 仪器的公开报告" : "场景设备；其演示读数与 Core 测量分别记录"}`;
  $("asset-capabilities").innerHTML = asset.actions
    .map((a) => `<span>${esc(labels[a] || a)}</span>`)
    .join("");
  const object = roots.get(id);
  if (object) {
    selectedBox.box.setFromObject(object);
    selectedBox.visible = true;
    if (focus) {
      const center = selectedBox.box.getCenter(new THREE.Vector3());
      controls.target.copy(center);
      camera.position.copy(center).add(new THREE.Vector3(3, 2.8, 4));
      controls.update();
    }
    dirty = true;
  }
}
$("asset-select").onchange = (e) => selectAsset(e.target.value, true);
$("snapshot").onclick = () => {
  if (renderer) {
    renderer.render(scene, camera);
    renderer.domElement.toBlob((b) => {
      if (b) save(b, "chemworld-laboratory.png");
    });
  }
};
function pause() {
  clearInterval(state.timer);
  state.timer = null;
  $("play").textContent = "▶";
  $("play").setAttribute("aria-label", "播放公开轨迹");
}
function setMode(mode) {
  pause();
  state.mode = mode;
  state.frames = mode === "recorded" ? state.demo.frames : state.liveFrames;
  state.index = mode === "recorded" ? 0 : Math.max(0, state.frames.length - 1);
  $("recorded").classList.toggle("active", mode === "recorded");
  $("live").classList.toggle("active", mode === "live");
  $("scene-mode").textContent =
    mode === "recorded" ? "公开轨迹回放" : "实时公开观测";
  $("source-description").textContent =
    mode === "recorded"
      ? "Core 开发示例 · 非论文样本"
      : "当前会话 · 仅显示已收到的公开帧";
  $("workflow-description").textContent =
    mode === "recorded"
      ? "固定八步示例 · 公开观测回放"
      : "随公开帧更新 · 可回看已收到的步骤";
  renderFrame();
}
$("recorded").onclick = () => setMode("recorded");
$("live").onclick = () => setMode("live");
function seek(index) {
  state.index = Math.max(0, Math.min(index, state.frames.length - 1));
  renderFrame();
}
$("play").onclick = () => {
  if (state.timer) {
    pause();
    return;
  }
  if (!state.frames.length) return;
  if (state.index === state.frames.length - 1) seek(0);
  $("play").textContent = "Ⅱ";
  $("play").setAttribute("aria-label", "暂停公开轨迹");
  state.timer = setInterval(() => {
    seek(state.index + 1);
    if (state.index === state.frames.length - 1) pause();
  }, 1800);
};
$("scrubber").oninput = (e) => {
  pause();
  seek(Number(e.target.value));
};
$("previous").onclick = () => {
  pause();
  seek(state.index - 1);
};
$("next").onclick = () => {
  pause();
  seek(state.index + 1);
};
function renderFrame() {
  const frame = state.frames[state.index];
  $("scrubber").max = Math.max(0, state.frames.length - 1);
  $("scrubber").value = state.index;
  $("step-position").textContent = frame
    ? `${state.index} / ${state.frames.length - 1}`
    : "0 / 0";
  $("step-title").textContent = frame ? titleOf(frame) : "等待 Core 会话";
  $("workflow-title").textContent =
    state.mode === "recorded"
      ? "从配液到终检"
      : frame?.task_id || "等待实时实验";
  $("steps").innerHTML = state.frames
    .slice(1)
    .map(
      (f, i) =>
        `<li><button data-step="${i + 1}" class="${state.index === i + 1 ? "active" : ""}"><span class="step-number ${i + 1 < state.index ? "step-done" : ""}">${i + 1 < state.index ? "✓" : i + 1}</span>${esc(titleOf(f))}</button></li>`,
    )
    .join("");
  $("steps")
    .querySelectorAll("button")
    .forEach(
      (b) =>
        (b.onclick = () => {
          pause();
          seek(Number(b.dataset.step));
        }),
    );
  if (!state.frames.length)
    $("steps").innerHTML =
      '<li class="small muted">连接带 BlenderObserver 的 Core 会话后，实验步骤会出现在这里。</li>';
  const metrics = [
    ["yield", "产率"],
    ["conversion", "转化率"],
    ["selectivity", "选择性"],
    ["purity", "纯度"],
  ];
  $("measurements").innerHTML = metrics
    .map(([key, label]) => {
      const value = frame?.observations[key];
      const known = typeof value === "number" && frame.observed_mask[key];
      return `<div class="measurement ${known ? "" : "unknown"}"><span>${label}</span><strong>${known ? (value * 100).toFixed(1) + "<small> %</small>" : "尚未测量"}</strong></div>`;
    })
    .join("");
  const budget = frame?.campaign;
  $("budget-label").textContent = budget
    ? `${budget.remaining_budget} / ${budget.budget}`
    : "—";
  $("budget-meter").style.width = budget
    ? `${100 * Math.max(0, Math.min(1, budget.remaining_budget / budget.budget))}%`
    : "0";
  $("report-text").textContent = frame?.report_text || "没有公开报告。";
  $("previous").disabled = !frame || state.index === 0;
  $("next").disabled = !frame || state.index === state.frames.length - 1;
  $("play").disabled = state.frames.length < 2;
  if (frame?.asset_id) selectAsset(frame.asset_id, false);
}
async function poll() {
  try {
    const [health, environment, timeline] = await Promise.all([
      api("/health"),
      api("/api/v1/environment/state"),
      api("/api/v1/chemworld/timeline"),
    ]);
    $("connection").textContent = health.bridge?.connected
      ? "本地服务在线 · Blender 已连接"
      : "本地服务在线 · 网页三维视图";
    const following = state.index >= state.liveFrames.length - 1;
    state.liveFrames = timeline.frames;
    if (state.mode === "live") {
      state.frames = state.liveFrames;
      if (following) state.index = Math.max(0, state.frames.length - 1);
      renderFrame();
      $("scene-mode").textContent = timeline.active_session_id
        ? "实时公开观测"
        : timeline.frames.length
          ? "最近会话回看"
          : "等待公开会话";
      $("source-description").textContent = timeline.active_session_id
        ? "当前会话 · 仅显示已收到的公开帧"
        : "会话未运行 · 保留最近公开记录";
    }
    const poses = environment.simulation.poses || {};
    for (const id of ["robot_01", "sample_tube_01"]) {
      const root = roots.get(id),
        pos = poses[id];
      if (root && pos) {
        root.position.set(pos[0], pos[2], -pos[1]);
        if (id === "robot_01")
          root.rotation.y =
            ((environment.robot.base_yaw_deg || 0) * Math.PI) / 180;
      }
    }
    updateArm(environment.robot, poses.robot_01);
    if (roots.has(state.selected))
      selectedBox.box.setFromObject(roots.get(state.selected));
    dirty = true;
    const task = state.transport
      ? environment.tasks.find((t) => t.id === state.transport)
      : environment.tasks.at(-1);
    const running =
      task && ["running", "pending", "queued"].includes(task.status);
    $("transport").disabled =
      Boolean(running) || Boolean(environment.robot.estopped);
    state.robotEstopped = environment.robot.estopped;
    $("estop").textContent = state.robotEstopped ? "复位" : "停止";
    const states = {
      succeeded: "已完成",
      running: "运行中",
      pending: "等待中",
      failed: "失败",
      interrupted: "已中断",
      cancelled: "已取消",
    };
    $("transport-status").textContent = environment.robot.estopped
      ? "虚拟急停已生效"
      : task
        ? `搬运${states[task.status] || task.status} · ${task.step_index ?? 0} / ${task.steps?.length || 5}`
        : "机器人待命";
  } catch (error) {
    $("connection").textContent = "本地连接中断 · 显示最后收到的状态";
  }
}
$("transport").onclick = async () => {
  try {
    $("transport").disabled = true;
    const task = await api("/api/v1/environment/demo/transport", {});
    state.transport = task.id;
    selectAsset("robot_01", true);
    await poll();
  } catch (error) {
    notice(`搬运未启动：${error.message}`);
    $("transport").disabled = false;
  }
};
$("estop").onclick = async () => {
  try {
    const resetting = state.robotEstopped;
    await api("/api/v1/assets/robot_01/actions", {
      action: resetting ? "reset_estop" : "estop",
    });
    await poll();
    notice(
      resetting
        ? "虚拟急停已复位；原任务保持中断，需显式提交新任务。"
        : "场景机器人已停止，可点击“复位”解除虚拟急停。",
    );
  } catch (error) {
    notice(error.message);
  }
};

function updateArm(robot, pose) {
  const root = roots.get("robot_01");
  if (!root || !pose) return;
  const yaw = (robot.base_yaw_deg * Math.PI) / 180,
    t = robot.arm_extension;
  const home = [
    pose[0] - 0.16 * Math.sin(yaw),
    pose[1] + 0.16 * Math.cos(yaw),
    pose[2] + 0.86,
  ];
  const delta = home.map(
    (v, i) => v * (1 - t) + robot.arm_target_m[i] * t - pose[i],
  );
  const wrist = new THREE.Vector3(
    Math.cos(yaw) * delta[0] + Math.sin(yaw) * delta[1],
    delta[2],
    Math.sin(yaw) * delta[0] - Math.cos(yaw) * delta[1],
  );
  const shoulder = new THREE.Vector3(0, 0.84, -0.08),
    direction = wrist.clone().sub(shoulder);
  const length = Math.min(0.859, Math.max(0.02, direction.length()));
  direction.normalize();
  const bend = new THREE.Vector3(0, 1, 0).addScaledVector(
    direction,
    -direction.y,
  );
  if (bend.length() < 0.001) bend.set(0, 0, -1);
  bend.normalize();
  const elbow = shoulder
    .clone()
    .add(wrist)
    .multiplyScalar(0.5)
    .addScaledVector(
      bend,
      Math.sqrt(Math.max(0, 0.43 ** 2 - (length / 2) ** 2)),
    );
  for (const object of root.children) {
    const role = object.userData.component;
    if (
      ["upper_arm", "upper_arm_stripe", "forearm", "forearm_stripe"].includes(
        role,
      )
    ) {
      const a = role.startsWith("upper") ? shoulder : elbow,
        b = role.startsWith("upper") ? elbow : wrist;
      object.position.copy(a).add(b).multiplyScalar(0.5);
      object.quaternion.setFromUnitVectors(
        new THREE.Vector3(0, 1, 0),
        b.clone().sub(a).normalize(),
      );
      object.scale.y = a.distanceTo(b);
    } else if (role === "shoulder_joint") object.position.copy(shoulder);
    else if (role === "elbow_joint") object.position.copy(elbow);
    else if (
      ["wrist_joint", "tool_coupler", "gripper_body", "gripper_jaw"].includes(
        role,
      )
    ) {
      object.position.copy(wrist);
      object.position.y += {
        wrist_joint: 0.085,
        tool_coupler: 0.055,
        gripper_body: 0.025,
        gripper_jaw: -0.035,
      }[role];
      if (role === "gripper_jaw")
        object.position.x +=
          object.userData.jaw_side * (robot.gripper_open ? 0.055 : 0.035);
    }
  }
}

const stories = {
  f1: {
    kicker: "F1 / SELECTIVE CORRECTION",
    title: "实验进步，是否伴随针对性的纠错？",
    description:
      "我们改变提供给 Agent 的初始说明，再观察它如何实验和修正预测。两配置的预测误差平均下降，但预设选择性纠错标准均未通过。",
    counts: [
      ["135 × 2", "计划实验任务"],
      ["45", "每配置 task–world 簇"],
      ["121 / 126", "DeepSeek / GPT 操作完成"],
    ],
    boundary:
      "纠错对比受初始误差余量影响。搜索进步和未通过纠错标准都不能单独识别反馈学习能力；额外回答轮次与证据包的效果尚未隔离。",
  },
  f2: {
    kicker: "F2 / STRUCTURAL IDENTIFICATION",
    title: "预测改善之后，结构仍需要单独验证。",
    description:
      "最小提交接口下，未知或错误先验条件没有恢复正确的函数族与指数。所有成功来自已提供正确规律的条件，属于知识保持。",
    counts: [
      ["120", "计划会话"],
      ["117 / 3", "有效完成 / 保留失败"],
      ["5", "复用世界"],
    ],
    boundary:
      "仅5个世界。工具对比估计可用性，GPT未主动调用工具；区间跨零不证明等价。公开合同缺少完整观测映射，同信息结构可识别性尚未建立。",
  },
  f3: {
    kicker: "F3 / EXECUTABLE KNOWLEDGE",
    title: "把预测写成规律，会丢失多少信息？",
    description:
      "对同一组查询，分别评价 Agent 的直接数值预测和它提交的可执行规律，测量表示转换带来的误差变化。",
    counts: [
      ["135 / 129", "DeepSeek / GPT 可评价规律"],
      ["0.0686", "DeepSeek 压缩损失"],
      ["0.0142", "GPT 压缩损失"],
    ],
    boundary:
      "DeepSeek同域容量控制覆盖135/135个预测状态，说明该合法表示能够容纳已有预测；不证明新条件下的结构恢复，亦不构成两模型相同覆盖的控制。",
  },
  f4: {
    kicker: "F4 / KNOWLEDGE AND ACTION",
    title: "提交的规律，能代表实际决策吗？",
    description:
      "在原 DeepSeek 未见方案队列中，规律隐含的最优选择与 Agent 的实际选择明显不同。显式知识是行为的不完整代理。",
    counts: [
      ["45", "计划单元 · DeepSeek"],
      ["0 / 45", "规律选择最优"],
      ["11 / 45", "Agent 选择最优"],
    ],
    boundary:
      "原纵向直接证据为DeepSeek-only，42个单元有可评价排名，其中12个跟随规律。该关联不识别内部信念、规律使用或因果中介，且缺少同协议无证据行动控制。",
  },
  m1: {
    kicker: "M1 / AGREEMENT UNDER FIXED EVIDENCE",
    title: "在固定信息下，规律与行动可以一致。",
    description:
      "交叉替换模型规律 / 数值拟合规律，以及 Agent / 确定性求最优，检查规律来源与决策方式对选择的影响。",
    counts: [
      ["10", "独立世界"],
      ["120 / 120", "完成会话"],
      ["40 / 40", "拟合规律下选择一致"],
    ],
    boundary:
      "拟合规律未达到预设实质收益标准。与历史协议同时改变了多个因素，不能把差异归因于某一个接口变化。原始证据与规律同时交付。",
  },
  m3: {
    kicker: "M3 / INDEPENDENT KNOWLEDGE UTILITY",
    title: "知识离开来源对话，仍然有用。",
    description:
      "全新接收者分别获得任务信息、原始证据、模型规律或拟合规律，再选择同世界的新候选方案。模型规律单独交付带来了明确决策收益。",
    counts: [
      ["10", "复用世界 · 新增 0"],
      ["160 / 160", "完成接收会话"],
      ["0", "失败 / 替换"],
    ],
    boundary:
      "最近邻证据检索在10/10世界达到最优；规律相对原始证据的差异区间跨零。这里只验证同世界新候选的上下文可携带性，未验证新机制迁移或实验节省。",
  },
};
document.querySelectorAll("[data-evidence]").forEach(
  (b) =>
    (b.onclick = () => {
      state.study = b.dataset.evidence;
      drawEvidence();
    }),
);
$("model-filter").onchange = drawEvidence;
$("download-data").onclick = () => {
  if (state.evidence)
    save(
      new Blob([JSON.stringify(state.evidence, null, 2)], {
        type: "application/json",
      }),
      "chemworld-evidence.json",
    );
};
$("download-chart").onclick = () => {
  const chart = $("evidence-chart").querySelector("svg");
  if (!chart) return;
  const clone = chart.cloneNode(true);
  const style = document.createElementNS("http://www.w3.org/2000/svg", "style");
  style.textContent =
    "text{font-family:Segoe UI,Microsoft YaHei,sans-serif;font-size:12px;fill:#697a84}";
  clone.prepend(style);
  save(
    new Blob([new XMLSerializer().serializeToString(clone)], {
      type: "image/svg+xml",
    }),
    `chemworld-${state.study}-${$("model-filter").value}.svg`,
  );
};
function svg(body, height = 300) {
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 ${height}" role="img" aria-label="${esc(stories[state.study].title)}"><title>${esc(stories[state.study].title)}</title><desc>${esc(stories[state.study].description + " " + stories[state.study].boundary + " 配置筛选：" + $("model-filter").selectedOptions[0].textContent + "；右侧配对区间始终为总体。")}</desc>${body}</svg>`;
}
function table(headers, rows) {
  return `<table><thead><tr>${headers.map((h) => `<th>${esc(h)}</th>`).join("")}</tr></thead><tbody>${rows.map((r) => `<tr>${r.map((v) => `<td>${esc(v)}</td>`).join("")}</tr>`).join("")}</tbody></table>`;
}
function drawEvidence() {
  const key = state.study,
    story = stories[key],
    data = state.evidence,
    model = $("model-filter").value;
  document.querySelectorAll("[data-evidence]").forEach((b) => {
    b.classList.toggle("active", b.dataset.evidence === key);
    b.setAttribute(
      "aria-selected",
      b.dataset.evidence === key ? "true" : "false",
    );
  });
  $("evidence-kicker").textContent = story.kicker;
  $("evidence-title").textContent = story.title;
  $("evidence-description").textContent = story.description;
  $("evidence-counts").innerHTML = story.counts
    .map(([n, label]) => `<div><strong>${n}</strong>${label}</div>`)
    .join("");
  $("evidence-boundary").textContent = story.boundary;
  $("model-filter").disabled = !["m1", "m3", "f2"].includes(key);
  $("chart-note").textContent = "";
  $("evidence-table").innerHTML = "";
  $("download-chart").disabled = !["m1", "m3", "f2"].includes(key);
  if (["m1", "m3", "f2"].includes(key) && !data) {
    $("evidence-chart").textContent = "论文汇总数据暂不可用。";
    return;
  }
  if (key === "m1" || key === "m3") {
    const block = data[key],
      conditions =
        key === "m3" ? ["none", "raw", "L", "F"] : ["L-A", "L-X", "F-A", "F-X"];
    const names =
      key === "m3"
        ? ["仅任务信息", "原始证据", "模型规律", "拟合规律"]
        : [
            "模型规律 · Agent",
            "模型规律 · 求最优",
            "拟合规律 · Agent",
            "拟合规律 · 求最优",
          ];
    const rows = conditions.map((condition, i) => {
      const selected = block.conditions.filter(
        (r) =>
          r.condition === condition && (model === "all" || r.model === model),
      );
      return {
        label: names[i],
        mean:
          selected.reduce((s, r) => s + r.mean_failure_aware_regret, 0) /
          selected.length,
        n: selected.reduce((s, r) => s + r.scheduled, 0),
        completed: selected.reduce((s, r) => s + r.completed, 0),
      };
    });
    const max = key === "m3" ? 0.2 : 0.025,
      x = (v) => 190 + (v / max) * 365;
    let body = "";
    for (let i = 0; i <= 4; i++) {
      const v = (max * i) / 4;
      body += `<line x1="${x(v)}" y1="27" x2="${x(v)}" y2="218" stroke="#e6ece9"/><text x="${x(v)}" y="244" text-anchor="middle">${v.toFixed(key === "m3" ? 2 : 3)}</text>`;
    }
    rows.forEach((r, i) => {
      const y = 47 + i * 47;
      body += `<text x="172" y="${y + 4}" text-anchor="end">${r.label}</text><line x1="${x(0)}" x2="${x(r.mean)}" y1="${y}" y2="${y}" stroke="${i === 2 ? "#187374" : "#7496ad"}" stroke-width="3"/><circle cx="${x(r.mean)}" cy="${y}" r="5" fill="${i === 2 ? "#187374" : "#7496ad"}"/><text x="${x(r.mean) + 11}" y="${y + 4}">${r.mean.toFixed(5)}</text>`;
    });
    body +=
      '<text x="345" y="277" text-anchor="middle">平均 regret · 越低越好</text>';
    const p = block.primary,
      wx = (v) => 800 + (v / (key === "m3" ? 0.4 : 0.065)) * 150;
    body +=
      '<text x="790" y="16" text-anchor="middle">逐世界配对效应 · 两模型等权</text>';
    body += `<line x1="${wx(0)}" y1="25" x2="${wx(0)}" y2="250" stroke="#a2b3b6" stroke-dasharray="4 4"/>`;
    block.world_effects.forEach((r, i) => {
      const y = 38 + i * 18;
      body += `<text x="625" y="${y + 4}">${r.world}</text><line x1="${wx(0)}" y1="${y}" x2="${wx(r.difference)}" y2="${y}" stroke="#d6e1dd"/><circle cx="${wx(r.difference)}" cy="${y}" r="4" fill="${r.task.startsWith("electro") ? "#187374" : "#bc8a4f"}"><title>${r.world}: ${r.difference.toFixed(6)}</title></circle>`;
    });
    const ticks = key === "m3" ? [-0.4, -0.2, 0, 0.2] : [-0.06, -0.03, 0, 0.03];
    body += ticks
      .map(
        (v) =>
          `<line x1="${wx(v)}" y1="257" x2="${wx(v)}" y2="262" stroke="#a2b3b6"/><text x="${wx(v)}" y="279" text-anchor="middle">${v.toFixed(2)}</text>`,
      )
      .join("");
    body += `<line x1="${wx(p.interval[0])}" y1="242" x2="${wx(p.interval[1])}" y2="242" stroke="#182c38" stroke-width="3"/><circle cx="${wx(p.mean_difference)}" cy="242" r="5" fill="#182c38"/><text x="790" y="308" text-anchor="middle">总体差 ${p.mean_difference.toFixed(5)} · 95% 区间</text><text x="790" y="330" text-anchor="middle">[${p.interval[0].toFixed(5)}, ${p.interval[1].toFixed(5)}]</text>`;
    $("evidence-chart").innerHTML =
      svg(body, 345) +
      `<div class="legend"><span><i style="background:#187374"></i>电化学世界</span><span><i style="background:#bc8a4f"></i>结晶世界</span><span>${key === "m3" ? "模型规律 − 仅任务信息；最近邻 regret = 0" : "拟合规律求最优 − 模型规律求最优"}</span></div>`;
    $("chart-note").textContent = "左图可切模型；右图始终为注册总体配对效应。";
    $("evidence-table").innerHTML = table(
      ["条件", "平均 regret", "完成 / 计划"],
      rows.map((r) => [r.label, r.mean.toFixed(8), `${r.completed} / ${r.n}`]),
    );
  } else if (key === "f2") {
    const priors = [
      ["opaque", "未知先验"],
      ["misindexed_nominal", "错误先验"],
      ["aligned_nominal", "正确先验"],
    ];
    const rows = priors.map(([arm, label]) => {
      const a = data.diagnostic.by_prior.filter(
        (r) => r.arm === arm && (model === "all" || r.model === model),
      );
      return {
        label,
        n: a.reduce((s, r) => s + r.scheduled, 0),
        done: a.reduce((s, r) => s + r.completed, 0),
        success: a.reduce((s, r) => s + r.joint_recovery, 0),
      };
    });
    let body = "";
    rows.forEach((r, i) => {
      const y = 45 + i * 66,
        x = 200,
        w = 550;
      body += `<text x="180" y="${y + 19}" text-anchor="end">${r.label}</text><rect x="${x}" y="${y}" width="${w}" height="29" fill="#e6edeb" rx="3"/><rect x="${x}" y="${y}" width="${(w * r.success) / r.n}" height="29" fill="#187374"/><rect x="${x + (w * r.done) / r.n}" y="${y}" width="${(w * (r.n - r.done)) / r.n}" height="29" fill="#bd8c50"/><text x="775" y="${y + 19}">${r.success} / ${r.n} ${i === 2 ? "知识保持" : "结构恢复"}</text>`;
    });
    $("evidence-chart").innerHTML =
      svg(body, 255) +
      '<div class="legend"><span><i style="background:#187374"></i>联合正确</span><span><i style="background:#e6edeb"></i>有效但未联合正确</span><span><i style="background:#bd8c50"></i>失败，保留分母</span></div>';
    $("chart-note").textContent =
      "函数族正确且指数误差 ≤ 0.10；所有工具条件合并展示。";
    $("evidence-table").innerHTML = table(
      ["初始描述", "联合正确", "有效 / 计划", "失败"],
      rows.map((r) => [r.label, r.success, `${r.done} / ${r.n}`, r.n - r.done]),
    );
  } else {
    const cards = {
      f1: [
        ["持续实验", "观察搜索过程与终点改善。"],
        ["预测更新", "分别记录实验前后的查询预测。"],
        ["选择性纠错", "比较错误先验与对照条件的改善，保留初始误差余量影响。"],
      ],
      f3: [
        ["逐点预测", "对固定查询记录直接数值答案。"],
        ["可执行表达", "把总结的规律放入相同评价器执行。"],
        ["压缩损失", "测量规律相对原预测的保真损失，同域容量单独检查。"],
      ],
      f4: [
        ["提交的规律", "从可执行规律推导候选选择。"],
        ["实际行动", "独立记录 Agent 对未见方案的选择。"],
        ["比较两者", "规律与行为不一致，不等于已观测到内部信念或因果机制。"],
      ],
    }[key];
    $("evidence-chart").innerHTML =
      `<div class="question-flow">${cards.map(([title, text], i) => `<div><p class="eyebrow">${String(i + 1).padStart(2, "0")}</p><strong>${title}</strong><p>${text}</p></div>`).join("")}</div>`;
    $("evidence-table").innerHTML = table(
      ["读出", "当前值"],
      story.counts.map(([v, k]) => [k, v]),
    );
  }
}

try {
  const [assets, demo, evidence] = await Promise.all([
    api("/api/v1/assets"),
    api("/explorer/demo.json"),
    api("/api/v1/explorer/evidence").catch((error) => {
      notice(`论文汇总暂不可用：${error.message}`);
      return null;
    }),
  ]);
  state.assets = assets.assets;
  state.demo = demo;
  state.evidence = evidence;
  $("asset-select").innerHTML =
    '<option value="">浏览全部设备</option>' +
    state.assets
      .map((a) => `<option value="${esc(a.id)}">${esc(a.name)}</option>`)
      .join("");
  setMode("recorded");
  selectAsset("reactor_01");
  setupScene();
  await poll();
  setInterval(poll, 2500);
} catch (error) {
  notice(`初始化失败：${error.message}`);
  $("loading").textContent = "本地数据无法载入，请检查服务连接。";
}
