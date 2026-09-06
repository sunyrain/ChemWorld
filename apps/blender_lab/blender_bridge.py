"""Blender main-thread adapter and native sidebar for the ChemLab REST API."""

import contextlib
import json
import math
import os
import subprocess
import time
import urllib.request
from pathlib import Path

import bpy
from bpy.props import BoolProperty, EnumProperty, FloatProperty, StringProperty

from .catalog import API_PORT, ASSETS, CATALOG

ROOT = Path(__file__).resolve().parent

BASE = os.environ.get("CHEMLAB_API_URL", f"http://127.0.0.1:{API_PORT}")
CACHE = {}
CONNECTED = False
LAST_ERROR = ""
LAST_FETCH = 0
LAST_ACK = 0
LAST_SELECTED = None
LAST_SAVE = 0
COMPONENTS = {}
LOGGED_ERROR = None
ENV_CACHE = {}
WORLD_CACHE = {}


def request(path, data=None, method=None, timeout=0.35):
    body = None if data is None else json.dumps(data).encode("utf-8")
    req = urllib.request.Request(
        BASE + path,
        data=body,
        method=method or ("GET" if body is None else "POST"),
        headers={"Content-Type": "application/json"},
    )
    # A local-only connection must not be sent through a system proxy.
    with urllib.request.build_opener(urllib.request.ProxyHandler({})).open(
        req, timeout=timeout
    ) as r:
        return json.load(r)


def start_service():
    try:
        data = request("/health")
        if data.get("integration") != "chemworld-blender-1":
            raise RuntimeError("Selected API port belongs to another service")
        return
    except (OSError, urllib.error.URLError):
        pass
    from urllib.parse import urlsplit

    repository = ROOT.parents[1]
    python = os.environ.get("CHEMWORLD_PYTHON")
    if not python:
        python = str(
            repository / ".venv" / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
        )
    if not Path(python).is_file():
        raise RuntimeError(
            "Run uv sync --extra dev, then uv run --no-sync python -m apps.blender_lab"
        )
    port = urlsplit(BASE).port or API_PORT
    data_dir = ROOT / "runtime" / str(port)
    data_dir.mkdir(parents=True, exist_ok=True)
    with (data_dir / "server.log").open("ab") as log:
        subprocess.Popen(
            [
                python,
                "-m",
                "apps.blender_lab.server",
                "--port",
                str(port),
                "--data-dir",
                str(data_dir),
            ],
            cwd=repository,
            stdout=log,
            stderr=log,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
        )


def objects_for(id):
    return COMPONENTS.get(id, ())


def component(id, role):
    return next((o for o in objects_for(id) if o.get("component") == role), None)


def select_asset(id):
    root = bpy.data.objects.get(id)
    if not root:
        return
    for o in bpy.context.selected_objects:
        o.select_set(False)
    root.select_set(True)
    bpy.context.view_layer.objects.active = root
    for o in objects_for(id):
        if o.type == "MESH" and not o.hide_get():
            o.select_set(True)
    bpy.context.scene.chemlab_asset = id


