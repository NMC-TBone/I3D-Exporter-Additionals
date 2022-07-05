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
import math

from mathutils import Matrix


class I3DEA_OT_remove_doubles(bpy.types.Operator):
    bl_idname = "i3dea.remove_doubles"
    bl_label = "Clean Object(s)"
    bl_description = "Removes custom split normals, set shade smooth and auto smooth, merge vertices."
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        smooth_angle = 180
        merge_threshold = .0001
        smooth_radians = math.radians(smooth_angle)
        sel_obj = bpy.context.selected_objects
        act_obj = bpy.context.active_object

        for obj in sel_obj:
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.select_all(action='DESELECT')
            obj.select_set(True)
            if obj.type == 'MESH':
                bpy.context.view_layer.objects.active = obj
                bpy.ops.mesh.customdata_custom_splitnormals_clear()
                bpy.context.object.data.auto_smooth_angle = smooth_radians
                bpy.context.object.data.use_auto_smooth = True
                bm = bmesh.new()
                bm.from_mesh(obj.data)
                bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=merge_threshold)
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
                bpy.ops.object.shade_smooth()
                self.report({'INFO'}, "Object(s) cleaned")
        for obj in sel_obj:
            obj.select_set(True)
        bpy.context.view_layer.objects.active = act_obj
        return {'FINISHED'}


class I3DEA_OT_mesh_name(bpy.types.Operator):
    bl_idname = "i3dea.mesh_name"
    bl_label = "Set Mesh Name"
    bl_description = "Take the Object Names --> Mesh Data name"
    bl_options = {'REGISTER', 'UNDO'}

    def meshName(self, context):
        objects = bpy.data.objects
        for obj in objects:
            if obj.data and obj.data.users == 1:
                obj.data.name = obj.name

    def execute(self, context):
        self.meshName(context)
        return {'FINISHED'}


class I3DEA_OT_ignore(bpy.types.Operator):
    bl_idname = "i3dea.ignore"
    bl_label = "Suffix _ignore"
    bl_description = "Add _ignore to all selected objects"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        objects = bpy.context.selected_objects
        for (i, o) in enumerate(objects):
            o.name = "{}_ignore".format(o.name)
        return {'FINISHED'}


class I3DEA_OT_mirror_orientation(bpy.types.Operator):
    bl_idname = "i3dea.mirror_orientation"
    bl_label = "Calculate Amount"
    bl_description = "Calculates how many track pieces that fit from given track piece length and curve length"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        types = ['MESH', 'CAMERA', 'EMPTY']

        selected_list = [obj for obj in bpy.context.selected_objects if obj.type in types]
        camera_list = [mesh for mesh in selected_list if mesh.type == 'CAMERA']
        mesh_list = [mesh for mesh in selected_list if mesh.type == 'MESH']
        empty_list = [mesh for mesh in selected_list if mesh.type == 'EMPTY']

        if len(bpy.context.selected_objects) == 3:
            for camera, mirror, target in zip(camera_list, mesh_list, empty_list):

                mirror_parent = get_parent(mirror.name)
                mirror_axis_target = bpy.ops.object.empty_add(type='ARROWS')
                mirror_axis_target = bpy.context.active_object
                mirror_axis_target.name = "mirror_axis_target"
                target_mirror = bpy.ops.object.empty_add(type='ARROWS')
                target_mirror = bpy.context.active_object
                target_mirror.name = "target_mirror"

                camera_pos = camera.location
                mirror_pos = mirror.location
                target_pos = target.location

                v1 = vector_norm([mirror_pos[0]-camera_pos[0], mirror_pos[1]-camera_pos[1], mirror_pos[2]-camera_pos[2]])
                v2 = vector_norm([mirror_pos[0]-target_pos[0], mirror_pos[1]-target_pos[1], mirror_pos[2]-target_pos[2]])

                v3 = [v1[0] + v2[0], v1[1] + v2[1], v1[2] + v2[2]]

                bpy.data.objects[target_mirror.name].location = (mirror_pos[0], mirror_pos[1], mirror_pos[2])
                bpy.data.objects[mirror_axis_target.name].location = (mirror_pos[0] - v3[0], mirror_pos[1] - v3[1], mirror_pos[2] - v3[2])

                mirror_axis_target.constraints.new('TRACK_TO')
                mirror_axis_target.constraints['Track To'].track_axis = 'TRACK_NEGATIVE_Z'
                mirror_axis_target.constraints['Track To'].up_axis = 'UP_Y'
                mirror_axis_target.constraints['Track To'].target = target_mirror
                # mirror_axis_target.rotation_euler = (0, math.radians(-180), 0)
                bpy.context.view_layer.objects.active = mirror_axis_target
                mirror_axis_target.select_set(True)
                bpy.ops.constraint.apply(constraint="Track To", owner='OBJECT')
                mirror_axis_target.select_set(False)

                matrix_world = mirror.matrix_world.copy()
                mirror.parent = mirror_axis_target
                mirror.matrix_parent_inverse = Matrix.Identity(4)
                mirror.matrix_world = matrix_world
                bpy.ops.object.select_all(action='DESELECT')
                bpy.context.view_layer.objects.active = mirror
                mirror.select_set(True)
                bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
                mirror.select_set(False)

                if mirror_parent is not None:
                    bpy.ops.object.select_all(action='DESELECT')
                    bpy.context.view_layer.objects.active = mirror_parent
                    mirror_parent.select_set(True)
                    mirror.select_set(True)
                    bpy.ops.object.parent_set(type='OBJECT', keep_transform=True)
                    mirror_parent.select_set(False)
                else:
                    bpy.ops.object.select_all(action='DESELECT')
                    bpy.context.view_layer.objects.active = mirror
                    mirror.select_set(True)
                    bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
                    mirror.select_set(False)

                bpy.data.objects.remove(mirror_axis_target)
                bpy.data.objects.remove(target_mirror)
#
        else:
            self.report({'ERROR'}, "You need to select 3 objects (camera, mirror, empty)")
        return {'FINISHED'}


def get_parent(node):
    parents = bpy.data.objects[node].parent
    parent = None
    if parents is None:
        pass
    else:
        parent = parents
    return parent


def vector_length(v):
    return math.sqrt(v[0]*v[0] + v[1]*v[1] + v[2]*v[2])


def vector_norm(v):
    length = vector_length(v)
    if length == 0:
        length = 1
    return [v[0]/length, v[1]/length, v[2]/length]
