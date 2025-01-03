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
    bl_description = "Create user attribute for selected object"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        i3dea = context.scene.i3dea
        obj = context.object

        if obj:
            if attr_name := i3dea.user_attribute_name != "":
                if attr_name in [k.split("_")[-1] for k in obj.keys() if k.startswith("userAttribute_")]:
                    self.report({'ERROR'}, f"Attribute {attr_name} already exist.")
                    return {'CANCELLED'}
                else:
                    attr_type = i3dea.user_attribute_type
                    create_attr_name = f"userAttribute_{attr_type}_{attr_name}"
                    match attr_type:
                        case 'boolean':
                            obj[create_attr_name] = False
                            ui = obj.id_properties_ui(create_attr_name)
                            ui.update(description=create_attr_name)
                            ui.update(default=False)
                        case 'integer':
                            obj[create_attr_name] = 0
                            ui = obj.id_properties_ui(create_attr_name)
                            ui.update(description=create_attr_name)
                            ui.update(default=0)
                            ui.update(min=-200)
                            ui.update(max=200)
                        case 'float':
                            obj[create_attr_name] = 0.0
                            ui = obj.id_properties_ui(create_attr_name)
                            ui.update(description=create_attr_name)
                            ui.update(default=0.0)
                            ui.update(min=-200)
                            ui.update(max=200)
                        case 'string' | 'scriptCallback':
                            obj[create_attr_name] = ""
                    return {'FINISHED'}
            else:
                self.report({'ERROR'}, "Attribute name can't be empty.")
                return {'CANCELLED'}


class I3DEA_OT_delete_user_attribute(bpy.types.Operator):
    bl_idname = "i3dea.delete_user_attribute"
    bl_label = "Delete User Attribute"
    bl_description = "Delete selected user attribute"
    bl_options = {'UNDO'}

    attribute_name: bpy.props.StringProperty()

    def execute(self, context):
        obj = context.object

        if obj and self.attribute_name in obj:
            del obj[self.attribute_name]

        return {'FINISHED'}


classes = (
    I3DEA_OT_create_user_attribute,
    I3DEA_OT_delete_user_attribute
)
register, unregister = bpy.utils.register_classes_factory(classes)