def apply_snapshot(snapshot):
    global CACHE, LAST_SELECTED
    errors = []
    CACHE = snapshot
    for id, s in snapshot["states"].items():
        root = bpy.data.objects.get(id)
        if root is None:
            errors.append(id + ": missing root")
            continue
        a = CATALOG[id]
        root.location = snapshot["poses"][id]
        for k, v in s.items():
            if isinstance(v, (str, int, float, bool)):
                root[k] = v
        root["state_json"] = json.dumps(s, ensure_ascii=False)
        root["applied_revision"] = snapshot["revision"]
        is_visible = s["visible"]
        for o in objects_for(id):
            role = o.get("component", "")
            visible = is_visible
            if role == "liquid":
                fraction = (
                    (s["remaining"] / a["quantity"])
                    if a["kind"] == "reagent"
                    else s.get("volume_ml", 0) / a.get("capacity_ml", 1)
                )
                visible &= fraction > 1e-7
                if "max_height" in o:
                    base = o["base_z"]
                    height = o["max_height"] * max(0.001, fraction)
                    # Cylinder meshes retain their originally generated depth.
                    zs = [v.co.z for v in o.data.vertices]
                    original = max(zs) - min(zs)
                    o.scale.z = height / original
                    o.location.z = base + height / 2
                if a["kind"] != "reagent" and s.get("contents"):
                    volumes = [c["volume_ml"] for c in s["contents"]]
                    total = sum(volumes)
                    color = [
                        sum(
                            CATALOG[c["reagent_id"]]["color"][i] * v
                            for c, v in zip(s["contents"], volumes, strict=False)
                        )
                        / total
                        for i in range(3)
                    ]
                    mat = o.active_material
                    mat.diffuse_color = (*color, 1)
                    next(n for n in mat.node_tree.nodes if n.type == "BSDF_PRINCIPLED").inputs[
                        "Base Color"
                    ].default_value = (
                        *color,
                        1,
                    )
            if role == "cap" and a["kind"] == "reagent":
                o.location.z = o["base_location"][2] + (0.1 if s["cap_open"] else 0)
            if role in {"sash", "sash_handle"}:
                o.location.z = o["base_location"][2] + s.get("sash_open_pct", 35) / 100 * 0.57
            if role in {"door", "door_window", "door_handle"} and a["kind"] in {"cabinet", "oven"}:
                # A hinged door subassembly rotates about the left vertical edge.
                base = o["base_location"]
                angle = -math.radians(105) if s.get("door_open") else 0
                pivot_x = -a["size"][0] / 2
                pivot_y = -a["size"][1] / 2
                dx, dy = base[0] - pivot_x, base[1] - pivot_y
                o.location = (
                    pivot_x + math.cos(angle) * dx - math.sin(angle) * dy,
                    pivot_y + math.sin(angle) * dx + math.cos(angle) * dy,
                    base[2],
                )
                o.rotation_euler.z = angle
            if role in {"lid", "lid_window"} and a["kind"] == "centrifuge":
                o.location.z = o["base_location"][2] + (0.3 if s["lid_open"] else 0)
            if role.startswith("water_stream"):
                visible &= s.get("water_on", False)
            if role == "status_led":
                on = s.get("running", s.get("fan_on", s.get("status") == "ready"))
                color = (0.08, 0.85, 0.43, 1) if on else (0.08, 0.24, 0.3, 1)
                o.active_material.diffuse_color = color
                bs = next(
                    n for n in o.active_material.node_tree.nodes if n.type == "BSDF_PRINCIPLED"
                )
                bs.inputs["Base Color"].default_value = color
                bs.inputs["Emission Color"].default_value = color
            if role == "hot_surface":
                heat = max(0, min(1, (s["temperature_c"] - 25) / 175))
                col = (0.12 + 0.65 * heat, 0.18 - 0.11 * heat, 0.21 - 0.15 * heat, 1)
                o.active_material.diffuse_color = col
                next(
                    n for n in o.active_material.node_tree.nodes if n.type == "BSDF_PRINCIPLED"
                ).inputs["Base Color"].default_value = col
            if role == "display":
                if "temperature_c" in s:
                    val = f"{s['temperature_c']:.1f} C"
                    if "stir_rpm" in s:
                        val += f" / {s['stir_rpm'] if s['running'] else 0:.0f} rpm"
                elif a["kind"] == "waste":
                    val = f"{s['volume_ml'] / 1000:.2f} / 10 L"
                elif a["kind"] == "centrifuge":
                    val = f"{s['remaining_s']:.0f}s" if s["running"] else s["status"].upper()
                else:
                    val = s.get("reading", s["status"].upper())
                if o.data.body != val:
                    o.data.body = val
            if role == "amount" and a["kind"] == "reagent":
                o.data.body = f"{s['remaining']:.1f} {a['unit']}"
            o.hide_render = not visible
            if o.hide_get() == visible:
                o.hide_set(not visible)
        root.hide_set(not is_visible)
    if snapshot["selected"] != LAST_SELECTED:
        LAST_SELECTED = snapshot["selected"]
        select_asset(LAST_SELECTED)
    if "robot_01" in snapshot["states"]:
        from .robot_visual import apply_robot

        apply_robot(snapshot["states"]["robot_01"], snapshot["poses"]["robot_01"])
    if (
        getattr(bpy.context.scene, "chemlab_follow_robot", False)
        and "Camera_Robot" in bpy.data.objects
    ):
        from mathutils import Vector

        camera = bpy.data.objects["Camera_Robot"]
        p = Vector(snapshot["poses"]["robot_01"])
        camera.location = p + Vector((2.7, -3.5, 2.3))
        camera.rotation_euler = (
            (p + Vector((0, 0, 0.78)) - camera.location).to_track_quat("-Z", "Y").to_euler()
        )
    bpy.context.scene["applied_revision"] = snapshot["revision"]
    return errors


