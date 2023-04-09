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
import bmesh
import math

import mathutils
from mathutils import Vector, Matrix

from ..helper_functions import check_i3d_exporter_type, check_obj_type, get_curve_length

giants_i3d, stjerne_i3d = check_i3d_exporter_type()


def create_empties(objs, amount):
    """
    It will add x amount of empties in between each object

    param objs: The objects the empties will be added in between
    param amount: The amount of empties that will be added between each object
    """
    for obj in objs:
        for _ in range(amount):
            empty = bpy.data.objects.new(obj.name + ".001", None)
            empty.empty_display_size = 0
            empty.location = obj.location
            bpy.context.collection.objects.link(empty)
            if obj.parent is not None:
                empty.parent = obj.parent
                empty.matrix_parent_inverse = obj.matrix_world.inverted()


class I3DEA_OT_add_empty(bpy.types.Operator):
    bl_label = "Create empties"
    bl_idname = "i3dea.add_empty"
    bl_description = "Create empties between selected objects"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        selected_list = [obj for obj in context.selected_objects if obj.type == 'MESH']
        create_empties(selected_list, context.scene.i3dea.add_empty_int)
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
            self.report({'ERROR'}, f"The active object ({context.active_object.name}) is not a curve")
            return {'CANCELLED'}
        else:
            curve_length = get_curve_length(context.object.name)
            context.scene.i3dea.curve_length_disp = str(round(curve_length, 6))
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
            curve_length = get_curve_length(curve.name)
            float_val = curve_length / bpy.context.scene.i3dea.piece_distance
            bpy.context.scene.i3dea.track_piece_amount = float_val
        return {'FINISHED'}


class I3DEA_OT_visualization(bpy.types.Operator):
    bl_idname = "i3dea.visualization"
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
            else:
                self.report({'ERROR'}, "No curve in scene")

        for piece, curve in zip(piece_list, curve_list):
            hierarchy_name = 'track_visualization'
            space = context.scene.i3dea.track_vis_distance
            curve_length = get_curve_length(curve.name)
            if bpy.context.scene.i3dea.track_type_method == 'CATERPILLAR':
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
                plane.modifiers["Array"].count = context.scene.i3dea.track_vis_amount
                plane.modifiers.new("Curve", 'CURVE')
                plane.modifiers["Curve"].object = curve
                plane.modifiers["Curve"].deform_axis = 'NEG_Y'
                plane.lock_location[0] = True
                plane.lock_location[2] = True
                plane.keyframe_insert("location", frame=1)
                plane.location[1] = curve_length
                plane.keyframe_insert("location", frame=250)
                new = bpy.data.objects.new(piece.name + "_visual", bpy.data.objects[piece.name].data)
                context.collection.objects.link(new)
                new.parent = plane
                new.hide_set(True)

            elif bpy.context.scene.i3dea.track_type_method == 'RUBBER':
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

            elif bpy.context.scene.i3dea.track_type_method == 'BOGIE':
                self.report({'WARNING'}, "Bogie is not supported yet")
                return {'CANCELLED'}

            def stop_anim(scene):
                if scene.frame_current == 250:
                    bpy.ops.screen.animation_cancel()

            bpy.app.handlers.frame_change_pre.append(stop_anim)
            bpy.ops.screen.animation_play()

        return {'FINISHED'}


class I3DEA_OT_visualization_del(bpy.types.Operator):
    bl_idname = "i3dea.visualization_del"
    bl_label = "Delete track visualization"
    bl_description = "Deletes the track visualization"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj_list = [obj for obj in bpy.data.objects if obj.name.startswith("track_visualization")]

        if obj_list:
            for obj in obj_list:
                for child in obj.children_recursive:
                    child.hide_set(False)
                    bpy.data.objects.remove(child)
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

        original_obj = context.object
        create_second_uv(original_obj, original_obj.name + "_UVset2", int(context.scene.i3dea.size_dropdown))

        if context.scene.i3dea.size_dropdown == '4':
            self.report({'INFO'}, "UVset2 2x2 Created")
        else:
            self.report({'INFO'}, "UVset2 4x4 Created")
        return {'FINISHED'}


