"""assets_importer.py importer for FS game files assets"""

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
import os
from pathlib import Path

class TOOLS_OT_assets(bpy.types.Operator):
    bl_label = "Import Assets"
    bl_idname = "tools.assets"
    bl_description = "Import Assets"
    bl_options = {'REGISTER', 'UNDO'}

    global file_path
    global inner_path
    global inner_path2
    file_path = Path(__file__).parent / "assets_blend/assets.blend"
    inner_path = 'Object'
    inner_path2 = 'Collection'

    # adapters
    def get_asset(self, name):
        if name == 'rearHitch':
            bpy.ops.wm.append(filepath=os.path.join(file_path, inner_path2, name), directory=os.path.join(file_path, inner_path2), filename=name, )
            return

        bpy.ops.wm.append(filepath=os.path.join(file_path, inner_path, name), directory=os.path.join(file_path, inner_path), filename=name, )

    def execute(self, context):
        name = context.scene.i3deapg.assets_dropdown
        self.get_asset(name)
        self.report({'INFO'}, name + " imported")
        return {'FINISHED'}