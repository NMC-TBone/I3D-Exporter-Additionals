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


"""
TODO:
    - See if it's possible to do more with fill volume checker
    - Make it possible to scale the curve to get an rounded value for the track amount
"""


import bpy
from mathutils import Vector

class I3DEA_OT_verify_scene(bpy.types.Operator):
    bl_idname = "i3dea.verify_scene"
    bl_label = "Verify Scene"
    bl_description = "Check the whole scene if there is something that may be wrong"

    def execute(self, context):
        is_placeable = False
        has_armature = False
        error_count = 0
        warning_count = 0
        info_count = 0
        poly_count = 0

        for obj in bpy.data.objects:
            if "placeable" in obj.name.lower():
                is_placeable = True
            for mat in obj.material_slots:
                if 'customShader' in mat.material:
                    if "placeableShader" or "buildingShader" in mat.material['customShader']:
                        is_placeable = True

        dg = bpy.context.evaluated_depsgraph_get()

        print("--------------------")
        print("VERIFY SCENE RESULTS")
        print("--------------------")

        for obj in bpy.data.objects:
            if obj.name.lower().endswith("_ignore"):
                children_objs = get_children(obj.name)
                if children_objs:
                    for _ in children_objs:
                        continue

            if obj.type != 'MESH':
                continue
            objs = obj.evaluated_get(dg)
            mesh = objs.to_mesh()
            poly_count += len(mesh.polygons)

            # if poly_count > 0 and ('I3D_nonRenderable' and 'I3D_mergeGroup' in obj) and (obj['I3D_nonRenderable'] and obj['I3D_mergeGroup'] == 0):
            #     print("Multiple shapes defined!")

            if 'I3D_static' in obj and obj['I3D_static'] == 1 and not is_placeable:
                print(f"RigidBody: {obj.name} is marked as static!")
                info_count += 1

            if 'I3D_nonRenderable' and 'I3D_mergeGroup' and 'I3D_clipDistance' and 'I3D_boundingVolume' in obj and obj['I3D_nonRenderable'] == 0 and obj['I3D_mergeGroup'] == 0 and obj['I3D_clipDistance'] == 0 and obj['I3D_boundingVolume'] == '':
                print(f"ClipDistance: {obj.name} has no clip distance set. This causes performance issues!")
                info_count += 1

            if 'decal' in obj.name.lower() and 'I3D_decalLayer' in obj and obj['I3D_decalLayer'] == 0:
                print(f"DecalLayer: {obj.name}, has decal layer set to 0")
                info_count += 1

            if ("decal" in obj.name.lower() == -1) and 'I3D_decalLayer' in obj and obj['I3D_decalLayer'] != 0:
                print("DecalLayer: Nodes have to be pre-/postfixed by 'decal' if decalLayer-attribute > 0")
                info_count += 1

            if 'fillvolume' in obj.name.lower() != -1:
                if 'I3D_cpuMesh' in obj and obj['I3D_cpuMesh'] == 0:
                    print(f"FillVolume {obj.name} is not marked as CPU-Mesh!")
                    warning_count += 1

            if 'I3D_collision' in obj and obj['I3D_collision'] == 1:
                if 'I3D_compound' in obj and obj['I3D_compound'] == 1 and 'I3D_trigger' in obj and obj['I3D_trigger'] == 0:
                    if obj.parent is None:
                        if "_main_component" not in obj.name:
                            print(f"Component: Object {obj.name} is marked as compound, but name convention is wrong. Should be x_main_component")
                            warning_count += 1

                if obj.scale != Vector((1, 1, 1)):
                    print(f"Scale: collision {obj.name} is not scaled 1 1 1, apply scale.")
                    warning_count += 1

            if 'effect' in obj.name.lower():
                if not obj.data.color_attributes:
                    print(f"EffectMesh: {obj.name}, is a effect but doesn't have a Vertex Color layer")
                    warning_count += 1
                if not len(obj.data.uv_layers) == 2:
                    print(f"EffectMesh: {obj.name}, is a effect but doesn't have 2 UV layers")
                    warning_count += 1

            for mo in obj.modifiers:
                if mo.type == "ARMATURE":
                    has_armature = True

            if has_armature and obj.modifiers and obj.modifiers[0].type != "ARMATURE":
                print("Armature modifier: Object {} has armature modifier, but it's not first modifier in the list.")
                warning_count += 1

        print("Errors:", error_count)
        print("Warnings:", warning_count)
        print("Info:", info_count)
        # print("Poly count:", poly_count)
        return {'FINISHED'}


def get_children(parent_obj):
    parent = bpy.data.objects[parent_obj]
    children = []
    for obj in parent.children:
        children.append(obj.name)
    return children


