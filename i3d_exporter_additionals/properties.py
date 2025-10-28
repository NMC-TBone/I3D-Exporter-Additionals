import bpy
from bpy.props import BoolProperty, CollectionProperty, EnumProperty, FloatProperty, IntProperty, StringProperty


class SubPoseItem(bpy.types.PropertyGroup):
    curve: StringProperty()


class PoseItem(bpy.types.PropertyGroup):
    name: StringProperty(name="Name", default="Pose")
    sub_pose_list: CollectionProperty(type=SubPoseItem)
    sub_pose_count: IntProperty(default=0)


class I3DEA_PG_List(bpy.types.PropertyGroup):
    # Dropdown for UV size
    size_dropdown: EnumProperty(
        name="Size List",
        description="List of UV size",
        items=[("4", "2x2", "Create UVset 2 2x2"), ("16", "4x4", "Create UVset 2 4x4")],
        default="4",
    )

    # Dropdown for skeletons
    skeletons_dropdown: EnumProperty(
        name="Skeletons List",
        description="List of skeletons",
        items=[
            ("create_base_vehicle", "Tractor", "Add Tractor Skeleton"),
            ("create_base_harvester", "Combine", "Add Harvester Skeleton"),
            ("create_base_tool", "Tool", "Add Tool Skeleton"),
            ("create_attacher_joints", "Attacher Joints", "Add Attacher Joint Skeleton"),
            ("create_player", "Player", "Add Player Skeleton"),
            ("create_lights", "Lights", "Add Lights Skeleton"),
            ("create_cameras_vehicle", "Cameras (Tractor)", "Add Cameras (Tractor) Skeleton"),
            ("create_cameras_harvester", "Cameras (Combine)", "Add Cameras (Combine) Skeleton"),
            ("create_traffic_vehicle", "Traffic Vehicle", "Add Traffic Vehicle Skeleton"),
            ("create_placeable", "Placeable", "Add Placeable Skeleton"),
            ("create_animal_husbandry", "Husbandry", "Add Husbandry Skeleton"),
        ],
    )

    # Dropdown for assets import
    assets_dropdown: EnumProperty(
        name="Assets List",
        description="List of assets",
        items=[
            (
                "",
                "Adapters",
                "Adapters",
            ),
            (
                "frontloaderAdapter",
                "frontloaderAdapter",
                "Import frontloaderAdapter",
            ),
            (
                "telehandlerAdapter",
                "telehandlerAdapter",
                "Import telehandlerAdapter",
            ),
            (
                "wheelloaderAdapter",
                "wheelloaderAdapter",
                "Import wheelloaderAdapter",
            ),
            (
                "",
                "Beacon Lights",
                "Beacon Lights",
            ),
            (
                "beaconLight01",
                "beaconLight01",
                "Import beaconLight01",
            ),
            (
                "beaconLight02",
                "beaconLight02",
                "Import beaconLight02",
            ),
            (
                "beaconLight03",
                "beaconLight03",
                "Import beaconLight03",
            ),
            (
                "beaconLight04",
                "beaconLight04",
                "Import beaconLight04",
            ),
            (
                "beaconLight05",
                "beaconLight05",
                "Import beaconLight05",
            ),
            (
                "beaconLight06",
                "beaconLight06",
                "Import beaconLight06",
            ),
            (
                "beaconLight07",
                "beaconLight07",
                "Import beaconLight07",
            ),
            (
                "beaconLight08",
                "beaconLight08",
                "Import beaconLight08",
            ),
            (
                "beaconLight09",
                "beaconLight09",
                "Import beaconLight09",
            ),
            (
                "beaconLight10",
                "beaconLight10",
                "Import beaconLight10",
            ),
            (
                "beaconLight11",
                "beaconLight11",
                "Import beaconLight11",
            ),
            (
                "",
                "Car Hitches",
                "Car Hitches",
            ),
            (
                "fifthWheel_decal",
                "fifthWheel_hitch",
                "Import fifthWheel_hitch",
            ),
            (
                "gooseneck_decal",
                "gooseneck_hitch",
                "Import gooseneck_hitch",
            ),
            (
                "",
                "Hitches",
                "Hitches",
            ),
            (
                "zetorHitch",
                "zetorHitch",
                "Import zetorHitch",
            ),
            (
                "",
                "Lower Link Balls",
                "Lower Link Balls",
            ),
            (
                "lowerLinkBallRight",
                "lowerLinkBalls",
                "Import lowerLinkBalls",
            ),
            (
                "",
                "Power Take Offs",
                "Power Take Offs",
            ),
            (
                "walterscheidW",
                "walterscheidW",
                "Import walterscheidW",
            ),
            (
                "walterscheidWWE",
                "walterscheidWWE",
                "Import walterscheidWWE",
            ),
            (
                "walterscheidWWZ",
                "walterscheidWWZ",
                "Import walterscheidWWZ",
            ),
            (
                "",
                "Reflectors",
                "Reflectors",
            ),
            (
                "bigTriangle",
                "bigTriangle",
                "Import bigTriangle",
            ),
            (
                "redOrangeRectangle_01",
                "redOrangeRectangle_01",
                "Import redOrangeRectangle_01",
            ),
            (
                "redRectangle_01",
                "redRectangle_01",
                "Import redRectangle_01",
            ),
            (
                "redRound_01",
                "redRound_01",
                "Import redRound_01",
            ),
            (
                "redRound_02",
                "redRound_02",
                "Import redRound_02",
            ),
            (
                "redRound_03",
                "redRound_03",
                "Import redRound_03",
            ),
            (
                "redRound_04",
                "redRound_04",
                "Import redRound_04",
            ),
            (
                "redTriangle_01",
                "redTriangle_01",
                "Import redTriangle_01",
            ),
            (
                "redTriangle_02",
                "redTriangle_02",
                "Import redTriangle_02",
            ),
            (
                "whiteRectangle_01",
                "whiteRectangle_01",
                "Import whiteRectangle_01",
            ),
            (
                "whiteRound_01",
                "whiteRound_01",
                "Import whiteRound_01",
            ),
            (
                "whiteRound_02",
                "whiteRound_02",
                "Import whiteRound_02",
            ),
            (
                "whiteRound_03",
                "whiteRound_03",
                "Import whiteRound_03",
            ),
            (
                "whiteRound_04",
                "whiteRound_04",
                "Import whiteRound_04",
            ),
            (
                "whiteTriangle_01",
                "whiteTriangle_01",
                "Import whiteTriangle_01",
            ),
            (
                "whiteTriangle_02",
                "whiteTriangle_02",
                "Import whiteTriangle_02",
            ),
            (
                "yellowRectangle_01",
                "yellowRectangle_01",
                "Import yellowRectangle_01",
            ),
            (
                "yellowRound_01",
                "yellowRound_01",
                "Import yellowRound_01",
            ),
            (
                "yellowRound_02",
                "yellowRound_02",
                "Import yellowRound_02",
            ),
            (
                "yellowRound_03",
                "yellowRound_03",
                "Import yellowRound_03",
            ),
            (
                "yellowRound_04",
                "yellowRound_04",
                "Import yellowRound_04",
            ),
            (
                "yellowTriangle_01",
                "yellowTriangle_01",
                "Import yellowTriangle_01",
            ),
            (
                "yellowTriangle_02",
                "yellowTriangle_02",
                "Import yellowTriangle_02",
            ),
            (
                "",
                "Skf Lincoln",
                "Skf Lincoln",
            ),
            (
                "skfLincoln",
                "skfLincoln",
                "Import skfLincoln",
            ),
            (
                "",
                "Upper Links",
                "Upper Links",
            ),
            (
                "johnDeere8RTUpperlink",
                "johnDeere8RTUpperlink",
                "Import johnDeere8RTUpperlink",
            ),
            (
                "johnDeereUpperlink",
                "johnDeereUpperlink",
                "Import johnDeereUpperlink",
            ),
            (
                "walterscheid01",
                "walterscheid01",
                "Import walterscheid01",
            ),
            (
                "walterscheid02",
                "walterscheid02",
                "Import walterscheid02",
            ),
            (
                "walterscheid03",
                "walterscheid03",
                "Import walterscheid03",
            ),
            (
                "walterscheid04",
                "walterscheid04",
                "Import walterscheid04",
            ),
            (
                "walterscheid05",
                "walterscheid05",
                "Import walterscheid05",
            ),
            (
                "",
                "Wheel Chocks",
                "Wheel Chocks",
            ),
            (
                "chockSupport",
                "chockSupport",
                "Import chockSupport",
            ),
            (
                "wheelChock01",
                "wheelChock01",
                "Import wheelChock01",
            ),
            (
                "wheelChock02",
                "wheelChock02",
                "Import Wheel Chock 02",
            ),
            (
                "wheelChock03",
                "wheelChock03",
                "Import wheelChock03",
            ),
            (
                "wheelChock04_parked",
                "wheelChock04",
                "Import wheelChock04",
            ),
            (
                "wheelChock05chain2",
                "wheelChock05",
                "Import Wheel Chock 05",
            ),
            (
                "",
                "Miscellaneous",
                "Miscellaneous",
            ),
            (
                "attacherTruckGeneric",
                "attacherTruckGeneric",
                "Import attacherTruckGeneric",
            ),
            (
                "glass",
                "camera_01",
                "Import camera_01",
            ),
            (
                "rotArm2",
                "camera_02",
                "Import camera_02",
            ),
            (
                "glass3",
                "camera_03",
                "Import camera_03",
            ),
            (
                "exhaustLicencePlateHolder",
                "exhaustLicencePlateHolder",
                "Import exhaustLicencePlateHolder",
            ),
            (
                "extinguisher",
                "extinguisher",
                "Import extinguisher",
            ),
            (
                "gps",
                "gps",
                "Import gps",
            ),
            (
                "rearHitch",
                "rearHitch",
                "Import rearHitch",
            ),
            (
                "smallWheel01",
                "smallWheel01",
                "Import smallWheel01",
            ),
            (
                "starFire",
                "starFire",
                "Import starFire",
            ),
            (
                "toolbar",
                "toolbar",
                "Import toolbar",
            ),
            (
                "toolbarWide",
                "toolbarWide",
                "Import toolbarWide",
            ),
            (
                "towBar",
                "towBar",
                "Import towBar",
            ),
            (
                "trailerLowAttacher",
                "trailerLowAttacher",
                "Import trailerLowAttacher",
            ),
            (
                "trailerToolBoxHolder",
                "trailerToolBox",
                "Import trailerToolBox",
            ),
            (
                "trailerToolBox02",
                "trailerToolBox02",
                "Import trailerToolBox02",
            ),
            (
                "triangleAdapter",
                "triangleAdapter",
                "Import triangleAdapter",
            ),
            (
                "upperLink",
                "upperLink",
                "Import upperLink",
            ),
            (
                "upperLinkSmall",
                "upperLinkSmall",
                "Import upperLinkSmall",
            ),
        ],
        default="frontloaderAdapter",
    )

    # Properties for material_tools
    material_name: StringProperty(
        name="Material name",
        description="Write name of the material you want to create",
        default="material_mat",
    )
    diffuse_box: BoolProperty(
        name="Add diffuse node",
        description="If checked it will create a image texture linked to Base Color",
        default=False,
    )
    alpha_box: BoolProperty(
        name="Alpha", description="If checked it will set alpha settings to diffuse node", default=False
    )
    diffuse_texture_path: StringProperty(
        name="Diffuse Texture",
        description="Add path to your diffuse texture.",
        subtype="FILE_PATH",
        default="",
    )
    spec_texture_path: StringProperty(
        name="Specular Texture",
        description="Add path to your specular texture.",
        subtype="FILE_PATH",
        default="",
    )
    normal_texture_path: StringProperty(
        name="Normal Texture",
        description="Add path to your normal map texture.",
        subtype="FILE_PATH",
        default="",
    )

    # i3dio_material handler
    shader_path: StringProperty(
        name="Path to shader location",
        description="Select path to the shader you want to apply",
        subtype="FILE_PATH",
        default="",
    )
    mask_map: StringProperty(
        name="Mask Map",
        description="Add mask map texture",
        subtype="FILE_PATH",
        default="",
    )
    dirt_diffuse: StringProperty(
        name="Dirt diffuse", description="Add dirt diffuse texture", subtype="FILE_PATH", default=""
    )
    shader_box: BoolProperty(
        name="Set shader path",
        description="If checked it will add the the path to the shader in material",
        default=True,
    )
    mask_map_box: BoolProperty(
        name="Set mask map path",
        description="If checked it will add the the path to mask map in material",
        default=True,
    )
    dirt_diffuse_box: BoolProperty(
        name="Set dirt diffuse path",
        description="If checked it add the the path to dirt diffuse in material",
        default=True,
    )

    # Track-Tools
    track_mode: EnumProperty(
        name="Track Mode",
        description="Track Mode",
        items=[
            ("MANUAL", "Manual Tools", ""),
            (
                "AUTOMATIC",
                "Automatic",
                "",
            ),
        ],
        default="MANUAL",
    )
    custom_text_box: BoolProperty(
        name="Custom name",
        description="If checked you will be able to add custom name for the track pieces",
        default=False,
    )
    custom_text: StringProperty(name="Custom track name", description="Set custom name", default="trackPiece")
    add_empty_int: IntProperty(name="Number of empties add: ", description="Place your number", default=1, min=1, max=5)
    piece_distance: FloatProperty(
        name="Track piece distance: ", description="Add track piece distance", default=0.2, precision=10, min=0.0001
    )
    curve_length_disp: StringProperty(name="curve_length", default="0.0")
    track_piece_amount: FloatProperty(
        name="Track pieces possible along curve",
        description="The amount of track links that will fit along the curve",
        min=1,
        max=400,
        default=1,
    )
    rubber_track: BoolProperty(
        name="Rubber Track", description="Check this if you want to visualize a rubber track", default=False
    )
    advanced_mode: BoolProperty(
        name="Advanced Mode", description="Add more options  for UVset2 creation and Track setup", default=False
    )
    add_empties: BoolProperty(
        name="Add Empties",
        description="If you check this it will add the amount of empties between each "
        "track link that's written bellow.",
        default=False,
    )
    track_type_method: EnumProperty(
        name="Track Method",
        items=[
            ("CATERPILLAR", "Caterpillar", ""),
            (
                "RUBBER",
                "Rubber",
                "",
            ),
            ("BOGIE", "Bogie", ""),
        ],
        description="Track visualization method, caterpillar, rubber or bogie",
        default="CATERPILLAR",
    )

    track_vis_amount: IntProperty(
        name="Amount of pieces", description="Amount of track pieces to use along the curve", default=1, min=1, max=200
    )

    track_vis_distance: FloatProperty(
        name="Distance between links",
        description="Distance between each link",
        default=0.2,
        precision=6,
        min=0.0001,
        max=5,
        unit="LENGTH",
    )

    # Automatic mode settings
    auto_use_uvset: BoolProperty(
        name="Create 2nd UV",
        description="If checked it will create 2nd UVset, else it will duplicate your 1st uv layer",
        default=False,
    )

    auto_uvset_dropdown: EnumProperty(
        name="Size List",
        description="List of UV size",
        items=[("4", "2x2", "Create UVset 2 2x2"), ("16", "4x4", "Create UVset 2 4x4")],
        default="4",
    )

    auto_add_vmask: BoolProperty(name="Add Vmask Objects", description="Adds pieces ready for AO bake", default=False)

    auto_fixed_amount: BoolProperty(
        name="Fixed Amount", description="If checked you will need to set the amount manually", default=False
    )

    auto_fxd_amount_int: IntProperty(
        name="Piece Amount",
        description="Fixed number of amount of pieces that will be added",
        default=1,
        min=1,
        max=200,
    )

    auto_add_empties: BoolProperty(
        name="Empty amount", description="If checked it will add the amount of empties bellow", default=False
    )

    auto_empty_int: IntProperty(
        name="Empty amount",
        description="Amount of empties that will be added between each track piece",
        default=1,
        min=1,
        max=5,
    )

    auto_allow_curve_scale: BoolProperty(
        name="Allow Curve Scale",
        description="If checked it will try to scale the curve so it perfectly fits the amount of track pieces",
        default=False,
    )

    selected_curve: bpy.props.PointerProperty(
        name="Select Curve",
        description="Select a curve object",
        type=bpy.types.Object,
        poll=lambda self, obj: obj.type == "CURVE",
    )

    auto_create_bbox: BoolProperty(name="Add BoundingVolume", description="Creates a BV around track", default=False)

    auto_name: StringProperty(name="Custom name", description="Name of the track setup", default="myTrack")

    auto_distance: FloatProperty(name="Distance between links", description="Distance between each link", default=0.2)

    # User Attribute properties.py
    user_attribute_name: StringProperty(name="Name", description="Name of the User Attribute.", default="")

    user_attribute_type: EnumProperty(
        name="Type",
        description="List of User Attributes",
        items=[
            ("boolean", "boolean", ""),
            ("float", "float", ""),
            ("integer", "integer", ""),
            ("string", "string", ""),
            ("scriptCallback", "scriptCallback", ""),
        ],
        default="boolean",
    )

    # Motion Path From Curves
    pose_list: CollectionProperty(type=PoseItem)
    pose_count: IntProperty(default=0)
    motion_type: EnumProperty(
        name="Motion Types",
        items=[
            (
                "UNIFORM",
                "Uniform Count",
                "Sets the fixed number of empties to be uniformly "
                "distributed across each curve, regardless of the curve's length. This ensures a consistent count of "
                "features across different curves, "
                "providing a uniform visual density irrespective of each curve's length",
            ),
            (
                "ADAPTIVE",
                "Adaptive Spacing",
                "Adjusts the spacing of empties based on the length of the longest curve, "
                "applying this uniform spacing across all curves. This method calculates the spacing by dividing the "
                "longest curve's length by the specified number, then uses this spacing to determine the number of "
                "empties on each curve. Shorter curves may have fewer empties due to their length, spaced out to match "
                "the longest curve's distribution",
            ),
            (
                "DISTANCE",
                "Distance",
                "Specifies the fixed distance between each empty, placing empties 0.2 units apart "
                "along each curve whatever the curve's length is. This setting ensures a consistent physical spacing "
                "between empties, suitable for detailed mapping along curves, regardless of the curve's total length",
            ),
        ],
    )

    motion_uniform: IntProperty(
        name="Uniform",
        description="Sets the fixed number of empties to be uniformly distributed across each curve, "
        "regardless of the curve's length. This ensures a consistent count of features across different curves. \n\n"
        "Example: Setting to 32 will distribute 32 empties evenly across all curves, "
        "providing a uniform visual density irrespective of each curve's length",
        default=32,
        min=1,
    )

    motion_adaptive: IntProperty(
        name="Adaptive",
        description="Adjusts the spacing of empties based on the length of the longest curve, "
        "applying this uniform spacing across all curves. This method calculates the spacing by dividing the "
        "longest curve's length by the specified number, "
        "then uses this spacing to determine the number of empties on each curve. "
        "Shorter curves may have fewer empties due to their length. \n\n"
        "Example: Setting to 32 calculates spacing from the longest curve to fit 32 empties. "
        "This spacing is then applied to all curves, so shorter curves will have fewer empties, "
        "spaced out to match the longest curve's distribution",
        default=32,
        min=1,
    )

    motion_distance: FloatProperty(
        name="Fixed Distance",
        description="Specifies the fixed distance between each empty. "
        "Lower values result in more empties closely spaced, suitable for detailed mapping along curves. \n\n"
        "Example: Setting to 0.2 will place empties 0.2 units apart along each curve whatever the curve's length is",
        default=0.2,
        min=0.001,
    )

    motion_hierarchy_name: StringProperty(name="Array Name", default="curveArray")

    motion_save_location: StringProperty(
        name="Save Location",
        description="Choose location where you want the array to be saved",
        default="",
        subtype="DIR_PATH",
    )


classes = (
    SubPoseItem,
    PoseItem,
    I3DEA_PG_List,
)
_register, _unregister = bpy.utils.register_classes_factory(classes)


def register() -> None:
    _register()
    bpy.types.Scene.i3dea = bpy.props.PointerProperty(type=I3DEA_PG_List)


def unregister() -> None:
    del bpy.types.Scene.i3dea
    _unregister()
