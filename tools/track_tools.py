"""track_tools.py includes different tools for uv"""

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


class I3DEA_OT_make_uvset(bpy.types.Operator):
    bl_label = "Generate UVset 2"
    bl_idname = "i3dea.make_uvset"
    bl_description = "Generate UVset 2 from selected objects."
    bl_options = {'REGISTER', 'UNDO'}

    def four(self, context):
        if not bpy.context.active_object:
            self.report({'ERROR'}, "No selected object!")
            return {'CANCELLED'}
        if len(bpy.context.selected_objects) > 0:
            mode = bpy.context.object.mode
            for obj in bpy.context.selected_objects:
                if not obj.type == "MESH":
                    continue
                if not mode == 'OBJECT':
                    bpy.ops.object.mode_set(mode='OBJECT')
        selected_obj = bpy.context.selected_objects
        for obj in selected_obj:
            if obj.type == 'MESH':
                obj.data.uv_layers[0].name = 'UVset1'
            if 'UVset2' not in obj.data.uv_layers:
                obj.data.uv_layers.new(name="UVset2")

        # start location X 0.25
        # start location Y 0.25
        # scale 0.5
        original_type = bpy.context.area.ui_type
        bpy.context.area.ui_type = 'UV'
        bpy.context.space_data.cursor_location[0] = 0.25
        bpy.context.space_data.cursor_location[1] = 0.25
        bpy.context.object.data.uv_layers['UVset2'].active = True
        bpy.ops.object.editmode_toggle()
        bpy.ops.uv.select_all(action='SELECT')
        bpy.context.space_data.pivot_point = 'CENTER'
        bpy.ops.uv.snap_selected(target='CURSOR_OFFSET')
        bpy.ops.transform.resize(value=[0.5, 0.5, 0.5])
        bpy.ops.object.editmode_toggle()
        bpy.context.object.name = context.scene.i3dea.custom_text + ".001"
        bpy.ops.object.duplicate_move()
        bpy.context.space_data.cursor_location[0] = 0.75
        bpy.context.space_data.cursor_location[1] = 0.25
        bpy.context.object.data.uv_layers['UVset2'].active = True
        bpy.ops.object.editmode_toggle()
        bpy.ops.uv.select_all(action='SELECT')
        bpy.ops.uv.snap_selected(target='CURSOR_OFFSET')
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.duplicate_move()
        bpy.context.space_data.cursor_location[0] = 0.75
        bpy.context.space_data.cursor_location[1] = 0.75
        bpy.context.object.data.uv_layers['UVset2'].active = True
        bpy.ops.object.editmode_toggle()
        bpy.ops.uv.select_all(action='SELECT')
        bpy.ops.uv.snap_selected(target='CURSOR_OFFSET')
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.duplicate_move()
        bpy.context.space_data.cursor_location[0] = 0.25
        bpy.context.space_data.cursor_location[1] = 0.75
        bpy.context.object.data.uv_layers['UVset2'].active = True
        bpy.ops.object.editmode_toggle()
        bpy.ops.uv.select_all(action='SELECT')
        bpy.ops.uv.snap_selected(target='CURSOR_OFFSET')
        bpy.ops.object.editmode_toggle()
        bpy.context.area.ui_type = original_type
        self.report({'INFO'}, "UVset2 2x2 Created")

    def sixteen(self, context):
        if not bpy.context.active_object:
            self.report({'ERROR'}, "No selected object!")
            return {'CANCELLED'}
        if len(bpy.context.selected_objects) > 0:
            mode = bpy.context.object.mode
            for obj in bpy.context.selected_objects:
                if not obj.type == "MESH":
                    continue
                if not mode == 'OBJECT':
                    bpy.ops.object.mode_set(mode='OBJECT')
        selected_obj = bpy.context.selected_objects
        for obj in selected_obj:
            if obj.type == 'MESH':
                obj.data.uv_layers[0].name = 'UVset1'
            if 'UVset2' not in obj.data.uv_layers:
                obj.data.uv_layers.new(name="UVset2")

        # start location X 0.125
        # start location Y 0.125
        # scale 0.25
        original_type = bpy.context.area.ui_type
        bpy.context.area.ui_type = 'UV'
        bpy.context.space_data.cursor_location[0] = 0.125
        bpy.context.space_data.cursor_location[1] = 0.125
        bpy.context.object.data.uv_layers['UVset2'].active = True
        bpy.ops.object.editmode_toggle()
        bpy.ops.uv.select_all(action='SELECT')
        bpy.context.space_data.pivot_point = 'CENTER'
        bpy.ops.uv.snap_selected(target='CURSOR_OFFSET')
        bpy.ops.transform.resize(value=[0.25, 0.25, 0.25])
        bpy.ops.object.editmode_toggle()
        bpy.context.object.name = context.scene.i3dea.custom_text + ".001"
        bpy.ops.object.duplicate_move()
        bpy.context.space_data.cursor_location[0] = 0.375
        bpy.context.space_data.cursor_location[1] = 0.125
        bpy.context.object.data.uv_layers['UVset2'].active = True
        bpy.ops.object.editmode_toggle()
        bpy.ops.uv.select_all(action='SELECT')
        bpy.ops.uv.snap_selected(target='CURSOR_OFFSET')
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.duplicate_move()
        bpy.context.space_data.cursor_location[0] = 0.625
        bpy.context.space_data.cursor_location[1] = 0.125
        bpy.context.object.data.uv_layers['UVset2'].active = True
        bpy.ops.object.editmode_toggle()
        bpy.ops.uv.select_all(action='SELECT')
        bpy.ops.uv.snap_selected(target='CURSOR_OFFSET')
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.duplicate_move()
        bpy.context.space_data.cursor_location[0] = 0.875
        bpy.context.space_data.cursor_location[1] = 0.125
        bpy.context.object.data.uv_layers['UVset2'].active = True
        bpy.ops.object.editmode_toggle()
        bpy.ops.uv.select_all(action='SELECT')
        bpy.ops.uv.snap_selected(target='CURSOR_OFFSET')
        bpy.ops.object.editmode_toggle()
        # start location X 0.875
        # start location Y 0.375
        bpy.ops.object.duplicate_move()
        bpy.context.space_data.cursor_location[0] = 0.875
        bpy.context.space_data.cursor_location[1] = 0.375
        bpy.context.object.data.uv_layers['UVset2'].active = True
        bpy.ops.object.editmode_toggle()
        bpy.ops.uv.select_all(action='SELECT')
        bpy.ops.uv.snap_selected(target='CURSOR_OFFSET')
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.duplicate_move()
        bpy.context.space_data.cursor_location[0] = 0.625
        bpy.context.space_data.cursor_location[1] = 0.375
        bpy.context.object.data.uv_layers['UVset2'].active = True
        bpy.ops.object.editmode_toggle()
        bpy.ops.uv.select_all(action='SELECT')
        bpy.ops.uv.snap_selected(target='CURSOR_OFFSET')
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.duplicate_move()
        bpy.context.space_data.cursor_location[0] = 0.375
        bpy.context.space_data.cursor_location[1] = 0.375
        bpy.context.object.data.uv_layers['UVset2'].active = True
        bpy.ops.object.editmode_toggle()
        bpy.ops.uv.select_all(action='SELECT')
        bpy.ops.uv.snap_selected(target='CURSOR_OFFSET')
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.duplicate_move()
        bpy.context.space_data.cursor_location[0] = 0.125
        bpy.context.space_data.cursor_location[1] = 0.375
        bpy.context.object.data.uv_layers['UVset2'].active = True
        bpy.ops.object.editmode_toggle()
        bpy.ops.uv.select_all(action='SELECT')
        bpy.ops.uv.snap_selected(target='CURSOR_OFFSET')
        bpy.ops.object.editmode_toggle()
        # start location X 0.125
        # start location Y 0.625
        bpy.ops.object.duplicate_move()
        bpy.context.space_data.cursor_location[0] = 0.125
        bpy.context.space_data.cursor_location[1] = 0.625
        bpy.context.object.data.uv_layers['UVset2'].active = True
        bpy.ops.object.editmode_toggle()
        bpy.ops.uv.select_all(action='SELECT')
        bpy.ops.uv.snap_selected(target='CURSOR_OFFSET')
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.duplicate_move()
        bpy.context.space_data.cursor_location[0] = 0.375
        bpy.context.space_data.cursor_location[1] = 0.625
        bpy.context.object.data.uv_layers['UVset2'].active = True
        bpy.ops.object.editmode_toggle()
        bpy.ops.uv.select_all(action='SELECT')
        bpy.ops.uv.snap_selected(target='CURSOR_OFFSET')
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.duplicate_move()
        bpy.context.space_data.cursor_location[0] = 0.625
        bpy.context.space_data.cursor_location[1] = 0.625
        bpy.context.object.data.uv_layers['UVset2'].active = True
        bpy.ops.object.editmode_toggle()
        bpy.ops.uv.select_all(action='SELECT')
        bpy.ops.uv.snap_selected(target='CURSOR_OFFSET')
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.duplicate_move()
        bpy.context.space_data.cursor_location[0] = 0.875
        bpy.context.space_data.cursor_location[1] = 0.625
        bpy.context.object.data.uv_layers['UVset2'].active = True
        bpy.ops.object.editmode_toggle()
        bpy.ops.uv.select_all(action='SELECT')
        bpy.ops.uv.snap_selected(target='CURSOR_OFFSET')
        bpy.ops.object.editmode_toggle()
        # start location X 0.875
        # start location Y 0.875
        bpy.ops.object.duplicate_move()
        bpy.context.space_data.cursor_location[0] = 0.875
        bpy.context.space_data.cursor_location[1] = 0.875
        bpy.context.object.data.uv_layers['UVset2'].active = True
        bpy.ops.object.editmode_toggle()
        bpy.ops.uv.select_all(action='SELECT')
        bpy.ops.uv.snap_selected(target='CURSOR_OFFSET')
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.duplicate_move()
        bpy.context.space_data.cursor_location[0] = 0.625
        bpy.context.space_data.cursor_location[1] = 0.875
        bpy.context.object.data.uv_layers['UVset2'].active = True
        bpy.ops.object.editmode_toggle()
        bpy.ops.uv.select_all(action='SELECT')
        bpy.ops.uv.snap_selected(target='CURSOR_OFFSET')
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.duplicate_move()
        bpy.context.space_data.cursor_location[0] = 0.375
        bpy.context.space_data.cursor_location[1] = 0.875
        bpy.context.object.data.uv_layers['UVset2'].active = True
        bpy.ops.object.editmode_toggle()
        bpy.ops.uv.select_all(action='SELECT')
        bpy.ops.uv.snap_selected(target='CURSOR_OFFSET')
        bpy.ops.object.editmode_toggle()
        bpy.ops.object.duplicate_move()
        bpy.context.space_data.cursor_location[0] = 0.125
        bpy.context.space_data.cursor_location[1] = 0.875
        bpy.context.object.data.uv_layers['UVset2'].active = True
        bpy.ops.object.editmode_toggle()
        bpy.ops.uv.select_all(action='SELECT')
        bpy.ops.uv.snap_selected(target='CURSOR_OFFSET')
        bpy.ops.object.editmode_toggle()
        bpy.context.area.ui_type = original_type
        self.report({'INFO'}, "UVset2 4x4 Created")

    def execute(self, context):
        if context.scene.i3dea.size_dropdown == 'four':
            self.four(context)
            return {'FINISHED'}
        if context.scene.i3dea.size_dropdown == 'sixteen':
            self.sixteen(context)
            return {'FINISHED'}
        return {'FINISHED'}


class I3DEA_OT_add_empty(bpy.types.Operator):
    bl_label = "Create empties"
    bl_idname = "i3dea.add_empty"
    bl_description = "Create empties between selected objects"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        selected_list = [obj for obj in bpy.context.selected_objects if obj.type == 'MESH']
        for _ in range(context.scene.i3dea.add_empty_int):
            for loop_obj in selected_list:
                # print(loop_obj)
                bpy.ops.object.empty_add(radius=0)
                empty = bpy.context.active_object
                empty.name = loop_obj.name + ".001"

                if loop_obj.parent is not None:
                    empty.parent = loop_obj.parent

        bpy.ops.object.select_all(action='DESELECT')
        for loop_obj in selected_list:
            bpy.data.objects[loop_obj.name].select_set(True)

            # attrs.select_set(True)

            self.report({'INFO'}, "Empties added")
            return {'FINISHED'}
