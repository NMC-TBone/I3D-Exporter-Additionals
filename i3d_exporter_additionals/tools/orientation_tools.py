"""freezeTools.py Includes tools to freeze translation, rotation and scale"""

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

import bpy
import math
import mathutils
import numpy as np


class I3DEA_OT_copy_orientation(bpy.types.Operator):
    bl_idname = "i3dea.copy_orientation"
    bl_label = "Copy Orientation"
    bl_description = "Copy Location/Rotation from active object to clipboard in Giants Editor format"
    state: bpy.props.IntProperty()

    @staticmethod
    def transform_matrix(matrix):
        rotation_minus90_x = np.array([
            [1, 0, 0, 0],
            [0, 0, 1, 0],
            [0, -1, 0, 0],
            [0, 0, 0, 1]])
        rotation_plus90_x = np.array([
            [1, 0, 0, 0],
            [0, 0, -1, 0],
            [0, 1, 0, 0],
            [0, 0, 0, 1]])
        return mathutils.Matrix(rotation_minus90_x.tolist()) @ matrix @ mathutils.Matrix(rotation_plus90_x.tolist())

    def execute(self, context):
        obj = context.object

        if not obj:
            self.report({'ERROR'}, "No object selected")
            return {'CANCELLED'}

        transformed_matrix = self.transform_matrix(obj.matrix_local)
        orientation = "0 0 0"

        if self.state == 1:
            t = transformed_matrix.to_translation()[:]
            orientation = " ".join("0" if abs(x) < 1e-6 else "{:.6f}".format(x) for x in t)

        elif self.state == 2:
            r = transformed_matrix.to_euler("XYZ")
            r = [math.degrees(x) for x in r]
            orientation = " ".join("0" if abs(x) < 1e-6 else "{:.6f}".format(x) for x in r)

        context.window_manager.clipboard = orientation
        self.report({'INFO'}, f'Orientation "{orientation}" from "{obj.name}" copied to clipboard')
        return {'FINISHED'}
