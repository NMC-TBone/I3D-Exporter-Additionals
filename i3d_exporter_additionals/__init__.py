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


_needs_reload = "bpy" in locals()

from . import ui, properties  # noqa: E402
from .tools import (          # noqa: E402
    align_hydraulic_pair,
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

if _needs_reload:
    import importlib
    for _m in (
        ui,
        properties,
        align_hydraulic_pair,
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
    ):
        importlib.reload(_m)


def register() -> None:
    properties.register()
    align_hydraulic_pair.register()
    track_tools.register()
    verifier.register()
    generate_empty_on_curves.register()
    mesh_tools.register()
    assets_importer.register()
    skeletons.register()
    material_tools.register()
    orientation_tools.register()
    user_attributes.register()
    properties_converter.register()
    giants_to_i3dio.register()
    ui.register()


def unregister() -> None:
    ui.unregister()
    giants_to_i3dio.unregister()
    properties_converter.unregister()
    user_attributes.unregister()
    orientation_tools.unregister()
    material_tools.unregister()
    skeletons.unregister()
    assets_importer.unregister()
    mesh_tools.unregister()
    generate_empty_on_curves.unregister()
    verifier.unregister()
    track_tools.unregister()
    align_hydraulic_pair.unregister()
    properties.unregister()


if __name__ == "__main__":
    register()
