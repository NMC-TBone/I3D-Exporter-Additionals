"""uv_tools.py includes different tools for uv"""

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

class TOOLS_OT_uvset(bpy.types.Operator):
    bl_label = "Generate UVset 2"
    bl_idname = "tools.make_uvset"
    bl_description = "Generate UVset 2 from selected objects."
    bl_options = {'REGISTER', 'UNDO'}

    def four(self):
        selected_obj = bpy.context.selected_objects
        for obj in selected_obj:
            if obj.type == 'MESH':
                obj.data.uv_layers[0].name = 'UVset1'
            if not 'UVset2' in obj.data.uv_layers:
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
        bpy.ops.transform.resize(value=(0.5, 0.5, 0.5))
        bpy.ops.object.editmode_toggle()
        bpy.context.object.name = "trackLink.001"
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

    def sixteen(self):
        selected_obj = bpy.context.selected_objects
        for obj in selected_obj:
            if obj.type == 'MESH':
                obj.data.uv_layers[0].name = 'UVset1'
            if not 'UVset2' in obj.data.uv_layers:
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
        bpy.ops.transform.resize(value=(0.25, 0.25, 0.25))
        bpy.ops.object.editmode_toggle()
        bpy.context.object.name = "trackLink.001"
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

    def execute(self, context):
        if context.scene.i3deapg.size_dropdown == 'four':
            self.four()
            self.report({'INFO'}, "UVset2 2x2 Created")
            return {'FINISHED'}
        if context.scene.i3deapg.size_dropdown == 'sixteen':
            self.sixteen()
            self.report({'INFO'}, "UVset2 4x4 Created")
            return {'FINISHED'}
        return {'FINISHED'}