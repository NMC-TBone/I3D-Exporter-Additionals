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

from ..helper_functions import ATTR_PREFIX, iter_user_attrs


class I3DEA_OT_create_user_attribute(bpy.types.Operator):
    bl_idname = "i3dea.create_user_attribute"
    bl_label = "Create User Attribute"
    bl_description = "Create user attribute for selected object"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        i3dea = context.scene.i3dea
        obj = context.active_object
        if not obj:
            self.report({"ERROR"}, "No active object.")
            return {"CANCELLED"}

        attr_name = i3dea.user_attribute_name
        if not attr_name:
            self.report({"ERROR"}, "Attribute name cannot be empty.")
            return {"CANCELLED"}

        existing_names = {n for _, _, n in iter_user_attrs(obj)}
        if attr_name in existing_names:
            self.report({"ERROR"}, f"Attribute {attr_name!r} already exist.")
            return {"CANCELLED"}

        key = f"{ATTR_PREFIX}{i3dea.user_attribute_type}_{attr_name}"
        attr_type = i3dea.user_attribute_type
        match attr_type:
            case "boolean":
                obj[key] = False
                ui = obj.id_properties_ui(key)
                ui.update(description=key, default=False)
            case "integer":
                obj[key] = 0
                ui = obj.id_properties_ui(key)
                ui.update(description=key, default=0, min=-200, max=200)
            case "float":
                obj[key] = 0.0
                ui = obj.id_properties_ui(key)
                ui.update(description=key, default=0.0, min=-200.0, max=200.0)
            case "string" | "scriptCallback":
                obj[key] = ""
        return {"FINISHED"}


class I3DEA_OT_delete_user_attribute(bpy.types.Operator):
    bl_idname = "i3dea.delete_user_attribute"
    bl_label = "Delete User Attribute"
    bl_description = "Delete selected user attribute"
    bl_options = {"UNDO"}

    attribute_name: bpy.props.StringProperty()

    def execute(self, context):
        obj = context.active_object
        if not obj:
            self.report({"ERROR"}, "No active object.")
            return {"CANCELLED"}

        if self.attribute_name in obj:
            del obj[self.attribute_name]

        return {"FINISHED"}


classes = (I3DEA_OT_create_user_attribute, I3DEA_OT_delete_user_attribute)
register, unregister = bpy.utils.register_classes_factory(classes)
