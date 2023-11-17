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


class I3DEA_OT_copy_orientation(bpy.types.Operator):
    bl_idname = "i3dea.copy_orientation"
    bl_label = "Copy Orientation"
    bl_description = "Copy selected object orientation to clipboard"
    state: bpy.props.IntProperty()

    def execute(self, context):
        def bake_transform_matrix(matrix):
            return mathutils.Matrix.Rotation(math.radians(-90), 4, "X") @ \
                matrix @ mathutils.Matrix.Rotation(math.radians(90), 4, "X")

        obj = bpy.context.object
        m = bake_transform_matrix(obj.matrix_local)
        orientation = "0 0 0"

        if 1 == self.state:
            t = m.to_translation()[:]
            orientation = "{0:.3f} {1:.3f} {2:.3f}".format(*t)

        elif 2 == self.state:
            r = m.to_euler("XYZ")
            r = (math.degrees(r.x) if (r.x > 1e-6 or r.x < -1e-6) else 0,
                 math.degrees(r.y) if (r.y > 1e-6 or r.y < -1e-6) else 0,
                 math.degrees(r.z) if (r.z > 1e-6 or r.z < -1e-6) else 0)
            orientation = "{0:.3f} {1:.3f} {2:.3f}".format(*r)

        bpy.context.window_manager.clipboard = orientation
        self.report({'INFO'}, f'{orientation} from {obj.name} copied to clipboard')
        return {'FINISHED'}
