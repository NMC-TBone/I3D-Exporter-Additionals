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
    "name": "I3D Exporter Additionals",
    "author": "T-Bone",
    "description": "Additionals For Giants I3D Exporter",
    "blender": (3, 0, 0),
    "version": (2, 0, 5),
    "location": "View3D > UI > GIANTS I3D Exporter > I3D Exporter Additionals",
    "warning": "",
    "category": "Game Engine"
}

import bpy


# Check if Giants I3D or Stjerne I3D addon is installed
def check_i3d_exporter_type():
    giants_i3d = False
    I3DRemoveAttributes: any = {}
    dcc: any = {}
    stjerne_i3d = False

    for a in bpy.context.preferences.addons:
        if a.module == "io_export_i3d":
            giants_i3d = True
            from io_export_i3d.dcc import dccBlender as dcc
            from io_export_i3d.dcc import I3DRemoveAttributes
        if a.module == "i3dio":
            stjerne_i3d = True

    return giants_i3d, stjerne_i3d, dcc, I3DRemoveAttributes


class I3DEA_PG_List(bpy.types.PropertyGroup):
    size_dropdown: bpy.props.EnumProperty(
        name="Size List",
        description="List of UV size",
        items=[
            ('four', "2x2", "Create UVset 2 2x2"),
            ('sixteen', "4x4", "Create UVset 2 4x4")],
        default='four')

    skeletons_dropdown: bpy.props.EnumProperty(
        items=[
            ('create_base_vehicle', 'Tractor', "Add Tractor Skeleton"),
            ('create_base_harvester', 'Combine', "Add Harvester Skeleton"),
            ('create_base_tool', 'Tool', "Add Tool Skeleton"),
            ('create_attacher_joints', 'Attacher Joints', "Add Attacher Joint Skeleton"),
            ('create_player', "Player", 'Add Player Skeleton'),
            ('create_lights', "Lights", 'Add Lights Skeleton'),
            ('create_cameras_vehicle', 'Cameras (Tractor)', "Add Cameras (Tractor) Skeleton"),
            ('create_cameras_harvester', 'Cameras (Combine)', "Add Cameras (Combine) Skeleton"),
            ('create_traffic_vehicle', 'Traffic Vehicle', "Add Traffic Vehicle Skeleton"),
            ('create_placeable', 'Placeable', "Add Placeable Skeleton"),
            ('create_animal_husbandry', 'Husbandry', "Add Husbandry Skeleton")
        ],
        name="Skeletons List",
        description="List of skeletons")

    assets_dropdown: bpy.props.EnumProperty(
        name="Assets List",
        description="List of assets",
        default='frontloaderAdapter',
        items=[('', "Adapters", "Adapters",),
               ('frontloaderAdapter', "frontloaderAdapter", "Import frontloaderAdapter",),
               ('telehandlerAdapter', "telehandlerAdapter", "Import telehandlerAdapter",),
               ('wheelloaderAdapter', "wheelloaderAdapter", "Import wheelloaderAdapter",),
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
               ('zetorHitch', "zetorHitch", "Import zetorHitch",),
               ('', "Lower Link Balls", "Lower Link Balls",),
               ('lowerLinkBalls', "lowerLinkBalls", "Import lowerLinkBalls",),
               ('', "Power Take Offs", "Power Take Offs",),
               ('walterscheidW', "walterscheidW", "Import walterscheidW",),
               ('walterscheidWWE', "walterscheidWWE", "Import walterscheidWWE",),
               ('walterscheidWWZ', "walterscheidWWZ", "Import walterscheidWWZ",),
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
               ('whiteRectangle_01', "whiteRectangle_01", "Import whiteRectangle_01",),
               ('whiteRound_01', "whiteRound_01", "Import whiteRound_01",),
               ('whiteRound_02', "whiteRound_02", "Import whiteRound_02",),
               ('whiteRound_03', "whiteRound_03", "Import whiteRound_03",),
               ('whiteRound_04', "whiteRound_04", "Import whiteRound_04",),
               ('whiteTriangle_01', "whiteTriangle_01", "Import whiteTriangle_01",),
               ('whiteTriangle_02', "whiteTriangle_02", "Import whiteTriangle_02",),
               ('yellowRectangle_01', "yellowRectangle_01", "Import yellowRectangle_01",),
               ('yellowRound_01', "yellowRound_01", "Import yellowRound_01",),
               ('yellowRound_02', "yellowRound_02", "Import yellowRound_02",),
               ('yellowRound_03', "yellowRound_03", "Import yellowRound_03",),
               ('yellowRound_04', "yellowRound_04", "Import yellowRound_04",),
               ('yellowTriangle_01', "yellowTriangle_01", "Import yellowTriangle_01",),
               ('yellowTriangle_02', "yellowTriangle_02", "Import yellowTriangle_02",),
               ('', "Skf Lincoln", "Skf Lincoln",),
               ('skfLincoln', "skfLincoln", "Import skfLincoln",),
               ('', "Upper Links", "Upper Links",),
               ('johnDeere8RTUpperlink', "johnDeere8RTUpperlink", "Import johnDeere8RTUpperlink",),
               ('johnDeereUpperlink', "johnDeereUpperlink", "Import johnDeereUpperlink",),
               ('walterscheid01', "walterscheid01", "Import walterscheid01",),
               ('walterscheid02', "walterscheid02", "Import walterscheid02",),
               ('walterscheid03', "walterscheid03", "Import walterscheid03",),
               ('walterscheid04', "walterscheid04", "Import walterscheid04",),
               ('walterscheid05', "walterscheid05", "Import walterscheid05",),
               ('', "Wheel Chocks", "Wheel Chocks",),
               ('chockSupport', "chockSupport", "Import chockSupport",),
               ('wheelChock01', "wheelChock01", "Import wheelChock01",),
               ('wheelChock02', "wheelChock02", "Import Wheel Chock 02",),
               ('wheelChock03', "wheelChock03", "Import wheelChock03",),
               ('wheelChock04', "wheelChock04", "Import wheelChock04",),
               ('wheelChock05', "wheelChock05", "Import Wheel Chock 05",),
               ('', "Miscellaneous", "Miscellaneous",),
               ('attacherTruckGeneric', "attacherTruckGeneric", "Import attacherTruckGeneric",),
               ('camera_01', "camera_01", "Import camera_01",),
               ('camera_02', "camera_02", "Import camera_02",),
               ('camera_03', "camera_03", "Import camera_03",),
               ('exhaustLicencePlateHolder', "exhaustLicencePlateHolder", "Import exhaustLicencePlateHolder",),
               ('extinguisher', "extinguisher", "Import extinguisher",),
               ('gps', "gps", "Import gps",),
               ('rearHitch', "rearHitch", "Import rearHitch",),
               ('smallWheel01', "smallWheel01", "Import smallWheel01",),
               ('starFire', "starFire", "Import starFire",),
               ('toolbar', "toolbar", "Import toolbar",),
               ('toolbarWide', "toolbarWide", "Import toolbarWide",),
               ('towBar', "towBar", "Import towBar",),
               ('trailerLowAttacher', "trailerLowAttacher", "Import trailerLowAttacher",),
               ('trailerToolBox', "trailerToolBox", "Import trailerToolBox",),
               ('trailerToolBox02', "trailerToolBox02", "Import trailerToolBox02",),
               ('triangleAdapter', "triangleAdapter", "Import triangleAdapter",),
               ('upperLink', "upperLink", "Import upperLink",),
               ('upperLinkSmall', "upperLinkSmall", "Import upperLinkSmall",), ])

    material_name: bpy.props.StringProperty(name="Material name", description="Write name of the material you want to create", default="material_mat")
    diffuse_box: bpy.props.BoolProperty(name="Add diffuse node", description="If checked it will create a image texture linked to Base Color", default=False)
    alpha_box: bpy.props.BoolProperty(name="Alpha", description="If checked it will set alpha settings to diffuse node", default=False)

    shader_path: bpy.props.StringProperty(name="Path to shader location", description="Select path to the shader you want to apply", subtype='FILE_PATH', default="")
    mask_map: bpy.props.StringProperty(name="Mask Map", description="Add mask map texture", subtype='FILE_PATH', default="")
    dirt_diffuse: bpy.props.StringProperty(name="Dirt diffuse", description="Add dirt diffuse texture", subtype='FILE_PATH', default="")
    shader_box: bpy.props.BoolProperty(name="Set shader path", description="If checked it will add the the path to the shader in material", default=True)
    mask_map_box: bpy.props.BoolProperty(name="Set mask map path", description="If checked it will add the the path to mask map in material", default=True)
    dirt_diffuse_box: bpy.props.BoolProperty(name="Set dirt diffuse path", description="If checked it add the the path to dirt diffuse in material", default=True)

    # Track-Tools
    custom_text_box: bpy.props.BoolProperty(name="Custom name", description="If checked you will be able to add custom name for the track pieces", default=False)
    custom_text: bpy.props.StringProperty(name="Custom track name", description="Set custom name", default="trackPiece")
    add_empty_int: bpy.props.IntProperty(name="Number of empties add: ", description="Place your number", default=1, min=1, max=5)

    UI_meshTools: bpy.props.BoolProperty(name="Mesh-Tools", default=False)
    UI_track_tools: bpy.props.BoolProperty(name="UV-Tools", default=False)
    UI_uvset: bpy.props.BoolProperty(name="UVset", default=False)
    UI_skeletons: bpy.props.BoolProperty(name="Skeletons", default=False)
    UI_materialTools: bpy.props.BoolProperty(name="Material-Tools", default=False)
    UI_create_mat: bpy.props.BoolProperty(name="Create material", default=False)
    UI_paths: bpy.props.BoolProperty(name="Add paths to material", default=False)
    UI_assets: bpy.props.BoolProperty(name="Assets Importer", default=False)


