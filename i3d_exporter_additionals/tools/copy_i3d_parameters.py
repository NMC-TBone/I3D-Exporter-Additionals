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

# copy_i3d_parameters.py - Copies every Community I3D Exporter (i3dio) specific parameter
# from the active object (and, where applicable, its object data) to all other selected objects.

import bpy

from ..helper_functions import check_i3d_exporter_type

# PropertyGroups (attached directly to the Object) that hold i3dio specific settings.
# Every simple property inside these groups gets copied verbatim.
OBJECT_PROPERTY_GROUPS = (
    "i3d_attributes",  # General I3D Object Attributes (rigidbody, visibility condition, joints, etc.)
    "i3d_mapping",  # I3D Mapping (is_mapped / mapping_name)
    "i3d_reference",  # Reference File (path / runtime_loaded / child_path)
    "i3d_merge_children",  # Merge Children (enabled / apply_transforms / interpolation_steps / reverse_order)
    "i3d_motion_path_array",  # Motion Path Array and all of its sub settings (use_geometry_nodes, etc.)
)

# Plain properties stored directly on the Object (not inside a PropertyGroup).
OBJECT_DIRECT_PROPERTIES = (
    "i3d_merge_group_index",  # Merge Group membership (index into scene.i3dio_merge_groups)
)


def _copy_property_group(source: bpy.types.PropertyGroup, target: bpy.types.PropertyGroup) -> None:
    """Copies every simple (non-collection, non-readonly) property from one PropertyGroup to another."""
    for prop in source.bl_rna.properties:
        identifier = prop.identifier
        if identifier == "rna_type" or prop.is_readonly or prop.type == "COLLECTION":
            continue
        try:
            setattr(target, identifier, getattr(source, identifier))
        except (AttributeError, TypeError, ValueError):
            continue  # Some properties may refuse a value (e.g. a pointer poll() rejecting it), just skip those


def _copy_data_attributes(source_obj: bpy.types.Object, target_obj: bpy.types.Object) -> bool:
    """Copies i3d_attributes stored on the object data (Mesh shape / Bounding Volume, or Light attributes).

    Only copied when both objects share the same data type (e.g. both MESH or both LIGHT),
    since the attributes themselves live on the data-block, not the object.
    """
    if source_obj.type != target_obj.type:
        return False
    if source_obj.type not in {"MESH", "LIGHT"}:
        return False
    if not hasattr(source_obj.data, "i3d_attributes") or not hasattr(target_obj.data, "i3d_attributes"):
        return False
    _copy_property_group(source_obj.data.i3d_attributes, target_obj.data.i3d_attributes)
    return True


class I3DEA_OT_copy_i3d_parameters(bpy.types.Operator):
    bl_idname = "i3dea.copy_i3d_parameters"
    bl_label = "Copy I3D Parameters"
    bl_description = (
        "Copies every Community I3D Exporter (i3dio) specific parameter from the active object "
        "to all other selected objects.\n"
        "Includes I3D Object Attributes, Merge Group, Merge Children, Mapping, Reference File and "
        "Motion Path Array (with all its sub settings, e.g. Use Geometry Nodes).\n"
        "If both objects are of the same type (Mesh or Light), the object data attributes "
        "(e.g. Bounding Volume, Shape/Light Attributes) are copied as well"
    )
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context: bpy.types.Context) -> bool:
        return (
            check_i3d_exporter_type()[1]  # Only makes sense with the Community (i3dio) exporter
            and context.active_object is not None
            and len(context.selected_objects) > 1
        )

    def execute(self, context: bpy.types.Context):
        active = context.active_object
        targets = [obj for obj in context.selected_objects if obj is not active]
        if not targets:
            self.report({"ERROR"}, "Select at least one other object in addition to the active object")
            return {"CANCELLED"}

        data_copied_count = 0
        for obj in targets:
            for group_name in OBJECT_PROPERTY_GROUPS:
                _copy_property_group(getattr(active, group_name), getattr(obj, group_name))

            for prop_name in OBJECT_DIRECT_PROPERTIES:
                setattr(obj, prop_name, getattr(active, prop_name))

            if _copy_data_attributes(active, obj):
                data_copied_count += 1

        self.report(
            {"INFO"},
            f"Copied I3D parameters from '{active.name}' to {len(targets)} object(s) "
            f"({data_copied_count} also received matching object-data attributes).",
        )
        return {"FINISHED"}


classes = (I3DEA_OT_copy_i3d_parameters,)
register, unregister = bpy.utils.register_classes_factory(classes)
