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

# track_tools.py includes different tools for uv

import bpy
import math

from mathutils import Vector

from ..helper_functions import check_obj_type, check_i3d_exporter_type

giants_i3d, stjerne_i3d, dcc, I3DRemoveAttributes = check_i3d_exporter_type()

"""
for obj in bpy.context.selected_objects:
    name = obj.name
    new_name = name.replace(".", "_")
    obj.name = new_name
"""


def getCurveLength(curve_obj):
    length = curve_obj.data.splines[0].calc_length(resolution=1024)
    return length


class I3DEA_OT_add_empty(bpy.types.Operator):
    bl_label = "Create empties"
    bl_idname = "i3dea.add_empty"
    bl_description = "Create empties between selected objects"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        selected_list = [obj for obj in bpy.context.selected_objects if obj.type == 'MESH']
        for _ in range(context.scene.i3dea.add_empty_int):
            for loop_obj in selected_list:
                bpy.ops.object.empty_add(radius=0)
                empty = bpy.context.active_object
                empty.name = loop_obj.name + ".001"
                if loop_obj.parent is not None:
                    empty.parent = loop_obj.parent

        bpy.ops.object.select_all(action='DESELECT')
        for loop_obj in selected_list:
            bpy.data.objects[loop_obj.name].select_set(True)
            self.report({'INFO'}, "Empties added")
            return {'FINISHED'}


class I3DEA_OT_curve_length(bpy.types.Operator):
    bl_idname = "i3dea.curve_length"
    bl_label = "Get Curve Length"
    bl_description = "Measure length of the selected curve"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if context.view_layer.objects.active is None:
            self.report({'ERROR'}, "No active object in scene")
            return {'CANCELLED'}
        if not context.object.type == "CURVE":
            self.report({'ERROR'}, "The active object [" + context.active_object.name + "] is not a curve")
            return {'CANCELLED'}
        else:
            curve_length = getCurveLength(context.object)
            bpy.context.scene.i3dea.curve_length_disp = curve_length
        return {'FINISHED'}


class I3DEA_OT_calculate_amount(bpy.types.Operator):
    bl_idname = "i3dea.calculate_amount"
    bl_label = "Calculate Amount"
    bl_description = "Calculates how many track pieces that fit from given track piece length and curve length"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if context.view_layer.objects.active is None:
            self.report({'ERROR'}, "No active object in scene")
            return {'CANCELLED'}

        elif len(context.selected_objects) == 2:
            obj1 = context.selected_objects[0].location
            obj2 = context.selected_objects[1].location
            context.scene.i3dea.piece_distance = abs(obj1[1] - obj2[1])
        elif context.object.type == 'CURVE':
            curve = bpy.context.object
            curve_length = getCurveLength(curve)
            float_val = curve_length/bpy.context.scene.i3dea.piece_distance
            bpy.context.scene.i3dea.track_piece_amount = float_val
        return {'FINISHED'}


class I3DEA_OT_track_on_curve(bpy.types.Operator):
    bl_idname = "i3dea.track_on_curve"
    bl_label = "Add track to curve"
    bl_description = "Makes a full setup to see how the track will look along the curve"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        piece_list = []
        curve_list = []

        for obj in context.selected_objects:
            if obj.type == 'MESH':
                piece_list.append(obj)
            if obj.type == 'CURVE':
                curve_list.append(obj)

        if len(curve_list) < 1:
            for curve in context.scene.objects:
                if curve.type == 'CURVE':
                    curve_list.append(curve)
                    break

        for piece, curve in zip(piece_list, curve_list):
            hierarchy_name = 'track_visualization'
            space = bpy.context.scene.i3dea.piece_distance
            curve_length = getCurveLength(curve)
            if not bpy.context.scene.i3dea.rubber_track:
                if bpy.context.scene.i3dea.track_piece_amount > 1:
                    piece_num = int(bpy.context.scene.i3dea.track_piece_amount)
                else:
                    piece_num = 25
                    self.report({'INFO'}, "No amount set in track piece amount, using default amount instead ({})".format(piece_num))

                bpy.ops.mesh.primitive_plane_add()
                plane = bpy.context.object
                plane.name = hierarchy_name
                plane.dimensions[1] = space
                bpy.ops.object.transform_apply(scale=True)
                plane.instance_type = 'FACES'
                plane.show_instancer_for_viewport = False
                plane.modifiers.new("Array", 'ARRAY')
                plane.modifiers["Array"].use_relative_offset = False
                plane.modifiers["Array"].use_constant_offset = True
                plane.modifiers["Array"].constant_offset_displace[0] = 0
                plane.modifiers["Array"].constant_offset_displace[1] = space
                plane.modifiers["Array"].count = piece_num
                plane.modifiers.new("Curve", 'CURVE')
                plane.modifiers["Curve"].object = curve
                plane.modifiers["Curve"].deform_axis = 'NEG_Y'
                plane.lock_location[0] = True
                plane.lock_location[2] = True
                plane.keyframe_insert("location", frame=1)
                plane.location[1] = curve_length
                plane.keyframe_insert("location", frame=250)
                piece.parent = plane
                piece.hide_set(True)

            if bpy.context.scene.i3dea.rubber_track:
                obj = context.object
                # bpy.ops.object.duplicate()
                duplicate = bpy.data.objects.new(hierarchy_name, bpy.data.objects[obj.name].data)
                duplicate.dimensions[1] = curve_length
                duplicate.modifiers.new("Curve", 'CURVE')
                duplicate.modifiers["Curve"].object = curve
                duplicate.modifiers["Curve"].deform_axis = 'NEG_Y'
                duplicate.keyframe_insert("location", frame=1)
                duplicate.location[1] = curve_length
                duplicate.keyframe_insert("location", frame=250)
                context.collection.objects.link(duplicate)

            def stop_anim(scene):
                if scene.frame_current == 250:
                    bpy.ops.screen.animation_cancel()

            bpy.app.handlers.frame_change_pre.append(stop_anim)
            bpy.ops.screen.animation_play()

        return {'FINISHED'}


