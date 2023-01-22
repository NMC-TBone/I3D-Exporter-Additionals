import bpy


def check_i3d_exporter_type():
    giants_i3d = False
    stjerne_i3d = False
    for a in bpy.context.preferences.addons:
        if a.module == "io_export_i3d":
            giants_i3d = True
        if a.module == "i3dio":
            stjerne_i3d = True
    return giants_i3d, stjerne_i3d


def check_obj_type(obj):
    if len(bpy.context.selected_objects) > 0:
        mode = bpy.context.object.mode
        for obj in bpy.context.selected_objects:
            if not obj.type == "MESH":
                continue
            if not mode == 'OBJECT':
                bpy.ops.object.mode_set(mode='OBJECT')
