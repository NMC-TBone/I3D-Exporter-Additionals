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
    def frontloaderAdapter(self):
        object_name = 'frontloaderAdapter'
        bpy.ops.wm.append(filepath=os.path.join(file_path, inner_path, object_name), directory=os.path.join(file_path, inner_path), filename=object_name)
    def telehandlerAdapter(self):
        object_name = 'telehandlerAdapter'
        bpy.ops.wm.append(filepath=os.path.join(file_path, inner_path, object_name), directory=os.path.join(file_path, inner_path), filename=object_name)
    def wheelloaderAdapter(self):
        object_name = 'wheelloaderAdapter'
        bpy.ops.wm.append(filepath=os.path.join(file_path, inner_path, object_name), directory=os.path.join(file_path, inner_path), filename=object_name)
    # beaconLights
    def beaconLight01(self):
        object_name = 'beaconLight01'
        bpy.ops.wm.append(filepath=os.path.join(file_path, inner_path, object_name), directory=os.path.join(file_path, inner_path), filename=object_name)
    def beaconLight02(self):
        object_name = 'beaconLight02'
        bpy.ops.wm.append(filepath=os.path.join(file_path, inner_path, object_name), directory=os.path.join(file_path, inner_path), filename=object_name)
    def beaconLight03(self):
        object_name = 'beaconLight03'
        bpy.ops.wm.append(filepath=os.path.join(file_path, inner_path, object_name), directory=os.path.join(file_path, inner_path), filename=object_name)
    def beaconLight04(self):
        object_name = 'beaconLight04'
        bpy.ops.wm.append(filepath=os.path.join(file_path, inner_path, object_name), directory=os.path.join(file_path, inner_path), filename=object_name)
    def beaconLight05(self):
        object_name = 'beaconLight05'
        bpy.ops.wm.append(filepath=os.path.join(file_path, inner_path, object_name), directory=os.path.join(file_path, inner_path), filename=object_name)
    def beaconLight06(self):
        object_name = 'beaconLight06'
        bpy.ops.wm.append(filepath=os.path.join(file_path, inner_path, object_name), directory=os.path.join(file_path, inner_path), filename=object_name)
    def beaconLight07(self):
        object_name = 'beaconLight07'
        bpy.ops.wm.append(filepath=os.path.join(file_path, inner_path, object_name), directory=os.path.join(file_path, inner_path), filename=object_name)
    def beaconLight08(self):
        object_name = 'beaconLight08'
        bpy.ops.wm.append(filepath=os.path.join(file_path, inner_path, object_name), directory=os.path.join(file_path, inner_path), filename=object_name)
    def beaconLight09(self):
        object_name = 'beaconLight09'
        bpy.ops.wm.append(filepath=os.path.join(file_path, inner_path, object_name), directory=os.path.join(file_path, inner_path), filename=object_name)
    def beaconLight10(self):
        object_name = 'beaconLight10'
        bpy.ops.wm.append(filepath=os.path.join(file_path, inner_path, object_name), directory=os.path.join(file_path, inner_path), filename=object_name)
    def beaconLight11(self):
        object_name = 'beaconLight11'
        bpy.ops.wm.append(filepath=os.path.join(file_path, inner_path, object_name), directory=os.path.join(file_path, inner_path), filename=object_name)
    # carHitches
    def fifthWheel_hitch(self):
        object_name = 'fifthWheel_hitch'
        object_name = 'fifthWheel_decal'
        bpy.ops.wm.append(filepath=os.path.join(file_path, inner_path, object_name), directory=os.path.join(file_path, inner_path), filename=object_name)
    def gooseneck_hitch(self):
        object_name = 'gooseneck_hitch'
        object_name = 'gooseneck_decal'
        bpy.ops.wm.append(filepath=os.path.join(file_path, inner_path, object_name), directory=os.path.join(file_path, inner_path), filename=object_name)
    # hitches
    def zetorHitch(self):
        object_name = 'zetorHitch'
        bpy.ops.wm.append(filepath=os.path.join(file_path, inner_path, object_name), directory=os.path.join(file_path, inner_path), filename=object_name)
    # lowerLinkBalls
    def lowerLinkBalls(self):
        object_name = 'lowerLinkBallLeft'
        object_name = 'lowerLinkBallRight'
        bpy.ops.wm.append(filepath=os.path.join(file_path, inner_path, object_name), directory=os.path.join(file_path, inner_path), filename=object_name)
    # powerTakeOffs
    def walterscheidW(self):
        object_name = 'walterscheidW'
        bpy.ops.wm.append(filepath=os.path.join(file_path, inner_path, object_name), directory=os.path.join(file_path, inner_path), filename=object_name)
    def walterscheidWWE(self):
        object_name = 'walterscheidWWE'
        bpy.ops.wm.append(filepath=os.path.join(file_path, inner_path, object_name), directory=os.path.join(file_path, inner_path), filename=object_name)
    def walterscheidWWZ(self):
        object_name = 'walterscheidWWZ'
        bpy.ops.wm.append(filepath=os.path.join(file_path, inner_path, object_name), directory=os.path.join(file_path, inner_path), filename=object_name)
    # reflectors
    def bigTriangle(self):
        object_name = 'bigTriangle'
        bpy.ops.wm.append(filepath=os.path.join(file_path, inner_path, object_name), directory=os.path.join(file_path, inner_path), filename=object_name)
    def redOrangeRectangle_01(self):
        object_name = 'redOrangeRectangle_01'
        bpy.ops.wm.append(filepath=os.path.join(file_path, inner_path, object_name), directory=os.path.join(file_path, inner_path), filename=object_name)
    def redRectangle_01(self):
        object_name = 'redRectangle_01'
        bpy.ops.wm.append(filepath=os.path.join(file_path, inner_path, object_name), directory=os.path.join(file_path, inner_path), filename=object_name)
    def redRound_01(self):
        object_name = 'redRound_01'
        bpy.ops.wm.append(filepath=os.path.join(file_path, inner_path, object_name), directory=os.path.join(file_path, inner_path), filename=object_name)
    def redRound_02(self):
        object_name = 'redRound_02'
        bpy.ops.wm.append(filepath=os.path.join(file_path, inner_path, object_name), directory=os.path.join(file_path, inner_path), filename=object_name)
    def redRound_03(self):
        object_name = 'redRound_03'
        bpy.ops.wm.append(filepath=os.path.join(file_path, inner_path, object_name), directory=os.path.join(file_path, inner_path), filename=object_name)
    def redRound_04(self):
        object_name = 'redRound_04'
        bpy.ops.wm.append(filepath=os.path.join(file_path, inner_path, object_name), directory=os.path.join(file_path, inner_path), filename=object_name)
    def redTriangle_01(self):
        object_name = 'redTriangle_01'
        bpy.ops.wm.append(filepath=os.path.join(file_path, inner_path, object_name), directory=os.path.join(file_path, inner_path), filename=object_name)
    def redTriangle_02(self):
        object_name = 'redTriangle_02'
        bpy.ops.wm.append(filepath=os.path.join(file_path, inner_path, object_name), directory=os.path.join(file_path, inner_path), filename=object_name)
    def whiteRectangle_01(self):
        object_name = 'whiteRectangle_01'
        bpy.ops.wm.append(filepath=os.path.join(file_path, inner_path, object_name), directory=os.path.join(file_path, inner_path), filename=object_name)
    def whiteRound_01(self):
        object_name = 'whiteRound_01'
        bpy.ops.wm.append(filepath=os.path.join(file_path, inner_path, object_name), directory=os.path.join(file_path, inner_path), filename=object_name)
    def whiteRound_02(self):
        object_name = 'whiteRound_02'
        bpy.ops.wm.append(filepath=os.path.join(file_path, inner_path, object_name), directory=os.path.join(file_path, inner_path), filename=object_name)
    def whiteRound_03(self):
        object_name = 'whiteRound_03'
        bpy.ops.wm.append(filepath=os.path.join(file_path, inner_path, object_name), directory=os.path.join(file_path, inner_path), filename=object_name)
    def whiteRound_04(self):
        object_name = 'whiteRound_04'
        bpy.ops.wm.append(filepath=os.path.join(file_path, inner_path, object_name), directory=os.path.join(file_path, inner_path), filename=object_name)
    def whiteTriangle_01(self):
        object_name = 'whiteTriangle_01'
        bpy.ops.wm.append(filepath=os.path.join(file_path, inner_path, object_name), directory=os.path.join(file_path, inner_path), filename=object_name)
    def whiteTriangle_02(self):
        object_name = 'whiteTriangle_02'
        bpy.ops.wm.append(filepath=os.path.join(file_path, inner_path, object_name), directory=os.path.join(file_path, inner_path), filename=object_name)
    def yellowRectangle_01(self):
        object_name = 'yellowRectangle_01'
        bpy.ops.wm.append(filepath=os.path.join(file_path, inner_path, object_name), directory=os.path.join(file_path, inner_path), filename=object_name)
    def yellowRound_01(self):
        object_name = 'yellowRound_01'
        bpy.ops.wm.append(filepath=os.path.join(file_path, inner_path, object_name), directory=os.path.join(file_path, inner_path), filename=object_name)
    def yellowRound_02(self):
        object_name = 'yellowRound_02'
        bpy.ops.wm.append(filepath=os.path.join(file_path, inner_path, object_name), directory=os.path.join(file_path, inner_path), filename=object_name)
    def yellowRound_03(self):
        object_name = 'yellowRound_03'
        bpy.ops.wm.append(filepath=os.path.join(file_path, inner_path, object_name), directory=os.path.join(file_path, inner_path), filename=object_name)
    def yellowRound_04(self):
        object_name = 'yellowRound_04'
        bpy.ops.wm.append(filepath=os.path.join(file_path, inner_path, object_name), directory=os.path.join(file_path, inner_path), filename=object_name)
    def yellowTriangle_01(self):
        object_name = 'yellowTriangle_01'
        bpy.ops.wm.append(filepath=os.path.join(file_path, inner_path, object_name), directory=os.path.join(file_path, inner_path), filename=object_name)
    def yellowTriangle_02(self):
        object_name = 'yellowTriangle_02'
        bpy.ops.wm.append(filepath=os.path.join(file_path, inner_path, object_name), directory=os.path.join(file_path, inner_path), filename=object_name)
    # skfLincoln
    def skfLincoln(self):
        object_name = 'skfLincolnskfLincoln'
        bpy.ops.wm.append(filepath=os.path.join(file_path, inner_path, object_name), directory=os.path.join(file_path, inner_path), filename=object_name, )
    # upperLinks
    def johnDeere8RTUpperlink(self):
        object_name = 'johnDeere8RTUpperlink'
        bpy.ops.wm.append(filepath=os.path.join(file_path, inner_path, object_name), directory=os.path.join(file_path, inner_path), filename=object_name, )
    def johnDeereUpperlink(self):
        object_name = 'johnDeereUpperlink'
        bpy.ops.wm.append(filepath=os.path.join(file_path, inner_path, object_name), directory=os.path.join(file_path, inner_path), filename=object_name, )
    def walterscheid01(self):
        object_name = 'walterscheid01'
        bpy.ops.wm.append(filepath=os.path.join(file_path, inner_path, object_name), directory=os.path.join(file_path, inner_path), filename=object_name, )
    def walterscheid02(self):
        object_name = 'walterscheid02'
        bpy.ops.wm.append(filepath=os.path.join(file_path, inner_path, object_name), directory=os.path.join(file_path, inner_path), filename=object_name, )
    def walterscheid03(self):
        object_name = 'walterscheid03'
        bpy.ops.wm.append(filepath=os.path.join(file_path, inner_path, object_name), directory=os.path.join(file_path, inner_path), filename=object_name, )
    def walterscheid04(self):
        object_name = 'walterscheid04'
        bpy.ops.wm.append(filepath=os.path.join(file_path, inner_path, object_name), directory=os.path.join(file_path, inner_path), filename=object_name, )
    def walterscheid05(self):
        object_name = 'walterscheid05'
        bpy.ops.wm.append(filepath=os.path.join(file_path, inner_path, object_name), directory=os.path.join(file_path, inner_path), filename=object_name, )
    # wheelChocks
    def chockSupport(self):
        object_name = 'chockSupport'
        bpy.ops.wm.append(filepath=os.path.join(file_path, inner_path, object_name), directory=os.path.join(file_path, inner_path), filename=object_name, )
    def wheelChock01(self):
        object_name = 'wheelChock01'
        bpy.ops.wm.append(filepath=os.path.join(file_path, inner_path, object_name), directory=os.path.join(file_path, inner_path), filename=object_name, )
    def wheelChock02(self):
        object_name = 'wheelChock02'
        bpy.ops.wm.append(filepath=os.path.join(file_path, inner_path, object_name), directory=os.path.join(file_path, inner_path), filename=object_name, )
    def wheelChock03(self):
        object_name = 'wheelChock03'
        bpy.ops.wm.append(filepath=os.path.join(file_path, inner_path, object_name), directory=os.path.join(file_path, inner_path), filename=object_name, )
    def wheelChock04(self):
        object_name = 'wheelChock04'
        object_name = 'wheelChock04_parked'
        bpy.ops.wm.append(filepath=os.path.join(file_path, inner_path, object_name), directory=os.path.join(file_path, inner_path), filename=object_name, )
    def wheelChock05(self):
        object_name = 'wheelChock05'
        object_name = 'wheelChock05_parked'
        object_name = 'wheelChock05chain2'
        bpy.ops.wm.append(filepath=os.path.join(file_path, inner_path, object_name), directory=os.path.join(file_path, inner_path), filename=object_name, )
    # Miscellaneous
    def attacherTruckGeneric(self):
        object_name = 'attacherTruckGeneric'
        bpy.ops.wm.append(filepath=os.path.join(file_path, inner_path, object_name), directory=os.path.join(file_path, inner_path), filename=object_name, )
    def camera_01(self):
        object_name = 'glass'
        bpy.ops.wm.append(filepath=os.path.join(file_path, inner_path, object_name), directory=os.path.join(file_path, inner_path), filename=object_name, )
    def camera_02(self):
        object_name = 'rotArm2'
        bpy.ops.wm.append(filepath=os.path.join(file_path, inner_path, object_name), directory=os.path.join(file_path, inner_path), filename=object_name, )
    def camera_03(self):
        object_name = 'glass3'
        bpy.ops.wm.append(filepath=os.path.join(file_path, inner_path, object_name), directory=os.path.join(file_path, inner_path), filename=object_name, )
    def exhaustLicencePlateHolder(self):
        object_name = 'exhaustLicencePlateHolder'
        bpy.ops.wm.append(filepath=os.path.join(file_path, inner_path, object_name), directory=os.path.join(file_path, inner_path), filename=object_name, )
    def extinguisher(self):
        object_name = 'extinguisher'
        bpy.ops.wm.append(filepath=os.path.join(file_path, inner_path, object_name), directory=os.path.join(file_path, inner_path), filename=object_name, )
    def gps(self):
        object_name = 'gps'
        bpy.ops.wm.append(filepath=os.path.join(file_path, inner_path, object_name), directory=os.path.join(file_path, inner_path), filename=object_name, )
    def rearHitch(self):
        object_name = 'rearHitch'
        bpy.ops.wm.append(filepath=os.path.join(file_path, inner_path2, object_name), directory=os.path.join(file_path, inner_path2), filename=object_name, )
    def smallWheel01(self):
        object_name = 'smallWheel01'
        bpy.ops.wm.append(filepath=os.path.join(file_path, inner_path, object_name), directory=os.path.join(file_path, inner_path), filename=object_name, )
    def starFire(self):
        object_name = 'starFire'
        bpy.ops.wm.append(filepath=os.path.join(file_path, inner_path, object_name), directory=os.path.join(file_path, inner_path), filename=object_name, )
    def toolbar(self):
        object_name = 'toolbar'
        bpy.ops.wm.append(filepath=os.path.join(file_path, inner_path, object_name), directory=os.path.join(file_path, inner_path), filename=object_name, )
    def toolbarWide(self):
        object_name = 'toolbarWide'
        bpy.ops.wm.append(filepath=os.path.join(file_path, inner_path, object_name), directory=os.path.join(file_path, inner_path), filename=object_name, )
    def towBar(self):
        object_name = 'towBar'
        bpy.ops.wm.append(filepath=os.path.join(file_path, inner_path, object_name), directory=os.path.join(file_path, inner_path), filename=object_name, )
    def trailerLowAttacher(self):
        object_name = 'trailerLowAttacher'
        bpy.ops.wm.append(filepath=os.path.join(file_path, inner_path, object_name), directory=os.path.join(file_path, inner_path), filename=object_name, )
    def trailerToolBox(self):
        object_name = 'trailerToolBoxHolder'
        bpy.ops.wm.append(filepath=os.path.join(file_path, inner_path, object_name), directory=os.path.join(file_path, inner_path), filename=object_name, )
    def trailerToolBox02(self):
        object_name = 'trailerToolBox02'
        bpy.ops.wm.append(filepath=os.path.join(file_path, inner_path, object_name), directory=os.path.join(file_path, inner_path), filename=object_name, )
    def triangleAdapter(self):
        object_name = 'triangleAdapter'
        bpy.ops.wm.append(filepath=os.path.join(file_path, inner_path, object_name), directory=os.path.join(file_path, inner_path), filename=object_name, )
    def upperLink(self):
        object_name = 'upperLink'
        bpy.ops.wm.append(filepath=os.path.join(file_path, inner_path, object_name), directory=os.path.join(file_path, inner_path), filename=object_name, )
    def upperLinkSmall(self):
        object_name = 'upperLinkSmall'
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
        # hitches
        if context.scene.i3deapg.assets_dropdown == 'zetorHitch':
            self.zetorHitch()
            self.report({'INFO'}, "zetorHitch imported")
            return {'FINISHED'}
        # lowerLinkBalls
        if context.scene.i3deapg.assets_dropdown == 'lowerLinkBalls':
            self.lowerLinkBalls()
            self.report({'INFO'}, "lowerLinkBalls imported")
            return {'FINISHED'}
        # powerTakeOffs
        if context.scene.i3deapg.assets_dropdown == 'walterscheidW':
            self.walterscheidW()
            self.report({'INFO'}, "walterscheidW imported")
            return {'FINISHED'}
        if context.scene.i3deapg.assets_dropdown == 'walterscheidWWE':
            self.walterscheidWWE()
            self.report({'INFO'}, "walterscheidWWE imported")
            return {'FINISHED'}
        if context.scene.i3deapg.assets_dropdown == 'walterscheidWWZ':
            self.walterscheidWWZ()
            self.report({'INFO'}, "walterscheidWWZ imported")
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
        if context.scene.i3deapg.assets_dropdown == 'whiteRectangle_01':
            self.whiteRectangle_01()
            self.report({'INFO'}, "whiteRectangle_01 imported")
            return {'FINISHED'}
        if context.scene.i3deapg.assets_dropdown == 'whiteRound_01':
            self.whiteRound_01()
            self.report({'INFO'}, "whiteRound_01 imported")
            return {'FINISHED'}
        if context.scene.i3deapg.assets_dropdown == 'whiteRound_02':
            self.whiteRound_02()
            self.report({'INFO'}, "whiteRound_02 imported")
            return {'FINISHED'}
        if context.scene.i3deapg.assets_dropdown == 'whiteRound_03':
            self.whiteRound_03()
            self.report({'INFO'}, "whiteRound_03 imported")
            return {'FINISHED'}
        if context.scene.i3deapg.assets_dropdown == 'whiteRound_04':
            self.whiteRound_04()
            self.report({'INFO'}, "whiteRound_04 imported")
            return {'FINISHED'}
        if context.scene.i3deapg.assets_dropdown == 'whiteTriangle_01':
            self.whiteTriangle_01()
            self.report({'INFO'}, "whiteTriangle_01 imported")
            return {'FINISHED'}
        if context.scene.i3deapg.assets_dropdown == 'whiteTriangle_02':
            self.whiteTriangle_02()
            self.report({'INFO'}, "whiteTriangle_02 imported")
            return {'FINISHED'}
        if context.scene.i3deapg.assets_dropdown == 'yellowRectangle_01':
            self.yellowRectangle_01()
            self.report({'INFO'}, "yellowRectangle_01 imported")
            return {'FINISHED'}
        if context.scene.i3deapg.assets_dropdown == 'yellowRound_01':
            self.yellowRound_01()
            self.report({'INFO'}, "yellowRound_01 imported")
            return {'FINISHED'}
        if context.scene.i3deapg.assets_dropdown == 'yellowRound_02':
            self.yellowRound_02()
            self.report({'INFO'}, "yellowRound_02 imported")
            return {'FINISHED'}
        if context.scene.i3deapg.assets_dropdown == 'yellowRound_03':
            self.yellowRound_03()
            self.report({'INFO'}, "yellowRound_03 imported")
            return {'FINISHED'}
        if context.scene.i3deapg.assets_dropdown == 'yellowRound_04':
            self.yellowRound_04()
            self.report({'INFO'}, "yellowRound_04 imported")
            return {'FINISHED'}
        if context.scene.i3deapg.assets_dropdown == 'yellowTriangle_01':
            self.yellowTriangle_01()
            self.report({'INFO'}, "yellowTriangle_01 imported")
            return {'FINISHED'}
        if context.scene.i3deapg.assets_dropdown == 'yellowTriangle_02':
            self.yellowTriangle_02()
            self.report({'INFO'}, "yellowTriangle_02 imported")
            return {'FINISHED'}
        # skfLincoln
        if context.scene.i3deapg.assets_dropdown == 'skfLincoln':
            self.skfLincoln()
            self.report({'INFO'}, "skfLincoln imported")
            return {'FINISHED'}
        # upperLinks
        if context.scene.i3deapg.assets_dropdown == 'johnDeere8RTUpperlink':
            self.johnDeere8RTUpperlink()
            self.report({'INFO'}, "johnDeere8RTUpperlink imported")
            return {'FINISHED'}
        if context.scene.i3deapg.assets_dropdown == 'johnDeereUpperlink':
            self.johnDeereUpperlink()
            self.report({'INFO'}, "johnDeereUpperlink imported")
            return {'FINISHED'}
        if context.scene.i3deapg.assets_dropdown == 'walterscheid01':
            self.walterscheid01()
            self.report({'INFO'}, "walterscheid01 imported")
            return {'FINISHED'}
        if context.scene.i3deapg.assets_dropdown == 'walterscheid02':
            self.walterscheid02()
            self.report({'INFO'}, "walterscheid02 imported")
            return {'FINISHED'}
        if context.scene.i3deapg.assets_dropdown == 'walterscheid03':
            self.walterscheid03()
            self.report({'INFO'}, "walterscheid03 imported")
            return {'FINISHED'}
        if context.scene.i3deapg.assets_dropdown == 'walterscheid04':
            self.walterscheid04()
            self.report({'INFO'}, "walterscheid04 imported")
            return {'FINISHED'}
        if context.scene.i3deapg.assets_dropdown == 'walterscheid05':
            self.walterscheid05()
            self.report({'INFO'}, "walterscheid05 imported")
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
        # Miscellaneous
        if context.scene.i3deapg.assets_dropdown == 'attacherTruckGeneric':
            self.attacherTruckGeneric()
            self.report({'INFO'}, "attacherTruckGeneric imported")
            return {'FINISHED'}
        if context.scene.i3deapg.assets_dropdown == 'camera_01':
            self.camera_01()
            self.report({'INFO'}, "camera_01 imported")
            return {'FINISHED'}
        if context.scene.i3deapg.assets_dropdown == 'camera_02':
            self.camera_02()
            self.report({'INFO'}, "camera_02 imported")
            return {'FINISHED'}
        if context.scene.i3deapg.assets_dropdown == 'camera_03':
            self.camera_03()
            self.report({'INFO'}, "camera_03 imported")
            return {'FINISHED'}
        if context.scene.i3deapg.assets_dropdown == 'exhaustLicencePlateHolder':
            self.exhaustLicencePlateHolder()
            self.report({'INFO'}, "exhaustLicencePlateHolder imported")
            return {'FINISHED'}
        if context.scene.i3deapg.assets_dropdown == 'extinguisher':
            self.extinguisher()
            self.report({'INFO'}, "extinguisher imported")
            return {'FINISHED'}
        if context.scene.i3deapg.assets_dropdown == 'gps':
            self.gps()
            self.report({'INFO'}, "gps imported")
            return {'FINISHED'}
        if context.scene.i3deapg.assets_dropdown == 'rearHitch':
            self.rearHitch()
            self.report({'INFO'}, "rearHitch imported")
            return {'FINISHED'}
        if context.scene.i3deapg.assets_dropdown == 'smallWheel01':
            self.smallWheel01()
            self.report({'INFO'}, "smallWheel01 imported")
            return {'FINISHED'}
        if context.scene.i3deapg.assets_dropdown == 'starFire':
            self.starFire()
            self.report({'INFO'}, "starFire imported")
            return {'FINISHED'}
        if context.scene.i3deapg.assets_dropdown == 'toolbar':
            self.toolbar()
            self.report({'INFO'}, "toolbar imported")
            return {'FINISHED'}
        if context.scene.i3deapg.assets_dropdown == 'toolbarWide':
            self.toolbarWide()
            self.report({'INFO'}, "toolbarWide imported")
            return {'FINISHED'}
        if context.scene.i3deapg.assets_dropdown == 'towBar':
            self.towBar()
            self.report({'INFO'}, "towBar imported")
            return {'FINISHED'}
        if context.scene.i3deapg.assets_dropdown == 'trailerLowAttacher':
            self.trailerLowAttacher()
            self.report({'INFO'}, "trailerLowAttacher imported")
            return {'FINISHED'}
        if context.scene.i3deapg.assets_dropdown == 'trailerToolBox':
            self.trailerToolBox()
            self.report({'INFO'}, "trailerToolBox imported")
            return {'FINISHED'}
        if context.scene.i3deapg.assets_dropdown == 'trailerToolBox02':
            self.trailerToolBox02()
            self.report({'INFO'}, "trailerToolBox02 imported")
            return {'FINISHED'}
        if context.scene.i3deapg.assets_dropdown == 'triangleAdapter':
            self.triangleAdapter()
            self.report({'INFO'}, "triangleAdapter imported")
            return {'FINISHED'}
        if context.scene.i3deapg.assets_dropdown == 'upperLink':
            self.upperLink()
            self.report({'INFO'}, "upperLink imported")
            return {'FINISHED'}
        if context.scene.i3deapg.assets_dropdown == 'upperLinkSmall':
            self.upperLinkSmall()
            self.report({'INFO'}, "upperLinkSmall imported")
            return {'FINISHED'}
        return {'FINISHED'}