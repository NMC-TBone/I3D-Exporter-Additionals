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


class I3DEA_OT_properties_converter(bpy.types.Operator):
    bl_idname = "i3dea.properties_converter"
    bl_label = "Convert I3D properties.py"
    bl_description = "Converts I3D properties.py from Stjerne exporter to Giants exporter"
    bl_options = {'REGISTER', 'UNDO'}

    properties = [('Giants', 'Stjerne')]

    def execute(self, context):
        for obj in bpy.data.objects:
            if obj:
                print("hello")
