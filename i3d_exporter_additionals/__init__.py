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
from . import ui


bl_info = {
    "name": "I3D Exporter Additionals",
    "author": "T-Bone",
    "description": "Additionals For I3D Exporter",
    "blender": (3, 5, 0),
    "version": (3, 2, 2),
    "location": "View3D > UI > I3D Exporter Additionals",
    "warning": "",
    "category": "Game Engine"
}

if "bpy" in locals():
    import importlib
    importlib.reload(helper_functions)
    importlib.reload(properties)
    importlib.reload(ui)
    importlib.reload(tools)
else:
    import bpy
    from . import properties
    from .tools import (
        assets_importer,
        orientation_tools,
        material_tools,
        mesh_tools,
        skeletons,
        track_tools,
        user_attributes,
        verifier,
        generate_empty_on_curves,
        properties_converter,
    )

classes = [
    properties.SubPoseItem,
    properties.PoseItem,
    properties.I3DEA_PG_List,
    track_tools.I3DEA_OT_make_uvset,
    track_tools.I3DEA_OT_add_empty,
    track_tools.I3DEA_OT_curve_length,
    track_tools.I3DEA_OT_calculate_amount,
    track_tools.I3DEA_OT_visualization,
    track_tools.I3DEA_OT_visualization_del,
    track_tools.I3DEA_OT_automatic_track_creation,
    mesh_tools.I3DEA_OT_remove_doubles,
    mesh_tools.I3DEA_OT_mesh_name,
    mesh_tools.I3DEA_OT_ignore,
    mesh_tools.I3DEA_OT_mirror_orientation,
    mesh_tools.I3DEA_OT_xml_config,
    mesh_tools.I3DEA_OT_fill_volume,
    mesh_tools.I3DEA_OT_convert_skinnedmesh,
    generate_empty_on_curves.PoseAddOperator,
    generate_empty_on_curves.PoseRemoveOperator,
    generate_empty_on_curves.AddCurveOperator,
    generate_empty_on_curves.RemoveCurveOperator,
    generate_empty_on_curves.I3DEA_OT_empties_along_curves,
    skeletons.I3DEA_OT_skeletons,
    material_tools.I3DEA_OT_mirror_material,
    material_tools.I3DEA_OT_remove_duplicate_material,
    material_tools.I3DEA_OT_setup_material,
    material_tools.I3DEA_OT_i3dio_material,
    orientation_tools.I3DEA_OT_copy_orientation,
    assets_importer.I3DEA_OT_assets,
    user_attributes.I3DEA_OT_create_user_attribute,
    user_attributes.I3DEA_OT_delete_user_attribute,
    verifier.I3DEA_OT_verify_scene,
    properties_converter.I3DEA_OT_properties_converter,

    # UI classes
    ui.I3DEA_PT_MainPanel,
    ui.I3DEA_PT_GeneralTools,
    ui.I3DEA_PT_PropConverter,
    ui.I3DEA_PT_UserAttributes,
    ui.I3DEA_PT_Skeletons,
    ui.I3DEA_PT_MaterialTools,
    ui.I3DEA_PT_AssetImporter,
    ui.I3DEA_PT_TrackTools,
    ui.I3DEA_PT_TrackSetup,
    ui.I3DEA_PT_CreateUvSet,
    ui.I3DEA_PT_CalcAmount,
    ui.I3DEA_PT_AddEmpties,
    ui.I3DEA_PT_CreateAutoTrack,
    ui.I3DEA_PT_TrackVisualization,
    ui.I3DEA_UL_PoseList,
    ui.I3DEA_UL_SubPoseCurveList,
    ui.I3DEA_PT_ArrayHierarchy,
    ui.I3DEA_PT_SubArrayHierarchy,
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.i3dea = bpy.props.PointerProperty(type=properties.I3DEA_PG_List)


def unregister():
    del bpy.types.Scene.i3dea
    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
