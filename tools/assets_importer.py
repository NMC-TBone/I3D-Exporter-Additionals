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

    global file_path
    global inner_path
    file_path = Path(__file__).parent / "assets_blend/assets.blend"
    inner_path = 'Object'

    # adapters
    def frontloaderAdapter(self):
        object_name = 'frontloaderAdapter_ignore'
        bpy.ops.wm.append(filepath=os.path.join(file_path, inner_path, object_name), directory=os.path.join(file_path, inner_path), filename=object_name)
    def telehandlerAdapter(self):
        object_name = 'telehandlerAdapter_ignore'
        bpy.ops.wm.append(filepath=os.path.join(file_path, inner_path, object_name), directory=os.path.join(file_path, inner_path), filename=object_name)
    def wheelloaderAdapter(self):
        object_name = 'wheelloaderAdapter_ignore'
        bpy.ops.wm.append(filepath=os.path.join(file_path, inner_path, object_name), directory=os.path.join(file_path, inner_path), filename=object_name)
    # beaconLights
    def beaconLight01(self):
        object_name = 'beaconLight01_ignore'
        bpy.ops.wm.append(filepath=os.path.join(file_path, inner_path, object_name), directory=os.path.join(file_path, inner_path), filename=object_name)
    def beaconLight02(self):
        object_name = 'beaconLight02_ignore'
        bpy.ops.wm.append(filepath=os.path.join(file_path, inner_path, object_name), directory=os.path.join(file_path, inner_path), filename=object_name)
    def beaconLight03(self):
        object_name = 'beaconLight03_ignore'
        bpy.ops.wm.append(filepath=os.path.join(file_path, inner_path, object_name), directory=os.path.join(file_path, inner_path), filename=object_name)
    def beaconLight04(self):
        object_name = 'beaconLight04_ignore'
        bpy.ops.wm.append(filepath=os.path.join(file_path, inner_path, object_name), directory=os.path.join(file_path, inner_path), filename=object_name)
    def beaconLight05(self):
        object_name = 'beaconLight05_ignore'
        bpy.ops.wm.append(filepath=os.path.join(file_path, inner_path, object_name), directory=os.path.join(file_path, inner_path), filename=object_name)
    def beaconLight06(self):
        object_name = 'beaconLight06_ignore'
        bpy.ops.wm.append(filepath=os.path.join(file_path, inner_path, object_name), directory=os.path.join(file_path, inner_path), filename=object_name)
    def beaconLight07(self):
        object_name = 'beaconLight07_ignore'
        bpy.ops.wm.append(filepath=os.path.join(file_path, inner_path, object_name), directory=os.path.join(file_path, inner_path), filename=object_name)
    def beaconLight08(self):
        object_name = 'beaconLight08_ignore'
        bpy.ops.wm.append(filepath=os.path.join(file_path, inner_path, object_name), directory=os.path.join(file_path, inner_path), filename=object_name)
    def beaconLight09(self):
        object_name = 'beaconLight09_ignore'
        bpy.ops.wm.append(filepath=os.path.join(file_path, inner_path, object_name), directory=os.path.join(file_path, inner_path), filename=object_name)
    def beaconLight10(self):
        object_name = 'beaconLight10_ignore'
        bpy.ops.wm.append(filepath=os.path.join(file_path, inner_path, object_name), directory=os.path.join(file_path, inner_path), filename=object_name)
    def beaconLight11(self):
        object_name = 'beaconLight11_ignore'
        bpy.ops.wm.append(filepath=os.path.join(file_path, inner_path, object_name), directory=os.path.join(file_path, inner_path), filename=object_name)
    # carHitches
    def fifthWheel_hitch(self):
        object_name = 'fifthWheel_hitch_ignore'
        object_name = 'fifthWheel_decal'
        bpy.ops.wm.append(filepath=os.path.join(file_path, inner_path, object_name), directory=os.path.join(file_path, inner_path), filename=object_name)
    def gooseneck_hitch(self):
        object_name = 'gooseneck_hitch_ignore'
        object_name = 'gooseneck_decal'
        bpy.ops.wm.append(filepath=os.path.join(file_path, inner_path, object_name), directory=os.path.join(file_path, inner_path), filename=object_name)
    # lowerLinkBalls
    def lowerLinkBalls(self):
        object_name = 'lowerLinkBallLeft_ignore'
        object_name = 'lowerLinkBallRight_ignore'
        bpy.ops.wm.append(filepath=os.path.join(file_path, inner_path, object_name), directory=os.path.join(file_path, inner_path), filename=object_name)
    # reflectors
    def bigTriangle(self):
        object_name = 'bigTriangle_ignore'
        bpy.ops.wm.append(filepath=os.path.join(file_path, inner_path, object_name), directory=os.path.join(file_path, inner_path), filename=object_name)
    def redOrangeRectangle_01(self):
        object_name = 'redOrangeRectangle_01_ignore'
        bpy.ops.wm.append(filepath=os.path.join(file_path, inner_path, object_name), directory=os.path.join(file_path, inner_path), filename=object_name)
    def redRectangle_01(self):
        object_name = 'redRectangle_01_ignore'
        bpy.ops.wm.append(filepath=os.path.join(file_path, inner_path, object_name), directory=os.path.join(file_path, inner_path), filename=object_name)
    def redRound_01(self):
        object_name = 'redRound_01_ignore'
        bpy.ops.wm.append(filepath=os.path.join(file_path, inner_path, object_name), directory=os.path.join(file_path, inner_path), filename=object_name)
    def redRound_02(self):
        object_name = 'redRound_02_ignore'
        bpy.ops.wm.append(filepath=os.path.join(file_path, inner_path, object_name), directory=os.path.join(file_path, inner_path), filename=object_name)
    def redRound_03(self):
        object_name = 'redRound_03_ignore'
        bpy.ops.wm.append(filepath=os.path.join(file_path, inner_path, object_name), directory=os.path.join(file_path, inner_path), filename=object_name)
    def redRound_04(self):
        object_name = 'redRound_04_ignore'
        bpy.ops.wm.append(filepath=os.path.join(file_path, inner_path, object_name), directory=os.path.join(file_path, inner_path), filename=object_name)
    def redTriangle_01(self):
        object_name = 'redTriangle_01_ignore'
        bpy.ops.wm.append(filepath=os.path.join(file_path, inner_path, object_name), directory=os.path.join(file_path, inner_path), filename=object_name)
    def redTriangle_02(self):
        object_name = 'redTriangle_02_ignore'
        bpy.ops.wm.append(filepath=os.path.join(file_path, inner_path, object_name), directory=os.path.join(file_path, inner_path), filename=object_name)
    # skfLincoln
    def skfLincoln(self):
        object_name = 'skfLincolnskfLincoln_ignore'
        bpy.ops.wm.append(filepath=os.path.join(file_path, inner_path, object_name), directory=os.path.join(file_path, inner_path), filename=object_name, )
    # wheelChocks
    def chockSupport(self):
        object_name = 'chockSupport_ignore'
        bpy.ops.wm.append(filepath=os.path.join(file_path, inner_path, object_name), directory=os.path.join(file_path, inner_path), filename=object_name, )
    def wheelChock01(self):
        object_name = 'wheelChock01_ignore'
        bpy.ops.wm.append(filepath=os.path.join(file_path, inner_path, object_name), directory=os.path.join(file_path, inner_path), filename=object_name, )
    def wheelChock02(self):
        object_name = 'wheelChock02_ignore'
        bpy.ops.wm.append(filepath=os.path.join(file_path, inner_path, object_name), directory=os.path.join(file_path, inner_path), filename=object_name, )
    def wheelChock03(self):
        object_name = 'wheelChock03_ignore'
        bpy.ops.wm.append(filepath=os.path.join(file_path, inner_path, object_name), directory=os.path.join(file_path, inner_path), filename=object_name, )
    def wheelChock04(self):
        object_name = 'wheelChock04_ignore'
        object_name = 'wheelChock04_parked'
        bpy.ops.wm.append(filepath=os.path.join(file_path, inner_path, object_name), directory=os.path.join(file_path, inner_path), filename=object_name, )
    def wheelChock05(self):
        object_name = 'wheelChock05_ignore'
        object_name = 'wheelChock05_parked'
        object_name = 'wheelChock05chain2'
        bpy.ops.wm.append(filepath=os.path.join(file_path, inner_path, object_name), directory=os.path.join(file_path, inner_path), filename=object_name, )

    def execute(self, context):
        # adapters
        if context.scene.i3deapg.assets_dropdown == 'frontloaderAdapter':
            self.frontloaderAdapter()
            self.report({'INFO'}, "frontloaderAdapter imported")
            return {'FINISHED'}
        if context.scene.i3deapg.assets_dropdown == 'telehandlerAdapter':
            self.telehandlerAdapter()
            self.report({'INFO'}, "telehandlerAdapter imported")
            return {'FINISHED'}
        if context.scene.i3deapg.assets_dropdown == 'wheelloaderAdapter':
            self.wheelloaderAdapter()
            self.report({'INFO'}, "wheelloaderAdapter imported")
            return {'FINISHED'}
        # beaconLights
        if context.scene.i3deapg.assets_dropdown == 'beaconLight01':
            self.beaconLight01()
            self.report({'INFO'}, "beaconLight01 imported")
            return {'FINISHED'}
        if context.scene.i3deapg.assets_dropdown == 'beaconLight02':
            self.beaconLight02()
            self.report({'INFO'}, "beaconLight02 imported")
            return {'FINISHED'}
        if context.scene.i3deapg.assets_dropdown == 'beaconLight03':
            self.beaconLight03()
            self.report({'INFO'}, "beaconLight03 imported")
            return {'FINISHED'}
        if context.scene.i3deapg.assets_dropdown == 'beaconLight04':
            self.beaconLight04()
            self.report({'INFO'}, "beaconLight04 imported")
            return {'FINISHED'}
        if context.scene.i3deapg.assets_dropdown == 'beaconLight05':
            self.beaconLight05()
            self.report({'INFO'}, "beaconLight05 imported")
            return {'FINISHED'}
        if context.scene.i3deapg.assets_dropdown == 'beaconLight06':
            self.beaconLight06()
            self.report({'INFO'}, "beaconLight06 imported")
            return {'FINISHED'}
        if context.scene.i3deapg.assets_dropdown == 'beaconLight07':
            self.beaconLight07()
            self.report({'INFO'}, "beaconLight07 imported")
            return {'FINISHED'}
        if context.scene.i3deapg.assets_dropdown == 'beaconLight08':
            self.beaconLight08()
            self.report({'INFO'}, "beaconLight08 imported")
            return {'FINISHED'}
        if context.scene.i3deapg.assets_dropdown == 'beaconLight09':
            self.beaconLight09()
            self.report({'INFO'}, "beaconLight09 imported")
            return {'FINISHED'}
        if context.scene.i3deapg.assets_dropdown == 'beaconLight10':
            self.beaconLight10()
            self.report({'INFO'}, "beaconLight10 imported")
            return {'FINISHED'}
        if context.scene.i3deapg.assets_dropdown == 'beaconLight11':
            self.beaconLight11()
            self.report({'INFO'}, "beaconLight11 imported")
            return {'FINISHED'}
        # carHitches
        if context.scene.i3deapg.assets_dropdown == 'fifthWheel_hitch':
            self.fifthWheel_hitch()
            self.report({'INFO'}, "fifthWheel_hitch imported")
            return {'FINISHED'}
        if context.scene.i3deapg.assets_dropdown == 'gooseneck_hitch':
            self.gooseneck_hitch()
            self.report({'INFO'}, "gooseneck_hitch imported")
            return {'FINISHED'}
        # lowerLinkBalls
        if context.scene.i3deapg.assets_dropdown == 'lowerLinkBalls':
            self.lowerLinkBalls()
            self.report({'INFO'}, "lowerLinkBalls imported")
            return {'FINISHED'}
        # reflectors
        if context.scene.i3deapg.assets_dropdown == 'bigTriangle':
            self.bigTriangle()
            self.report({'INFO'}, "bigTriangle imported")
            return {'FINISHED'}
        if context.scene.i3deapg.assets_dropdown == 'redOrangeRectangle_01':
            self.redOrangeRectangle_01()
            self.report({'INFO'}, "redOrangeRectangle_01 imported")
            return {'FINISHED'}
        if context.scene.i3deapg.assets_dropdown == 'redRectangle_01':
            self.redRectangle_01()
            self.report({'INFO'}, "redRectangle_01 imported")
            return {'FINISHED'}
        if context.scene.i3deapg.assets_dropdown == 'redRound_01':
            self.redRound_01()
            self.report({'INFO'}, "redRound_01 imported")
            return {'FINISHED'}
        if context.scene.i3deapg.assets_dropdown == 'redRound_02':
            self.redRound_02()
            self.report({'INFO'}, "redRound_02 imported")
            return {'FINISHED'}
        if context.scene.i3deapg.assets_dropdown == 'redRound_03':
            self.redRound_03()
            self.report({'INFO'}, "redRound_03 imported")
            return {'FINISHED'}
        if context.scene.i3deapg.assets_dropdown == 'redRound_04':
            self.redRound_04()
            self.report({'INFO'}, "redRound_04 imported")
            return {'FINISHED'}
        if context.scene.i3deapg.assets_dropdown == 'redTriangle_01':
            self.redTriangle_01()
            self.report({'INFO'}, "redTriangle_01 imported")
            return {'FINISHED'}
        if context.scene.i3deapg.assets_dropdown == 'redTriangle_02':
            self.redTriangle_02()
            self.report({'INFO'}, "redTriangle_02 imported")
            return {'FINISHED'}
        # reflectors
        if context.scene.i3deapg.assets_dropdown == 'skfLincoln':
            self.skfLincoln()
            self.report({'INFO'}, "skfLincoln imported")
            return {'FINISHED'}
        # wheelChocks
        if context.scene.i3deapg.assets_dropdown == 'chockSupport':
            self.chockSupport()
            self.report({'INFO'}, "chockSupport imported")
            return {'FINISHED'}
        if context.scene.i3deapg.assets_dropdown == 'wheelChock01':
            self.wheelChock01()
            self.report({'INFO'}, "wheelChock01 imported")
            return {'FINISHED'}
        if context.scene.i3deapg.assets_dropdown == 'wheelChock02':
            self.wheelChock02()
            self.report({'INFO'}, "wheelChock02 imported")
            return {'FINISHED'}
        if context.scene.i3deapg.assets_dropdown == 'wheelChock03':
            self.wheelChock03()
            self.report({'INFO'}, "wheelChock03 imported")
            return {'FINISHED'}
        if context.scene.i3deapg.assets_dropdown == 'wheelChock04':
            self.wheelChock04()
            self.report({'INFO'}, "wheelChock04 imported")
            return {'FINISHED'}
        if context.scene.i3deapg.assets_dropdown == 'wheelChock05':
            self.wheelChock05()
            self.report({'INFO'}, "wheelChock05 imported")
            return {'FINISHED'}
        return {'FINISHED'}