def timer():
    global LAST_FETCH, LAST_ACK, CONNECTED, LAST_ERROR, LOGGED_ERROR, ENV_CACHE, WORLD_CACHE
    if not bpy.context.scene.get("chemlab_version"):
        return 1
    now = time.monotonic()
    if now - LAST_FETCH >= 0.5:
        LAST_FETCH = now
        try:
            snapshot = request("/api/v1/state")
            errors = (
                apply_snapshot(snapshot) if snapshot["revision"] != CACHE.get("revision") else []
            )
            CONNECTED = True
            LAST_ERROR = ""
            if now - LAST_ACK > 1:
                LAST_ACK = now
                ENV_CACHE = request("/api/v1/environment/state")
                WORLD_CACHE = request("/api/v1/chemworld/frame")
                apply_world_frame(WORLD_CACHE)
                ack = {
                    "applied_revision": snapshot["revision"],
                    "object_count": len(COMPONENTS),
                    "file": bpy.data.filepath,
                    "errors": errors,
                }
                request("/api/v1/bridge", ack)
                # Local evidence includes actual observed Blender component state.
                evidence = dict(
                    **ack,
                    observed_at=time.time(),
                    selected=bpy.context.view_layer.objects.active.get("lab_id")
                    if bpy.context.view_layer.objects.active
                    else None,
                    assets={
                        id: {
                            "location": list(bpy.data.objects[id].location),
                            "hidden": bpy.data.objects[id].hide_get(),
                            "state": json.loads(bpy.data.objects[id]["state_json"]),
                            "components": {
                                o.name: {
                                    "role": o.get("component"),
                                    "location": list(o.location),
                                    "rotation": list(o.rotation_euler),
                                    "scale": list(o.scale),
                                    "hidden": o.hide_get(),
                                    "text": o.data.body if o.type == "FONT" else None,
                                }
                                for o in objects_for(id)
                            },
                        }
                        for id in COMPONENTS
                    },
                )
                (ROOT / "runtime" / "bridge_observed.tmp").write_text(
                    json.dumps(evidence, ensure_ascii=False), encoding="utf-8"
                )
                os.replace(
                    ROOT / "runtime" / "bridge_observed.tmp",
                    ROOT / "runtime" / "bridge_observed.json",
                )
        except Exception as e:
            CONNECTED = False
            LAST_ERROR = str(e)
            if LAST_ERROR != LOGGED_ERROR:
                print("ChemLab bridge:", LAST_ERROR)
                LOGGED_ERROR = LAST_ERROR
    dt = 0.1
    for id, s in CACHE.get("states", {}).items():
        a = CATALOG[id]
        if s.get("running"):
            rpm = s.get("stir_rpm", s.get("speed_rpm", 0))
            spin = min(rpm, 240) * math.tau / 60 * dt
            for o in objects_for(id):
                if o.get("component") in {"impeller", "stirbar", "rotor"}:
                    o.rotation_euler.z += spin
            if a.get("vessel"):
                obj = component(a["vessel"], "stirbar")
                if obj:
                    obj.rotation_euler.z += spin
    for screen in bpy.data.screens:
        for area in screen.areas:
            if area.type == "VIEW_3D":
                area.tag_redraw()
    return 0.1 if CONNECTED else 1


ASSET_ITEMS = [(a["id"], a["name"], a["id"]) for a in ASSETS]
SAMPLE_ITEMS = [(a["id"], a["name"], a["id"]) for a in ASSETS if a["kind"] in {"vessel", "reactor"}]
TARGET_ITEMS = [
    (a["id"], a["name"], a["id"]) for a in ASSETS if a["kind"] in {"vessel", "reactor", "waste"}
]


