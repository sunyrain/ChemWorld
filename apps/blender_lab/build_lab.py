# Blender executes --python files outside the package import machinery.
if __package__ in {None, ""}:
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    __package__ = "apps.blender_lab"

"""Build the editable laboratory using Blender's native data API."""
import json
import math
import sys
from pathlib import Path

import bpy
from mathutils import Vector

ROOT = Path(__file__).resolve().parent
from .catalog import ASSETS, VERSION, public_asset

M = {}
CURRENT = None
COLLECTION = None


def material(name, color, metallic=0, rough=0.4, transmission=0, emission=0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    m.diffuse_color = (*color[:3], color[3] if len(color) > 3 else 1)
    bs = next(n for n in m.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    bs.inputs["Base Color"].default_value = (*color[:3], 1)
    bs.inputs["Metallic"].default_value = metallic
    bs.inputs["Roughness"].default_value = rough
    bs.inputs["Transmission Weight"].default_value = transmission
    if transmission:
        bs.inputs["IOR"].default_value = 1.45
    if emission:
        bs.inputs["Emission Color"].default_value = (*color[:3], 1)
        bs.inputs["Emission Strength"].default_value = emission
    return m


def attach(o, role, mat=None, parent=True):
    o.name = (CURRENT.name + "__" if CURRENT and parent else "ENV__") + role
    for col in list(o.users_collection):
        col.objects.unlink(o)
    COLLECTION.objects.link(o)
    if CURRENT and parent:
        o.parent = CURRENT
        o["lab_id"] = CURRENT["lab_id"]
        o["component"] = role
    if mat:
        o.data.materials.append(M[mat] if isinstance(mat, str) else mat)
    return o


def cube(role, loc, size, mat, bevel=0.015):
    x, y, z = [v / 2 for v in size]
    verts = [
        (-x, -y, -z),
        (-x, -y, z),
        (-x, y, -z),
        (-x, y, z),
        (x, -y, -z),
        (x, -y, z),
        (x, y, -z),
        (x, y, z),
    ]
    faces = [(0, 4, 6, 2), (1, 3, 7, 5), (0, 1, 5, 4), (2, 6, 7, 3), (0, 2, 3, 1), (4, 5, 7, 6)]
    mesh = bpy.data.meshes.new(role)
    mesh.from_pydata(verts, [], [tuple(reversed(f)) for f in faces])
    mesh.update()
    o = bpy.data.objects.new(role, mesh)
    o.location = loc
    attach(o, role, mat)
    if bevel:
        mod = o.modifiers.new("Machined edges", "BEVEL")
        mod.width = min(bevel, min(size) / 4)
        mod.segments = 3
        mod = o.modifiers.new("Corner normals", "WEIGHTED_NORMAL")
    return o


def cyl(role, loc, radius, depth, mat, radius2=None, rot=None, vertices=40):
    # Direct mesh avoids the quadratic dependency updates of repeated operators.
    r2 = radius if radius2 is None else radius2
    verts = [
        (r * math.cos(2 * math.pi * i / vertices), r * math.sin(2 * math.pi * i / vertices), z)
        for r, z in [(radius, -depth / 2), (r2, depth / 2)]
        for i in range(vertices)
    ]
    faces = [tuple(reversed(range(vertices))), tuple(range(vertices, 2 * vertices))] + [
        (i, (i + 1) % vertices, (i + 1) % vertices + vertices, i + vertices)
        for i in range(vertices)
    ]
    mesh = bpy.data.meshes.new(role)
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    o = bpy.data.objects.new(role, mesh)
    o.location = loc
    if rot:
        o.rotation_euler = rot
    attach(o, role, mat)
    for p in o.data.polygons:
        p.use_smooth = len(p.vertices) == 4
    return o


def tube(role, points, radius, mat):
    data = bpy.data.curves.new(role, "CURVE")
    data.dimensions = "3D"
    data.resolution_u = 12
    data.bevel_depth = radius
    data.bevel_resolution = 3
    sp = data.splines.new("POLY")
    sp.points.add(len(points) - 1)
    for p, co in zip(sp.points, points, strict=False):
        p.co = (*co, 1)
    o = bpy.data.objects.new(role, data)
    attach(o, role, mat)
    return o


def ring(role, loc, r, thickness, mat):
    return tube(
        role,
        [
            (
                loc[0] + r * math.cos(i * math.tau / 64),
                loc[1] + r * math.sin(i * math.tau / 64),
                loc[2],
            )
            for i in range(65)
        ],
        thickness,
        mat,
    )


def sphere(role, loc, size, mat):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, location=loc)
    o = bpy.context.object
    o.scale = size
    attach(o, role, mat)
    for p in o.data.polygons:
        p.use_smooth = True
    return o


def text(role, body, loc, size=0.09, mat="ink", rotation=(math.pi / 2, 0, 0), align="CENTER"):
    data = bpy.data.curves.new(role, "FONT")
    data.body = body
    data.size = size
    data.align_x = align
    data.align_y = "CENTER"
    data.extrude = 0.0005
    o = bpy.data.objects.new(role, data)
    o.location = loc
    o.rotation_euler = rotation
    attach(o, role, mat)
    return o


def panel(label, width=0.45, y=-0.3, z=0.25):
    cube("nameplate", (0, y, z), (width, 0.012, 0.11), "navy", 0.004)
    text("name", label, (0, y - 0.009, z), min(0.045, width / max(10, len(label)) * 1.5), "white")


def display(body, loc=(0, -0.25, 0.12), width=0.26):
    cube("display_frame", loc, (width + 0.024, 0.024, 0.12), "black", 0.008)
    o = text("display", body, (loc[0], loc[1] - 0.014, loc[2]), 0.038, "screen")
    return o


def led(loc):
    m = material(CURRENT.name + "_indicator", (0.05, 0.55, 0.32), rough=0.2, emission=0.7)
    return cyl("status_led", loc, 0.016, 0.012, m, rot=(math.pi / 2, 0, 0), vertices=20)


def vessel_body(style="beaker", r=0.14, h=0.38):
    # Thin-walled open glass shell, with visible rolled lip and graduation marks.
    profile = (
        [(r * 0.9, 0), (r, 0.02), (r, h)]
        if style == "beaker"
        else [(r * 0.84, 0), (r, 0.03), (r * 0.38, h * 0.76), (r * 0.38, h)]
    )
    n = 64
    th = 0.003
    rings = profile + [(rad - th, z) for rad, z in reversed(profile)]
    verts = [
        (rad * math.cos(i * math.tau / n), rad * math.sin(i * math.tau / n), z)
        for rad, z in rings
        for i in range(n)
    ]
    faces = [
        (k * n + i, k * n + (i + 1) % n, (k + 1) * n + (i + 1) % n, (k + 1) * n + i)
        for k in range(len(rings) - 1)
        for i in range(n)
    ]
    mesh = bpy.data.meshes.new("Borosilicate vessel")
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    o = bpy.data.objects.new("glass", mesh)
    attach(o, "glass", "glass")
    for p in mesh.polygons:
        p.use_smooth = True
    ring("lip", (0, 0, h), profile[-1][0], 0.004, "glass_edge")
    cyl("base", (0, 0, 0.005), r * 0.88, 0.008, "glass")
    liquidmat = material(CURRENT.name + "_liquid", (0.05, 0.48, 0.68), rough=0.2, transmission=0.18)
    liq = cyl("liquid", (0, 0, h * 0.28), r * 0.88, h * 0.52, liquidmat)
    liq["max_height"] = h * 0.78
    liq["base_z"] = 0.012
    for i in range(1, 5):
        z = i * h * 0.17
        tube(
            "graduation_" + str(i),
            [(-r * 0.48, -r * 0.91, z), (r * 0.1, -r * 0.99, z)],
            0.0018,
            "white",
        )
    if style == "beaker":
        cube("stirbar", (0, 0, 0.025), (0.13, 0.026, 0.026), "white", 0.012)


def build_bench(a):
    w, d, h = a["size"]
    cube("plinth", (0, 0, 0.1), (w - 0.12, d - 0.12, 0.2), "navy")
    cube("cabinet", (0, 0, h * 0.48), (w - 0.08, d - 0.08, h - 0.14), "white")
    cube("worktop", (0, 0, h - 0.035), (w, d, 0.07), "counter", 0.025)
    count = max(2, int(w / 0.62))
    for i in range(count):
        x = -w / 2 + (i + 0.5) * w / count
        cube(
            "drawer_" + str(i),
            (x, -d / 2 - 0.002, h - 0.19),
            (w / count - 0.035, 0.025, 0.21),
            "white",
        )
        cube("door_" + str(i), (x, -d / 2 - 0.002, 0.36), (w / count - 0.035, 0.025, 0.43), "pale")
        cube(
            "handle_" + str(i), (x, -d / 2 - 0.035, h - 0.18), (0.22, 0.045, 0.018), "metal", 0.007
        )
    panel(a["label"], min(1.5, w * 0.8), -d / 2 - 0.025, 0.19)


def build_hood(a):
    w, d, h = a["size"]
    cube("back", (0, d / 2 - 0.05, h / 2), (w, 0.1, h), "white")
    for x in [-w / 2 + 0.05, w / 2 - 0.05]:
        cube("pillar", (x, 0, h / 2), (0.1, d, h), "white")
    cube("roof", (0, 0, h - 0.14), (w, d, 0.28), "white")
    cube("valance", (0, -d / 2 - 0.02, h - 0.13), (w, 0.05, 0.23), "navy")
    text("title", "VENTILATED REACTION", (0, -d / 2 - 0.052, h - 0.13), 0.082, "white")
    cube("light", (0, 0.08, h - 0.3), (w - 0.25, 0.12, 0.025), "light")
    for i in range(8):
        cube("baffle", (0, d / 2 - 0.112, 0.3 + i * 0.12), (w - 0.25, 0.015, 0.025), "metal", 0.002)
    # Sash is a linked subassembly; API raises it vertically.
    cube("sash", (0, -d / 2, 0.93), (w - 0.2, 0.009, 0.7), "sash_glass", 0.003)
    cube("sash_handle", (0, -d / 2 - 0.025, 0.58), (w - 0.16, 0.04, 0.028), "metal", 0.006)
    for x in [-0.72, 0.72]:
        cyl(
            "service_valve", (x, -d / 2 - 0.04, 0.13), 0.045, 0.035, "blue", rot=(math.pi / 2, 0, 0)
        )
    cyl("exhaust", (0, 0.12, h + 0.16), 0.22, 0.32, "metal")
    led((w / 2 - 0.17, -d / 2 - 0.053, h - 0.14))


def build_reactor(a):
    cube("base", (0, 0, 0.035), (0.65, 0.52, 0.07), "metal")
    for x in [-0.25, 0.25]:
        cyl("frame", (x, 0.13, 0.55), 0.014, 1.08, "metal")
        cube("foot", (x, 0, 0.07), (0.055, 0.45, 0.06), "navy")
    tube("crossbar", [(-0.25, 0.13, 1.07), (0.25, 0.13, 1.07)], 0.016, "metal")
    vessel_body("beaker", 0.17, 0.44)
    # Lift vessel assembly within its support frame.
    for o in list(CURRENT.children):
        if o.get("component", "") in {"glass", "lip", "base", "liquid", "stirbar"} or o.get(
            "component", ""
        ).startswith("graduation"):
            if o.get("component") == "base" and o.type == "MESH" and len(o.data.vertices) == 8:
                continue
            o.location.z += 0.2
            if o.get("component") == "liquid":
                o["base_z"] += 0.2
    for z in [0.23, 0.61]:
        ring("jacket_flange", (0, 0, z), 0.185, 0.018, "metal")
    cyl("jacket", (0, 0, 0.43), 0.193, 0.34, "glass")
    cyl("lid", (0, 0, 0.665), 0.195, 0.045, "metal")
    cyl("shaft", (0, 0, 0.68), 0.009, 0.65, "metal")
    cube("motor", (0, 0, 1.03), (0.19, 0.18, 0.25), "blue")
    cube("impeller", (0, 0, 0.28), (0.23, 0.025, 0.025), "metal", 0.007)
    for x in [-0.12, 0.12]:
        cyl("port", (x, 0, 0.73), 0.026, 0.12, "glass")
        ring("joint", (x, 0, 0.76), 0.028, 0.009, "teal")
    tube(
        "coolant_in",
        [(0.19, 0, 0.28), (0.3, 0.02, 0.28), (0.32, 0.3, 0.13), (0.54, 0.4, 0.13)],
        0.012,
        "blue",
    )
    tube(
        "coolant_out",
        [(0.19, 0, 0.56), (0.36, 0.05, 0.56), (0.4, 0.31, 0.2), (0.6, 0.4, 0.2)],
        0.012,
        "red",
    )
    display("25.0 C / 0 rpm", (0, -0.28, 0.105), 0.43)
    text("title", "R-01  /  1000 mL", (0, -0.196, 0.49), 0.031, "white")
    led((0.25, -0.28, 0.12))


def build_condenser(a):
    cube("stand", (0, 0, 0.015), (0.4, 0.4, 0.03), "metal")
    cyl("support", (0.15, 0.13, 0.52), 0.008, 1.02, "metal")
    sphere("receiver", (0, 0, 0.17), (0.12, 0.12, 0.13), "glass")
    cyl("neck", (0, 0, 0.32), 0.034, 0.17, "glass")
    cyl("condenser_jacket", (0, 0, 0.65), 0.047, 0.46, "glass")
    pts = [
        (0.02 * math.cos(i * 0.24), 0.02 * math.sin(i * 0.24), 0.44 + i * 0.0017)
        for i in range(240)
    ]
    tube("coil", pts, 0.0045, "glass_edge")
    for z in [0.42, 0.9]:
        ring("joint", (0, 0, z), 0.043, 0.01, "teal")
    tube("hose", [(0, 0, 0.47), (-0.11, 0.1, 0.48), (-0.15, 0.19, 0.2)], 0.008, "blue")
    liq = cyl(
        "liquid",
        (0, 0, 0.14),
        0.09,
        0.12,
        material(a["id"] + "_liquid", (0.15, 0.65, 0.72), transmission=0.2),
    )
    liq["base_z"] = 0.06
    liq["max_height"] = 0.18
    panel("REFLUX", 0.3, -0.2, 0.06)


def build_hotplate(a):
    cube("body", (0, 0, 0.075), (0.58, 0.5, 0.15), "white")
    cube("panel", (0, -0.255, 0.08), (0.55, 0.016, 0.12), "navy", 0.005)
    cyl(
        "hot_surface",
        (0, 0, 0.18),
        0.235,
        0.045,
        material(a["id"] + "_heat", (0.3, 0.34, 0.37), metallic=0.7),
    )
    display("25 C / 0 rpm", (-0.04, -0.268, 0.09), 0.3)
    cyl("knob", (0.22, -0.283, 0.085), 0.031, 0.025, "metal", rot=(math.pi / 2, 0, 0))
    led((-0.24, -0.274, 0.09))


def build_bath(a):
    w, d, h = a["size"]
    cube("base", (0, 0, 0.04), (w, d, 0.08), "white")
    for x in [-w / 2 + 0.04, w / 2 - 0.04]:
        cube("side", (x, 0, h / 2), (0.08, d, h), "metal")
    for y in [-d / 2 + 0.035, d / 2 - 0.035]:
        cube("end", (0, y, h / 2), (w - 0.1, 0.07, h), "metal")
    cube("bath_water", (0, 0, h - 0.09), (w - 0.17, d - 0.14, 0.04), "water", 0.005)
    for x in [-0.22, 0, 0.22]:
        cyl("sample_tube", (x, 0.02, h - 0.025), 0.048, 0.23, "glass")
        cyl("sample_cap", (x, 0.02, h + 0.095), 0.052, 0.025, "blue")
    display("25.0 C", (0, -d / 2 - 0.022, 0.2), 0.32)
    led((0.32, -d / 2 - 0.02, 0.2))


def build_oven(a):
    w, d, h = a["size"]
    cube("body", (0, 0, h / 2), (w, d, h), "white", 0.05)
    cube("cavity", (0, -d / 2 - 0.006, 0.65), (0.8, 0.017, 0.92), "black")
    for z in [0.38, 0.63, 0.87]:
        for x in [-0.3, -0.15, 0, 0.15, 0.3]:
            tube("shelf_bar", [(x, -d / 2 - 0.02, z), (x, -0.02, z)], 0.008, "metal")
    cube("door", (0, -d / 2 - 0.035, 0.64), (0.88, 0.07, 1.01), "pale", 0.035)
    cube("door_window", (0, -d / 2 - 0.076, 0.67), (0.59, 0.012, 0.66), "smoke_glass")
    cube("door_handle", (0.32, -d / 2 - 0.12, 0.64), (0.035, 0.075, 0.38), "metal")
    display("25.0 C", (-0.08, -d / 2 - 0.022, 1.3), 0.44)
    led((0.34, -d / 2 - 0.024, 1.3))
    for i in range(9):
        cube("vent", (-0.32 + i * 0.08, -d / 2 - 0.01, 0.08), (0.042, 0.025, 0.025), "navy", 0.004)
    text("title", "DRYING OVEN", (0, -d / 2 - 0.02, 1.43), 0.055, "ink")


def build_chiller(a):
    w, d, h = a["size"]
    cube("body", (0, 0, h / 2), (w, d, h), "white", 0.035)
    for z in [0.12, 0.17, 0.22, 0.27, 0.32, 0.37]:
        cube("vent", (0, -d / 2 - 0.004, z), (w - 0.1, 0.018, 0.018), "navy", 0.003)
    display("20 C", (0, -d / 2 - 0.02, 0.51), 0.26)
    led((0.16, -d / 2 - 0.02, 0.51))
    ring("reservoir", (0, 0, h + 0.008), 0.1, 0.012, "metal")


def build_balance(a):
    cube("base", (0, 0, 0.07), (0.58, 0.5, 0.14), "white")
    cube("granite", (0, 0, 0.013), (0.62, 0.54, 0.025), "counter")
    cyl("pan", (0, 0, 0.17), 0.14, 0.015, "metal")
    for x in [-0.24, 0.24]:
        for y in [-0.19, 0.19]:
            cube("post", (x, y, 0.36), (0.014, 0.014, 0.46), "metal", 0.004)
    for x in [-0.24, 0.24]:
        cube("shield", (x, 0, 0.36), (0.003, 0.39, 0.45), "glass", 0.001)
    cube("shield_back", (0, 0.19, 0.36), (0.48, 0.003, 0.45), "glass", 0.001)
    cube("top", (0, 0, 0.6), (0.52, 0.44, 0.025), "pale")
    display("0.0000 g", (0, -0.26, 0.09), 0.33)
    led((0.22, -0.266, 0.09))


def build_ph(a):
    cube("base", (0, -0.06, 0.07), (0.43, 0.32, 0.14), "white")
    display("pH READY", (0, -0.23, 0.09), 0.29)
    cyl("rod", (0.16, 0.14, 0.31), 0.008, 0.58, "metal")
    tube("arm", [(0.16, 0.14, 0.57), (-0.12, 0.14, 0.57), (-0.12, 0.04, 0.57)], 0.009, "metal")
    cyl("electrode", (-0.12, 0.04, 0.37), 0.018, 0.24, "navy")
    cyl("probe_tip", (-0.12, 0.04, 0.22), 0.008, 0.08, "glass_edge")
    cyl("cup", (-0.12, 0.04, 0.14), 0.07, 0.17, "glass")
    ring("cup_rim", (-0.12, 0.04, 0.225), 0.07, 0.004, "glass_edge")
    tube(
        "cable",
        [(-0.12, 0.04, 0.49), (-0.06, 0.18, 0.57), (0.22, 0.23, 0.48), (0.2, 0.15, 0.07)],
        0.005,
        "black",
    )
    led((0.17, -0.23, 0.095))


def build_spectrometer(a):
    w, d, h = a["size"]
    ftir = a["kind"] == "ftir"
    cube("base", (0, 0, 0.045), (w, d, 0.09), "navy", 0.025)
    cube("housing", (0, 0, h / 2 + 0.03), (w - 0.025, d - 0.025, h - 0.07), "white", 0.055)
    if ftir:
        cube("sample_deck", (-0.17, -0.02, h + 0.003), (0.35, 0.35, 0.045), "metal")
        cyl("ATR_crystal", (-0.17, -0.02, h + 0.03), 0.038, 0.01, "black")
        cyl("arm", (-0.17, 0.2, h + 0.18), 0.02, 0.36, "metal")
        cube("pressure_arm", (-0.17, 0.075, h + 0.35), (0.095, 0.27, 0.055), "navy")
        cyl("press", (-0.17, -0.02, h + 0.26), 0.012, 0.14, "metal")
        cyl("press_knob", (-0.17, 0.04, h + 0.415), 0.05, 0.06, "black")
    else:
        cube("sample_lid", (-0.16, 0, h + 0.015), (0.4, 0.49, 0.025), "navy")
        cube("lid_grip", (-0.16, -0.15, h + 0.037), (0.15, 0.035, 0.025), "metal")
        for i in range(3):
            cube("cuvette", (0.22, -0.08 + i * 0.09, h + 0.08), (0.04, 0.04, 0.13), "glass", 0.002)
    display("READY", (0.09, -d / 2 - 0.01, 0.22), 0.34)
    led((w / 2 - 0.07, -d / 2 - 0.02, 0.22))
    text(
        "title", "ATR - FTIR" if ftir else "UV - VIS", (-0.16, -d / 2 - 0.019, 0.105), 0.048, "ink"
    )
    for i in range(5):
        cube(
            "side_vent", (w / 2 - 0.003, 0.1, 0.12 + i * 0.042), (0.012, 0.25, 0.012), "navy", 0.002
        )


def build_centrifuge(a):
    cube("body", (0, 0, 0.18), (0.63, 0.56, 0.36), "white", 0.07)
    cyl("rotor", (0, 0, 0.34), 0.23, 0.03, "metal")
    for i in range(8):
        angle = i * math.tau / 8
        cyl(
            "rotor_slot",
            (0.16 * math.cos(angle), 0.16 * math.sin(angle), 0.36),
            0.027,
            0.025,
            "black",
        )
    cyl("lid", (0, 0, 0.39), 0.27, 0.06, "blue")
    cyl("lid_window", (0, 0, 0.425), 0.16, 0.012, "smoke_glass")
    display("READY", (0, -0.286, 0.17), 0.29)
    led((0.24, -0.286, 0.17))


def build_rack(a):
    for z in [0.035, 0.2]:
        cube("rack", (0, 0, z), (0.6, 0.28, 0.025), "blue", 0.01)
    for x in [-0.26, 0.26]:
        cube("leg", (x, 0, 0.12), (0.025, 0.27, 0.24), "blue", 0.007)
    for i in range(6):
        x = -0.215 + i * 0.086
        cyl("test_tube", (x, -0.03, 0.21), 0.023, 0.32, "glass")
        sphere("rounded_bottom", (x, -0.03, 0.055), (0.023, 0.023, 0.028), "glass")
        cyl("tube_content", (x, -0.03, 0.12), 0.019, 0.11, "water")
        cyl("cap", (x, -0.03, 0.375), 0.026, 0.026, "teal" if i % 2 else "blue")
    for i in range(3):
        x = -0.14 + i * 0.14
        cyl("pipette", (x, 0.08, 0.32), 0.015, 0.36, "white")
        cyl("pipette_button", (x, 0.08, 0.51), 0.025, 0.025, "blue")
        cyl("tip", (x, 0.08, 0.1), 0.012, 0.11, "glass", radius2=0.003)


def build_cabinet(a):
    w, d, h = a["size"]
    solvent = a.get("model") == "solvents"
    mat = "yellow" if solvent else "white"
    cube("back", (0, d / 2 - 0.03, h / 2), (w, 0.06, h), mat)
    for x in [-w / 2 + 0.03, w / 2 - 0.03]:
        cube("side", (x, 0, h / 2), (0.06, d, h), mat)
    for z in [0.06, 0.52, 1.06] if solvent else [0.08, 0.64, 1.18, 1.66]:
        cube("shelf", (0, 0, z), (w, d, 0.04), mat)
    # Transparent inspection panel makes inventories legible; doors open through API.
    cube(
        "door",
        (0, -d / 2 - 0.015, h / 2),
        (w - 0.07, 0.028, h - 0.12),
        "cabinet_glass" if not solvent else "amber_glass",
        0.01,
    )
    cube("door_handle", (w * 0.34, -d / 2 - 0.05, h / 2), (0.025, 0.045, 0.23), "metal")
    panel(a["label"], w - 0.08, -d / 2 - 0.045, h - 0.07)
    if solvent:
        text("symbol", "!", (-w * 0.33, -d / 2 - 0.054, 0.2), 0.12, "red")


def build_reagent(a):
    w, _d, h = a["size"]
    r = w * 0.42
    bodymat = "amber" if a["id"] in {"ethanol_01", "indicator_01"} else "bottle_glass"
    cyl("bottle", (0, 0, h * 0.38), r, h * 0.7, bodymat)
    cyl("shoulder", (0, 0, h * 0.75), r, h * 0.12, bodymat, radius2=r * 0.5)
    cyl("neck", (0, 0, h * 0.84), r * 0.5, h * 0.13, bodymat)
    cyl("cap", (0, 0, h * 0.95), r * 0.59, h * 0.13, "blue" if a["unit"] == "ml" else "navy")
    liquid = cyl(
        "liquid",
        (0, 0, h * 0.33),
        r * 0.86,
        h * 0.6,
        material(
            a["id"] + "_liquid",
            a["color"],
            rough=0.25,
            transmission=0.1 if a["unit"] == "ml" else 0,
        ),
    )
    liquid["base_z"] = 0.013
    liquid["max_height"] = h * 0.64
    cube("label", (0, -r - 0.003, h * 0.42), (w * 0.79, 0.009, h * 0.38), "white", 0.003)
    text(
        "chemical",
        a["label"],
        (0, -r - 0.01, h * 0.47),
        0.022 if len(a["label"]) < 10 else 0.016,
        "ink",
    )
    text("amount", f"{a['quantity']} {a['unit']}", (0, -r - 0.01, h * 0.35), 0.019, "ink")
    cube(
        "label_band",
        (0, -r - 0.01, h * 0.24),
        (w * 0.79, 0.006, 0.018),
        material(a["id"] + "_band", a["color"]),
        0.001,
    )


def build_sink(a):
    w, d, _h = a["size"]
    cube("basin", (0, 0, 0.025), (w, d, 0.05), "metal")
    cube("dark_basin", (0, 0, 0.055), (w - 0.13, d - 0.13, 0.025), "counter", 0.07)
    for x in [-w / 2 + 0.03, w / 2 - 0.03]:
        cube("rim", (x, 0, 0.08), (0.06, d, 0.09), "metal")
    for y in [-d / 2 + 0.03, d / 2 - 0.03]:
        cube("rim", (0, y, 0.08), (w, 0.06, 0.09), "metal")
    pts = [
        (0.12, 0.3, 0.07),
        (0.12, 0.3, 0.38),
        (0.12, 0.25, 0.47),
        (0.12, 0.07, 0.47),
        (0.12, -0.01, 0.39),
    ]
    tube("faucet", pts, 0.02, "metal")
    cube("lever", (0.22, 0.3, 0.13), (0.14, 0.034, 0.018), "blue")
    stream = cyl("water_stream", (0.12, -0.01, 0.24), 0.01, 0.3, "water")
    stream.hide_render = True
    stream.hide_set(True)
    cyl("drain", (0, 0, 0.074), 0.045, 0.01, "metal")


def build_eyewash(a):
    cyl("base", (0, 0, 0.03), 0.2, 0.06, "metal")
    cyl("pipe", (0, 0, 0.5), 0.035, 1, "green")
    sphere("bowl", (0, 0, 1.02), (0.24, 0.21, 0.08), "green")
    for x in [-0.11, 0.11]:
        tube("nozzle", [(x, 0, 1.03), (x, 0, 1.14), (x * 0.6, 0, 1.17)], 0.015, "metal")
        cyl("water_stream", (x * 0.6, 0, 1.23), 0.009, 0.12, "water")
    cube("pedal", (0, -0.15, 0.14), (0.23, 0.15, 0.04), "green")
    panel("EYEWASH", 0.4, 0.2, 1.35)


def build_waste(a):
    w, d, h = a["size"]
    cube(
        "container",
        (0, 0, h * 0.45),
        (w, d, h * 0.9),
        "yellow" if a["id"] == "waste_solvent" else "pale",
        0.055,
    )
    cyl("cap", (0, 0, h * 0.95), 0.09, 0.08, "navy")
    tube(
        "handle",
        [(-0.1, 0, h * 0.8), (-0.1, 0, h * 1.02), (0.1, 0, h * 1.02), (0.1, 0, h * 0.8)],
        0.02,
        "navy",
    )
    panel(a["label"], w - 0.02, -d / 2 - 0.015, h * 0.5)
    text("display", "0 / 10 L", (0, -d / 2 - 0.024, h * 0.27), 0.032, "ink")


def build_extinguisher(a):
    cyl("tank", (0, 0, 0.32), 0.12, 0.54, "red")
    sphere("shoulder", (0, 0, 0.59), (0.12, 0.12, 0.08), "red")
    cyl("neck", (0, 0, 0.68), 0.035, 0.12, "metal")
    cube("lever", (0.03, 0, 0.73), (0.19, 0.04, 0.025), "black")
    tube(
        "hose",
        [(0.04, 0, 0.7), (0.16, 0, 0.63), (0.17, 0, 0.2), (0.13, -0.03, 0.1)],
        0.015,
        "black",
    )
    cube("label", (0, -0.122, 0.38), (0.15, 0.006, 0.23), "white", 0.003)
    text("fire", "FIRE", (0, -0.127, 0.4), 0.042, "red")


BUILDERS = {
    "bench": build_bench,
    "hood": build_hood,
    "reactor": build_reactor,
    "hotplate": build_hotplate,
    "bath": build_bath,
    "oven": build_oven,
    "chiller": build_chiller,
    "balance": build_balance,
    "ph_meter": build_ph,
    "uvvis": build_spectrometer,
    "ftir": build_spectrometer,
    "centrifuge": build_centrifuge,
    "rack": build_rack,
    "cabinet": build_cabinet,
    "reagent": build_reagent,
    "sink": build_sink,
    "eyewash": build_eyewash,
    "waste": build_waste,
    "extinguisher": build_extinguisher,
}


def environment():
    cube("foundation", (0, 0, -0.17), (9.25, 7.75, 0.32), "navy", 0.1)
    cube("floor", (0, 0, 0.005), (8.9, 7.35, 0.055), "floor", 0.02)
    for x in range(-4, 5):
        cube("tile_joint", (x, 0, 0.035), (0.009, 7.3, 0.002), "grout", 0)
    for y in range(-3, 4):
        cube("tile_joint", (0, y, 0.035), (8.85, 0.009, 0.002), "grout", 0)
    cube("north_wall", (0, 3.64, 1.6), (9.05, 0.14, 3.2), "wall", 0.025)
    cube("west_wall", (-4.48, 0.03, 1.6), (0.14, 7.35, 3.2), "wall", 0.025)
    cube("north_skirt", (0, 3.53, 0.1), (8.9, 0.05, 0.16), "metal", 0.005)
    cube("west_skirt", (-4.38, 0, 0.1), (0.05, 7.25, 0.16), "metal", 0.005)
    cube("top_trim", (0, 3.54, 3.08), (8.9, 0.06, 0.1), "navy")
    cube("west_trim", (-4.39, 0, 3.08), (0.06, 7.3, 0.1), "navy")
    cube("north_band", (0, 3.552, 1.98), (8.85, 0.015, 0.025), "teal", 0.002)
    # Utility trunking above rear instruments, with separately modelled sockets.
    cube("service_rail", (1.5, 3.51, 1.45), (4.7, 0.08, 0.14), "pale")
    for x in [0, 0.65, 1.3, 1.95, 2.6, 3.25]:
        cube("outlet", (x, 3.454, 1.46), (0.13, 0.016, 0.1), "white", 0.005)
        for dx in [-0.026, 0.026]:
            cube("socket", (x + dx, 3.44, 1.46), (0.014, 0.006, 0.04), "navy", 0.003)
    cube("lab_sign", (0.6, 3.535, 2.62), (5.65, 0.045, 0.66), "navy", 0.02)
    text("wordmark", "SCIENCE OS  /  CHEMLAB", (0.6, 3.5, 2.69), 0.24, "white")
    text(
        "subtitle",
        "SMALL-SCALE CHEMISTRY  |  VIRTUAL INSTRUMENTS",
        (0.6, 3.495, 2.43),
        0.085,
        "screen",
    )
    # Tall daylight window on west wall.
    cube("window_frame", (-4.383, 0.48, 2.23), (0.045, 2.25, 1.32), "navy")
    cube("window", (-4.352, 0.48, 2.23), (0.02, 2.08, 1.16), "window")
    for y in [-0.18, 1.14]:
        cube("mullion", (-4.333, y, 2.23), (0.025, 0.035, 1.18), "white", 0.002)
    cube("noticeboard", (-4.335, -2.48, 2.24), (0.06, 1.2, 0.72), "navy")
    text(
        "notice",
        "REAGENT\nSTORAGE",
        (-4.296, -2.48, 2.26),
        0.13,
        "white",
        (math.pi / 2, 0, math.pi / 2),
    )
    # Deliberate floor zoning: inset bars and generous central circulation.
    for x in [-2.06, 2.06]:
        cube("island_zone", (x, -0.65, 0.04), (0.025, 2.05, 0.003), "teal", 0)
    for y in [-1.67, 0.37]:
        cube("island_zone", (0, y, 0.04), (4.15, 0.025, 0.003), "teal", 0)
    text("floor_title", "CHEMLAB  /  01", (0, -2.91, 0.042), 0.32, "navy", (0, 0, 0))
    text(
        "floor_subtitle",
        "REACTION   /   PREPARATION   /   ANALYSIS",
        (0, -3.27, 0.043),
        0.105,
        "ink",
        (0, 0, 0),
    )
    for x, y in [(-1.9, -2.18), (2.15, -0.25)]:
        cyl("stool_seat", (x, y, 0.52), 0.22, 0.09, "navy")
        cyl("stool_pole", (x, y, 0.28), 0.025, 0.45, "metal")
        ring("footrest", (x, y, 0.23), 0.16, 0.012, "metal")
        for i in range(5):
            ang = i * math.tau / 5
            tube(
                "stool_leg",
                [(x, y, 0.13), (x + 0.22 * math.cos(ang), y + 0.22 * math.sin(ang), 0.075)],
                0.014,
                "metal",
            )
    # Front plate on the plinth, visible in the overall render.
    text(
        "plinth_label",
        "SCIENCE OS     /     CHEMISTRY LABORATORY",
        (0, -3.885, -0.12),
        0.125,
        "white",
    )


def camera(name, loc, target, ortho=None):
    data = bpy.data.cameras.new(name)
    o = bpy.data.objects.new(name, data)
    COLLECTION.objects.link(o)
    o.location = loc
    o.rotation_euler = (Vector(target) - o.location).to_track_quat("-Z", "Y").to_euler()
    if ortho:
        data.type = "ORTHO"
        data.ortho_scale = ortho
    else:
        data.lens = 48
    data.clip_end = 200
    return o


def light(name, loc, energy, size, color, target):
    data = bpy.data.lights.new(name, "AREA")
    data.energy = energy
    data.shape = "DISK"
    data.size = size
    data.color = color
    o = bpy.data.objects.new(name, data)
    COLLECTION.objects.link(o)
    o.location = loc
    o.rotation_euler = (Vector(target) - o.location).to_track_quat("-Z", "Y").to_euler()


def main():
    global CURRENT, COLLECTION, M
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.name = "ChemLab | Virtual Chemistry Laboratory"
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.length_unit = "METERS"
    for name, color, metal, rough, trans, emit in [
        ("white", (0.78, 0.84, 0.88), 0.05, 0.32, 0, 0),
        ("pale", (0.56, 0.66, 0.72), 0.1, 0.4, 0, 0),
        ("navy", (0.019, 0.053, 0.084), 0.15, 0.3, 0, 0),
        ("ink", (0.018, 0.045, 0.065), 0, 0.6, 0, 0),
        ("counter", (0.037, 0.073, 0.088), 0.18, 0.26, 0, 0),
        ("metal", (0.44, 0.55, 0.61), 0.8, 0.24, 0, 0),
        ("blue", (0.022, 0.17, 0.39), 0.15, 0.29, 0, 0),
        ("teal", (0.016, 0.42, 0.44), 0.12, 0.32, 0, 0),
        ("green", (0.018, 0.38, 0.18), 0.1, 0.3, 0, 0),
        ("red", (0.64, 0.045, 0.028), 0.15, 0.3, 0, 0),
        ("yellow", (0.9, 0.57, 0.055), 0.08, 0.38, 0, 0),
        ("black", (0.008, 0.017, 0.022), 0.05, 0.32, 0, 0),
        ("glass", (0.86, 0.95, 1), 0, 0.08, 0.92, 0),
        ("glass_edge", (0.38, 0.76, 0.83), 0.05, 0.17, 0.3, 0),
        ("sash_glass", (0.83, 0.96, 1), 0, 0.08, 0.98, 0),
        ("bottle_glass", (0.82, 0.92, 0.92), 0, 0.12, 0.8, 0),
        ("cabinet_glass", (0.72, 0.85, 0.9), 0, 0.12, 0.9, 0),
        ("amber_glass", (0.95, 0.7, 0.23), 0, 0.15, 0.8, 0),
        ("amber", (0.34, 0.15, 0.025), 0, 0.19, 0.52, 0),
        ("smoke_glass", (0.06, 0.15, 0.19), 0.25, 0.19, 0.4, 0),
        ("water", (0.04, 0.46, 0.69), 0.08, 0.16, 0.28, 0),
        ("screen", (0.22, 0.93, 0.82), 0, 0.25, 0, 0.8),
        ("light", (0.76, 0.9, 1), 0, 0.25, 0, 3),
        ("window", (0.44, 0.76, 0.91), 0, 0.3, 0, 0.5),
        ("floor", (0.39, 0.49, 0.54), 0.05, 0.65, 0, 0),
        ("grout", (0.27, 0.35, 0.4), 0, 0.8, 0, 0),
        ("wall", (0.67, 0.76, 0.79), 0, 0.8, 0, 0),
    ]:
        M[name] = material(name, color, metal, rough, trans, emit)
    COLLECTION = bpy.data.collections.new("00 / ARCHITECTURE")
    scene.collection.children.link(COLLECTION)
    environment()
    zonecols = {}
    for a in ASSETS:
        if a["id"] in {"robot_01", "sample_tube_01"}:
            continue
        zone = a["zone"]
        if zone not in zonecols:
            zonecols[zone] = bpy.data.collections.new(zone.upper())
            scene.collection.children.link(zonecols[zone])
        COLLECTION = bpy.data.collections.new(a["id"] + " | " + a["name"])
        zonecols[zone].children.link(COLLECTION)
        CURRENT = bpy.data.objects.new(a["id"], None)
        COLLECTION.objects.link(CURRENT)
        CURRENT.empty_display_type = "PLAIN_AXES"
        CURRENT.empty_display_size = 0.055
        CURRENT.location = a["location"]
        CURRENT["lab_id"] = a["id"]
        CURRENT["lab_root"] = True
        CURRENT["name_zh"] = a["name"]
        CURRENT["kind"] = a["kind"]
        CURRENT["api_endpoint"] = "http://127.0.0.1:8877/api/v1/assets/" + a["id"]
        CURRENT["supported_actions"] = ", ".join(a["actions"])
        if a["kind"] == "vessel":
            if a.get("model") == "condenser":
                build_condenser(a)
            else:
                vessel_body(
                    "flask" if a.get("model") == "flask" else "beaker",
                    a["size"][0] / 2,
                    a["size"][2],
                )
        else:
            BUILDERS[a["kind"]](a)
        for o in CURRENT.children:
            o["base_location"] = list(o.location)
            o["base_rotation"] = list(o.rotation_euler)
        if a["kind"] in {"reagent", "reactor", "vessel", "waste"}:
            CURRENT["capacity"] = a.get("capacity_ml", a.get("quantity", 0))
    CURRENT = None
    COLLECTION = bpy.data.collections.new("90 / CAMERAS & LIGHTING")
    scene.collection.children.link(COLLECTION)
    scene.camera = camera("Camera_Overview", (11, -15, 12), (0, 0.1, 0.7), 13.3)
    camera("Camera_Reaction", (1, -5.3, 4.5), (-2.55, 2.4, 1.45), 4.5)
    camera("Camera_Analysis", (5, -3.3, 4.25), (1.3, 2.5, 1.22), 5.5)
    camera("Camera_Preparation", (4, -5, 4), (0, -0.65, 1.1), 5.1)
    light("Key softbox", (1, -3, 9), 2400, 7, (0.82, 0.91, 1), (0, 0, 0))
    light("Daylight", (-3, -1, 5), 1400, 5, (0.63, 0.84, 1), (-1, 1, 0))
    light("Warm rim", (3, 5, 7), 2400, 5, (1, 0.88, 0.69), (0, 1, 0))
    light("Front fill", (4, -7, 3), 1100, 5, (0.81, 1, 0.99), (0, 0, 1))
    world = bpy.data.worlds.new("Studio atmosphere")
    scene.world = world
    world.color = (0.2, 0.2, 0.2)
    world.use_nodes = True
    world.node_tree.nodes["Background"].inputs[0].default_value = (0.12, 0.17, 0.22, 1)
    world.node_tree.nodes["Background"].inputs[1].default_value = 0.4
    scene.render.engine = "CYCLES"
    scene.cycles.samples = 48
    scene.cycles.use_denoising = True
    scene.cycles.max_bounces = 10
    scene.cycles.transmission_bounces = 8
    try:
        prefs = bpy.context.preferences.addons["cycles"].preferences
        prefs.compute_device_type = "OPTIX"
        prefs.get_devices()
        for dev in prefs.devices:
            dev.use = dev.type == "OPTIX"
        if any(d.use for d in prefs.devices):
            scene.cycles.device = "GPU"
    except Exception as e:
        print("GPU fallback", e)
    scene.render.resolution_x = 1800
    scene.render.resolution_y = 1400
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.film_transparent = False
    scene.view_settings.view_transform = "AgX"
    scene.view_settings.exposure = -0.45
    scene["chemlab_version"] = VERSION
    scene["chemlab_root"] = str(ROOT)
    scene["api_base"] = "http://127.0.0.1:8877"
    scene["simulation_note"] = (
        "Virtual educational laboratory. Analytical results are synthetic, not validated chemistry."
    )
    scene["asset_count"] = len(ASSETS)
    from .polish_glass import polish

    polish()
    # A runnable Text block is available without enabling global auto-run.
    boot = bpy.data.texts.new("START_CHEMLAB.py")
    boot.write(
        "import sys\nfrom pathlib import Path\nimport bpy\n"
        "p=Path(bpy.data.filepath).parents[2]\n"
        "if str(p) not in sys.path: sys.path.insert(0,str(p))\n"
        "from apps.blender_lab import blender_bridge\nblender_bridge.register()\n"
    )
    welcome = bpy.data.texts.new("README / 使用说明")
    welcome.write(
        "ChemWorld Blender Lab\n"
        "Run uv run --no-sync python -m apps.blender_lab --blender /path/to/blender\n"
        "See apps/blender_lab/README.md. Physical hardware output is not enabled.\n"
    )
    for scr in bpy.data.screens:
        for area in scr.areas:
            if area.type == "VIEW_3D":
                area.spaces.active.region_3d.view_perspective = "CAMERA"
                area.spaces.active.overlay.show_overlays = False
                sh = area.spaces.active.shading
                sh.type = "MATERIAL"
                sh.use_scene_world = False
                sh.use_scene_lights = False
                area.spaces.active.region_3d.view_camera_zoom = 0
    bpy.ops.object.select_all(action="DESELECT")
    bpy.context.view_layer.objects.active = bpy.data.objects["reactor_01"]
    bpy.data.objects["reactor_01"].select_set(True)
    # Empty vessels until the included demo transfers tracked inventory.
    for a in ASSETS:
        if a["kind"] in {"reactor", "vessel"}:
            for o in bpy.data.objects[a["id"]].children:
                if o.get("component") == "liquid":
                    o.hide_render = True
                    o.hide_set(True)
    ROOT.mkdir(parents=True, exist_ok=True)
    (ROOT / "renders").mkdir(exist_ok=True)
    (ROOT / "asset_manifest.json").write_text(
        json.dumps([public_asset(a) for a in ASSETS], ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    from .tour import install

    install()
    from .robot_visual import build

    build()
    bpy.ops.wm.save_as_mainfile(filepath=str(ROOT / "ChemLab.blend"))
    print("BUILD_COMPLETE", len(ASSETS), "assets", len(bpy.data.objects), "objects")
    if "--render" in sys.argv:
        scene.render.filepath = str(ROOT / "renders" / "overview.png")
        bpy.ops.render.render(write_still=True)


if __name__ == "__main__":
    main()
