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


class I3DEA_OT_verify_scene(bpy.types.Operator):
    bl_idname = "i3dea.verify_scene"
    bl_label = "Verify Scene"
    bl_description = "Check the whole scene if there is something that may be wrong"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        error_count = 0
        warning_count = 0
        info_count = 0

        dg = bpy.context.evaluated_depsgraph_get()
        for obj in bpy.data.objects:
            if obj.type == 'MESH':
                obj = obj.evaluated_get(dg)
                mesh = obj.to_mesh()
                poly_count = len(mesh.polygons)

                if poly_count > 0 and hasattr(obj, 'I3D_nonRenderable') == 0 and hasattr(obj, 'I3D_mergeGroup') == 0:
                    print("Multiple shapes defined!")

            if obj.type == 'MESH' and hasattr(obj, 'I3D_static') == 1:
                print("RigidBody: {} is marked as static!".format(obj.name))
                info_count += 1

            if obj.type == 'MESH' and hasattr(obj, 'I3D_nonRenderable') == 0 and hasattr(obj, 'I3D_mergeGroup') == 0 and hasattr(obj, 'I3D_boundingVolume') == '' and hasattr(obj, 'I3D_clipDistance') == 0:
                print("ClipDistance: {} has no clip distance set. This causes performance issues!".format(obj.name))
                info_count += 1

            if obj.type == 'MESH':
                decal_layer = hasattr(obj, 'I3D_decalLayer')
                if decal_layer == 0 and ("decal" in obj.name.lower() != -1):
                    print("DecalLayer: {}, has decal layer set to 0".format(obj.name))
                    info_count += 1
                elif decal_layer != 0 and ("decal" in obj.name.lower() == -1):
                    print("DecalLayer: Nodes have to be pre-/postfixed by 'decal' if decalLayer-attribute > 0")
                    info_count += 1

                if 'fillvolume' in obj.name.lower() != -1:
                    if hasattr(obj, 'I3D_cpuMesh') == 0:
                        print("FillVolume is not marked as CPU-Mesh!")
                        warning_count += 1



        print("Errors:", error_count)
        print("Warnings:", warning_count)
        print("Info:", info_count)




        pass
        return {'FINISHED'}