class I3DEA_PT_panel(bpy.types.Panel):
    """ GUI Panel for the I3D Exporter Additionals visible in the 3D Viewport """
    bl_idname = "I3DEA_PT_panel"
    bl_label = "I3D Exporter Additionals"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "GIANTS I3D Exporter"

    def draw(self, context):
        layout = self.layout
        giants_i3d, stjerne_i3d, dcc, I3DRemoveAttributes = check_i3d_exporter_type()
        if giants_i3d and stjerne_i3d:
            # "Exporter selection" box
            layout.label(text="Both Giants & Stjerne I3D exporter is enabled", icon='ERROR')
            layout.label(text="Recommend to disable one of them as it can cause some issues")
            # layout.label(text="Do you want do disable one of them?")
            # layout.operator("i3dea.addon_disable_giants", text="Giants")
            # layout.operator("i3dea.addon_disable_stjerne", text="Stjerne")
        # "Mesh-Tools" box
        box = layout.box()
        row = box.row()
        # extend button for
        row.prop(context.scene.i3dea, "UI_meshTools", text="Mesh-Tools", icon='TRIA_DOWN' if context.scene.i3dea.UI_meshTools else 'TRIA_RIGHT', icon_only=False, emboss=False)
        # expanded view
        if context.scene.i3dea.UI_meshTools:
            row = box.row()
            row.operator("i3dea.remove_doubles", text="Clean Meshes")
            row.operator("i3dea.mesh_name", text="Set Mesh Name")
            row = box.row()
            row.operator("i3dea.curve_length", text="Get Curve Length")

            if giants_i3d:
                row.operator("i3dea.ignore", text="Add Suffix _ignore")
        # "Track-Tools" Box
        box = layout.box()
        row = box.row()
        # expand button for "Track-Tools"
        row.prop(context.scene.i3dea, "UI_track_tools", text="Track-Tools", icon='TRIA_DOWN' if context.scene.i3dea.UI_track_tools else 'TRIA_RIGHT', icon_only=False, emboss=False)
        # expanded view
        if context.scene.i3dea.UI_track_tools:
            col = box.column()
            box = col.box()
            row = box.row()
            row.prop(context.scene.i3dea, "UI_uvset", text="UVset 2", icon='TRIA_DOWN' if context.scene.i3dea.UI_uvset else 'TRIA_RIGHT', icon_only=False, emboss=False)
            if context.scene.i3dea.UI_uvset:
                row = box.row()
                row.prop(context.scene.i3dea, "custom_text_box", text="Custom Name")
                if context.scene.i3dea.custom_text_box:
                    row = box.row()
                    row.prop(context.scene.i3dea, "custom_text", text="Custom track name")
                row = box.row()
                row.prop(context.scene.i3dea, "size_dropdown", text="")
                row.operator("i3dea.make_uvset", text="Create UVset 2")
            box = col.box()
            row = box.row()
            row.prop(context.scene.i3dea, "add_empty_int", text="")
            row.operator("i3dea.add_empty", text="Add Empty")
        # ---------------------------------------------------------------
        # "Skeleton-Tools" Box
        box = layout.box()
        row = box.row()
        # expand button for "Skeletons"
        row.prop(context.scene.i3dea, "UI_skeletons", text="Skeletons", icon='TRIA_DOWN' if context.scene.i3dea.UI_skeletons else 'TRIA_RIGHT', icon_only=False, emboss=False)
        # expanded view
        if context.scene.i3dea.UI_skeletons:
            row = box.row()
            row.prop(context.scene.i3dea, "skeletons_dropdown", text="")
            row.operator("i3dea.skeletons", text="Create")
        # ---------------------------------------------------------------
        # "Material-Tools" box
        box = layout.box()
        row = box.row()
        # extend button for "Material-Tools"
        row.prop(context.scene.i3dea, "UI_materialTools", text="Material-Tools", icon='TRIA_DOWN' if context.scene.i3dea.UI_materialTools else 'TRIA_RIGHT', icon_only=False, emboss=False)
        # expanded view
        if context.scene.i3dea.UI_materialTools:
            row = box.row()
            row.operator("i3dea.mirror_material", text="Add Mirror Material")
            row.operator("i3dea.remove_duplicate_material", text="Remove Duplicate Materials")
            col = box.column()
            box = col.box()
            row = box.row()
            row.prop(context.scene.i3dea, "UI_create_mat", text="Create a material", icon='TRIA_DOWN' if context.scene.i3dea.UI_create_mat else 'TRIA_RIGHT', icon_only=False, emboss=False)
            if context.scene.i3dea.UI_create_mat:
                # row.label(text="Create a material")
                row = box.row()
                row.prop(context.scene.i3dea, "diffuse_box", text="Diffuse")
                if context.scene.i3dea.diffuse_box:
                    row.prop(context.scene.i3dea, "alpha_box", text="Alpha")
                row = box.row()
                row.prop(context.scene.i3dea, "material_name", text="")
                row = box.row()
                row.operator("i3dea.setup_material", text="Create " + bpy.context.scene.i3dea.material_name)
            if stjerne_i3d:
                box = col.box()
                row = box.row()
                row.prop(context.scene.i3dea, "UI_paths", text="Add paths to material", icon='TRIA_DOWN' if context.scene.i3dea.UI_paths else 'TRIA_RIGHT', icon_only=False, emboss=False)
                if context.scene.i3dea.UI_paths:
                    row = box.row()
                    row.prop(context.scene.i3dea, "shader_box", text="")
                    row.prop(context.scene.i3dea, "shader_path", text="Shader path")
                    row = box.row()
                    row.prop(context.scene.i3dea, "mask_map_box", text="")
                    row.prop(context.scene.i3dea, "mask_map", text="Mask texture")
                    row = box.row()
                    row.prop(context.scene.i3dea, "dirt_diffuse_box", text="")
                    row.prop(context.scene.i3dea, "dirt_diffuse", text="Dirt texture")
                    row = box.row()
                    row.operator("i3dea.i3dio_material", text="Run")
        # -----------------------------------------
        # "Assets Importer" box
        box = layout.box()
        row = box.row()
        # extend button for "Assets Importer"
        row.prop(context.scene.i3dea, "UI_assets", text="Assets Importer", icon='TRIA_DOWN' if context.scene.i3dea.UI_assets else 'TRIA_RIGHT', icon_only=False, emboss=False)
        # expanded view
        if context.scene.i3dea.UI_assets:
            row = box.row()
            row.prop(context.scene.i3dea, "assets_dropdown", text="")
            row = box.row()
            row.operator("i3dea.assets", text="Import Asset")
        # -----------------------------------------


