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
    - See if it's possible to do more with fill volume checker
    - Make it possible to scale the curve to get an rounded value for the track amount
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
    importlib.reload(properties)
    importlib.reload(ui)
    importlib.reload(tools)
else:
    from . import properties, ui
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
    )


import bpy


classes = [
    properties.I3DEA_custom_ObjectProps,
    properties.I3DEA_PG_List,
    ui.I3DEA_PT_panel,
    track_tools.I3DEA_OT_make_uvset,
    track_tools.I3DEA_OT_add_empty,
    track_tools.I3DEA_OT_curve_length,
    track_tools.I3DEA_OT_calculate_amount,
    track_tools.I3DEA_OT_visualization,
    track_tools.I3DEA_OT_visualization_del,
    mesh_tools.I3DEA_OT_remove_doubles,
    mesh_tools.I3DEA_OT_mesh_name,
    mesh_tools.I3DEA_OT_ignore,
    mesh_tools.I3DEA_OT_mirror_orientation,
    mesh_tools.I3DEA_OT_xml_config,
    mesh_tools.I3DEA_OT_fill_volume,
    generate_empty_on_curves.I3DEA_OT_empties_along_curves,
    generate_empty_on_curves.I3DEA_UL_selected_curves,
    generate_empty_on_curves.I3DEA_UL_selected_curves2,
    skeletons.I3DEA_OT_skeletons,
    material_tools.I3DEA_OT_mirror_material,
    material_tools.I3DEA_OT_remove_duplicate_material,
    material_tools.I3DEA_OT_setup_material,
    material_tools.I3DEA_OT_i3dio_material,
    orientation_tools.I3DEA_OT_copy_orientation,
    assets_importer.I3DEA_OT_assets,
    user_attributes.I3DEA_OT_create_user_attribute,
    verifier.I3DEA_OT_verify_scene,
]


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.i3dea = bpy.props.PointerProperty(type=properties.I3DEA_PG_List)


def unregister():
    del bpy.types.Scene.i3dea
    for cls in classes:
        bpy.utils.unregister_class(cls)
