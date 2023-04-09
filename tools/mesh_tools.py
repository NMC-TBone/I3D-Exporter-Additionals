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

# mesh_tools.py includes different tools for mesh

import bpy
import bmesh
import math

from mathutils import Matrix, Vector


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
                bpy.ops.object.shade_smooth(use_auto_smooth=True)
                bpy.context.object.data.auto_smooth_angle = smooth_radians
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


class I3DEA_OT_xml_config(bpy.types.Operator):
    bl_idname = "i3dea.xml_config"
    bl_label = "Enable export to i3dMappings"
    bl_description = "When you run this all selected objects will be setup to export to i3dMappings and set the object name as Node ID"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        for obj in bpy.context.selected_objects:
            obj["I3D_XMLconfigBool"] = 1
            obj["I3D_XMLconfigID"] = obj.name
        return {'FINISHED'}


def check_parallel(fill_volume):
    # https://blender.stackexchange.com/questions/75517/selecting-faces-in-python
    def find_direction(normal, direction, limit=1.0):
        return direction.dot(normal) > limit

    def find_bottom(normal, limit=0.9999999):
        return find_direction(normal, Vector((0, 0, -1)), limit)

    def find_top(normal, limit=0.9999999):
        return find_direction(normal, Vector((0, 0, 1)), limit)

    def find_face_count():
        # Add all selected faces from bottom to a list
        sel_faces = []
        for faces in bpy.context.object.data.polygons:
            if faces.select:
                sel_faces.append(face)
        # print("Face count ", len(sel_faces))
        return len(sel_faces)

    def linked_faces():
        # runs linked flat faces and store the new selected faces to later compare number with find_face_count
        sel_faces_linked = []
        previous_mode = bpy.context.object.mode
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.faces_select_linked_flat(sharpness=math.radians(15))
        bpy.ops.object.editmode_toggle()
        for faces in bpy.context.object.data.polygons:
            if faces.select:
                sel_faces_linked.append(faces)
        bpy.ops.object.mode_set(mode=previous_mode, toggle=False)
        # print("Linked faces ", len(sel_faces_linked))
        return len(sel_faces_linked)

    prev_mode = fill_volume.mode
    bpy.ops.object.editmode_toggle()
    prev_select_type = bpy.context.tool_settings.mesh_select_mode[:]
    for poly in fill_volume.data.polygons:
        poly.select = False

    bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='FACE')
    bpy.context.tool_settings.mesh_select_mode = (False, False, True)
    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

    # Selects the bottom face
    for face in fill_volume.data.polygons:
        face.select = find_bottom(face.normal)

    bottom = False
    if True in [mesh.select for mesh in fill_volume.data.polygons]:
        bottom = True
        if find_face_count() != linked_faces():
            bottom = False

    # need to clear selection to get correct result for top faces
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

    # selects top faces
    for face in fill_volume.data.polygons:
        face.select = find_top(face.normal)

    top = False
    if True in [mesh.select for mesh in fill_volume.data.polygons]:
        top = True
        if find_face_count() != linked_faces():
            top = False

    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.select_all(action='DESELECT')

    bpy.context.tool_settings.mesh_select_mode = prev_select_type
    bpy.ops.object.mode_set(mode=prev_mode, toggle=False)

    return bottom, top


class I3DEA_OT_fill_volume(bpy.types.Operator):
    bl_idname = "i3dea.fill_volume"
    bl_label = "Check Fill Volume"
    bl_description = "Check if fill volume bottom face is flat"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if bpy.context.object.type == 'MESH':
            original_mode = bpy.context.object.mode
            bpy.ops.object.mode_set(mode='OBJECT')
            fill_volume = context.object
            if check_parallel(fill_volume)[0]:
                if check_parallel(fill_volume)[1]:
                    self.report({'INFO'}, fill_volume.name + " passed the tests")
                else:
                    self.report({'ERROR'}, fill_volume.name + " doesn't have parallel bottom and top face")
            else:
                self.report({'ERROR'}, fill_volume.name + " doesn't have flat bottom face")

            bpy.ops.object.select_all(action='DESELECT')
            fill_volume.select_set(True)
            context.view_layer.objects.active = fill_volume
            bpy.ops.object.mode_set(mode=original_mode)
        return {'FINISHED'}


class I3DEA_OT_mirror_orientation(bpy.types.Operator):
    bl_idname = "i3dea.mirror_orientation"
    bl_label = "Set Mirror Orientation"
    bl_description = "Sets mirror orientation based on camera and ref empty"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        camera = None
        mirror = None
        target = None
        for obj in bpy.context.selected_objects:
            # Get each selected object type (3 in total)
            if obj.type == 'CAMERA':
                camera = obj
            elif obj.type == 'MESH':
                mirror = obj
            elif obj.type == 'EMPTY':
                target = obj

        if camera and mirror and target:
            mirror_parent = mirror.parent if mirror.parent else None

            mirror_axis_target = bpy.data.objects.new("mirror_axis_target", None)
            bpy.context.collection.objects.link(mirror_axis_target)

            # Calculate the mirror_axis_target location
            v1 = (mirror.location - camera.location).normalized()
            v2 = (mirror.location - target.location).normalized()
            v3 = v1 + v2

            mirror_axis_target.location = mirror.location - v3

            # Using TRACK_TO constraint to correctly set up the orientation of the mirror
            mirror_axis_target.constraints.new('TRACK_TO')
            mirror_axis_target.constraints['Track To'].track_axis = 'TRACK_NEGATIVE_Z'
            mirror_axis_target.constraints['Track To'].up_axis = 'UP_Y'
            mirror_axis_target.constraints['Track To'].target = mirror
            bpy.ops.object.select_all(action='DESELECT')
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

            mirror_matrix = mirror.matrix_world.copy()
            if mirror_parent:
                mirror.parent = mirror_parent
            else:
                mirror.parent = None
            mirror.matrix_world = mirror_matrix

            bpy.data.objects.remove(mirror_axis_target)

        else:
            self.report({'ERROR'}, "You need to select 3 objects (camera, mirror, empty)")
        return {'FINISHED'}