class I3DEA_OT_track_on_curve_delete(bpy.types.Operator):
    bl_idname = "i3dea.track_on_curve_delete"
    bl_label = "Delete track visualization"
    bl_description = "Deletes the track visualization"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj_list = [obj for obj in bpy.data.objects if obj.name.startswith("track_visualization")]

        if obj_list:
            for obj in obj_list:
                for child in obj.children_recursive:
                    child.hide_set(False)
                bpy.data.objects.remove(obj)
                self.report({'INFO'}, "Track Visualization deleted")
        return {'FINISHED'}


class I3DEA_OT_make_uvset(bpy.types.Operator):
    bl_label = "Generate UVset 2"
    bl_idname = "i3dea.make_uvset"
    bl_description = "Generate UVset 2 from selected objects."
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if not context.object:
            self.report({'ERROR'}, "No selected object!")
            return {'CANCELLED'}
        if not context.object.type == 'MESH':
            self.report({'ERROR'}, "Selected object is not a mesh!")
            return {'CANCELLED'}

        name = "track"
        if bpy.context.scene.i3dea.custom_text_box:
            name = bpy.context.scene.i3dea.custom_text

        original_obj = context.object
        check_obj_type(original_obj)
        original_obj.name = "originalMesh"
        duplicated_obj = create_second_uv(original_obj, name)
        for obj in duplicated_obj:
            obj.select_set(True)

        if not context.scene.i3dea.advanced_mode:
            if context.scene.i3dea.size_dropdown == 'four':
                self.report({'INFO'}, "UVset2 2x2 Created")
            else:
                self.report({'INFO'}, "UVset2 4x4 Created")
            return {'FINISHED'}

        elif context.scene.i3dea.advanced_mode and not context.scene.i3dea.all_curves == "None":
            vmask_bake = vmask_bake_objs(duplicated_obj, name)
            bpy.ops.object.empty_add(radius=0)
            empty_parent = context.object
            empty_parent.name = name
            bpy.ops.object.empty_add(radius=0)
            track_geo = bpy.context.object
            track_geo.name = "{}Geo".format(name)
            if giants_i3d:
                dcc.I3DSetAttrBool(track_geo.name, 'I3D_receiveShadows', True)
                dcc.I3DSetAttrBool(track_geo.name, 'I3D_castsShadows', True)
                dcc.I3DSetAttrBool(track_geo.name, 'I3D_clipDistance', 300)
                dcc.I3DSetAttrBool(track_geo.name, 'I3D_mergeChildren', True)
                dcc.I3DSetAttrBool(track_geo.name, 'I3D_objectDataExportOrientation', True)
                dcc.I3DSetAttrBool(track_geo.name, 'I3D_objectDataExportPosition', True)
            obj_name = track_geo.name
            dim_x = original_obj.dimensions[0]
            bbox = create_bbox(context.scene.i3dea.all_curves, name, obj_name, dim_x)
            bbox.hide_set(True)
            all_pieces = create_from_amount(duplicated_obj)
            for obj in all_pieces:
                obj.select_set(True)
                obj.parent = track_geo

            if context.scene.i3dea.add_empties:
                bpy.ops.i3dea.add_empty()

            track_geo.parent = empty_parent

            if "zzz_data_ignore" not in bpy.data.objects:
                bpy.ops.object.empty_add(radius=0)
                data_ignore = bpy.context.object
                data_ignore.name = "zzz_data_ignore"
            data_ignore = bpy.data.objects["zzz_data_ignore"]

            bpy.data.objects[context.scene.i3dea.all_curves].parent = data_ignore
            original_obj.parent = data_ignore
            vmask_bake.parent = data_ignore
            self.report({'INFO'}, "Full track setup created and ready for export!")
            return {'FINISHED'}


