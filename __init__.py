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

bl_info = {
    "name" : "I3D Exporter Additionals",
    "author" : "T-Bone",
    "description" : "Additionals For Giants I3D Exporter",
    "blender" : (3, 0, 0),
    "version" : (1, 0, 4),
    "location" : "View3D > UI > GIANTS I3D Exporter > I3D Exporter Additionals",
    "warning" : "",
    "category" : "Game Engine"
}

import bpy

class I3DEA_PG_List(bpy.types.PropertyGroup):
    size_dropdown: bpy.props.EnumProperty(
            name="Size List",
            description="List of UV size",
            items=[('four', "2x2", "Create UVset 2 2x2", 1),
                   ('sixteen', "4x4", "Create UVseet 2 4x4", 2)],
            default = 'four')

    skeletons_dropdown: bpy.props.EnumProperty(
        name="Skeletons List",
        description="List of skeletons",
        items=[('createBaseVehicle', "Tractor", "Add Tractor Skeleton", 1),
               ('createBaseHarvester', "Combine", "Add Harvester Skeleton", 2),
               ('createBaseTool', "Tool", "Add Tool Skeleton", 3),
               ('createAttacherJoints', "Attacher Joints", "Add Attacher Joint Skeleton", 4),
               ('createPlayer', "Player", "Add Player Skeleton", 5),
               ('createLights', "Lights", "Add Lights Skeleton", 6),
               ('createCamerasVehicle', "Cameras (Tractor)", "Add Cameras (Tractor) Skeleton", 7),
               ('createCamerasHarvester', "Cameras (Combine)", "Add Cameras (Combine) Skeleton", 8),
               ('createTrafficVehicle', "Traffic Vehicle", "Add Traffic Vehicle Skeleton", 9),
               ('createPlaceable', "Placeable", "Add Placeable Skeleton", 10),
               ('createAnimalHusbandry', "Husbandry", "Add Husbandry Skeleton", 11)],
        default = 'createBaseVehicle')
    
    assets_dropdown: bpy.props.EnumProperty(
        name="Assets List",
        description="List of assets",
        default = 'frontloaderAdapter',
        items=[('',                          "Adapters",                  "Adapters",),
               ('frontloaderAdapter',        "frontloaderAdapter",        "Import frontloaderAdapter",),
               ('telehandlerAdapter',        "telehandlerAdapter",        "Import telehandlerAdapter",),
               ('wheelloaderAdapter',        "wheelloaderAdapter",        "Import wheelloaderAdapter",),
               ('',                          "Beacon Lights",             "Beacon Lights",),
               ('beaconLight01',             "beaconLight01",             "Import beaconLight01",),
               ('beaconLight02',             "beaconLight02",             "Import beaconLight02",),
               ('beaconLight03',             "beaconLight03",             "Import beaconLight03",),
               ('beaconLight04',             "beaconLight04",             "Import beaconLight04",),
               ('beaconLight05',             "beaconLight05",             "Import beaconLight05",),
               ('beaconLight06',             "beaconLight06",             "Import beaconLight06",),
               ('beaconLight07',             "beaconLight07",             "Import beaconLight07",),
               ('beaconLight08',             "beaconLight08",             "Import beaconLight08",),
               ('beaconLight09',             "beaconLight09",             "Import beaconLight09",),
               ('beaconLight10',             "beaconLight10",             "Import beaconLight10",),
               ('beaconLight11',             "beaconLight11",             "Import beaconLight11",),
               ('',                          "Car Hitches",               "Car Hitches",),
               ('fifthWheel_hitch',          "fifthWheel_hitch",          "Import fifthWheel_hitch",),
               ('gooseneck_hitch',           "gooseneck_hitch",           "Import gooseneck_hitch",),
               ('',                          "Hitches",                   "Hitches",),
               ('zetorHitch',                "zetorHitch",                "Import zetorHitch",),
               ('',                          "Lower Link Balls",          "Lower Link Balls",),
               ('lowerLinkBalls',            "lowerLinkBalls",            "Import lowerLinkBalls",),
               ('',                          "Power Take Offs",           "Power Take Offs",),
               ('walterscheidW',             "walterscheidW",             "Import walterscheidW",),
               ('walterscheidWWE',           "walterscheidWWE",           "Import walterscheidWWE",),
               ('walterscheidWWZ',           "walterscheidWWZ",           "Import walterscheidWWZ",),
               ('',                          "Reflectors",                "Reflectors",),
               ('bigTriangle',               "bigTriangle",               "Import bigTriangle",),
               ('redOrangeRectangle_01',     "redOrangeRectangle_01",     "Import redOrangeRectangle_01",),
               ('redRectangle_01',           "redRectangle_01",           "Import redRectangle_01",),
               ('redRound_01',               "redRound_01",               "Import redRound_01",),
               ('redRound_02',               "redRound_02",               "Import redRound_02",),
               ('redRound_03',               "redRound_03",               "Import redRound_03",),
               ('redRound_04',               "redRound_04",               "Import redRound_04",),
               ('redTriangle_01',            "redTriangle_01",            "Import redTriangle_01",),
               ('redTriangle_02',            "redTriangle_02",            "Import redTriangle_02",),
               ('whiteRectangle_01',         "whiteRectangle_01",         "Import whiteRectangle_01",),
               ('whiteRound_01',             "whiteRound_01",             "Import whiteRound_01",),
               ('whiteRound_02',             "whiteRound_02",             "Import whiteRound_02",),
               ('whiteRound_03',             "whiteRound_03",             "Import whiteRound_03",),
               ('whiteRound_04',             "whiteRound_04",             "Import whiteRound_04",),
               ('whiteTriangle_01',          "whiteTriangle_01",          "Import whiteTriangle_01",),
               ('whiteTriangle_02',          "whiteTriangle_02",          "Import whiteTriangle_02",),
               ('yellowRectangle_01',        "yellowRectangle_01",        "Import yellowRectangle_01",),
               ('yellowRound_01',            "yellowRound_01",            "Import yellowRound_01",),
               ('yellowRound_02',            "yellowRound_02",            "Import yellowRound_02",),
               ('yellowRound_03',            "yellowRound_03",            "Import yellowRound_03",),
               ('yellowRound_04',            "yellowRound_04",            "Import yellowRound_04",),
               ('yellowTriangle_01',         "yellowTriangle_01",         "Import yellowTriangle_01",),
               ('yellowTriangle_02',         "yellowTriangle_02",         "Import yellowTriangle_02",),
               ('',                          "Skf Lincoln",               "Skf Lincoln",),
               ('skfLincoln',                "skfLincoln",                "Import skfLincoln",),
               ('',                          "Upper Links",               "Upper Links",),
               ('johnDeere8RTUpperlink',     "johnDeere8RTUpperlink",     "Import johnDeere8RTUpperlink",),
               ('johnDeereUpperlink',        "johnDeereUpperlink",        "Import johnDeereUpperlink",),
               ('walterscheid01',            "walterscheid01",            "Import walterscheid01",),
               ('walterscheid02',            "walterscheid02",            "Import walterscheid02",),
               ('walterscheid03',            "walterscheid03",            "Import walterscheid03",),
               ('walterscheid04',            "walterscheid04",            "Import walterscheid04",),
               ('walterscheid05',            "walterscheid05",            "Import walterscheid05",),
               ('',                          "Wheel Chocks",              "Wheel Chocks",),
               ('chockSupport',              "chockSupport",              "Import chockSupport",),
               ('wheelChock01',              "wheelChock01",              "Import wheelChock01",),
               ('wheelChock02',              "wheelChock02",              "Import Wheel Chock 02",),
               ('wheelChock03',              "wheelChock03",              "Import wheelChock03",),
               ('wheelChock04',              "wheelChock04",              "Import wheelChock04",),
               ('wheelChock05',              "wheelChock05",              "Import Wheel Chock 05",),
               ('',                          "Miscellaneous",             "Miscellaneous",),
               ('attacherTruckGeneric',      "attacherTruckGeneric",      "Import attacherTruckGeneric",),
               ('camera_01',                 "camera_01",                 "Import camera_01",),
               ('camera_02',                 "camera_02",                 "Import camera_02",),
               ('camera_03',                 "camera_03",                 "Import camera_03",),
               ('exhaustLicencePlateHolder', "exhaustLicencePlateHolder", "Import exhaustLicencePlateHolder",),
               ('extinguisher',              "extinguisher",              "Import extinguisher",),
               ('gps',                       "gps",                       "Import gps",),
               ('rearHitch',                 "rearHitch",                 "Import rearHitch",),
               ('smallWheel01',              "smallWheel01",              "Import smallWheel01",),
               ('starFire',                  "starFire",                  "Import starFire",),
               ('toolbar',                   "toolbar",                   "Import toolbar",),
               ('toolbarWide',               "toolbarWide",               "Import toolbarWide",),
               ('towBar',                    "towBar",                    "Import towBar",),
               ('trailerLowAttacher',        "trailerLowAttacher",        "Import trailerLowAttacher",),
               ('trailerToolBox',            "trailerToolBox",            "Import trailerToolBox",),
               ('trailerToolBox02',          "trailerToolBox02",          "Import trailerToolBox02",),
               ('triangleAdapter',           "triangleAdapter",           "Import triangleAdapter",),
               ('upperLink',                 "upperLink",                 "Import upperLink",),
               ('upperLinkSmall',            "upperLinkSmall",            "Import upperLinkSmall",),])

    UI_meshTools: bpy.props.BoolProperty (name="Mesh-Tools", default= False)
    UI_uvTools: bpy.props.BoolProperty (name="UV-Tools", default= False )
    UI_skeletons: bpy.props.BoolProperty (name="Skeletons", default = False )
    UI_materialTools: bpy.props.BoolProperty (name="Material-Tools", default = False )
    UI_assets: bpy.props.BoolProperty (name="Assets Importer", default = False )

