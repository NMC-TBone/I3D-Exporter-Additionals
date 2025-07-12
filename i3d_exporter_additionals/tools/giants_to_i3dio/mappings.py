from .property_handlers import (
    has_rigid_body,
    has_joint,
    has_visibility_condition,
    convert_collision_mask_handler,
    migrate_mask,
    migrate_merge_children,
    migrate_i3d_mapping,
    migrate_split_type_and_uvs,
    migrate_cpu_mesh,
    migrate_vertex_compression_range,
    migrate_lod_distances,
)


def expand_object_prop_mappings(base_mappings: dict) -> dict:
    expanded = dict(base_mappings)
    for k in list(base_mappings):
        if k.startswith("i3D_"):
            new_key = k.replace("i3D_", "I3D_")
            if new_key not in expanded:
                expanded[new_key] = base_mappings[k]
    return expanded


BASE_OBJECT_PROP_MAPPINGS = {
    # key: (attribute_name, type, handler or None, location, allowed_type, condition)
    # locaation: "obj" or "data" (.i3d_attributes)
    # allowed_type: 'ANY', 'MESH', 'EMPTY', etc.
    # Note: I3D_XMLconfigID handles mapping for armature bones as well.
    "I3D_XMLconfigBool": (None, bool, migrate_i3d_mapping, "obj", "ANY", None),
    "i3D_lockedGroup": ("locked_group", int, None, "obj", "ANY", None),
    "i3D_clipDistance": ("clip_distance", float, None, "obj", "ANY",  # Default in Giants Exp is 0.0, skip if 0.0
                         lambda obj: float(obj.get("i3D_clipDistance", 0.0)) != 0.0),
    "i3D_objectMask": (None, int, lambda o, v: migrate_mask(o, v, attr_path="object_mask"), "obj", "ANY", None),
    "i3D_forceVisibilityCondition": ("use_parent", bool,
                                     lambda o, v: setattr(o.i3d_attributes, "use_parent", not v), "obj", "ANY", None),
    "i3D_minuteOfDayStart": ("minute_of_day_start", int, None, "obj", "ANY", has_visibility_condition),
    "i3D_minuteOfDayEnd": ("minute_of_day_end", int, None, "obj", "ANY", has_visibility_condition),
    "i3D_dayOfYearStart": ("day_of_year_start", int, None, "obj", "ANY", has_visibility_condition),
    "i3D_dayOfYearEnd": ("day_of_year_end", int, None, "obj", "ANY", has_visibility_condition),
    "i3D_weatherMask": (
        None, str, lambda o, v: migrate_mask(o, v, attr_path="weather_required_mask"),
        "obj", "ANY", has_visibility_condition
    ),
    "i3D_weatherPreventMask": (
        None, str, lambda o, v: migrate_mask(o, v, attr_path="weather_prevent_mask"),
        "obj", "ANY", has_visibility_condition
    ),
    "i3D_viewerSpacialityMask": (
        None, str, lambda o, v: migrate_mask(o, v, attr_path="viewer_spaciality_required_mask"),
        "obj", "ANY", has_visibility_condition
    ),
    "i3D_viewerSpacialityPreventMask": (
        None, str, lambda o, v: migrate_mask(o, v, attr_path="viewer_spaciality_prevent_mask"),
        "obj", "ANY", has_visibility_condition
    ),
    "i3D_renderInvisible": ("render_invisible", bool, None, "obj", "ANY", has_visibility_condition),

    # MESH object properties
    # Rigid body properties (rigid body type handled separately)
    "i3D_collision": ("collision", bool, None, "obj", "MESH", has_rigid_body),
    "i3D_compound": ("compound", bool, None, "obj", "MESH",
                     lambda obj: getattr(obj.i3d_attributes, "rigid_body_type", "none") in {"dynamic", "kinematic"}),
    "i3D_collisionFilterGroup": (
        None, int, lambda o, v: migrate_mask(o, v, attr_path="collision_filter_group"), "obj", "MESH", has_rigid_body
    ),
    "i3D_collisionFilterMask": (
        None, int, lambda o, v: migrate_mask(o, v, attr_path="collision_filter_mask"), "obj", "MESH", has_rigid_body
    ),
    "i3D_restitution": ("restitution", float, None, "obj", "MESH", has_rigid_body),
    "i3D_staticFriction": ("static_friction", float, None, "obj", "MESH", has_rigid_body),
    "i3D_dynamicFriction": ("dynamic_friction", float, None, "obj", "MESH", has_rigid_body),
    "i3D_linearDamping": ("linear_damping", float, None, "obj", "MESH", has_rigid_body),
    "i3D_angularDamping": ("angular_damping", float, None, "obj", "MESH", has_rigid_body),
    "i3D_density": ("density", float, None, "obj", "MESH", has_rigid_body),
    "i3D_solverIterationCount": ("solver_iteration_count", int, None, "obj", "MESH", has_rigid_body),
    "i3D_trigger": ("trigger", bool, None, "obj", "MESH", has_rigid_body),
    "i3D_splitType": (
        None, int, migrate_split_type_and_uvs, "obj", "MESH",
        lambda obj: getattr(obj.i3d_attributes, "rigid_body_type", "none") == "static"
    ),
    "i3D_mergeChildren": (None, bool, migrate_merge_children, "obj", "MESH", None),

    # Mesh properties
    "i3D_castsShadows": ("casts_shadows", bool, None, "data", "MESH", None),
    "i3D_receiveShadows": ("receive_shadows", bool, None, "data", "MESH", None),
    "i3D_renderedInViewports": ("rendered_in_viewports", bool, None, "data", "MESH", None),
    "i3D_nonRenderable": ("non_renderable", bool, None, "data", "MESH", None),
    "i3D_oc": ("is_occluder", bool, None, "data", "MESH", None),
    "i3D_terrainDecal": ("terrain_decal", bool, None, "data", "MESH", None),
    "i3D_cpuMesh": (None, bool, migrate_cpu_mesh, "data", "MESH", None),
    "i3D_doubleSided": ("double_sided", bool, None, "data", "MESH", None),
    "i3D_navMeshMask": (
        None, int, lambda o, v: migrate_mask(o, v, attr_path="nav_mesh_mask", data_target=True), "data", "MESH", None
    ),
    "i3D_decalLayer": ("decal_layer", int, None, "data", "MESH", None),
    "i3D_vertexCompressionRange": (None, str, migrate_vertex_compression_range, "data", "MESH", None),

    # Empty object properties
    "i3D_lod": (None, bool, migrate_lod_distances, "obj", "EMPTY", None),

    "i3D_joint": ("joint", bool, None, "obj", "EMPTY", None),
    "i3D_projection": ("projection", bool, None, "obj", "EMPTY", has_joint),
    "i3D_projDistance": ("projection_distance", float, None, "obj", "EMPTY", has_joint),
    "i3D_projAngle": ("projection_angle", float, None, "obj", "EMPTY", has_joint),
    "i3D_xAxisDrive": ("x_axis_drive", bool, None, "obj", "EMPTY", has_joint),
    "i3D_yAxisDrive": ("y_axis_drive", bool, None, "obj", "EMPTY", has_joint),
    "i3D_zAxisDrive": ("z_axis_drive", bool, None, "obj", "EMPTY", has_joint),
    "i3D_drivePos": ("drive_position", bool, None, "obj", "EMPTY", has_joint),
    "i3D_driveForceLimit": ("drive_force_limit", float, None, "obj", "EMPTY", has_joint),
    "i3D_driveSpring": ("drive_spring", float, None, "obj", "EMPTY", has_joint),
    "i3D_driveDamping": ("drive_damping", float, None, "obj", "EMPTY", has_joint),
    "i3D_breakableJoint": ("breakable_joint", bool, None, "obj", "EMPTY", has_joint),
    "i3D_joinBreakForce": ("joint_break_force", float, None, "obj", "EMPTY", has_joint),
    "i3D_jointBreakTorque": ("joint_break_torque", float, None, "obj", "EMPTY", has_joint),

    # Legacy keys, that isn't used by Giants FS25 exporter, but might still exist on objects.
    "I3D_collisionMask": (None, int, convert_collision_mask_handler, "obj", 'MESH', has_rigid_body),
}
# Giants decided to convert all "I3D_" keys to "i3D_" keys in FS25.
# To support files created with older exporter versions (which may still have "I3D_" keys),
# auto-expand the mapping to include both variants for every "i3D_" key.
OBJECT_PROP_MAPPINGS = expand_object_prop_mappings(BASE_OBJECT_PROP_MAPPINGS)


# Copied from i3dio:
OLD_TO_NEW_PARAMETERS = {
    'morphPosition': 'morphPos',
    'scrollPosition': 'scrollPos',
    'blinkOffset': 'blinkMulti',
    'offsetUV': 'offsetUV',
    'uvCenterSize': 'uvCenterSize',
    'uvScale': 'uvScale',
    'lengthAndRadius': 'lengthAndRadius',
    'widthAndDiam': 'widthAndDiam',
    'connectorPos': 'connectorPos',
    'numberOfStatics': 'numberOfStatics',
    'connectorPosAndScale': 'connectorPosAndScale',
    'lengthAndDiameter': 'lengthAndDiameter',
    'backLightScale': 'backLightScale',
    'amplFreq': 'amplFreq',
    'shaking': 'shaking',
    'rotationAngle': 'rotationAngle',
    'directionBend': 'directionBend',
    'controlPointAndLength': 'controlPointAndLength',
}
OLD_TO_NEW_CUSTOM_TEXTURES = {'mTrackArray': 'trackArray'}
