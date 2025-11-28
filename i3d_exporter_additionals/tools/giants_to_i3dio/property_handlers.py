import bpy

from ...helper_functions import get_from_addon_module
from .logging_config import logger

GIANTS_DEFAULT_MASK_VALUES = {4294967295, 255, 0}


def has_rigid_body(obj: bpy.types.Object) -> bool:
    """Checks if the object has a rigid body type set."""
    return getattr(obj.i3d_attributes, "rigid_body_type", "none") != "none"


def has_joint(obj: bpy.types.Object) -> bool:
    """Checks if the object is a joint."""
    return getattr(obj.i3d_attributes, "joint", False)


def has_visibility_condition(obj: bpy.types.Object) -> bool:
    """Checks if the object has a visibility condition set."""
    return not getattr(obj.i3d_attributes, "use_parent", True)


def convert_collision_mask_handler(obj: bpy.types.Object, value: int) -> None:
    if value in GIANTS_DEFAULT_MASK_VALUES:
        return
    if (collisions := get_from_addon_module("i3dio.ui.collision_data", "COLLISIONS")) is None:
        logger.warning("COLLISIONS data not found in i3dio addon. Skipping collision mask conversion.")
        return
    rule_lookup = {rule.mask_old: rule for rule in collisions["rules"]}
    rule = rule_lookup.get(value)
    if rule is None:
        logger.warning(f"{obj.name}: No rule found for collision mask {value!r}.")
        return
    is_trigger = obj.i3d_attributes.trigger
    if (apply_rule_to_mask := get_from_addon_module("i3dio.ui.collision_data", "apply_rule_to_mask")) is None:
        logger.warning("apply_rule_to_mask not found in i3dio addon. Skipping collision mask conversion.")
        return
    result = apply_rule_to_mask(rule, is_trigger)
    obj.i3d_attributes.collision_filter_group = result["group_hex"]
    obj.i3d_attributes.collision_filter_mask = result["mask_hex"]
    logger.info(
        f"{obj.name}: Converted collision mask {value!r} to group {result['group_hex']} and mask {result['mask_hex']}."
    )


def migrate_merge_children(obj: bpy.types.Object, value: bool) -> None:
    obj.i3d_merge_children.enabled = value
    freeze_props = {
        "i3D_mergeChildrenFreezeTranslation",
        "i3D_mergeChildrenFreezeRotation",
        "i3D_mergeChildrenFreezeScale",
        "I3D_mergeChildrenFreezeTranslation",
        "I3D_mergeChildrenFreezeRotation",
        "I3D_mergeChildrenFreezeScale",
    }
    if any(hasattr(obj, prop) and getattr(obj, prop) for prop in freeze_props):
        obj.i3d_merge_children.apply_transforms = True


def get_clean_name(name: str) -> str:
    """
    Cleans the object name by removing any prefix before the last colon.
    If no colon is found, returns the original name.
    """
    return name.split(":")[-1] if ":" in name else name


def migrate_i3d_mapping(obj: bpy.types.Object, value: bool) -> None:
    """
    Migrates the I3D_XMLconfigBool property to the i3d_mapping.is_mapped attribute
    and sets the mapping_name if I3D_XMLconfigID is present and different from the object name.
    """
    obj.i3d_mapping.is_mapped = value
    xml_config_id = obj.get("I3D_XMLconfigID", "")
    if value and xml_config_id and xml_config_id != get_clean_name(obj.name):
        obj.i3d_mapping.mapping_name = xml_config_id

    # Handle armature bones
    if obj.type == "ARMATURE" and hasattr(obj.data, "bones"):
        for bone in obj.data.bones:
            bone_value = bone.get("I3D_XMLconfigBool", False)
            bone.i3d_mapping.is_mapped = bone_value
            bone_xml_config_id = bone.get("I3D_XMLconfigID", "")
            if bone_value and bone_xml_config_id and bone_xml_config_id != get_clean_name(bone.name):
                bone.i3d_mapping.mapping_name = bone_xml_config_id