def asset_changed(scene, context):
    state = CACHE.get("states", {}).get(scene.chemlab_asset, {})
    for field, prop in [
        ("target_temperature_c", "chemlab_temperature"),
        ("stir_rpm", "chemlab_rpm"),
        ("speed_rpm", "chemlab_rpm"),
        ("duration_s", "chemlab_duration"),
        ("path_length_cm", "chemlab_path"),
        ("sash_open_pct", "chemlab_sash"),
    ]:
        if field in state:
            setattr(scene, prop, state[field])


class CHEMLAB_OT_command(bpy.types.Operator):
    bl_idname = "chemlab.command"
    bl_label = "执行操作"
    bl_description = "Operate the selected virtual instrument through its REST API"
    command: StringProperty()

    @classmethod
    def description(cls, context, properties):
        return {
            "tour_play": "从头播放 20 秒镜头导览，依次展示各实验区",
            "tour_pause": "暂停当前镜头动画",
            "tour_video": "使用本机播放器观看已导出的 MP4 视频",
            "demo": "启动实时加热、搅拌和测量，并切到反应装置近景",
        }.get(properties.command, "操作当前选择的虚拟设备")

    def execute(self, context):
        global LAST_ERROR
        scene = context.scene
        id = scene.chemlab_asset
        a = CATALOG[id]
        try:
            if self.command == "connect":
                start_service()
            elif self.command == "select":
                request(f"/api/v1/assets/{id}/actions", {"action": "select"})
                select_asset(id)
            elif self.command == "configure":
                data = {}
                for key in a["fields"]:
                    if key == "target_temperature_c":
                        data[key] = scene.chemlab_temperature
                    elif key in {"stir_rpm", "speed_rpm"}:
                        data[key] = scene.chemlab_rpm
                    elif key == "duration_s":
                        data[key] = scene.chemlab_duration
                    elif key == "path_length_cm":
                        data[key] = scene.chemlab_path
                    elif key == "sash_open_pct":
                        data[key] = scene.chemlab_sash
                if data:
                    request(f"/api/v1/assets/{id}", data, "PATCH")
            elif self.command.startswith("toggle:"):
                key = self.command.split(":")[1]
                current = request(f"/api/v1/assets/{id}")["state"][key]
                request(f"/api/v1/assets/{id}", {key: not current}, "PATCH")
            elif self.command == "dispense":
                request(
                    f"/api/v1/assets/{id}/actions",
                    {
                        "action": "dispense",
                        "target_id": scene.chemlab_target,
                        "amount": scene.chemlab_amount,
                        "unit": a["unit"],
                    },
                )
            elif self.command == "transfer":
                request(
                    "/api/v1/transfers",
                    {
                        "source_id": id,
                        "target_id": scene.chemlab_target,
                        "amount": scene.chemlab_amount,
                        "unit": "ml",
                    },
                )
            elif self.command == "save":
                bpy.ops.wm.save_as_mainfile(filepath=str(ROOT / "ChemLab.blend"))
            elif self.command == "demo":
                if context.screen.is_animation_playing:
                    bpy.ops.screen.animation_cancel(restore_frame=False)
                from .demo import run_demo

                run_demo(BASE)
                context.scene.camera = bpy.data.objects["Camera_Reaction"]
                context.scene.render.resolution_x = 1600
                context.scene.render.resolution_y = 1100
                for area in context.screen.areas:
                    if area.type == "VIEW_3D":
                        area.spaces.active.region_3d.view_perspective = "CAMERA"
                self.report({"INFO"}, "实验已启动：观察温度和搅拌；观看镜头动画请点击播放导览")
                return {"FINISHED"}
            elif self.command == "tour_play":
                from .tour import play

                play(context)
            elif self.command == "tour_pause":
                from .tour import pause

                pause(context)
            elif self.command == "tour_video":
                path = ROOT / "renders" / "ChemLab_Tour.mp4"
                if not path.exists() or not (ROOT / "verification" / "tour_render.json").exists():
                    raise RuntimeError("视频正在生成；可以先点击播放 20 秒导览")
                os.startfile(str(path))
            else:
                data = {"action": self.command}
                if self.command in {"measure", "weigh"}:
                    data["sample_id"] = scene.chemlab_sample
                request(f"/api/v1/assets/{id}/actions", data)
            LAST_ERROR = ""
            self.report({"INFO"}, "操作已完成")
            return {"FINISHED"}
        except urllib.error.HTTPError as e:
            LAST_ERROR = json.loads(e.read()).get("error", str(e))
            self.report({"WARNING"}, LAST_ERROR)
        except Exception as e:
            LAST_ERROR = str(e)
            self.report({"ERROR"}, LAST_ERROR)
        return {"CANCELLED"}


