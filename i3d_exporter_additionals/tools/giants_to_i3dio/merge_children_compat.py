"""Convert importer-split Merge Children roots to zero-vertex meshes for i3dio."""

import re

import bpy

from .logging_config import logger

_NATURAL_PARTS = re.compile(r"(\d+)")
_SLOT_KEY = "_i3d_mergeChildrenSlot"

MergeChildrenRoots = list[tuple[bpy.types.Object, int]]


def _natural_key(obj: bpy.types.Object) -> list[int | str]:
    """Mirror the Community Exporter's natural child-name ordering."""
    return [int(x) if x.isdigit() else x.lower() for x in _NATURAL_PARTS.split(obj.name)]


def is_merge_children_empty(obj: bpy.types.Object) -> bool:
    return obj.type == "EMPTY" and bool(obj.get("i3D_mergeChildren", obj.get("I3D_mergeChildren", False)))


def _validate_root(root: bpy.types.Object, children: list[bpy.types.Object]) -> int:
    if root.library or root.override_library or not root.users_collection:
        raise ValueError(f"{root.name}: linked/override or unlinked Merge Children root")
    if root.animation_data or root.constraints or root.instance_collection:
        raise ValueError(
            f"{root.name}: animated, constrained or instanced Merge Children root; "
            "automatic replacement could lose data"
        )
    if root.parent is not None and root.parent_type != "OBJECT":
        raise ValueError(f"{root.name}: unsupported non-object parent")

    if any(child.type != "MESH" or child.parent_type != "OBJECT" for child in children):
        raise ValueError(f"{root.name}: expected direct mesh children")

    children = sorted(children, key=_natural_key)
    if root.i3d_merge_children.reverse_order:
        children.reverse()
    slots = [child.get(_SLOT_KEY) for child in children]
    if any(type(slot) is not int for slot in slots):
        raise ValueError(f"{root.name}: expected integer slot metadata on every Merge Children child")

    # The Community Exporter generates generic g as (child_index * steps) / 32767.
    step = slots[1] - slots[0] if len(slots) > 1 else 1
    if not 1 <= step <= 10 or slots[0] != 0 or any(slot != index * step for index, slot in enumerate(slots)):
        raise ValueError(
            f"{root.name}: original g slots {slots[:12]} do not match "
            "Community Exporter child ordering; conversion cancelled"
        )
    return step


def plan_merge_children_empty_roots() -> MergeChildrenRoots:
    """Validate importer-marked roots before migration changes the file."""
    roots = []
    for root in bpy.data.objects:
        if not is_merge_children_empty(root):
            continue
        children = list(root.children)
        if not any(_SLOT_KEY in child for child in children):
            logger.warning("%s: Skipping Merge Children Empty without importer slot metadata", root.name)
            continue
        roots.append((root, _validate_root(root, children)))
    return roots


def _replace_empty(root: bpy.types.Object, interpolation_steps: int) -> None:
    original_name = root.name
    view_layer = bpy.context.view_layer
    was_active = view_layer.objects.active == root
    was_selected = root.select_get()
    was_hidden = root.hide_get()

    mesh = bpy.data.meshes.new(original_name + "_MergeChildrenRoot")
    replacement = bpy.data.objects.new(original_name + "_MergeChildrenRoot", mesh)

    # Copy exporter-relevant object and importer IDProperties (including mapping
    # data and originalNodeId). Shape-level GIANTS properties will migrate onto
    # the new mesh datablock in the regular object migration pass.
    for key in root.keys():
        if key == "_RNA_UI":
            continue
        replacement[key] = root[key]
        try:
            replacement.id_properties_ui(key).update(**root.id_properties_ui(key).as_dict())
        except (AttributeError, TypeError, ValueError):
            pass  # UI metadata is optional; values were copied above.

    replacement.parent = root.parent
    replacement.matrix_parent_inverse = root.matrix_parent_inverse
    replacement.rotation_mode = root.rotation_mode
    replacement.location = root.location
    replacement.rotation_euler = root.rotation_euler
    replacement.rotation_quaternion = root.rotation_quaternion
    replacement.rotation_axis_angle = root.rotation_axis_angle
    replacement.scale = root.scale
    replacement.delta_location = root.delta_location
    replacement.delta_rotation_euler = root.delta_rotation_euler
    replacement.delta_rotation_quaternion = root.delta_rotation_quaternion
    replacement.delta_scale = root.delta_scale
    replacement.hide_render = root.hide_render
    replacement.hide_viewport = root.hide_viewport
    replacement.display_type = root.display_type
    replacement.color = root.color[:]
    merge_settings = replacement.i3d_merge_children
    merge_settings.interpolation_steps = interpolation_steps
    merge_settings.reverse_order = root.i3d_merge_children.reverse_order
    merge_settings.apply_transforms = root.i3d_merge_children.apply_transforms
    replacement["_i3d_kind"] = "Shape"

    # Remap collections and object references, including child parent pointers.
    # Keeping the same parent space lets Blender evaluate the children's own transforms.
    root.user_remap(replacement)
    bpy.data.objects.remove(root, do_unlink=True)
    replacement.name = original_name

    if was_active:
        view_layer.objects.active = replacement
    replacement.select_set(was_selected)
    replacement.hide_set(was_hidden)
    logger.info("%s: Replaced Merge Children Empty with mesh root (step=%d)", original_name, interpolation_steps)


def convert_merge_children_empty_roots(roots: MergeChildrenRoots | None = None) -> int:
    """Replace validated roots, checking the layout first when called directly."""
    if roots is None:
        roots = plan_merge_children_empty_roots()
    for root, step in roots:
        _replace_empty(root, step)
    if roots:
        bpy.context.view_layer.update()
    return len(roots)
