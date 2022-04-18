"""mesh_tools.py includes different tools for mesh"""

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

import bmesh
import bpy
from bpy.types import Operator
from math import radians

class TOOLS_OT_removeDoubles(Operator):
    bl_idname = "tools.remove_doubles"
    bl_label = "Clean Object(s)"
    bl_description = "Removes custom split normals, set shade smooth and auto smooth, merge vertices."
    bl_options = {'UNDO'}

    def cleanObjects(self, context):
        SmoothAngle = 180
        MergeThreshold = .0001
        smooth_radians = radians(SmoothAngle)

        for obj in bpy.context.selected_objects:
            if not isinstance(obj.data, bpy.types.Mesh):
                continue
            bpy.ops.mesh.customdata_custom_splitnormals_clear()
            bpy.ops.object.shade_smooth()
            obj.data.use_auto_smooth = True
            obj.data.auto_smooth_angle = smooth_radians
            bm = bmesh.new()
            bm.from_mesh(obj.data)
            bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=MergeThreshold)
            bm.to_mesh(obj.data)
            bm.free()
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_all(action='DESELECT')
            bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='EDGE')
            bpy.ops.mesh.edges_select_sharp(sharpness=0.872665)
            bpy.ops.mesh.mark_sharp()
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.tris_convert_to_quads(uvs=True)
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.select_all(action='DESELECT')
            self.report({'INFO'}, "Object(s) cleaned")

    def execute(self, context):
        self.cleanObjects(context)
        return {'FINISHED'}

class TOOLS_OT_meshName(Operator):
    bl_idname = "tools.mesh_name"
    bl_label = "Set Mesh Name"
    bl_description = "Take the Object Names --> Mesh Data name"
    bl_options = {'UNDO'}

    def meshName(self, context):
        objects = bpy.data.objects
        for obj in objects:
          if obj.data and obj.data.users == 1:
            obj.data.name = obj.name

    def execute(self, context):
        self.meshName(context)
        return {'FINISHED'}

class TOOLS_OT_getCurveLength(Operator):
    bl_idname = "tools.curve_length"
    bl_label = "Get Curve Length"
    bl_description = "Measure length of the selected curve"

    @classmethod
    def poll(cls, context):
        return context.object is not None

    def execute(self, context):
        if bpy.context.active_object.type == "CURVE":
            curveLength = bpy.context.active_object.data.splines[0].calc_length(resolution = 1024)
            self.report({'INFO'}, bpy.utils.units.to_string(bpy.context.scene.unit_settings.system, 'LENGTH', curveLength))
        else:
            self.report({'WARNING'}, "Active object is not a curve")
            return{'CANCELLED'}
        return {'FINISHED'}