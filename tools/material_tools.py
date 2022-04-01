"""material_tools.py includes different material tools"""

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

import bpy

class TOOLS_OT_mirrorMaterial(bpy.types.Operator):
    bl_idname = "tools.mirror_material"
    bl_label = "Add Mirror Material"
    bl_description = "Adds mirror_mat to materials"

    def execute(self, context):
        if context.scene.I3D_UIexportSettings.I3D_shaderFolderLocation == "":
            self.report({'ERROR'}, "Shader Folder location is not set!")
            return {'CANCELLED'}
        material = bpy.data.materials.get("mirror_mat")
        if material:
            self.report({'ERROR'}, "Mirror Material already created!")
            return {'CANCELLED'}
        if not bpy.context.active_object.type == "MESH":
            self.report({'ERROR'}, "Selected Object is not a mesh!")
            return {'CANCELLED'}
        else:
            material = bpy.data.materials.new(name="mirror_mat")
            material.use_nodes = True
            principled_node = material.node_tree.nodes.get('Principled BSDF')
            principled_node.inputs[0].default_value = (0.0001, 0.0001, 0.0001, 1)
            principled_node.inputs[6].default_value = 1
            principled_node.inputs[7].default_value = 1
            principled_node.inputs[9].default_value = 1
            mirror_mat = bpy.data.materials.get('mirror_mat')

            for obj in bpy.context.selected_objects:
                obj.active_material_index = 0
                for i in range(len(obj.material_slots)):
                    bpy.ops.object.material_slot_remove({'object': obj})
                obj.data.materials.append(mirror_mat)
                bpy.context.object.active_material['customShader'] = "$data\\shaders\\mirrorShader.xml"
                bpy.context.object.active_material['shadingRate'] = "1x1"
            self.report({'INFO'}, "Created material: mirror_mat")
            return {'FINISHED'}

            # TODO: fix issue when export mirror_mat it's missing <Reflectionmap type="planar" refractiveIndex="10" bumpScale="0.1"/> in the .i3d

class TOOLS_OT_removeDuplicateMaterial(bpy.types.Operator):
    bl_idname = "tools.remove_duplicate_material"
    bl_label = "Remove Duplicate Materials"
    bl_description = "Removes all duplicated/not assigned materials"

    def execute(self, context):
        for ob in bpy.context.scene.objects:
            if not ob.material_slots:
                continue
            bpy.ops.object.material_slot_remove_unused({"object": context.scene.objects[0]})
        for mat in bpy.data.materials:
            if not mat.users:
                bpy.data.materials.remove(mat)
        bpy.ops.outliner.orphans_purge()
        self.report({'INFO'}, "Unused material slots & Orphan Data removed")
        return {'FINISHED'}

def register():
    bpy.types.Material.custom_shader = bpy.props.StringProperty(
        name='customShader',
        )

def unregister():
    del bpy.types.Material.custom_shader