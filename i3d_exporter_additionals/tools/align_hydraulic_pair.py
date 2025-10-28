import bpy
from mathutils import Matrix, Vector


def _single_user(obj: bpy.types.Object) -> None:
    if obj.type == "MESH" and obj.data and obj.data.users > 1:
        obj.data = obj.data.copy()


def _aim_rot_preserve_roll(from_loc: Vector, to_loc: Vector, y_sign: float, old_rot_world_3x3: Matrix) -> Matrix:
    """World rotation so local Y (±) aims at target, preserving roll from old X. Returns 3x3 (columns=basis)."""
    fwd = to_loc - from_loc
    if fwd.length_squared == 0.0:
        return old_rot_world_3x3.copy()

    y_rot = (fwd if y_sign > 0.0 else -fwd).normalized()

    # preserve roll using old world +X
    x_rot_old = old_rot_world_3x3.col[0]
    x_proj = x_rot_old - y_rot * x_rot_old.dot(y_rot)
    if x_proj.length_squared < 1e-12:
        x_proj = y_rot.cross(Vector((0, 0, 1)))  # fallback to Y × up(+Z)
        if x_proj.length_squared < 1e-12:
            x_proj = Vector((1, 0, 0))
    x_rot = x_proj.normalized()
    z_rot = x_rot.cross(y_rot).normalized()

    return Matrix((x_rot, y_rot, z_rot)).transposed()


def _apply_rotation_keep_mesh(
    obj: bpy.types.Object,
    r_new_3x3: Matrix,
    loc_snapshot: Vector,
    r_old_3x3_snapshot: Matrix,
    scale_snapshot: Vector,
) -> None:
    """Apply using snapshots; counter-rotate mesh; write matrix_world directly."""
    if obj.type != "MESH":
        return
    _single_user(obj)  # Ensure single user for mesh data to prevent unwanted edits on duplicates

    # Build matrices from the SNAPSHOT (pre-change) state
    scale_matrix = Matrix.Diagonal((scale_snapshot.x, scale_snapshot.y, scale_snapshot.z, 1.0))
    r_old4 = r_old_3x3_snapshot.to_4x4()
    r_new4 = r_new_3x3.to_4x4()

    # Exact local-space correction that preserves world-space shape:
    # (works for non-uniform scales; may introduce local shear, which cancels with scale_matrix)
    matrix_mesh = scale_matrix.inverted_safe() @ r_new4.inverted_safe() @ r_old4 @ scale_matrix
    obj.data.transform(matrix_mesh)
    obj.data.update()

    # Build the desired world matrix from the same snapshots
    translation = Matrix.Translation(loc_snapshot)
    matrix_world_new = translation @ r_new4 @ scale_matrix

    # Let Blender resolve locals (plays nicely with parenting)
    obj.matrix_world = matrix_world_new


class I3DEA_OT_align_hydraulic_pair(bpy.types.Operator):
    bl_idname = "i3dea.align_hydraulic_pair"
    bl_label = "Align Hydraulic Pair"
    bl_description = "Align the selected hydraulic pair (cylinder and piston) along the specified axis"
    bl_options = {"REGISTER", "UNDO"}

    swap_roles: bpy.props.BoolProperty(
        name="Swap Roles",
        description="If active is actually the punch, swap",
        default=False,
    )

    @classmethod
    def poll(cls, context):
        cls.poll_message_set("Select exactly two mesh objects")
        selected_objects = [obj for obj in context.selected_objects if obj.type == "MESH"]
        return len(selected_objects) == 2

    def _resolve_roles(self, context: bpy.types.Context, selected_objects: list[bpy.types.Object]):
        a, b = selected_objects
        active = context.view_layer.objects.active
        an, bn = a.name.lower(), b.name.lower()
        if "punch" in an and "punch" not in bn:
            housing, punch = b, a
        elif "punch" in bn and "punch" not in an:
            housing, punch = a, b
        else:
            housing = active if active in selected_objects else a
            punch = b if a is housing else a

        if self.swap_roles:
            housing, punch = punch, housing
        return housing, punch

    def execute(self, context):
        original_mode = None
        active_object = context.view_layer.objects.active
        if active_object and active_object.mode != "OBJECT" and bpy.ops.object.mode_set.poll():
            original_mode = active_object.mode
            bpy.ops.object.mode_set(mode="OBJECT")
        context.view_layer.update()

        selected_objects = [obj for obj in context.selected_objects if obj.type == "MESH"]
        housing, punch = self._resolve_roles(context, selected_objects)

        h_loc, h_rot_q, h_scale = housing.matrix_world.decompose()
        p_loc, p_rot_q, p_scale = punch.matrix_world.decompose()
        rot_housing_old = h_rot_q.to_matrix()
        rot_punch_old = p_rot_q.to_matrix()

        rot_housing_new = _aim_rot_preserve_roll(
            from_loc=h_loc, to_loc=p_loc, y_sign=-1.0, old_rot_world_3x3=rot_housing_old
        )
        rot_punch_new = _aim_rot_preserve_roll(
            from_loc=p_loc, to_loc=h_loc, y_sign=+1.0, old_rot_world_3x3=rot_punch_old
        )

        _apply_rotation_keep_mesh(housing, rot_housing_new, h_loc, rot_housing_old, h_scale)
        _apply_rotation_keep_mesh(punch, rot_punch_new, p_loc, rot_punch_old, p_scale)

        context.view_layer.update()
        if active_object and original_mode and bpy.ops.object.mode_set.poll():
            bpy.ops.object.mode_set(mode=original_mode)

        self.report({"INFO"}, f"Aligned {housing.name!r} (-Y) and {punch.name!r} (+Y)")
        return {"FINISHED"}


classes = (I3DEA_OT_align_hydraulic_pair,)
register, unregister = bpy.utils.register_classes_factory(classes)
