import bpy

from .logging_config import logger
from .mappings import OBJECT_PROP_MAPPINGS

USER_ATTRIBUTE_DATA_FIELDS = {
    "boolean": "data_boolean",
    "string": "data_string",
    "scriptCallback": "data_scriptCallback",
    "float": "data_float",
    "integer": "data_integer",
}


def migrate_objects() -> None:
    # Handle merge groups first to ensure info is not lost during cleanup later.
    group_num_to_index = migrate_merge_groups()
    # Handle bounding volumes after merge groups to ensure correct assignment.
    migrate_bounding_volumes(group_num_to_index)

    for obj in bpy.data.objects:
        migrate_rigid_body_type(obj)
        migrate_giants_object_properties(obj)
        migrate_user_attributes(obj)
        if obj.name.lower().endswith("_ignore"):
            obj.i3d_attributes.exclude_from_export = True
            obj.name = obj.name[:-7]  # Remove the "_ignore" suffix
            logger.info(f"{obj.name}: Marked as excluded from export due to '_ignore' suffix.")


def migrate_giants_object_properties(obj: bpy.types.Object) -> bool:
    for giants_key, (attr_name, typ, handler, location, allowed_type, condition) in OBJECT_PROP_MAPPINGS.items():
        if allowed_type != "ANY" and obj.type != allowed_type:
            continue
        if giants_key not in obj:
            continue
        if condition and not condition(obj):
            continue
        value = typ(obj[giants_key])
        if handler:
            handler(obj, value)
        else:
            target = obj.i3d_attributes if location == "obj" else getattr(obj.data, "i3d_attributes", None)
            if target is not None:
                setattr(target, attr_name, value)
                logger.info(f"{obj.name}: Migrated {giants_key} to {attr_name} with value {value}.")
            else:
                logger.warning(f"{obj.name}: Could not find target for {giants_key} ({location}).")


def migrate_rigid_body_type(obj: bpy.types.Object) -> None:
    """Special handling for rigid body types, giants uses separate bool props, i3dio uses enum."""
    if obj.type != "MESH":
        return
    suffixes = ("static", "dynamic", "kinematic", "compoundChild")
    prefixes = ("i3D_", "I3D_")

    selected = next((s for p in prefixes for s in suffixes if obj.get(f"{p}{s}")), "none")
    obj.i3d_attributes.rigid_body_type = selected


def migrate_user_attributes(obj: bpy.types.Object) -> None:
    """
    Converts Giants-style userAttribute_* custom props to i3dio User Attribute items.
    Example: userAttribute_boolean_myAttr=True → attribute_list: type=boolean, name='myFAttr', data_boolean=True
    """
    for key in list(obj.keys()):
        user_attribute = _read_giants_user_attribute(obj, key)
        if user_attribute is None:
            continue
        attr_type, attr_name, data_field, value = user_attribute

        attrs = obj.i3d_user_attributes
        new_attr = attrs.attribute_list.add()
        new_attr.name = attr_name
        new_attr.type = data_field
        setattr(new_attr, data_field, value)

        logger.info(f"{obj.name}: Migrated user attribute {attr_name} ({attr_type}) with value {value!r}")


def _read_giants_user_attribute(obj: bpy.types.Object, key: str) -> tuple[str, str, str, object] | None:
    if not key.startswith("userAttribute_"):
        return None

    try:
        _, attr_type, attr_name = key.split("_", 2)
    except ValueError:
        return None

    data_field = USER_ATTRIBUTE_DATA_FIELDS.get(attr_type)
    if data_field is None:
        return None

    value = obj[key]
    try:
        match attr_type:
            case "boolean":
                value = bool(value)
            case "integer":
                value = int(value)
            case "float":
                value = float(value)
            case "string" | "scriptCallback":
                value = str(value)
    except (ValueError, TypeError):
        return None

    return attr_type, attr_name, data_field, value