class CHEMLAB_OT_camera(bpy.types.Operator):
    bl_idname = "chemlab.camera"
    bl_label = "切换视角"
    camera_name: StringProperty()

    def execute(self, context):
        if context.screen.is_animation_playing:
            bpy.ops.screen.animation_cancel(restore_frame=False)
        context.scene.camera = bpy.data.objects[self.camera_name]
        context.scene.render.resolution_x = 1800 if self.camera_name == "Camera_Overview" else 1600
        context.scene.render.resolution_y = 1400 if self.camera_name == "Camera_Overview" else 1100
        for area in context.screen.areas:
            if area.type == "VIEW_3D":
                area.spaces.active.region_3d.view_perspective = "CAMERA"
                area.spaces.active.region_3d.view_camera_zoom = 10
                area.spaces.active.region_3d.view_camera_offset = (0.07, 0)
        return {"FINISHED"}


class CHEMLAB_PT_panel(bpy.types.Panel):
    bl_label = "ChemLab · 化学实验室"
    bl_idname = "CHEMLAB_PT_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "ChemLab"

    def draw(self, context):
        layout = self.layout
        s = context.scene
        layout.label(
            text="API 已连接" if CONNECTED else "API 未连接",
            icon="LINKED" if CONNECTED else "UNLINKED",
        )
        layout.label(text=BASE)
        if not CONNECTED:
            layout.operator("chemlab.command", text="启动 / 连接服务").command = "connect"
        row = layout.row(align=True)
        for title, cam in [
            ("全景", "Overview"),
            ("反应", "Reaction"),
            ("表征", "Analysis"),
            ("配液", "Preparation"),
        ]:
            row.operator("chemlab.camera", text=title).camera_name = "Camera_" + cam
        box = layout.box()
        row = box.row(align=True)
        row.operator("chemlab.command", text="播放 20 秒导览", icon="PLAY").command = "tour_play"
        row.operator("chemlab.command", text="暂停", icon="PAUSE").command = "tour_pause"
        if (
            context.screen.is_animation_playing
            and context.scene.camera
            and context.scene.camera.name == "Camera_ChemLab_Tour"
        ):
            box.label(text=f"正在播放：{(s.frame_current - 1) / 20:.1f} / 20 秒")
        else:
            box.label(text="镜头动画 · 空格键也可播放 / 暂停")
        if (ROOT / "renders" / "ChemLab_Tour.mp4").exists() and (
            ROOT / "verification" / "tour_render.json"
        ).exists():
            box.operator(
                "chemlab.command", text="观看导览视频", icon="FILE_MOVIE"
            ).command = "tour_video"
        layout.separator()
        layout.prop(s, "chemlab_asset", text="设备")
        id = s.chemlab_asset
        a = CATALOG[id]
        state = CACHE.get("states", {}).get(id, {})
        layout.operator(
            "chemlab.command", text="选中此设备", icon="RESTRICT_SELECT_OFF"
        ).command = "select"
        layout.label(text=id)
        box = layout.box()
        box.label(
            text="状态："
            + {
                "running": "运行中",
                "idle": "待机",
                "ready": "测量完成",
                "complete": "已完成",
                "offline": "离线",
            }.get(state.get("status", "offline"), state.get("status", "离线"))
        )
        for key, label in [
            ("temperature_c", "当前温度 °C"),
            ("volume_ml", "容器体积 mL"),
            ("remaining", "剩余库存"),
            ("reading", "读数"),
            ("remaining_s", "剩余时间 s"),
        ]:
            if key in state:
                val = state[key]
                box.label(
                    text=f"{label}: {val:.2f}"
                    if isinstance(val, (float, int))
                    else f"{label}: {val}"
                )
        fields = a["fields"]
        for key, prop, label in [
            ("target_temperature_c", "chemlab_temperature", "目标温度 °C"),
            ("stir_rpm", "chemlab_rpm", "转速 rpm"),
            ("speed_rpm", "chemlab_rpm", "转速 rpm"),
            ("duration_s", "chemlab_duration", "时长 s"),
            ("path_length_cm", "chemlab_path", "光程 cm"),
            ("sash_open_pct", "chemlab_sash", "视窗开度 %"),
        ]:
            if key in fields:
                layout.prop(s, prop, text=label)
        if any(f["type"] != "boolean" for f in fields.values()):
            layout.operator("chemlab.command", text="应用参数").command = "configure"
        for key, label in [
            ("fan_on", "通风"),
            ("cap_open", "瓶盖"),
            ("door_open", "柜门"),
            ("lid_open", "机盖"),
            ("water_on", "供水"),
        ]:
            if key in fields:
                layout.operator(
                    "chemlab.command", text=f"{label}：{'开' if state.get(key) else '关'} / 切换"
                ).command = "toggle:" + key
        row = layout.row(align=True)
        for action, label in [("start", "启动"), ("stop", "停止"), ("tare", "去皮")]:
            if action in a["actions"]:
                row.operator("chemlab.command", text=label).command = action
        if "dispense" in a["actions"] or a["kind"] in {"vessel", "reactor"}:
            layout.prop(s, "chemlab_target", text="目标容器")
            layout.prop(s, "chemlab_amount", text="转移量 " + a.get("unit", "ml"))
            layout.operator("chemlab.command", text="移液 / 加料").command = (
                "dispense" if a["kind"] == "reagent" else "transfer"
            )
        for action, label in [("measure", "测量样品"), ("weigh", "称量样品")]:
            if action in a["actions"]:
                layout.prop(s, "chemlab_sample", text="样品")
                layout.operator("chemlab.command", text=label).command = action
        if state.get("last_result_id"):
            layout.label(text=state["last_result_id"])
        if LAST_ERROR:
            box = layout.box()
            box.alert = True
            for i in range(0, len(LAST_ERROR), 38):
                box.label(text=LAST_ERROR[i : i + 38])
        layout.separator()
        layout.label(text="教学模拟 · 表征结果为合成数据", icon="INFO")
        layout.operator(
            "chemlab.command", text="启动实验（加热 / 搅拌 / 测量）", icon="PLAY"
        ).command = "demo"
        layout.operator("chemlab.command", text="保存实验室", icon="FILE_TICK").command = "save"


