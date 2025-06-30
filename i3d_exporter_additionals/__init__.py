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

if "bpy" in locals():
    import importlib
    importlib.reload(ui)
    importlib.reload(properties)
    importlib.reload(tools)
else:
    from . import ui
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
        giants_to_i3dio,
    )


def register() -> None:
    ui.register()
    track_tools.register()
    verifier.register()
    properties.register()
    generate_empty_on_curves.register()
    mesh_tools.register()
    assets_importer.register()
    skeletons.register()
    material_tools.register()
    orientation_tools.register()
    user_attributes.register()
    properties_converter.register()
    giants_to_i3dio.register()


def unregister() -> None:
    giants_to_i3dio.unregister()
    properties.unregister()
    ui.unregister()
    track_tools.unregister()
    verifier.unregister()
    generate_empty_on_curves.unregister()
    mesh_tools.unregister()
    assets_importer.unregister()
    skeletons.unregister()
    material_tools.unregister()
    orientation_tools.unregister()
    user_attributes.unregister()
    properties_converter.unregister()


if __name__ == "__main__":
    register()
