"""Editable mobile manipulator geometry and a consistent two-link visual IK chain."""

import math
from pathlib import Path

import bpy
from mathutils import Quaternion, Vector

from . import build_lab as g
from .catalog import CATALOG, VERSION

ROOT = Path(__file__).resolve().parent


def setup_asset(a):
    collection = bpy.data.collections.new(a["id"] + " | " + a["name"])
    group = bpy.data.collections.get("AUTOMATION")
    if group is None:
        group = bpy.data.collections.new("AUTOMATION")
        bpy.context.scene.collection.children.link(group)
    group.children.link(collection)
    root = bpy.data.objects.new(a["id"], None)
    collection.objects.link(root)
    root.location = a["location"]
    root.empty_display_type = "PLAIN_AXES"
    root.empty_display_size = 0.1
    for key, value in {
        "lab_id": a["id"],
        "lab_root": True,
        "name_zh": a["name"],
        "kind": a["kind"],
        "api_endpoint": "http://127.0.0.1:8877/api/v1/assets/" + a["id"],
        "supported_actions": ", ".join(a["actions"]),
    }.items():
        root[key] = value
    g.CURRENT = root
    g.COLLECTION = collection
    g.M = {m.name: m for m in bpy.data.materials}
    return root


def build():
    if "robot_01" not in bpy.data.objects:
        root = setup_asset(CATALOG["robot_01"])
        g.cyl("base_shell", (0, 0, 0.19), 0.30, 0.29, "white")
        g.cyl("lower_bumper", (0, 0, 0.07), 0.325, 0.07, "navy")
        g.ring("status_ring", (0, 0, 0.31), 0.303, 0.012, "teal")
        g.cyl("deck", (0, 0, 0.35), 0.30, 0.04, "metal")
        for x in [-0.277, 0.277]:
            for y in [-0.14, 0.14]:
                wheel = g.cyl(
                    "wheel",
                    (x, y, 0.08),
                    0.095,
                    0.045,
                    "black",
                    rot=(0, math.pi / 2, 0),
                    vertices=40,
                )
                wheel["wheel_spin"] = True
                g.cyl(
                    "wheel_hub", (x * 1.09, y, 0.08), 0.043, 0.015, "metal", rot=(0, math.pi / 2, 0)
                )
        for y in [-0.27, 0.27]:
            g.cube("bumper_sensor", (0, y, 0.18), (0.16, 0.025, 0.055), "black", 0.009)
        g.cyl("lidar_base", (0, -0.2, 0.405), 0.08, 0.035, "black")
        g.cyl("lidar_lens", (0, -0.2, 0.443), 0.065, 0.05, "blue")
        g.cyl("lidar_cap", (0, -0.2, 0.478), 0.073, 0.02, "navy")
        g.cyl("arm_pedestal", (0, 0.08, 0.56), 0.105, 0.38, "white")
        g.cyl("arm_pedestal_band", (0, 0.08, 0.72), 0.112, 0.055, "teal")
        g.cube("screen_support", (0, -0.13, 0.68), (0.055, 0.065, 0.31), "metal")
        g.cube("touchscreen", (0, -0.17, 0.835), (0.28, 0.05, 0.2), "navy", 0.02)
        g.text("assistant_title", "LAB ASSIST", (0, -0.199, 0.875), 0.033, "screen")
        g.text("display", "READY", (0, -0.201, 0.805), 0.026, "white")
        g.cyl("estop_base", (0.22, -0.08, 0.39), 0.035, 0.025, "yellow")
        g.cyl("estop_button", (0.22, -0.08, 0.414), 0.025, 0.025, "red")
        g.cube("sample_tray", (0.0, 0.16, 0.54), (0.22, 0.24, 0.04), "navy", 0.02)
        g.cyl("tray_recess", (0, 0.16, 0.564), 0.055, 0.015, "teal")
        for role in ["upper_arm", "forearm"]:
            g.cyl(role, (0, 0, 1), 0.046, 1, "white")
            g.cube(role + "_stripe", (0, 0, 1), (0.025, 0.08, 1), "teal", 0.005)
        for role in ["shoulder_joint", "elbow_joint", "wrist_joint"]:
            g.sphere(role, (0, 0, 1), (0.072, 0.072, 0.072), "blue")
        g.cyl("tool_coupler", (0, 0, 1), 0.049, 0.085, "metal")
        g.cube("gripper_body", (0, 0, 1), (0.13, 0.07, 0.055), "navy", 0.01)
        for side in [-1, 1]:
            jaw = g.cube("gripper_jaw", (side * 0.045, 0, 1), (0.018, 0.045, 0.1), "metal", 0.004)
            jaw["jaw_side"] = side
        g.text("fleet_id", "M-01", (0, -0.307, 0.205), 0.056, "navy")
        for obj in root.children:
            obj["base_location"] = list(obj.location)
            obj["base_rotation"] = list(obj.rotation_euler)
    if "sample_tube_01" not in bpy.data.objects:
        root = setup_asset(CATALOG["sample_tube_01"])
        g.cyl("sample_body", (0, 0, 0.095), 0.035, 0.18, "bottle_glass")
        g.cyl("sample_base", (0, 0, 0.012), 0.034, 0.015, "white")
        g.cyl("sample_cap", (0, 0, 0.195), 0.04, 0.035, "teal")
        g.cube("sample_label", (0, -0.035, 0.10), (0.052, 0.008, 0.068), "white", 0.003)
        g.text("sample_id", "S-01", (0, -0.041, 0.1), 0.018, "navy")
    root = bpy.data.objects["sample_tube_01"]
    if not any(o.get("component") == "liquid" for o in root.children):
        g.CURRENT = root
        g.COLLECTION = root.users_collection[0]
        liquid = g.cyl(
            "liquid",
            (0, 0, 0.04),
            0.03,
            0.055,
            g.material("sample_tube_01_liquid", (0.05, 0.4, 0.7), rough=0.2),
        )
        liquid["max_height"] = 0.16
        liquid["base_z"] = 0.018
        for obj in root.children:
            obj["base_location"] = list(obj.location)
            obj["base_rotation"] = list(obj.rotation_euler)
    # Free the mobile base corridor by moving the two existing stools as whole assemblies.
    if not bpy.context.scene.get("automation_stools_relocated"):
        for obj in bpy.data.objects:
            if obj.name.startswith("ENV__stool") or obj.name.startswith("ENV__footrest"):
                (
                    1
                    if obj.name.endswith(".001") and not obj.name.startswith("ENV__stool_leg")
                    else 0
                )
                # Curve legs contain absolute coordinates; classify using their geometric centroid.
                points = []
                if obj.type == "CURVE" and obj.data.splines:
                    points = [Vector(p.co[:3]) for sp in obj.data.splines for p in sp.points]
                center = sum(points, Vector()) / len(points) if points else obj.location.copy()
                old = (-1.9, -2.18) if center.x < 0 else (2.15, -0.25)
                new = (-3.6, -0.95) if center.x < 0 else (2.25, -3.1)
                obj.location.x += new[0] - old[0]
                obj.location.y += new[1] - old[1]
        bpy.context.scene["automation_stools_relocated"] = True
    if "Camera_Robot" not in bpy.data.objects:
        g.CURRENT = None
        g.COLLECTION = bpy.data.collections["90 / CAMERAS & LIGHTING"]
        g.camera("Camera_Robot", (3.1, -5.9, 3.2), (0.35, -2.1, 0.78), 3.0)
    if "ENV__robot_dock" not in bpy.data.objects:
        g.CURRENT = None
        g.COLLECTION = bpy.data.collections["AUTOMATION"]
        g.M = {m.name: m for m in bpy.data.materials}
        g.cube("robot_dock", (0.45, -2.25, 0.045), (0.95, 0.95, 0.008), "navy", 0.04)
        for x in [0.02, 0.88]:
            g.cube("dock_edge", (x, -2.25, 0.051), (0.018, 0.84, 0.004), "teal", 0)
        g.text("dock_label", "MOBILE LAB ASSIST", (0.45, -2.82, 0.052), 0.075, "teal", (0, 0, 0))
    scene = bpy.context.scene
    scene["chemlab_version"] = VERSION
    scene["asset_count"] = len(CATALOG)
    scene["environment_id"] = "scienceos.chemlab"
    apply_robot(CATALOG["robot_01"]["initial_state"], list(bpy.data.objects["robot_01"].location))