class CHEMLAB_OT_environment(bpy.types.Operator):
    bl_idname = "chemlab.environment"
    bl_label = "环境操作"
    bl_description = "控制虚拟机器人、查看通用实验环境"
    command: StringProperty()

    def execute(self, context):
        global LAST_ERROR
        scene = context.scene
        try:
            if self.command in {"navigate", "pick", "place", "home", "estop", "reset_estop"}:
                data = {"action": self.command}
                if self.command in {"navigate", "place"}:
                    data["station"] = scene.chemlab_station
                if self.command == "pick":
                    data["asset_id"] = "sample_tube_01"
                request("/api/v1/assets/robot_01/actions", data, timeout=5)
            elif self.command == "transport":
                request("/api/v1/environment/demo/transport", {}, timeout=5)
                scene.chemlab_follow_robot = True
                scene.camera = bpy.data.objects["Camera_Robot"]
            elif self.command == "focus":
                scene.chemlab_follow_robot = True
                scene.camera = bpy.data.objects["Camera_Robot"]
                request("/api/v1/assets/robot_01/actions", {"action": "select"})
            elif self.command == "overview":
                scene.chemlab_follow_robot = False
                scene.camera = bpy.data.objects["Camera_Overview"]
            elif self.command == "docs":
                os.startfile(str(ROOT / "ENVIRONMENT.md"))
            if self.command in {"focus", "overview", "transport"}:
                if context.screen.is_animation_playing:
                    bpy.ops.screen.animation_cancel(restore_frame=False)
                scene.render.resolution_x = 1800 if self.command == "overview" else 1600
                scene.render.resolution_y = 1400 if self.command == "overview" else 1100
                for area in context.screen.areas:
                    if area.type == "VIEW_3D":
                        area.spaces.active.region_3d.view_perspective = "CAMERA"
                        area.spaces.active.region_3d.view_camera_zoom = 10
                        area.spaces.active.region_3d.view_camera_offset = (0.07, 0)
            LAST_ERROR = ""
            self.report({"INFO"}, "指令已接收；下方状态显示实际执行进度")
            return {"FINISHED"}
        except urllib.error.HTTPError as e:
            LAST_ERROR = json.loads(e.read()).get("error", str(e))
        except Exception as e:
            LAST_ERROR = str(e)
        self.report({"ERROR"}, LAST_ERROR)
        return {"CANCELLED"}