def create_second_uv(original_obj, name):
    # Create a copy/duplicate of the active object
    obj = original_obj.copy()
    obj.data = original_obj.data.copy()
    bpy.context.collection.objects.link(obj)
    obj.name = name

    # Check if UVset2 exist
    if 'UVset2' not in obj.data.uv_layers:
        obj.data.uv_layers.new(name="UVset2")
    obj.data.uv_layers['UVset2'].active = True
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = None

    # UV cursor coordinates
    values = ((0.25, 0.25), (0.75, 0.25), (0.75, 0.75), (0.25, 0.75))
    if bpy.context.scene.i3dea.size_dropdown == 'sixteen':
        values = ((0.125, 0.125), (0.375, 0.125), (0.625, 0.125), (0.875, 0.125), (0.875, 0.375), (0.625, 0.375), (0.375, 0.375), (0.125, 0.375), (0.125, 0.625), (0.375, 0.625),
                  (0.625, 0.625), (0.875, 0.625), (0.875, 0.875), (0.625, 0.875), (0.375, 0.875), (0.125, 0.875))
    # list of objects created in for loop
    duplicated_obj = []
    for i, value in enumerate(values):
        duplicate = obj.copy()
        duplicate.data = obj.data.copy()
        bpy.context.collection.objects.link(duplicate)
        duplicate.select_set(True)
        bpy.context.view_layer.objects.active = duplicate
        bpy.context.object.name = name + ".001"
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.object.mode_set(mode='OBJECT')
        original_type = bpy.context.area.ui_type
        bpy.context.area.ui_type = 'UV'
        bpy.context.space_data.cursor_location = value
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.uv.select_all(action='SELECT')
        bpy.context.space_data.pivot_point = 'CENTER'
        bpy.ops.uv.snap_selected(target='CURSOR_OFFSET')
        if bpy.context.scene.i3dea.size_dropdown == 'sixteen':
            bpy.ops.transform.resize(value=[0.25, 0.25, 0.25])
        else:
            bpy.ops.transform.resize(value=[0.5, 0.5, 0.5])
        bpy.ops.object.mode_set(mode='OBJECT')
        duplicated_obj.append(duplicate)
        duplicate.select_set(False)
        # Set ui back to the ui started in
        bpy.context.area.ui_type = original_type

    # Remove the first duplicated object
    bpy.data.objects.remove(obj)
    return duplicated_obj


def vmask_bake_objs(objs, name):
    bpy.ops.object.empty_add(radius=0)
    vmask_empty = bpy.context.object
    vmask_empty.name = "objsForBake"

    location = 0
    for obj in objs:
        location += 2
        vmask_obj = obj.copy()
        vmask_obj.data = obj.data.copy()
        bpy.context.collection.objects.link(vmask_obj)
        vmask_obj.select_set(True)
        vmask_obj.name = name + "_vmask.001"
        vmask_obj.parent = vmask_empty
        vmask_obj.data.uv_layers.remove(vmask_obj.data.uv_layers[0])
    return vmask_empty


def create_bbox(curve_name, name, obj_name, dim_x):
    prev_sel = bpy.context.selected_objects
    prev_cursor = Vector(bpy.context.scene.cursor.location)
    curve = bpy.data.objects[curve_name]
    curve.select_set(True)
    bpy.context.view_layer.objects.active = curve
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.curve.select_all(action='SELECT')
    bpy.ops.view3d.snap_cursor_to_selected()
    bpy.ops.object.mode_set(mode='OBJECT')
    curve_dim = curve.dimensions
    # Create bbox
    bpy.ops.mesh.primitive_cube_add()
    bbox = bpy.context.object
    bbox.name = "zzz_bbox_{}Geo".format(name)
    dim = curve_dim + Vector((1.0, 1.0, 1.0))
    bbox.dimensions = dim
    bpy.context.view_layer.update()
    bbox.dimensions[0] = dim_x + 1
    bpy.context.view_layer.update()
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if giants_i3d:
        dcc.I3DSetAttrString(bbox.name, 'I3D_boundingVolume', obj_name)
    bbox.select_set(False)
    bpy.context.scene.cursor.location = prev_cursor

    for obj in prev_sel:
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
    return bbox


def create_from_amount(objects):
    amount = int(bpy.context.scene.i3dea.track_piece_amount)
    obj_list = objects

    index = 0
    while len(obj_list) < amount:
        bpy.ops.object.select_all(action='DESELECT')
        old_object = obj_list[index]
        old_object.select_set(True)
        bpy.context.view_layer.objects.active = old_object
        bpy.ops.object.duplicate_move()
        new_object = bpy.context.object
        obj_list.append(new_object)
        index += 1
    return obj_list
