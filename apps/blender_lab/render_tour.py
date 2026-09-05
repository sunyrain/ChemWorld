# Blender executes --python files outside the package import machinery.
if __package__ in {None, ""}:
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    __package__ = "apps.blender_lab"

"""Render the native tour from the saved model without changing the live experiment."""
import json
import math
import sys
import time
from pathlib import Path

import bpy

ROOT = Path(__file__).resolve().parent
from . import blender_bridge as bridge
from . import tour
from .catalog import ASSETS
from .client import ChemLabClient

(ROOT / "renders").mkdir(exist_ok=True)
(ROOT / "verification").mkdir(exist_ok=True)
scene = bpy.context.scene
snapshot = ChemLabClient().request("/api/v1/state")
bridge.COMPONENTS = {a["id"]: list(bpy.data.objects[a["id"]].children) for a in ASSETS}
bridge.LAST_SELECTED = snapshot["selected"]
bridge.apply_snapshot(snapshot)
scene.camera = tour.install()
scene.render.resolution_x = 1280
scene.render.resolution_y = 720
scene.render.resolution_percentage = 100
scene.render.engine = "CYCLES"
scene.cycles.samples = 12
scene.cycles.use_denoising = True
scene.cycles.max_bounces = 6
scene.cycles.use_adaptive_sampling = True
scene.cycles.adaptive_threshold = 0.1
scene.render.use_persistent_data = True
scene.cycles.device = "CPU"
try:
    prefs = bpy.context.preferences.addons["cycles"].preferences
    prefs.compute_device_type = "OPTIX"
    prefs.get_devices()
    for device in prefs.devices:
        device.use = device.type == "OPTIX"
    if any(device.use for device in prefs.devices):
        scene.cycles.device = "GPU"
except Exception as exc:
    print("GPU unavailable; rendering on CPU:", exc, flush=True)

# Deterministic rotation for this recorded visualization. The actual API state is untouched.
for asset_id in ["reactor_01", "beaker_01"]:
    for obj in bridge.objects_for(asset_id):
        if obj.get("component") in {"impeller", "stirbar"}:
            initial = obj.rotation_euler.z
            obj.rotation_euler.z = initial
            obj.keyframe_insert(data_path="rotation_euler", index=2, frame=1)
            obj.rotation_euler.z = initial + math.tau * 40
            obj.keyframe_insert(data_path="rotation_euler", index=2, frame=tour.END)

scene.frame_set(1)
if "--eevee" in sys.argv:
    scene.render.engine = "CYCLES" if "--cycles" in sys.argv else "BLENDER_EEVEE"
if "--still" in sys.argv:
    scene.render.image_settings.file_format = "PNG"
    scene.render.filepath = str(ROOT / "renders" / "tour_preview.png")
    bpy.ops.render.render(write_still=True)
    print(
        "FORMATS",
        [
            i.identifier
            for i in scene.render.image_settings.bl_rna.properties["file_format"].enum_items
        ],
        flush=True,
    )
    print("RENDER_PROPS", list(scene.render.bl_rna.properties.keys()), flush=True)
else:
    scene.render.image_settings.media_type = "VIDEO"
    scene.render.image_settings.file_format = "FFMPEG"
    scene.render.ffmpeg.format = "MPEG4"
    scene.render.ffmpeg.codec = "H264"
    scene.render.ffmpeg.constant_rate_factor = "MEDIUM"
    scene.render.ffmpeg.ffmpeg_preset = "GOOD"
    scene.render.filepath = str(ROOT / "renders" / "ChemLab_Tour.mp4")
    start = time.time()
    bpy.ops.render.render(animation=True)
    result = {
        "success": True,
        "frames": tour.END,
        "fps": tour.FPS,
        "duration_seconds": 20,
        "width": 1280,
        "height": 720,
        "elapsed_seconds": time.time() - start,
        "file": scene.render.filepath,
        "api_revision": snapshot["revision"],
    }
    (ROOT / "verification" / "tour_render.json").write_text(
        json.dumps(result, indent=2), encoding="utf-8"
    )
    print("TOUR_RENDERED", json.dumps(result), flush=True)