class CHEMLAB_PT_environment(bpy.types.Panel):
    bl_label = "移动助手与环境"
    bl_idname = "CHEMLAB_PT_environment"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "自动化"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        robot = CACHE.get("states", {}).get("robot_01", {})
        layout.label(text="通用环境 · 虚拟执行", icon="WORLD")
        layout.label(text="API 已连接" if CONNECTED else "API 未连接")
        layout.label(text="scienceos.chemlab / 36 个对象")
        row = layout.row(align=True)
        row.operator("chemlab.environment", text="跟随机器人").command = "focus"
        row.operator("chemlab.environment", text="全景").command = "overview"
        layout.operator(
            "chemlab.environment", text="运行样品搬运演示", icon="PLAY"
        ).command = "transport"
        layout.prop(scene, "chemlab_station", text="停靠位")
        layout.operator("chemlab.environment", text="前往停靠位").command = "navigate"
        row = layout.row(align=True)
        row.operator("chemlab.environment", text="抓取样品管").command = "pick"
        row.operator("chemlab.environment", text="放置样品管").command = "place"
        layout.operator("chemlab.environment", text="返回待命位").command = "home"
        row = layout.row(align=True)
        row.alert = True
        row.operator("chemlab.environment", text="急停", icon="CANCEL").command = "estop"
        row.operator("chemlab.environment", text="解除急停").command = "reset_estop"
        box = layout.box()
        labels = {
            "idle": "待命",
            "navigating": "移动中",
            "manipulating": "抓取 / 放置中",
            "estopped": "已急停",
            "stopped": "已停止",
        }
        box.label(text="机器人：" + labels.get(robot.get("status"), robot.get("status", "未连接")))
        box.label(text="夹持：" + (robot.get("held_asset_id") or "空"))
        box.label(text=f"模拟电量：{robot.get('battery_pct', 100):.1f}%")
        tasks = ENV_CACHE.get("tasks", [])
        if tasks:
            task = tasks[-1]
            box.label(text=f"任务：{task['status']}")
            box.label(
                text=(
                    f"步骤：{min(task['step_index'] + 1, len(task['steps']))}"
                    f" / {len(task['steps'])}"
                )
            )
            if task.get("reason"):
                box.label(text=task["reason"][:36])
        box = layout.box()
        box.label(text="真实设备反馈：只读监督")
        supervision = ENV_CACHE.get("supervision", {})
        box.label(text=f"已配对：{len(supervision.get('bindings', []))} 个")
        for comparison in supervision.get("comparisons", [])[:3]:
            box.label(text=comparison["asset_id"] + ": " + comparison["status"])
        if LAST_ERROR:
            box = layout.box()
            box.alert = True
            for i in range(0, len(LAST_ERROR), 32):
                box.label(text=LAST_ERROR[i : i + 32])
        layout.label(text="运动为几何演示；尚未连接真实机器人", icon="INFO")
        layout.operator("chemlab.command", text="保存实验室", icon="FILE_TICK").command = "save"


def apply_world_frame(bundle):
    frame = bundle.get("frame")
    if frame is None:
        return
    scene = bpy.context.scene
    scene["chemworld_public_json"] = json.dumps(frame, ensure_ascii=False, allow_nan=False)
    target = frame.get("asset_id")
    if target in COMPONENTS:
        display = component(target, "display")
        if display:
            display.data.body = f"CW {frame['step']} | {frame.get('operation') or 'READY'}"


