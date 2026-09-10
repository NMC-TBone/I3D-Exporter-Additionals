# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

import math

import bmesh
import bpy
import mathutils
from bpy_extras.io_utils import axis_conversion


class I3DEA_OT_copy_transform(bpy.types.Operator):
    bl_idname = "i3dea.copy_transform"
    bl_label = "Copy Transform"
    bl_description = "Copy Location/Rotation from active object or EditBone to clipboard in Giants Editor format"
    state: bpy.props.IntProperty()

    # Conversion matrix for transforming from Blender's coordinate system (Z-up, -Y-forward)
    # to Giants Editor's coordinate system (Y-up, Z-forward)
    conversion_matrix: mathutils.Matrix = axis_conversion(to_forward="-Z", to_up="Y").to_4x4()

    @staticmethod
    def format_transformation(values) -> str:
        return " ".join("0" if math.isclose(x, 0, abs_tol=1e-5) else f"{x:.6f}" for x in values)

    @staticmethod
    def apply_root_bone_fix(matrix: mathutils.Matrix) -> mathutils.Matrix:
        """
        Adjust the rotation of the root bone to align with I3D conventions.

        Blender's root bone orientation does not match I3D orientation like other bones.
        So this method applies a -90-degree rotation correction around the X-axis.
        """
        rotation_fix = mathutils.Matrix.Rotation(math.radians(-90), 4, "X")
        # Extract translation
        translation = matrix.to_translation()
        # Apply rotation fix and reapply translation
        fixed_matrix = rotation_fix @ matrix.to_3x3().to_4x4()
        fixed_matrix.translation = translation
        return fixed_matrix

    def handle_bone_transformation(self, bone: bpy.types.EditBone) -> mathutils.Matrix:
        """
        Transform the bone's local matrix into I3D coordinates.

        For bones with a parent:
        - Compute the transformation relative to the parent bone's matrix (local transformation).

        For the root bone:
        - Apply a global transformation using the conversion matrix to match I3D coordinates.
        - Apply additional rotation correction for root bones.
        """
        # Bone space in blender is the same as Giants Editor space (except for root bone(?))
        # Blender bone space = Y-up, Z-forward, Giants space = Y-up, Z-forward
        if bone.parent:
            # Compute local transformation relative to the parent bone
            local_matrix = bone.parent.matrix.inverted() @ bone.matrix
            return local_matrix
        else:
            # Apply global transformation and rotation fix for root bones
            root_matrix = self.conversion_matrix @ bone.matrix @ self.conversion_matrix.inverted()
            return self.apply_root_bone_fix(root_matrix)

    def execute(self, context):
        obj = context.object

        if not obj:
            self.report({"ERROR"}, "No object selected")
            return {"CANCELLED"}

        if obj.type == "ARMATURE" and context.mode == "EDIT_ARMATURE":
            active_bone = context.active_bone
            if not active_bone:
                self.report({"ERROR"}, "No active bone selected. Switch to Edit Mode and select a bone.")
                return {"CANCELLED"}
            transformed_matrix = self.handle_bone_transformation(active_bone)
            source_name = active_bone.name
        else:
            transformed_matrix = self.conversion_matrix @ obj.matrix_local @ self.conversion_matrix.inverted()
            source_name = obj.name

        transformation = "0 0 0"
        if self.state == 1:
            transformation = self.format_transformation(transformed_matrix.to_translation()[:])
        elif self.state == 2:
            r = [math.degrees(x) for x in transformed_matrix.to_euler("XYZ")]
            transformation = self.format_transformation(r)

        context.window_manager.clipboard = transformation
        self.report({"INFO"}, f'Transformation "{transformation}" from "{source_name}" copied to clipboard')
        return {"FINISHED"}


class I3DEA_OT_align_origin_to_face_normal(bpy.types.Operator):
    bl_idname = "i3dea.align_origin_to_face_normal"
    bl_label = "Align Origin to Face Normal"
    bl_description = "Align the object's local axis to the active face normal without changing the mesh orientation"
    bl_options = {"REGISTER", "UNDO"}

    axis: bpy.props.EnumProperty(
        name="Axis",
        description="Local axis to align to the active face normal",
        items=[
            ("X", "X", "Align the local X axis to the active face normal"),
            ("Y", "Y", "Align the local Y axis to the active face normal"),
            ("Z", "Z", "Align the local Z axis to the active face normal"),
        ],
        default="Z",
    )

    flip: bpy.props.BoolProperty(
        name="Flip",
        description="Align the selected axis opposite to the active face normal",
        default=False,
    )

    @classmethod
    def poll(cls, context: bpy.types.Context) -> bool:
        cls.poll_message_set("Active object must be a mesh in Edit Mode")
        obj = context.active_object
        return obj is not None and obj.type == "MESH" and obj.mode == "EDIT"

    def execute(self, context: bpy.types.Context):
        obj = context.active_object

        bm = bmesh.from_edit_mesh(obj.data)
        face = bm.faces.active

        if face is None or not face.select:
            self.report({"ERROR"}, "Select an active face")
            return {"CANCELLED"}

        tangent_local = face.calc_tangent_edge_pair().normalized()
        bitangent_local = face.normal.cross(tangent_local).normalized()

        # Transform the face basis into world space.
        world_matrix = obj.matrix_world.to_3x3()

        tangent = (world_matrix @ tangent_local).normalized()
        bitangent = world_matrix @ bitangent_local

        # Keep the basis orthogonal even with non-uniform object scale.
        bitangent -= tangent * bitangent.dot(tangent)
        bitangent.normalize()

        normal = tangent.cross(bitangent).normalized()

        axis_index = {"X": 0, "Y": 1, "Z": 2}[self.axis]
        secondary_index = (axis_index + 1) % 3
        tertiary_index = (axis_index + 2) % 3

        if self.flip:
            normal = -normal
            tangent, bitangent = bitangent, tangent

        columns = [mathutils.Vector()] * 3
        columns[axis_index] = normal
        columns[secondary_index] = tangent
        columns[tertiary_index] = bitangent

        target_rotation = mathutils.Matrix(columns).transposed()

        current_world = obj.matrix_world.copy()
        current_rotation = current_world.to_quaternion().to_matrix()
        current_linear = current_world.to_3x3()

        # Preserve scale/shear while replacing only the object's orientation.
        remaining_transform = current_rotation.inverted() @ current_linear
        new_linear = target_rotation @ remaining_transform

        new_world = new_linear.to_4x4()
        new_world.translation = current_world.translation

        # Counter-transform the mesh so it remains unchanged in world space.
        mesh_correction = new_world.inverted() @ current_world

        bpy.ops.object.mode_set(mode="OBJECT")

        try:
            # Avoid modifying other objects that share this mesh datablock.
            if obj.data.users > 1:
                obj.data = obj.data.copy()

            obj.data.transform(mesh_correction, shape_keys=True)
            obj.matrix_world = new_world
            obj.data.update()

        finally:
            if bpy.ops.object.mode_set.poll():
                bpy.ops.object.mode_set(mode="EDIT")

        self.report({"INFO"}, f"Aligned origin of '{obj.name}' to active face normal")
        return {"FINISHED"}


classes = (I3DEA_OT_copy_transform, I3DEA_OT_align_origin_to_face_normal)
register, unregister = bpy.utils.register_classes_factory(classes)
