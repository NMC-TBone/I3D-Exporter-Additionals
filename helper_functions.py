import bpy
from mathutils import Vector, Matrix


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


def apply_transforms(ob_name, use_loc=False, use_rot=False, use_scale=False, apply_all=False):
    """
    Applies scale for object

    https://blender.stackexchange.com/questions/159538/how-to-apply-all-transformations-to-an-object-at-low-level
    """
    if apply_all:
        use_loc = True
        use_rot = True
        use_scale = True

    ob = bpy.data.objects[ob_name]
    mb = ob.matrix_basis
    I = Matrix()
    loc, rot, scale = mb.decompose()

    # rotation
    t = Matrix.Translation(loc)
    r = mb.to_3x3().normalized().to_4x4()
    s = Matrix.Diagonal(scale).to_4x4()

    transform = [I] * 3
    basis = [t, r, s]

    def swap(i):
        transform[i], basis[i] = basis[i], transform[i]

    if use_loc:
        swap(0)
    if use_rot:
        swap(1)
    if use_scale:
        swap(2)

    M = transform[0] @ transform[1] @ transform[2]
    if hasattr(ob.data, "transform"):
        ob.data.transform(M)
    for c in ob.children:
        c.matrix_local = M @ c.matrix_local

    ob.matrix_basis = basis[0] @ basis[1] @ basis[2]
    return


def get_curve_length(curve_name):
    """
    Returns length of curve and if the scale is not 1 1 1, it will be applied first to get the correct result
    """
    if bpy.data.objects[curve_name].scale != Vector((1, 1, 1)):
        print(f"{curve_name} scale is not 1 1 1, applying scale automatically.")
        apply_transforms(curve_name, use_scale=True)
    length = bpy.data.objects[curve_name].data.splines[0].calc_length(resolution=1024)
    return length
