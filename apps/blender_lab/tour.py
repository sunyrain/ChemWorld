"""Native camera keyframes: playable with Blender's timeline, with no API needed."""

from pathlib import Path

import bpy

ROOT = Path(__file__).resolve().parent
NAME = "Camera_ChemLab_Tour"
FPS = 20
END = 400


def install():
    scene = bpy.context.scene
    cam = bpy.data.objects.get(NAME)
    if cam is None:
        data = bpy.data.cameras.new(NAME)
        cam = bpy.data.objects.new(NAME, data)
        bpy.data.collections["90 / CAMERAS & LIGHTING"].objects.link(cam)
    cam.animation_data_clear()
    cam.data.animation_data_clear()
    cam.data.type = "ORTHO"
    cam.rotation_mode = "XYZ"
    cam["description"] = "20-second laboratory camera tour. Spacebar plays the keyframes."
    shots = [
        (1, "Overview", 18.3),
        (32, "Overview", 17.5),
        (90, "Reaction", 5.6),
        (118, "Reaction", 5.3),
        (177, "Analysis", 6.8),
        (208, "Analysis", 6.4),
        (267, "Preparation", 6.2),
        (307, "Preparation", 5.8),
        (375, "Overview", 18.3),
        (400, "Overview", 18.3),
    ]
    for frame, name, scale in shots:
        source = bpy.data.objects["Camera_" + name]
        cam.location = source.location
        cam.rotation_euler = source.rotation_euler
        cam.data.ortho_scale = scale
        cam.keyframe_insert(data_path="location", frame=frame)
        cam.keyframe_insert(data_path="rotation_euler", frame=frame)
        cam.data.keyframe_insert(data_path="ortho_scale", frame=frame)
    for marker in list(scene.timeline_markers):
        if marker.name.startswith("ChemLab /"):
            scene.timeline_markers.remove(marker)
    for frame, title in [
        (1, "全景"),
        (90, "反应装置"),
        (177, "表征仪器"),
        (267, "配液与加热"),
        (375, "全景"),
    ]:
        scene.timeline_markers.new("ChemLab / " + title, frame=frame)
    scene.frame_start = 1
    scene.frame_end = END
    scene.render.fps = FPS
    scene.sync_mode = "FRAME_DROP"
    scene["chemlab_tour"] = (
        "20 seconds: overview, reaction, analysis, preparation. Native camera keyframes."
    )
    return cam


def prepare_view(context):
    scene = context.scene
    scene.camera = bpy.data.objects.get(NAME) or install()
    scene.frame_set(1)
    scene.render.resolution_x = 1280
    scene.render.resolution_y = 720
    scene.render.resolution_percentage = 100
    for area in context.screen.areas:
        if area.type == "VIEW_3D":
            shading = area.spaces.active.shading
            shading.type = "MATERIAL"
            shading.use_scene_lights = True
            shading.use_scene_world = True
            region = area.spaces.active.region_3d
            region.view_perspective = "CAMERA"
            region.view_camera_zoom = 20
            region.view_camera_offset = (0.065, 0)


def play(context):
    if context.screen.is_animation_playing:
        bpy.ops.screen.animation_cancel(restore_frame=False)
    prepare_view(context)
    bpy.ops.screen.animation_play()


def pause(context):
    if context.screen.is_animation_playing:
        bpy.ops.screen.animation_cancel(restore_frame=False)


if __name__ == "__main__":
    install()
