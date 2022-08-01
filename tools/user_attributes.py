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

# user_attributes.py makes it possible to easily add userAttributes that will work with Giants I3D exporter
# Integer isn't a supported type by Giants I3D exporter

import bpy


class I3DEA_OT_create_user_attribute(bpy.types.Operator):
    bl_idname = "i3dea.create_user_attribute"
    bl_label = "Create User Attribute"
    bl_description = "Create user attribute for selected objects"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        attr_type = context.scene.i3dea.user_attribute_type
        attr_name = context.scene.i3dea.user_attribute_name
        create_attr_name = "userAttribute_{}_{}".format(attr_type, attr_name)
        obj = context.object

        if obj:
            if context.scene.i3dea.user_attribute_name:
                if attr_type == 'boolean':
                    obj[create_attr_name] = False
                    ui = obj.id_properties_ui(create_attr_name)
                    ui.update(description=create_attr_name)
                    ui.update(default=False)
                    ui.update(min=False)
                    ui.update(max=True)
                if attr_type == 'float':
                    obj[create_attr_name] = 0.0
                    ui = obj.id_properties_ui(create_attr_name)
                    ui.update(description=create_attr_name)
                    ui.update(default=0.0)
                    ui.update(min=-200)
                    ui.update(max=200)
                if attr_type == 'string':
                    obj[create_attr_name] = ""
                if attr_type == 'scriptCallback':
                    obj[create_attr_name] = ""
        return {'FINISHED'}
