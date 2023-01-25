import bpy
from mathutils import Vector

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


def get_curve_length(curve_name):
    """
    Returns length of curve and if the scale is not 1 1 1, it will be applied first to get the correct result
    """
    if bpy.data.objects[curve_name].scale != Vector((1, 1, 1)):
        print(f"{curve_name} scale is not 1 1 1, this can lead to wrong result.")
    length = bpy.data.objects[curve_name].data.splines[0].calc_length(resolution=1024)
    return length
