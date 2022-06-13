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

from .. import check_i3d_exporter_type

giants_i3d, stjerne_i3d, dcc, I3DRemoveAttributes = check_i3d_exporter_type()


class I3DEA_OT_mirror_material(bpy.types.Operator):
    bl_idname = "i3dea.mirror_material"
    bl_label = "Add Mirror Material"
    bl_description = "Adds mirror_mat to materials"

    def execute(self, context):
        if giants_i3d:
            if context.scene.I3D_UIexportSettings.I3D_shaderFolderLocation == "":
                self.report({'ERROR'}, "Shader Folder location is not set!")
                return {'CANCELLED'}
        material = bpy.data.materials.get("mirror_mat")
        if material:
            self.report({'ERROR'}, "Mirror Material already exists!")
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
                if giants_i3d:
                    bpy.context.object.active_material['customShader'] = "$data\\shaders\\mirrorShader.xml"
                    bpy.context.object.active_material['shadingRate'] = "1x1"
            self.report({'INFO'}, "Created material: mirror_mat")
            return {'FINISHED'}

            # FIXME: i3d exporter currently doesn't export the mirror material correctly to i3d.


class I3DEA_OT_remove_duplicate_material(bpy.types.Operator):
    bl_idname = "i3dea.remove_duplicate_material"
    bl_label = "Remove Duplicate Materials"
    bl_description = "Removes all duplicated/not assigned materials"

    def execute(self, context):
        bpy.ops.object.mode_set(mode='OBJECT')
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


class I3DEA_OT_setup_material(bpy.types.Operator):
    bl_idname = "i3dea.setup_material"
    bl_label = "Make Material"
    bl_description = "Set up a material with all the material nodes correctly connected"

    def execute(self, context):
        mat_name = bpy.context.scene.i3dea.material_name
        mat = bpy.data.materials.get(mat_name)
        if not mat:
            mat = bpy.data.materials.new(name=mat_name)
            mat.use_nodes = True
            nodes = mat.node_tree.nodes
            links = mat.node_tree.links
            principled = nodes.get("Principled BSDF")
            normal = nodes.new("ShaderNodeNormalMap")
            img_tex_normal = nodes.new("ShaderNodeTexImage")
            img_tex_spec = nodes.new("ShaderNodeTexImage")
            normal.location = (-210, -250)
            img_tex_normal.location = (-510, -250)
            links.new(normal.outputs["Normal"], principled.inputs["Normal"])
            links.new(img_tex_normal.outputs["Color"], normal.inputs["Color"])
            img_tex_spec.location = (-510, 80)
            if giants_i3d:
                links.new(img_tex_spec.outputs["Color"], principled.inputs["Specular"])
            if stjerne_i3d:
                sep_rgb = nodes.new("ShaderNodeSeparateRGB")
                sep_rgb.location = (-210, 90)
                links.new(img_tex_spec.outputs["Color"], sep_rgb.inputs["Image"])
            if bpy.context.scene.i3dea.diffuse_box:
                img_tex_diffuse = nodes.new("ShaderNodeTexImage")
                img_tex_diffuse.location = (-510, 310)
                links.new(img_tex_diffuse.outputs["Color"], principled.inputs["Base Color"])
            self.report({'INFO'}, mat_name + " created")

        for obj in bpy.context.selected_objects:
            if not obj.type == "MESH":
                continue
            obj.active_material_index = 0
            for i in range(len(obj.material_slots)):
                bpy.ops.object.material_slot_remove({'object': obj})
            obj.data.materials.append(mat)

        if len(bpy.context.selectable_objects) > 0:
            self.report({'INFO'}, mat_name + " applied to selected objects")

        return {'FINISHED'}


class I3DEA_OT_i3dio_material(bpy.types.Operator):
    bl_idname = "i3dea.i3dio_material"
    bl_label = "Add material settings (stjerne addon)"
    bl_description = "Setup material setting for multiple materials at once"

    def execute(self, context):
        for obj in bpy.context.selected_objects:
            for slot in obj.material_slots:
                if context.scene.i3dea.shader_path == "":
                    self.report({'ERROR'}, "You have not entered shader file path")
                    return {'CANCELLED'}
                if slot.material:
                    loc = context.scene.i3dea.shader_path
                    slot.material.i3d_attributes.source = loc
                    return {'FINISHED'}

                    # name = context.scene.i3dea.skeletons_dropdown
                    # getattr(I3DEA_OT_skeletons, name)(self)
                    # self.report({'INFO'}, name + " skeleton added")


def register():
    bpy.types.Material.custom_shader = bpy.props.StringProperty(
        name='customShader',
    )


def unregister():
    del bpy.types.Material.custom_shader
