# Blender executes --python files outside the package import machinery.
if __package__ in {None, ""}:
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    __package__ = "apps.blender_lab"

"""Run with: blender ChemLab.blend --python startup.py"""
import sys
from pathlib import Path

import bpy

ROOT = Path(__file__).resolve().parent


def initialize():
    from . import blender_bridge

    blender_bridge.register()
    # Region visibility must only be changed on a live window's active screen.
    # Updating inactive screens can crash Blender 5.2's ED_area_init.
    for window in bpy.context.window_manager.windows:
        with bpy.context.temp_override(window=window):
            for area in window.screen.areas:
                if area.type == "VIEW_3D":
                    area.spaces.active.show_region_ui = True
                    area.spaces.active.region_3d.view_perspective = "CAMERA"
                    area.spaces.active.overlay.show_overlays = False
    return None


bpy.app.timers.register(initialize, first_interval=1.0)
