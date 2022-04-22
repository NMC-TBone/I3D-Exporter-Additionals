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
    "version" : (1, 0, 1),
    "location" : "View3D > UI > GIANTS I3D Exporter > I3D Exporter Additionals",
    "warning" : "W.I.P",
    "category" : "Generic"
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
        items=[('', "Adapters", "Adapters",),
               ('frontloaderAdapter', "Frontloader Adapter", "Import Frontloader Adapter",),
               ('telehandlerAdapter', "Telehandler Adapter", "Import Telehandler Adapter",),
               ('wheelloaderAdapter', "Wheelloader Adapter", "Import Wheelloader Adapter",),
               ('', "Beacon Lights", "Beacon Lights",),
               ('beaconLight01', "beaconLight01", "Import beaconLight01",),
               ('beaconLight02', "beaconLight02", "Import beaconLight02",),
               ('beaconLight03', "beaconLight03", "Import beaconLight03",),
               ('beaconLight04', "beaconLight04", "Import beaconLight04",),
               ('beaconLight05', "beaconLight05", "Import beaconLight05",),
               ('beaconLight06', "beaconLight06", "Import beaconLight06",),
               ('beaconLight07', "beaconLight07", "Import beaconLight07",),
               ('beaconLight08', "beaconLight08", "Import beaconLight08",),
               ('beaconLight09', "beaconLight09", "Import beaconLight09",),
               ('beaconLight10', "beaconLight10", "Import beaconLight10",),
               ('beaconLight11', "beaconLight11", "Import beaconLight11",),
               ('', "Car Hitches", "Car Hitches",),
               ('fifthWheel_hitch', "fifthWheel_hitch", "Import fifthWheel_hitch",),
               ('gooseneck_hitch', "gooseneck_hitch", "Import gooseneck_hitch",),
               ('', "Hitches", "Hitches",),
               ('', "Lights", "Lights",),
               ('', "Lower Link Balls", "Lower Link Balls",),
               ('lowerLinkBalls', "lowerLinkBalls", "Import lowerLinkBalls",),
               ('', "Power Take Offs", "Power Take Offs",),
               ('', "Reflectors", "Reflectors",),
               ('bigTriangle', "bigTriangle", "Import bigTriangle",),
               ('redOrangeRectangle_01', "redOrangeRectangle_01", "Import redOrangeRectangle_01",),
               ('redRectangle_01', "redRectangle_01", "Import redRectangle_01",),
               ('redRound_01', "redRound_01", "Import redRound_01",),
               ('redRound_02', "redRound_02", "Import redRound_02",),
               ('redRound_03', "redRound_03", "Import redRound_03",),
               ('redRound_04', "redRound_04", "Import redRound_04",),
               ('redTriangle_01', "redTriangle_01", "Import redTriangle_01",),
               ('redTriangle_02', "redTriangle_02", "Import redTriangle_02",),
               ('redRound_02', "redRound_02", "Import redRound_02",),
               ('', "Skf Lincoln", "Skf Lincoln",),
               ('skfLincoln', "skfLincoln", "Import skfLincoln",),
               ('', "Upper Links", "Upper Links",),
               ('', "Wheel Chocks", "Wheel Chocks",),
               ('chockSupport', "chockSupport", "Import chockSupport",),
               ('wheelChock01', "wheelChock01", "Import wheelChock01",),
               ('wheelChock02', "wheelChock02", "Import Wheel Chock 02",),
               ('wheelChock03', "Wheel Chock 03", "Import Wheel Chock 03",),
               ('wheelChock04', "Wheel Chock 04", "Import Wheel Chock 04",),
               ('wheelChock05', "Wheel Chock 05", "Import Wheel Chock 05",),],
        default = 'chockSupport')

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