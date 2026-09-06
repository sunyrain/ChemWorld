# Blender executes --python files outside the package import machinery.
if __package__ in {None, ""}:
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    __package__ = "apps.blender_lab"

"""Readable transparent display materials for small-scale apparatus."""
import bpy


def polish():
    for name, reflection in [
        ("glass", 0.08),
        ("sash_glass", 0.035),
        ("bottle_glass", 0.09),
        ("cabinet_glass", 0.045),
        ("amber_glass", 0.085),
    ]:
        mat = bpy.data.materials.get(name)
        if not mat:
            continue
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        bs = nodes.get("Principled BSDF")
        bs.inputs["Transmission Weight"].default_value = 0
        bs.inputs["Roughness"].default_value = 0.12
        transparent = nodes.get("Clear visibility") or nodes.new("ShaderNodeBsdfTransparent")
        transparent.name = "Clear visibility"
        transparent.inputs[0].default_value = (1, 1, 1, 1)
        mix = nodes.get("Readable glass") or nodes.new("ShaderNodeMixShader")
        mix.name = "Readable glass"
        mix.inputs[0].default_value = reflection
        links.new(transparent.outputs[0], mix.inputs[1])
        links.new(bs.outputs[0], mix.inputs[2])
        links.new(mix.outputs[0], nodes.get("Material Output").inputs["Surface"])
    bpy.context.scene["glass_display_note"] = (
        "Glass uses a transparent display material to keep contents readable."
    )


if __name__ == "__main__":
    import sys
    from pathlib import Path

    root = Path(__file__).resolve().parent
    sys.path.insert(0, str(root))
    from . import blender_bridge as bridge
    from .catalog import ASSETS
    from .client import ChemLabClient

    snap = ChemLabClient().request("/api/v1/state")
    bridge.COMPONENTS = {a["id"]: list(bpy.data.objects[a["id"]].children) for a in ASSETS}
    bridge.LAST_SELECTED = snap["selected"]
    bridge.apply_snapshot(snap)
    polish()
    s = bpy.context.scene
    s.camera = bpy.data.objects["Camera_Preparation"]
    s.render.resolution_x = 1400
    s.render.resolution_y = 1000
    s.cycles.samples = 48
    p = bpy.context.preferences.addons["cycles"].preferences
    p.compute_device_type = "OPTIX"
    p.get_devices()
    for d in p.devices:
        d.use = d.type == "OPTIX"
    s.cycles.device = "GPU"
    s.render.filepath = str(root / "renders" / "glass_check.png")
    bpy.ops.render.render(write_still=True)
