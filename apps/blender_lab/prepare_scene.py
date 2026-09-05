# Blender executes --python files outside the package import machinery.
if __package__ in {None, ""}:
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    __package__ = "apps.blender_lab"

"""Prepare a portable baseline from an open model; does not load a user's runtime inventory."""

import tempfile
from pathlib import Path

import bpy
from mathutils import Vector

from . import blender_bridge as bridge
from .catalog import ASSETS, CATALOG
from .engine import Lab

root = Path(__file__).resolve().parent
scene = bpy.context.scene
scene["chemlab_root"] = "//"
scene["api_base"] = "http://127.0.0.1:8877"
scene["integration"] = "chemworld-blender-1"
scene.render.filepath = "//renders/overview.png"
scene.render.resolution_x = 1800
scene.render.resolution_y = 1400
scene.camera = bpy.data.objects["Camera_Overview"]
for key in list(scene.keys()):
    if key.startswith("chemworld_public"):
        del scene[key]
for asset in ASSETS:
    bpy.data.objects[asset["id"]]["api_endpoint"] = (
        scene["api_base"] + "/api/v1/assets/" + asset["id"]
    )
bridge.COMPONENTS = {aid: list(bpy.data.objects[aid].children) for aid in CATALOG}
with tempfile.TemporaryDirectory() as data_dir:
    lab = Lab(data_dir)
    snapshot = lab.snapshot()
    bridge.LAST_SELECTED = snapshot["selected"]
    errors = bridge.apply_snapshot(snapshot)
    if errors:
        raise RuntimeError(errors)
bpy.context.view_layer.update()
if len(bridge.COMPONENTS) != 36 or len(bridge.COMPONENTS["robot_01"]) != 39:
    raise RuntimeError("Scene assets are incomplete")
for wheel in (o for o in bridge.COMPONENTS["robot_01"] if o.get("component") == "wheel"):
    axle = wheel.matrix_basis.to_3x3() @ Vector((0, 0, 1))
    if (axle.normalized() - Vector((1, 0, 0))).length > 1e-5:
        raise RuntimeError("Wheel axle is misaligned")
for text in list(bpy.data.texts):
    bpy.data.texts.remove(text)
boot = bpy.data.texts.new("START_CHEMLAB.py")
boot.write(
    "import sys\nfrom pathlib import Path\nimport bpy\n"
    "p=Path(bpy.data.filepath).parents[2]\n"
    "if str(p) not in sys.path: sys.path.insert(0,str(p))\n"
    "from apps.blender_lab import blender_bridge\nblender_bridge.register()\n"
)
scene.frame_set(1)
bpy.ops.wm.save_as_mainfile(filepath=str(root / "ChemLab.blend"))
print("PORTABLE_SCENE_READY: 36 assets, 39 robot parts, default inventory, relative startup")