def apply_robot(state, pose):
    from .lab_environment import robot_tcp

    root = bpy.data.objects.get("robot_01")
    if root is None:
        return
    yaw = math.radians(state["base_yaw_deg"])
    root.rotation_euler.z = yaw
    tcp = Vector(robot_tcp(pose, state))
    origin = Vector(pose)

    def local(world):
        p = world - origin
        return Vector(
            (
                math.cos(yaw) * p.x + math.sin(yaw) * p.y,
                -math.sin(yaw) * p.x + math.cos(yaw) * p.y,
                p.z,
            )
        )

    wrist = local(tcp)
    shoulder = Vector((0, 0.08, 0.84))
    delta = wrist - shoulder
    length = min(0.859, max(0.02, delta.length))
    direction = delta.normalized()
    up = Vector((0, 0, 1))
    bend = up - up.dot(direction) * direction
    if bend.length < 0.001:
        bend = Vector((0, 1, 0))
    bend.normalize()
    elbow = (shoulder + wrist) / 2 + bend * math.sqrt(max(0, 0.43**2 - (length / 2) ** 2))

    def link(obj, start, end):
        obj.location = (start + end) / 2
        obj.rotation_euler = (end - start).to_track_quat("Z", "Y").to_euler()
        obj.scale.z = (end - start).length

    for obj in root.children:
        role = obj.get("component", "")
        if role in {"upper_arm", "upper_arm_stripe"}:
            link(obj, shoulder, elbow)
        elif role in {"forearm", "forearm_stripe"}:
            link(obj, elbow, wrist)
        elif role == "shoulder_joint":
            obj.location = shoulder
        elif role == "elbow_joint":
            obj.location = elbow
        elif role == "wrist_joint":
            obj.location = wrist + Vector((0, 0, 0.085))
        elif role == "tool_coupler":
            obj.location = wrist + Vector((0, 0, 0.055))
        elif role == "gripper_body":
            obj.location = wrist + Vector((0, 0, 0.025))
        elif role == "gripper_jaw":
            obj.location = wrist + Vector(
                (obj["jaw_side"] * (0.055 if state["gripper_open"] else 0.035), 0, -0.035)
            )
        elif role == "wheel":
            obj.rotation_mode = "QUATERNION"
            obj.rotation_quaternion = Quaternion((0, 1, 0), math.pi / 2) @ Quaternion(
                (0, 0, 1), math.radians(state["wheel_angle_deg"])
            )
        elif role == "display":
            obj.data.body = state["status"].upper()[:18]


if __name__ == "__main__":
    build()