def clean_giants_object_properties() -> None:
    """Remove Giants object properties after all object data has been migrated."""
    for obj in bpy.data.objects:
        for key in list(obj.keys()):
            if _read_giants_user_attribute(obj, key) is not None:
                del obj[key]
        clean_giants_keys(obj)


def clean_giants_keys(obj: bpy.types.Object) -> None:
    """Remove Giants object keys using the i3D_/I3D_ prefixes."""
    del_count = 0
    for key in list(obj.keys()):
        if key.startswith("i3D_") or key.startswith("I3D_"):
            del_count += 1
            del obj[key]
    logger.info(f"{obj.name}: Cleaned {del_count} Giants keys.")


def migrate_merge_groups() -> dict[int, int]:
    logger.info("Migrating merge groups...")
    scene = bpy.context.scene
    group_map = {}
    root_map = {}
    referenced_groups = set()

    # Collect all group memberships and root info
    objects = [obj for obj in bpy.data.objects if obj.type == "MESH"]
    for obj in objects:
        group_id = obj.get("i3D_mergeGroup") or obj.get("I3D_mergeGroup")
        if group_id is not None and group_id >= 1:  # In Giants Exporter merge groups start at 1, 0 = no group
            referenced_groups.add(group_id)
            group_map.setdefault(group_id, []).append(obj)
            if obj.get("i3D_mergeGroupRoot") or obj.get("I3D_mergeGroupRoot"):
                root_map[group_id] = obj

    # Create merge groups in group_id order, map number to index
    merge_group_number_to_index = {}
    for idx, group_id in enumerate(sorted(referenced_groups)):
        mg = scene.i3dio_merge_groups.add()
        mg.name = f"MergeGroup_{group_id}"
        mg_index = len(scene.i3dio_merge_groups) - 1
        merge_group_number_to_index[group_id] = mg_index

        for obj_ in group_map[group_id]:
            obj_.i3d_merge_group_index = mg_index
        # Assign root if present
        if group_id in root_map:
            mg.root = root_map[group_id]
        elif group_map[group_id]:
            mg.root = group_map[group_id][0]
    logger.info("Merge group migration completed.")
    return merge_group_number_to_index


def migrate_bounding_volumes(merge_group_number_to_index: dict) -> None:
    logger.info("Migrating bounding volumes...")
    scene = bpy.context.scene
    mgroups = scene.i3dio_merge_groups

    objects = [obj for obj in bpy.data.objects if obj.type == "MESH"]
    for bv_obj in objects:
        bv_name = bv_obj.get("i3D_boundingVolume", "") or bv_obj.get("I3D_boundingVolume", "")
        if not bv_name or bv_name in {"", "None"}:
            continue
        if bv_name.startswith("MERGEGROUP_"):
            try:
                group_num = int(bv_name.split("_")[1])
            except (IndexError, ValueError):
                logger.warning(f"{bv_obj.name}: Could not parse merge group from {bv_name!r}.")
                continue
            mg_index = merge_group_number_to_index.get(group_num)
            if mg_index is None or mg_index >= len(mgroups):
                logger.warning(f"{bv_obj.name}: : Merge group {group_num} not found.")
                continue
            target_obj = mgroups[mg_index].root
            if not target_obj:
                logger.warning(f"{bv_obj.name}: Merge group {group_num} has no root object.")
                continue
            target_obj.data.i3d_attributes.bounding_volume_object = bv_obj
            logger.info(f"{bv_obj.name}: Assigned bounding volume to merge group {group_num} root ({target_obj.name}).")
        else:
            target_obj = bpy.data.objects.get(bv_name)
            if not target_obj:
                logger.warning(f"{bv_obj.name}: Target object {bv_name!r} not found for bounding volume.")
                continue
            target_obj.data.i3d_attributes.bounding_volume_object = bv_obj
            logger.info(f"{bv_obj.name}: Assigned as bounding volume for {bv_name}.")
    logger.info("Bounding volume migration completed.")
