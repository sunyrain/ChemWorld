"""Export the existing scene for the web viewer without changing the .blend source."""

import argparse
import sys
from pathlib import Path

import bpy


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(sys.argv[sys.argv.index("--") + 1 :])
    args.output.parent.mkdir(parents=True, exist_ok=True)
    scene = bpy.context.scene
    scene.frame_set(1)
    # The saved scene remains untouched. Converted text retains reader-visible instrument labels.
    bpy.ops.object.select_all(action="DESELECT")
    for obj in scene.objects:
        if obj.type == "FONT" and "SCIENCE OS" in obj.data.body:
            obj.data.body = obj.data.body.replace("SCIENCE OS", "CHEMWORLD")
        if obj.type in {"MESH", "FONT", "CURVE", "EMPTY"}:
            obj.hide_set(False)
            obj.select_set(True)
    print(f"Export: {len(bpy.context.selected_objects)} scene objects selected", flush=True)
    bpy.ops.export_scene.gltf(
        filepath=str(args.output),
        export_format="GLB",
        use_selection=True,
        export_apply=True,
        export_extras=True,
        export_animations=False,
        export_cameras=False,
        export_lights=False,
        export_yup=True,
    )
    print(f"Export completed 1/1: {args.output.stat().st_size / 1e6:.2f} MB; ETA 0s", flush=True)


if __name__ == "__main__":
    main()
