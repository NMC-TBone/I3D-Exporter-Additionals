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


"""
TODO:
    - Make a script to check if scale for collisions are 1 1 1
        - Perhaps extend it to verify more
    - See if it's possible to do more with fill volume checker
    - Make support for rubber tracks for track visualization
    - Create a importer for in game lights
"""


bl_info = {
    "name": "I3D Exporter Additionals",
    "author": "T-Bone",
    "description": "Additionals For Giants I3D Exporter",
    "blender": (3, 0, 0),
    "version": (2, 0, 8),
    "location": "View3D > UI > GIANTS I3D Exporter > I3D Exporter Additionals",
    "warning": "",
    "category": "Game Engine"
}


if "bpy" in locals():
    import importlib
    importlib.reload(ui)
    importlib.reload(tools)
else:
    from .tools import (
        assets_importer,
        freeze_tools,
        material_tools,
        mesh_tools,
        skeletons,
        track_tools,
        user_attributes,
    )
    from . import ui


import bpy


class I3DEA_PG_List(bpy.types.PropertyGroup):
    size_dropdown: bpy.props.EnumProperty(
        name="Size List",
        description="List of UV size",
        items=[
            ('four', '2x2', "Create UVset 2 2x2"),
            ('sixteen', '4x4', "Create UVset 2 4x4")],
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
               ('fifthWheel_decal', "fifthWheel_hitch", "Import fifthWheel_hitch",),
               ('gooseneck_decal', "gooseneck_hitch", "Import gooseneck_hitch",),
               ('', "Hitches", "Hitches",),
               ('zetorHitch', "zetorHitch", "Import zetorHitch",),
               ('', "Lower Link Balls", "Lower Link Balls",),
               ('lowerLinkBallRight', "lowerLinkBalls", "Import lowerLinkBalls",),
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
               ('wheelChock04_parked', "wheelChock04", "Import wheelChock04",),
               ('wheelChock05chain2', "wheelChock05", "Import Wheel Chock 05",),
               ('', "Miscellaneous", "Miscellaneous",),
               ('attacherTruckGeneric', "attacherTruckGeneric", "Import attacherTruckGeneric",),
               ('glass', "camera_01", "Import camera_01",),
               ('rotArm2', "camera_02", "Import camera_02",),
               ('glass3', "camera_03", "Import camera_03",),
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
               ('trailerToolBoxHolder', "trailerToolBox", "Import trailerToolBox",),
               ('trailerToolBox02', "trailerToolBox02", "Import trailerToolBox02",),
               ('triangleAdapter', "triangleAdapter", "Import triangleAdapter",),
               ('upperLink', "upperLink", "Import upperLink",),
               ('upperLinkSmall', "upperLinkSmall", "Import upperLinkSmall",), ])

    material_name: bpy.props.StringProperty(name="Material name", description="Write name of the material you want to create", default="material_mat")
    diffuse_box: bpy.props.BoolProperty(name="Add diffuse node", description="If checked it will create a image texture linked to Base Color", default=False)
    alpha_box: bpy.props.BoolProperty(name="Alpha", description="If checked it will set alpha settings to diffuse node", default=False)
    diffuse_texture_path: bpy.props.StringProperty(name="Diffuse", description="Add path to your diffuse texture.", subtype='FILE_PATH', default="")
    spec_texture_path: bpy.props.StringProperty(name="Specular", description="Add path to your specular texture.", subtype='FILE_PATH', default="")
    normal_texture_path: bpy.props.StringProperty(name="Normal", description="Add path to your normal map texture.", subtype='FILE_PATH', default="")

    shader_path: bpy.props.StringProperty(name="Path to shader location", description="Select path to the shader you want to apply", subtype='FILE_PATH', default="")
    mask_map: bpy.props.StringProperty(name="Mask Map", description="Add mask map texture", subtype='FILE_PATH', default="")
    dirt_diffuse: bpy.props.StringProperty(name="Dirt diffuse", description="Add dirt diffuse texture", subtype='FILE_PATH', default="")
    shader_box: bpy.props.BoolProperty(name="Set shader path", description="If checked it will add the the path to the shader in material", default=True)
    mask_map_box: bpy.props.BoolProperty(name="Set mask map path", description="If checked it will add the the path to mask map in material", default=True)
    dirt_diffuse_box: bpy.props.BoolProperty(name="Set dirt diffuse path", description="If checked it add the the path to dirt diffuse in material", default=True)

    # Track-Tools
    def get_all_curves(self, context):
        """ Returns enum elements of all Curves of the current Scene. """
        # From Giants I3D Exporter

        curves = tuple()
        curves += (("None", "None", "None", 0),)
        try:
            num = 1
            for curveName in [obj.name for obj in context.scene.objects if obj.type == 'CURVE']:
                curves += ((curveName, curveName, curveName, num),)
                num += 1
            return curves
        except:
            return curves

    custom_text_box: bpy.props.BoolProperty(name="Custom name", description="If checked you will be able to add custom name for the track pieces", default=False)
    custom_text: bpy.props.StringProperty(name="Custom track name", description="Set custom name", default="trackPiece")
    add_empty_int: bpy.props.IntProperty(name="Number of empties add: ", description="Place your number", default=1, min=1, max=5)
    piece_distance: bpy.props.FloatProperty(name="Track piece distance: ", description="Add track piece distance", default=0.2, precision=10, min=0.0001)
    curve_length_disp: bpy.props.FloatProperty(name="curve_length", default=0.0, precision=10)
    track_piece_amount: bpy.props.FloatProperty(name="Track pieces possible along curve", description="The amount of track links that will fit along the curve", min=1, max=400, default=1)
    rubber_track: bpy.props.BoolProperty(name="Rubber Track", description="Check this if you want to visualize a rubber track", default=False)
    advanced_mode: bpy.props.BoolProperty(name="Advanced Mode", description="Add more options  for UVset2 creation and Track setup", default=False)
    all_curves: bpy.props.EnumProperty(items=get_all_curves, name="Select A Curve")
    add_empties: bpy.props.BoolProperty(name="Add Empties", description="If you check this it will add the amount of empties between each track link that's written bellow.", default=False)

    # User Attributes
    user_attribute_name: bpy.props.StringProperty(name="Name", description="Name of the User Attribute.", default="")
    user_attribute_type: bpy.props.EnumProperty(
        name="Type",
        description="List of UV size",
        items=[
            ('boolean', "boolean", ""),
            ('float', "float", ""),
            ('string', "string", ""),
            ('scriptCallback', "scriptCallback", ""),],
        default='boolean')

    UI_meshTools: bpy.props.BoolProperty(name="Mesh-Tools", default=False)
    UI_user_attributes: bpy.props.BoolProperty(name="User Attributes", default=False)
    UI_track_tools: bpy.props.BoolProperty(name="UV-Tools", default=False)
    UI_uvset: bpy.props.BoolProperty(name="UVset", default=False)
    UI_skeletons: bpy.props.BoolProperty(name="Skeletons", default=False)
    UI_materialTools: bpy.props.BoolProperty(name="Material-Tools", default=False)
    UI_create_mat: bpy.props.BoolProperty(name="Create material", default=False)
    UI_paths: bpy.props.BoolProperty(name="Add paths to material", default=False)
    UI_assets: bpy.props.BoolProperty(name="Assets Importer", default=False)
    UI_active_obj: bpy.props.StringProperty(name="Active Object Name", default="")




classes = [
    I3DEA_PG_List,
    ui.I3DEA_PT_panel,
    track_tools.I3DEA_OT_make_uvset,
    track_tools.I3DEA_OT_add_empty,
    track_tools.I3DEA_OT_curve_length,
    track_tools.I3DEA_OT_calculate_amount,
    track_tools.I3DEA_OT_track_on_curve,
    track_tools.I3DEA_OT_track_on_curve_delete,
    mesh_tools.I3DEA_OT_remove_doubles,
    mesh_tools.I3DEA_OT_mesh_name,
    mesh_tools.I3DEA_OT_ignore,
    mesh_tools.I3DEA_OT_mirror_orientation,
    mesh_tools.I3DEA_OT_xml_config,
    mesh_tools.I3DEA_OT_fill_volume,
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
    user_attributes.I3DEA_OT_create_user_attribute,
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.i3dea = bpy.props.PointerProperty(type=I3DEA_PG_List)


def unregister():
    del bpy.types.Scene.i3dea
    for cls in classes:
        bpy.utils.unregister_class(cls)