class I3DEA_OT_automatic_track_creation(bpy.types.Operator):
    bl_label = "Generate UVset 2"
    bl_idname = "i3dea.automatic_track_creation"
    bl_description = "Create track setup depending on the above settings."
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        i3dea = context.scene.i3dea
        sel_obj = context.object
        if not sel_obj:
            self.report({'ERROR'}, "No selected object!")
            return {'CANCELLED'}
        if not sel_obj.type == 'MESH':
            self.report({'ERROR'}, "Selected object is not a mesh!")
            return {'CANCELLED'}
        if i3dea.auto_all_curves == "None":
            self.report({'ERROR'}, "No curve chosen!")
            return {'CANCELLED'}

        name = i3dea.auto_name if i3dea.auto_name else "myTrack"

        if "zzz_data_ignore" not in bpy.data.objects:
            data_ignore = bpy.data.objects.new("zzz_data_ignore", None)
            bpy.context.collection.objects.link(data_ignore)
            data_ignore.empty_display_size = 0
        data_ignore = bpy.data.objects["zzz_data_ignore"]

        track_main_parent = bpy.data.objects.new(name, None)
        bpy.context.collection.objects.link(track_main_parent)
        track_main_parent.empty_display_size = 0
        track_geo = bpy.data.objects.new(f"{name}Geo", None)
        bpy.context.collection.objects.link(track_geo)
        track_geo.empty_display_size = 0
        track_geo.location = sel_obj.location
        track_geo.parent = track_main_parent
        track_geo.matrix_parent_inverse = track_main_parent.matrix_world.inverted()

        if giants_i3d:
            track_geo['I3D_receiveShadows'] = True
            track_geo['I3D_castsShadows'] = True
            track_geo['I3D_clipDistance'] = 300.00
            track_geo['I3D_mergeChildren'] = True
            track_geo['I3D_objectDataExportOrientation'] = True
            track_geo['I3D_objectDataExportPosition'] = True

        if i3dea.auto_create_bbox:
            create_bbox(i3dea.auto_all_curves, name, track_geo.name, sel_obj.dimensions[0])

        if i3dea.auto_use_uvset:
            second_uv = create_second_uv(sel_obj, name, int(i3dea.auto_uvset_dropdown))
            if i3dea.auto_add_vmask:
                vmask = vmask_bake_objs(second_uv, name)
                vmask.parent = data_ignore
        else:
            second_uv = create_second_uv(sel_obj, name, int(i3dea.auto_uvset_dropdown), existing_uv=True)

        if not i3dea.auto_allow_curve_scale:
            amount = i3dea.auto_fxd_amount_int if i3dea.auto_fixed_amount \
                else round(get_curve_length(i3dea.auto_all_curves) / i3dea.auto_distance)

        else:
            amount = scale_curve_to_fit_distance(i3dea.auto_all_curves, i3dea.auto_distance)

        all_pieces = create_from_amount(second_uv, amount)
        for obj in all_pieces:
            obj.parent = track_geo
            obj.matrix_parent_inverse = track_geo.matrix_world.inverted()

        if i3dea.auto_add_empties:
            create_empties(all_pieces, i3dea.auto_empty_int)

        bpy.data.objects[i3dea.auto_all_curves].parent = data_ignore
        sel_obj.parent = data_ignore
        sel_obj.matrix_parent_inverse = data_ignore.matrix_world.inverted()
        self.report({'INFO'}, "Full track setup created and ready for export!")
        return {'FINISHED'}