class I3DEA_OT_addon_disable_giants(bpy.types.Operator):
    bl_idname = "i3dea.addon_disable_giants"
    bl_label = "Disable Giants Exporter"
    bl_description = "Disable Giants Exporter"
    bl_options = {'UNDO'}

    def execute(self, context):
        bpy.ops.preferences.addon_disable(module='io_export_i3d')
        self.report({'INFO'}, "Giants I3D Exporter is now disabled")
        return {'FINISHED'}


class I3DEA_OT_addon_disable_stjerne(bpy.types.Operator):
    bl_idname = "i3dea.addon_disable_stjerne"
    bl_label = "Disable Stjerne Exporter"
    bl_description = "Disable Stjerne Exporter"
    bl_options = {'UNDO'}

    def execute(self, context):
        bpy.ops.preferences.addon_disable(module='i3dio')
        self.report({'INFO'}, "Stjerne I3D Exporter is now disabled")
        return {'FINISHED'}


from .tools import (mesh_tools, track_tools, skeletons, material_tools, freeze_tools, assets_importer, )

classes = [
    I3DEA_PG_List,
    I3DEA_PT_panel,
    I3DEA_OT_addon_disable_giants,
    I3DEA_OT_addon_disable_stjerne,
    track_tools.I3DEA_OT_make_uvset,
    track_tools.I3DEA_OT_add_empty,
    mesh_tools.I3DEA_OT_remove_doubles,
    mesh_tools.I3DEA_OT_mesh_name,
    mesh_tools.I3DEA_OT_curve_length,
    mesh_tools.I3DEA_OT_ignore,
    skeletons.I3DEA_OT_skeletons,
    material_tools.I3DEA_OT_mirror_material,
    material_tools.I3DEA_OT_remove_duplicate_material,
    material_tools.I3DEA_OT_setup_material,
    material_tools.I3DEA_OT_i3dio_material,
    freeze_tools.I3DEA_OT_freeze_trans,
    freeze_tools.I3DEA_OT_freeze_rot,
    freeze_tools.I3DEA_OT_freeze_scale,
    freeze_tools.I3DEA_OT_freeze_all,
    assets_importer.I3DEA_OT_assets,
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.i3dea = bpy.props.PointerProperty(type=I3DEA_PG_List)


def unregister():
    del bpy.types.Scene.i3dea
    for cls in classes:
        bpy.utils.unregister_class(cls)
