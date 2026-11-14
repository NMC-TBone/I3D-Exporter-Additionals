"""Optional compatibility with Nadine Brinkmann's i3D Importer.

Only act when imported debug materials are *assigned* to mesh slots.
The normal GIANTS -> Community workflow has no dependency on the importer.
"""

import bpy


def _assigned_debug_materials():
    """Yield (object, slot index, debug material) for currently assigned previews."""
    for obj in bpy.data.objects:
        if obj.type != "MESH":
            continue
        for index, slot in enumerate(obj.material_slots):
            mat = slot.material
            if mat is not None and mat.get("_i3d_material_kind") == "debug" and "_i3d_material_id" in mat:
                yield obj, index, mat


def _operator_available(name: str) -> bool:
    try:
        return getattr(bpy.ops.fs25, name).poll()
    except (AttributeError, RuntimeError):
        return False


def prepare_importer_materials() -> bool:
    """Sync assigned debug previews and restore export material assignments.

    Uses the importer's PUBLIC operators only. In particular, do not call its
    scope='all' sync: that would overwrite export data from unused debug copies.
    Does not invoke Prepare for Export (which also alters scene visibility,
    configurations and mesh geometry).
    """
    if not (assigned := list(_assigned_debug_materials())):
        return False

    if not (_operator_available("sync_debug_to_export_material") and _operator_available("switch_materials")):
        raise RuntimeError("Enable Nadine's i3D Importer to prepare assigned debug materials")

    # Verify every assigned preview has an export counterpart before changing data.
    export_keys = {
        (mat.get("_i3d_material_id"), mat.get("_i3d_import_uuid"))
        for mat in bpy.data.materials
        if mat.get("_i3d_material_kind") == "export"
    }
    for _, _, mat in assigned:
        key = (mat.get("_i3d_material_id"), mat.get("_i3d_import_uuid"))
        if key not in export_keys:
            raise RuntimeError(f"No export counterpart for debug material '{mat.name}'")

    # Sync only debug materials that are actually assigned to objects.
    # scope='selected' uses context.active_object.active_material in the importer.
    synced = set()
    for obj, slot_index, mat in assigned:
        material_key = mat.as_pointer()
        if material_key in synced:
            continue
        previous_index = obj.active_material_index
        try:
            obj.active_material_index = slot_index
            with bpy.context.temp_override(object=obj, active_object=obj):
                result = bpy.ops.fs25.sync_debug_to_export_material("EXEC_DEFAULT", scope="selected")
            if "FINISHED" not in result:
                raise RuntimeError(f"Could not sync debug material '{mat.name}'")
            synced.add(material_key)
        finally:
            obj.active_material_index = previous_index

    result = bpy.ops.fs25.switch_materials("EXEC_DEFAULT", target_kind="export", scope="all_imported")
    if "FINISHED" not in result or any(_assigned_debug_materials()):
        raise RuntimeError("Some imported debug materials were not switched to export materials")

    return True
