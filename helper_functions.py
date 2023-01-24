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


def get_curve_length(curve_obj):
    """
    Returns length of curve and if the scale is not 1 1 1, it will be applied first to get the correct result
    """
    if curve_obj.scale != Vector((1, 1, 1)):
        print(f"{curve_obj.name} scale is not 1 1 1, scale will be applied.")
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    length = curve_obj.data.splines[0].calc_length(resolution=1024)
    return length
