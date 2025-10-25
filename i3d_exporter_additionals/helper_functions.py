import importlib
import sys

import addon_utils
import bpy
from mathutils import Matrix, Vector

ATTR_PREFIX = "userAttribute_"


def check_i3d_exporter_type() -> tuple[bool, bool]:
    giants_enabled = addon_utils.check("io_export_i3d")[1] or addon_utils.check("io_export_i3d_10_0_0")[1]
    i3dio_enabled = any(a.module.endswith(".i3dio") for a in bpy.context.preferences.addons.values())
    return giants_enabled, i3dio_enabled


def get_i3dio_preferences() -> bpy.types.AddonPreferences | None:
    i3dio = next((a for a in bpy.context.preferences.addons.values() if a.module.endswith(".i3dio")), None)
    return i3dio.preferences if i3dio else None


def check_obj_type(obj):
    if len(bpy.context.selected_objects) > 0:
        mode = bpy.context.object.mode
        for obj in bpy.context.selected_objects:
            if not obj.type == "MESH":
                continue
            if not mode == "OBJECT":
                bpy.ops.object.mode_set(mode="OBJECT")


def get_from_addon_module(module_path: str, attr_name: str):
    """
    Fetches an attribute (variable, class, function, etc.) from a (possibly nested) Blender addon module.

    Args:
        module_path (str): The Python module path, e.g. "i3dio.ui.collision_data"
        attr_name (str): The name of the attribute to fetch.

    Returns:
        The object if found, otherwise None.
    """
    mod = sys.modules.get(module_path)
    if mod is None:
        try:
            mod = importlib.import_module(module_path)
        except ImportError:
            print(f"Module {module_path!r} could not be imported.")
            return None
    return getattr(mod, attr_name, None)


def apply_transforms(obj: bpy.types.Object, use_loc=False, use_rot=False, use_scale=False, apply_all=False) -> None:
    """
    Applies orientation for object

    https://blender.stackexchange.com/questions/159538/how-to-apply-all-transformations-to-an-object-at-low-level
    """
    if apply_all:
        use_loc = True
        use_rot = True
        use_scale = True

    mb = obj.matrix_basis
    identity_matrix = Matrix()
    loc, _rot, scale = mb.decompose()

    # rotation
    t = Matrix.Translation(loc)
    r = mb.to_3x3().normalized().to_4x4()
    s = Matrix.Diagonal(scale).to_4x4()

    transform = [identity_matrix] * 3
    basis = [t, r, s]

    def swap(i):
        transform[i], basis[i] = basis[i], transform[i]

    if use_loc:
        swap(0)
    if use_rot:
        swap(1)
    if use_scale:
        swap(2)

    matrix = transform[0] @ transform[1] @ transform[2]
    if hasattr(obj.data, "transform"):
        obj.data.transform(matrix)
    for c in obj.children:
        c.matrix_local = matrix @ c.matrix_local

    obj.matrix_basis = basis[0] @ basis[1] @ basis[2]
    return


def get_curve_length(curve: bpy.types.Object) -> float:
    """
    Returns length of curve and if the scale is not 1 1 1, it will be applied first to get the correct result
    """
    if curve.scale != Vector((1, 1, 1)):
        print(f"{curve.name} scale is not 1 1 1, applying scale automatically.")
        apply_transforms(curve, use_scale=True)
    length = curve.data.splines[0].calc_length(resolution=1024)
    return length


def is_blend_saved():
    """
    Check if blend file is saved
    """
    if bpy.data.is_saved:
        return True
    return False


def split_key(key: str) -> tuple[str, str] | None:
    """Return (type, name) if this is a userAttribute key; else None."""
    if not key.startswith(ATTR_PREFIX):
        return None
    parts = key.split("_", 2)
    if len(parts) < 3:
        return None
    # parts: ["userAttribute", "{type}", "{name...}"]
    return parts[1], parts[2]


def iter_user_attrs(obj: bpy.types.Object):
    """Yield (key, type, name) for all userAttribute_* on obj."""
    for k in obj.keys():
        sp = split_key(k)
        if sp:
            a_type, a_name = sp
            yield k, a_type, a_name
