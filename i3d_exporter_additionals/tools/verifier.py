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

# Test the whole scene to check if there is any issues in the setup before export to i3d

import bpy
from mathutils import Vector

MAX_OBJECT_COUNT = 150
MAX_POLY_COUNT = 200000
MAX_MERGE_GROUP_MEMBERS = 60


class I3DEA_OT_verify_scene(bpy.types.Operator):
    bl_idname = "i3dea.verify_scene"
    bl_label = "Verify Scene"
    bl_description = "Check the whole scene if there is something that may be wrong"

    def check_placeable(self, obj):
        if "placeable" in obj.name.lower():
            return True
        for mat in obj.material_slots:
            if 'customShader' in mat.material:
                if "placeableShader" or "buildingShader" in mat.material['customShader']:
                    return True
        return False

    def execute(self, context):
        component_number = 1
        is_placeable = any(self.check_placeable(obj) for obj in bpy.data.objects)
        error_count = 0
        warning_count = 0
        info_count = 0
        total_object_count = 0
        total_poly_count = 0

        dg = bpy.context.evaluated_depsgraph_get()

        print("--------------------")
        print("VERIFY SCENE RESULTS")
        print("--------------------")

        ignored_obj_names = set()
        for obj in bpy.data.objects:
            if obj.name.lower().endswith("_ignore"):
                children_objs = get_children(obj.name)
                ignored_obj_names.update(obj.name for obj in children_objs)

        for obj in bpy.data.objects:
            if obj.name in ignored_obj_names:
                continue

            if obj.type != 'MESH':
                continue
            name_lower = obj.name.lower()
            has_armature = any(mo.type == "ARMATURE" for mo in obj.modifiers)

            eval_obj = obj.evaluated_get(dg)
            mesh = bpy.data.meshes.new_from_object(eval_obj)
            poly_count = len(mesh.polygons)

            is_non_renderable = obj.get('I3D_nonRenderable', 0) == 1
            merge_group = obj.get('I3D_mergeGroup', 0)

            if poly_count > 0 and not is_non_renderable and merge_group == 0:
                total_object_count += 1
                print(total_poly_count, "before")
                total_poly_count += poly_count
                print(total_poly_count, "after")

                if len([o for o in bpy.data.objects if o.data == mesh]) > 1:
                    self.report({'WARNING'}, f"Multiple shapes defined for {obj.name}!")
                    warning_count += 1

            bpy.data.meshes.remove(mesh)

            if 'I3D_static' in obj and obj['I3D_static'] == 1 and not is_placeable:
                print(f"RigidBody: {obj.name} is marked as static!")
                info_count += 1

            clip_distance_conditions = [('I3D_nonRenderable', lambda v: v == 0),
                                        ('I3D_mergeGroup', lambda v: v == 0),
                                        ('I3D_clipDistance', lambda v: v == 0),
                                        ('I3D_boundingVolume', lambda v: v == '')]

            if all(key in obj and condition(obj[key]) for key, condition in clip_distance_conditions):
                print(f"ClipDistance: {obj.name} has no clip distance set. This causes performance issues!")
                info_count += 1

            decal_layer = obj.get('I3D_decalLayer', 0)
            if 'decal' in name_lower and decal_layer == 0:
                print(f"Decal Layer: {obj.name}, has decal layer set to 0")
                info_count += 1
            elif decal_layer > 0 and 'decal' not in name_lower:
                print("Decal Layer: Nodes have to be pre-/postfixed by 'decal' if decalLayer-attribute > 0")
                info_count += 1

            if 'fillvolume' in name_lower:
                if obj.get('I3D_cpuMesh') == 0:
                    print(f"FillVolume: {obj.name} is not marked as CPU-Mesh!")
                    warning_count += 1

            collision = obj.get('I3D_collision', False)
            compound = obj.get('I3D_compound', False)
            trigger = obj.get('I3D_trigger', False)
            if collision is True:
                if compound is True and trigger is False and obj.parent is None:
                    expected_suffix = "_main_component1" if component_number == 1 else f"_component{component_number}"
                    if not obj.name.endswith(expected_suffix):
                        print(f"Component: Object {obj.name} is marked as compound, "
                              f"but name convention is wrong. Should be {expected_suffix}")
                        warning_count += 1
                    component_number += 1

                if obj.scale != Vector((1, 1, 1)):
                    print(f"Scale: collision {obj.name} is not scaled 1 1 1, apply scale.")
                    warning_count += 1

            if 'effect' in name_lower:
                if not obj.data.color_attributes:
                    print(f"EffectMesh: {obj.name}, is a effect but doesn't have a Vertex Color layer")
                    warning_count += 1
                if not len(obj.data.uv_layers) == 2:
                    print(f"EffectMesh: {obj.name}, is a effect but doesn't have 2 UV layers")
                    warning_count += 1

            if has_armature and obj.modifiers and obj.modifiers[0].type != "ARMATURE":
                print(f"Armature modifier: Object {obj.name} has armature modifier, but it's not first modifier in the list.")
                warning_count += 1

        if total_poly_count > MAX_POLY_COUNT:
            print(f"Poly count: {total_poly_count} is very high. This cause performance issues. Try to reduce it")
            error_count += 1

        if total_object_count > MAX_OBJECT_COUNT:
            print(f"Object count: {total_object_count} mesh objects is very high This cause performance issues. "
                  "consider merging some objects")
            error_count += 1

        print("Errors:", error_count)
        print("Warnings:", warning_count)
        print("Info:", info_count)
        print("Poly count:", total_poly_count)
        print("Object count:", total_object_count)
        self.report({'INFO'}, f'Errors: {error_count}, Warnings: {warning_count}, Info: {info_count} '
                    '(check console for details))')
        return {'FINISHED'}


def get_children(parent_obj):
    children = []
    to_visit = [bpy.data.objects[parent_obj]]

    while to_visit:
        curr_ob = to_visit.pop()
        children.extend(curr_ob.children)
        to_visit.extend(curr_ob.children)

    return children