def create_second_uv(original_obj, name, amount, existing_uv=False):
    """
    Creates second UV set for the given object by copying it multiple times and transforming each copy's UV set.

    param original_obj: Active object that will be used when this function is called
    param name:
    """
    grid_size = math.ceil(math.sqrt(amount))
    ref_obj = original_obj.copy()
    ref_obj.data = original_obj.data.copy()
    if not existing_uv:
        if 'uvSet2' not in ref_obj.data.uv_layers:
            ref_obj.data.uv_layers.new(name="uvSet2")
    else:
        if len(ref_obj.data.uv_layers) < 2:
            ref_obj.data.uv_layers.new(name="uvSet2")

    new_objs = []
    for i, _ in enumerate(range(amount)):
        new_obj = ref_obj.copy()
        new_obj.data = ref_obj.data.copy()

        bpy.context.collection.objects.link(new_obj)

        new_obj.name = f"{name}_{i:03}"

        bm = bmesh.new()
        bm.from_mesh(new_obj.data)

        uv2 = bm.loops.layers.uv[1]
        uv1 = bm.loops.layers.uv[0]

        for bm_vert in bm.verts:
            for link_loop in bm_vert.link_loops:
                uv2_data = link_loop[uv2]
                uv1_data = link_loop[uv1]
                scale_matrix = mathutils.Matrix.Diagonal((1 / grid_size, 1 / grid_size))
                uv2_data.uv = uv1_data.uv @ scale_matrix
                pos = divmod(i, grid_size)
                uv2_data.uv[0] = uv2_data.uv[0] + (pos[1] / grid_size)
                uv2_data.uv[1] = uv2_data.uv[1] + (1 - ((pos[0] + 1) / grid_size))
        bm.to_mesh(new_obj.data)
        new_objs.append(new_obj)

    bpy.data.objects.remove(ref_obj, do_unlink=True)
    return new_objs


def vmask_bake_objs(objs, name):
    """
    Input objects will be spread out in a line and 1st uv will be removed so its ready for bake

    param objs: objects to be added to vmask bake
    param name:
    """
    vmask_empty = bpy.data.objects.new("objsForBake", None)
    bpy.context.collection.objects.link(vmask_empty)
    vmask_empty.empty_display_size = 0

    location = 0
    for i, obj in enumerate(objs):
        location += 1
        vmask_obj = obj.copy()
        vmask_obj.data = obj.data.copy()
        bpy.context.collection.objects.link(vmask_obj)
        vmask_obj.select_set(True)
        vmask_obj.name = f"{name}_vmask_{i:03}"
        vmask_obj.location[1] = location
        vmask_obj.parent = vmask_empty
        vmask_obj.data.uv_layers.remove(vmask_obj.data.uv_layers[0])
    return vmask_empty


def create_bbox(curve_name, name, obj_name, dim_x):
    """
    Creates a bounding box/volume around the curve

    param curve_name: Name of the curve
    param name: name of the bbox
    param obj_name: Name of object
    param dim_x: X dimension
    """
    curve = bpy.data.objects[curve_name]
    bbox = [Vector(b) for b in curve.bound_box]
    center = sum(bbox, Vector()) / 8
    center = curve.matrix_world @ center
    bpy.ops.mesh.primitive_cube_add(location=center)
    bbox = bpy.context.object
    bbox.name = "zzz_bbox_{}Geo".format(name)
    dim = curve.dimensions + Vector((1.0, 1.0, 1.0))
    bbox.dimensions = dim
    bpy.context.view_layer.update()
    bbox.dimensions[0] = dim_x + 1
    bpy.context.view_layer.update()
    matrix = bbox.matrix_world.copy()
    for vert in bbox.data.vertices:
        vert.co = matrix @ vert.co
    bbox.matrix_world.identity()

    if giants_i3d:
        bbox['I3D_boundingVolume'] = obj_name
    bbox.hide_set(True)
    return bbox


def create_from_amount(objects, amount):
    """
    Takes in a list of objects and duplicates them until the desired amount is reached.
    The new objects will have names that are incremented from the original objects.

    param objects: List with all the objects to be duplicated x times
    param amount: Amount of times the loop will be run
    """
    obj_list = objects
    last_suffix = int(obj_list[-1].name.split("_")[-1])
    for i in range(amount - len(obj_list)):
        old_object = obj_list[i % len(obj_list)]
        new_object = old_object.copy()
        new_object.data = old_object.data.copy()
        new_object.name = "{}_{:03d}".format(old_object.name.split("_")[0], last_suffix+i+1)
        bpy.context.collection.objects.link(new_object)
        obj_list.append(new_object)
    return obj_list


def scale_curve_to_fit_distance(curve_name, distance):
    i = 0
    while True:
        length = get_curve_length(curve_name)
        amount = length / distance
        if math.isclose(round(amount, 4) % 1, 0) or i > 250:
            break
        rounded_amount = round(amount)
        scale_factor = rounded_amount / amount
        scale_matrix = Matrix.Scale(scale_factor, 4)
        bpy.data.objects[curve_name].data.transform(scale_matrix)
        i += 1
    return round(amount)