class I3DEA_PT_Panel(bpy.types.Panel):
    """ GUI Panel for the I3D Exporter Additionals visible in the 3D Viewport """
    bl_idname       = "I3DEA_PT_Panel"
    bl_label        = "I3D Exporter Additionals"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "GIANTS I3D Exporter"
    bl_options = {'DEFAULT_CLOSED'}

    def draw( self, context):
        layout = self.layout
        # "Mesh-Tools" box
        box = layout.box()
        row = box.row()
        # extend button for
        row.prop(context.scene.i3deapg, "UI_meshTools", text="Mesh-Tools", icon='TRIA_DOWN' if context.scene.i3deapg.UI_meshTools else 'TRIA_RIGHT', icon_only=False, emboss=False)
        # expanded view
        if context.scene.i3deapg.UI_meshTools:
            row = box.row()
            row.operator("tools.remove_doubles", text="Clean Meshes")
            row.operator("tools.mesh_name", text="Set Mesh Name")
            row = box.row()
            row.operator("tools.curve_length", text="Get Curve Length")
            row.operator("tools.ignore", text="Add Suffix _ignore")
        # "UV-Tools" Box
        box = layout.box()
        row = box.row()
        # expand button for "UV-Tools"
        row.prop(context.scene.i3deapg,"UI_uvTools", text="UV-Tools", icon='TRIA_DOWN' if context.scene.i3deapg.UI_uvTools else 'TRIA_RIGHT', icon_only=False, emboss=False)
        # expanded view
        if context.scene.i3deapg.UI_uvTools:
            row = box.row()
            row.prop(context.scene.i3deapg, "size_dropdown", text="")
            row.operator("tools.make_uvset", text="Create UVset 2")
        #---------------------------------------------------------------
        # "Skeleton-Tools" Box
        box = layout.box()
        row = box.row()
        # expand button for "Skeletons"
        row.prop(context.scene.i3deapg,"UI_skeletons", text="Skeletons", icon='TRIA_DOWN' if context.scene.i3deapg.UI_skeletons else 'TRIA_RIGHT', icon_only=False, emboss=False)
        # expanded view
        if context.scene.i3deapg.UI_skeletons:
            row = box.row()
            row.prop(context.scene.i3deapg, "skeletons_dropdown", text="")
            row.operator("tools.skeletons_create", text="Create")
        #---------------------------------------------------------------
        # "Material-Tools" box
        box = layout.box()
        row = box.row()
        # extend button for "Material-Tools"
        row.prop(context.scene.i3deapg,"UI_materialTools", text="Material-Tools", icon='TRIA_DOWN' if context.scene.i3deapg.UI_materialTools else 'TRIA_RIGHT', icon_only=False, emboss=False)
        # expanded view
        if context.scene.i3deapg.UI_materialTools:
            row = box.row()
            row.operator("tools.mirror_material", text="Add Mirror Material")
            row.operator("tools.remove_duplicate_material", text="Remove Duplicate Materials")
        #-----------------------------------------
        # "Assets Importer" box
        box = layout.box()
        row = box.row()
        # extend button for "Assets Importer"
        row.prop(context.scene.i3deapg,"UI_assets", text="Assets Importer", icon='TRIA_DOWN' if context.scene.i3deapg.UI_assets else 'TRIA_RIGHT', icon_only=False, emboss=False)
        # expanded view
        if context.scene.i3deapg.UI_assets:
            row = box.row()
            # row.menu("I3DEA_MT_asset_category")
            row.prop(context.scene.i3deapg, "assets_dropdown", text="")
            row = box.row()
            # row.prop(context.scene.i3deapg, "assets_dropdown", text="")
            row.operator("tools.assets", text="Import Asset")
        #-----------------------------------------

from .tools import (mesh_tools, uv_tools, skeletons, material_tools, freeze_tools, assets_importer,)

classes = [
    I3DEA_PG_List,
    I3DEA_PT_Panel,
    uv_tools.TOOLS_OT_uvset,
    mesh_tools.TOOLS_OT_removeDoubles,
    mesh_tools.TOOLS_OT_meshName,
    mesh_tools.TOOLS_OT_getCurveLength,
    mesh_tools.TOOLS_OT_ignore,
    skeletons.TOOLS_OT_skeletons,
    material_tools.TOOLS_OT_mirrorMaterial,
    material_tools.TOOLS_OT_removeDuplicateMaterial,
    freeze_tools.TOOLS_OT_freezeTrans,
    freeze_tools.TOOLS_OT_freezeRot,
    freeze_tools.TOOLS_OT_freezeScale,
    freeze_tools.TOOLS_OT_freezeAll,
    assets_importer.TOOLS_OT_assets,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
        bpy.types.Scene.i3deapg = bpy.props.PointerProperty(type=I3DEA_PG_List)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
        del bpy.types.Scene.i3deapg