def migrate_split_type_and_uvs(obj: bpy.types.Object, value: int) -> None:
    if value == 0:
        return  # No split type
    # Set split_type
    obj.i3d_attributes.split_type = value

    # Collect split_uvs values
    keys = ["i3D_splitMinU", "i3D_splitMinV", "i3D_splitMaxU", "i3D_splitMaxV", "i3D_splitUvWorldScale"]
    values = []
    any_found = False
    for k in keys:
        val = obj.get(k)
        if val is not None:
            values.append(float(val))
            any_found = True
        else:
            values.append(0.0)

    if any_found:
        obj.i3d_attributes.split_uvs = values


def migrate_mask(obj: bpy.types.Object, value, *, attr_path: str, data_target: bool = False):
    """
    Converts a Giants decimal mask value (int or str) to a hex string and writes to the given attribute path.
    - obj: the object
    - value: the value from Giants (int/str)
    - attr_path: the destination attribute, e.g. "collision_filter_mask"
    - data_target: if True, write to obj.data.i3d_attributes, else obj.i3d_attributes
    """
    try:
        if int(value) in GIANTS_DEFAULT_MASK_VALUES:
            return  # Default mask, no conversion needed
        hexval = f"{int(value):x}" if value else "0"
        target = obj.data.i3d_attributes if data_target else obj.i3d_attributes
        setattr(target, attr_path, hexval)
    except Exception as e:
        logger.warning(f"{obj.name}: Could not convert {attr_path} value {value!r} to hex: {e}")


def migrate_cpu_mesh(obj: bpy.types.Object, value: bool) -> None:
    """Converts Giants cpuMesh bool to i3dio cpu_mesh enum ("0" or "256")."""
    obj.data.i3d_attributes.cpu_mesh = "256" if value else "0"


def migrate_vertex_compression_range(obj: bpy.types.Object, value: str) -> None:
    """Converts Giants vertexCompressionRange string to i3dio vertex_compression_range enum."""
    # Giants store int as string, but our enum expects a float string or "auto".
    try:
        obj.data.i3d_attributes.vertex_compression_range = str(float(value)) if value else "auto"
    except ValueError:
        logger.warning(f"{obj.name}: Could not convert vertexCompressionRange value {value!r} to float string.")


def migrate_lod_distances(obj: bpy.types.Object, value: bool) -> None:
    """Converts Giants LOD distance properties (i3D_lod0-3) to i3dio LOD distances vector."""
    if not value:
        return
    # Check if object has enough children for a valid LOD setup.
    # LOD requires at least 2 children: LOD 0 (always distance 0.0), plus at least one additional LOD.
    n_children = len(obj.children)
    if n_children < 2:
        logger.warning(f"{obj.name}: Not enough children for LOD (has {n_children}), skipping LOD migration.")
        return

    # Collect and validate distances
    giants_lod_keys = ["i3D_lod0", "i3D_lod1", "i3D_lod2", "i3D_lod3"]
    lod_values = []
    for key in giants_lod_keys:
        val = obj.get(key, 0.0)
        try:
            lod_values.append(float(val))
        except (ValueError, TypeError):
            logger.warning(f"{obj.name}: Could not convert {key} value {val!r} to float, using 0.0.")
            lod_values.append(0.0)

    # Enforce correct order, log any corrections
    for i in range(1, 4):
        if lod_values[i] < lod_values[i - 1]:
            logger.warning(
                f"{obj.name}: LOD distance {i} ({lod_values[i]}) < previous level ({lod_values[i - 1]}), clamping."
            )
            lod_values[i] = lod_values[i - 1]

    # Assign only up to the number of children (min 2, max 4), fill to length 4 with 0.0 as needed.
    lod_vec = lod_values[: min(max(n_children, 2), 4)]
    lod_vec += [0.0] * (4 - len(lod_vec))  # Ensure exactly 4 elements for i3dio
    obj.i3d_attributes.lod_distances = lod_vec
