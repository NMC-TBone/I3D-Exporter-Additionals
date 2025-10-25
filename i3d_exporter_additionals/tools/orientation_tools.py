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


classes = (I3DEA_OT_copy_transform,)
register, unregister = bpy.utils.register_classes_factory(classes)