class CHEMLAB_PT_chemworld(bpy.types.Panel):
    bl_label = "ChemWorld 公开实验状态"
    bl_idname = "CHEMLAB_PT_chemworld"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "ChemWorld"

    def draw(self, context):
        layout = self.layout
        layout.label(text="ChemWorld 负责实验结果与预算", icon="WORLD")
        layout.label(text="Blender 展示公开状态与机器人动作")
        frame = WORLD_CACHE.get("frame")
        if not frame:
            layout.label(text="等待 ChemWorld / Task Lab 连接")
            layout.label(text="启动说明见 apps/blender_lab/README.md")
            return
        layout.label(text="任务: " + str(frame["task_id"]))
        layout.label(text=f"步骤: {frame['step']} / 操作: {frame.get('operation') or 'reset'}")
        layout.label(text="状态: " + frame["status"])
        campaign = frame["campaign"]
        layout.label(text=f"剩余操作预算: {campaign['remaining_budget']} / {campaign['budget']}")
        layout.label(
            text="会话: "
            + ("已连接" if WORLD_CACHE.get("active_session_id") else "已结束，保留最后观测")
        )
        box = layout.box()
        box.label(text="已公开的观测；未测量项不显示")
        for key, value in frame["observations"].items():
            if value is not None:
                box.label(text=f"{key}: {value:.4g}")
        if frame["mapping_status"] == "report_only":
            layout.label(text="当前操作仅报告展示，无对应仪器模型")
        layout.label(text="场景库存与搬运样品为独立演示状态")
        layout.label(text="真实设备输出未启用", icon="INFO")


CLASSES = [
    CHEMLAB_PT_chemworld,
    CHEMLAB_OT_command,
    CHEMLAB_OT_camera,
    CHEMLAB_PT_panel,
    CHEMLAB_OT_environment,
    CHEMLAB_PT_environment,
]


def register():
    global COMPONENTS
    if bpy.app.timers.is_registered(timer):
        return
    for cls in CLASSES:
        old = getattr(bpy.types, cls.__name__, None)
        if old:
            with contextlib.suppress(RuntimeError):
                bpy.utils.unregister_class(old)
        bpy.utils.register_class(cls)
    props = {
        "chemlab_station": EnumProperty(
            items=[
                ("preparation", "配液交接位", ""),
                ("analysis", "表征交接位", ""),
                ("reaction", "反应区停靠位", ""),
                ("home", "待命位", ""),
            ],
            default="preparation",
        ),
        "chemlab_follow_robot": BoolProperty(default=False),
        "chemlab_asset": EnumProperty(
            items=ASSET_ITEMS, default="reactor_01", update=asset_changed
        ),
        "chemlab_sample": EnumProperty(items=SAMPLE_ITEMS, default="beaker_01"),
        "chemlab_target": EnumProperty(items=TARGET_ITEMS, default="beaker_01"),
        "chemlab_temperature": FloatProperty(default=45, min=5, max=200),
        "chemlab_rpm": FloatProperty(default=180, min=0, max=6000),
        "chemlab_duration": FloatProperty(default=60, min=1, max=3600),
        "chemlab_amount": FloatProperty(default=25, min=0.001, max=10000),
        "chemlab_path": FloatProperty(default=1, min=0.1, max=5),
        "chemlab_sash": FloatProperty(default=35, min=0, max=100),
    }
    for name, prop in props.items():
        setattr(bpy.types.Scene, name, prop)
    COMPONENTS = {
        a["id"]: list(bpy.data.objects[a["id"]].children)
        for a in ASSETS
        if a["id"] in bpy.data.objects
    }
    (ROOT / "runtime").mkdir(exist_ok=True)
    start_service()
    bpy.app.timers.register(timer, first_interval=0.5, persistent=True)
    print("ChemLab bridge registered:", len(COMPONENTS), "assets")


def unregister():
    if bpy.app.timers.is_registered(timer):
        bpy.app.timers.unregister(timer)
    for cls in reversed(CLASSES):
        with contextlib.suppress(RuntimeError):
            bpy.utils.unregister_class(cls)
    for name in [
        "chemlab_asset",
        "chemlab_sample",
        "chemlab_target",
        "chemlab_temperature",
        "chemlab_rpm",
        "chemlab_duration",
        "chemlab_amount",
        "chemlab_path",
        "chemlab_sash",
        "chemlab_station",
        "chemlab_follow_robot",
    ]:
        if hasattr(bpy.types.Scene, name):
            delattr(bpy.types.Scene, name)


if __name__ == "__main__":
    register()
