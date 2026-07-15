from __future__ import annotations

import importlib
import sys
from typing import TypeVar

import bpy
from mathutils import Matrix, Vector

ATTR_PREFIX = "userAttribute_"

T = TypeVar("T")


def get_enabled_addon(module_or_suffix: str) -> bpy.types.Addon | None:
    """Returns the enabled Addon entry from bpy prefs"""
    addons = bpy.context.preferences.addons

    # legacy add-ons
    add = addons.get(module_or_suffix)
    if add is not None:
        return add
    # Extension add-ons
    suffix = f".{module_or_suffix.lstrip('.')}"
    return next((a for a in addons.values() if a.module.endswith(suffix)), None)


def get_addon_module_name(module_or_suffix: str) -> str | None:
    add = get_enabled_addon(module_or_suffix)
    return add.module if add else None


def get_addon_preferences(module_or_suffix: str) -> bpy.types.AddonPreferences | None:
    add = get_enabled_addon(module_or_suffix)
    return add.preferences if add else None


def addon_submodule(base_module: str, relative_module: str) -> str:
    relative_module = relative_module.lstrip(".")
    return f"{base_module}.{relative_module}" if relative_module else base_module


def get_from_addon(
    addon_module_or_suffix: str,
    relative_module: str,
    attr_name: str,
    *,
    default: T | None = None,
) -> T | None:
    """
    Fetch an attribute from an enabled Blender add-on, handling extension prefixes.
    Example:
      get_from_addon("i3dio", "ui.collision_data", "COLLISIONS")
    """
    base = get_addon_module_name(addon_module_or_suffix)
    if base is None:
        return default
    module_path = addon_submodule(base, relative_module)
    mod = sys.modules.get(module_path)
    if mod is None:
        try:
            mod = importlib.import_module(module_path)
        except ModuleNotFoundError:
            return default
    return getattr(mod, attr_name, default)


def get_enabled_addons_by_prefix(module_prefix: str) -> list[bpy.types.Addon]:
    return [
        addon
        for addon in bpy.context.preferences.addons.values()
        if (name := addon.module.rsplit(".", 1)[-1]) == module_prefix or name.startswith(f"{module_prefix}_")
    ]


def check_i3d_exporter_type() -> tuple[bool, bool]:
    return bool(get_enabled_addons_by_prefix("io_export_i3d")), get_addon_module_name("i3dio") is not None


def check_obj_type(obj):
    if len(bpy.context.selected_objects) > 0:
        mode = bpy.context.object.mode
        for obj in bpy.context.selected_objects:
            if not obj.type == "MESH":
                continue
            if not mode == "OBJECT":
                bpy.ops.object.mode_set(mode="OBJECT")


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
