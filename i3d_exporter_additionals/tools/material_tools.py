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

# material_tools.py includes different material tools

import bpy

from ..helper_functions import check_i3d_exporter_type

giants_i3d, stjerne_i3d = check_i3d_exporter_type()


class I3DEA_OT_mirror_material(bpy.types.Operator):
    bl_idname = "i3dea.mirror_material"
    bl_label = "Add Mirror Material"
    bl_description = "Adds mirror_mat to materials"
    bl_options = {'REGISTER', 'UNDO'}

    def create_mirror_material(self):
        material = bpy.data.materials.new(name="mirror_mat")
        material.use_nodes = True
        principled_node = material.node_tree.nodes.get('Principled BSDF')
        principled_node.inputs["Base Color"].default_value = (0.000001, 0.000001, 0.000001, 1)
        principled_node.inputs["Metallic"].default_value = 1
        if bpy.app.version >= (4, 0, 0):
            principled_node.inputs["Specular IOR Level"].default_value = 1
        else:
            principled_node.inputs["Specular"].default_value = 1
        principled_node.inputs["Roughness"].default_value = 1
        return material

    def execute(self, context):
        if stjerne_i3d:
            if context.preferences.addons['i3dio'].preferences.fs_data_path == "":
                self.report({'ERROR'}, "FS Data Folder is not set!")
                return {'CANCELLED'}

        if bpy.data.materials.get("mirror_mat"):
            self.report({'ERROR'}, "Mirror Material already exists!")
            return {'CANCELLED'}

        if not context.object.type == "MESH":
            self.report({'ERROR'}, "Selected Object is not a mesh!")
            return {'CANCELLED'}

        mirror_mat = self.create_mirror_material()

        for obj in context.selected_objects:
            obj.data.materials.clear()
            obj.data.materials.append(mirror_mat)

            if giants_i3d:
                obj.active_material['customShader'] = "$data\\shaders\\mirrorShader.xml"
                obj.active_material['shadingRate'] = "1x1"
            if stjerne_i3d:
                data_folder = context.preferences.addons['i3dio'].preferences.fs_data_path
                obj.active_material.i3d_attributes.source = f"{data_folder}shaders\\mirrorShader.xml"

        self.report({'INFO'}, "Created material: mirror_mat")
        return {'FINISHED'}


class I3DEA_OT_remove_duplicate_material(bpy.types.Operator):
    bl_idname = "i3dea.remove_duplicate_material"
    bl_label = "Remove Duplicate Materials"
    bl_description = "Removes all duplicated/not assigned materials"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.object.mode_set(mode='OBJECT')
        for ob in bpy.context.scene.objects:
            if not ob.material_slots:
                continue
            bpy.ops.object.material_slot_remove_unused()
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
    bl_options = {'REGISTER', 'UNDO'}

    def create_material(self, mat_name):
        mat = bpy.data.materials.get(mat_name)
        if not mat:
            mat = bpy.data.materials.new(name=mat_name)
            mat.use_nodes = True
        return mat

    def load_image_to_node(self, node, image_path, color_space='sRGB'):
        if image_path == "":
            return
        try:
            image_name = image_path.split("\\")[-1]
            existing_img = bpy.data.images.get(image_name)
            if not existing_img:
                node.image = bpy.data.images.load(image_path)
            else:
                node.image = existing_img
            node.image.colorspace_settings.name = color_space
        except Exception as e:
            print(f"Failed to load image {image_path}: {e}")

    def setup_normal_map(self, nodes, links, image_path):
        normal = nodes.new("ShaderNodeNormalMap")
        img_tex_normal = nodes.new("ShaderNodeTexImage")
        normal.location = (-210, -250)
        img_tex_normal.location = (-510, -250)
        links.new(normal.outputs["Normal"], nodes.get("Principled BSDF").inputs["Normal"])
        links.new(img_tex_normal.outputs["Color"], normal.inputs["Color"])
        self.load_image_to_node(img_tex_normal, image_path, 'Non-Color')

    def setup_specular_map(self, nodes, links, image_path):
        img_tex_spec = nodes.new("ShaderNodeTexImage")
        img_tex_spec.location = (-510, 32)
        if giants_i3d:
            if bpy.app.version >= (4, 0, 0):
                links.new(img_tex_spec.outputs["Color"], nodes.get("Principled BSDF").inputs["Specular IOR Level"])
            else:
                links.new(img_tex_spec.outputs["Color"], nodes.get("Principled BSDF").inputs["Specular"])
        elif stjerne_i3d:
            sep_rgb = nodes.new("ShaderNodeSeparateRGB")
            sep_rgb.name = "Glossmap"
            sep_rgb.location = (-210, 90)
            links.new(img_tex_spec.outputs["Color"], sep_rgb.inputs["Image"])
        self.load_image_to_node(img_tex_spec, image_path, 'Non-Color')

    def setup_diffuse_map(self, nodes, links, image_path, use_alpha):
        img_tex_diffuse = nodes.new("ShaderNodeTexImage")
        img_tex_diffuse.location = (-510, 310)
        links.new(img_tex_diffuse.outputs["Color"], nodes.get("Principled BSDF").inputs["Base Color"])
        if use_alpha:
            links.new(img_tex_diffuse.outputs["Alpha"], nodes.get("Principled BSDF").inputs["Alpha"])
        self.load_image_to_node(img_tex_diffuse, image_path)

    def apply_material_to_selected(self, context, mat):
        applied_count = 0
        for obj in context.selected_objects:
            if obj.type == "MESH":
                obj.data.materials.clear()
                obj.data.materials.append(mat)
                applied_count += 1
        return applied_count

    def execute(self, context):
        i3dea = context.scene.i3dea
        mat = self.create_material(i3dea.material_name)
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links

        self.setup_normal_map(nodes, links, i3dea.normal_texture_path)
        self.setup_specular_map(nodes, links, i3dea.spec_texture_path)

        if i3dea.diffuse_box:
            self.setup_diffuse_map(nodes, links, i3dea.diffuse_texture_path, i3dea.alpha_box)

        applied_amount = self.apply_material_to_selected(context, mat)

        if applied_amount > 0:
            self.report({'INFO'}, f"{i3dea.material_name} applied to selected objects")
        else:
            self.report({'INFO'}, f"{i3dea.material_name} created")

        return {'FINISHED'}


class I3DEA_OT_i3dio_material(bpy.types.Operator):
    bl_idname = "i3dea.i3dio_material"
    bl_label = "Add material settings (stjerne addon)"
    bl_description = "Setup material setting for multiple materials at once"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        selected_list = []

        for obj in bpy.context.selected_objects:
            if obj.type == "MESH":
                selected_list.append(obj)

        for loop_obj in selected_list:
            bpy.context.view_layer.objects.active = loop_obj
            loop_obj.select_set(state=True, view_layer=None)

            for num in range(0, len(loop_obj.material_slots)):
                loop_obj.active_material_index = num
                material = loop_obj.active_material
                shader_loc = context.scene.i3dea.shader_path

                if bpy.context.scene.i3dea.shader_box:
                    if shader_loc:
                        material.i3d_attributes.source = shader_loc

                if not material.i3d_attributes.source:
                    self.report({'ERROR'}, f"Something went wrong with this obj/mat: {loop_obj.name} | "
                                           f"{loop_obj.active_material.name}")
                    continue
                else:
                    if bpy.context.scene.i3dea.mask_map_box:
                        mask = context.scene.i3dea.mask_map
                        if mask:
                            material.i3d_attributes.shader_textures[0].source = mask
                    if bpy.context.scene.i3dea.dirt_diffuse_box:
                        dirt = context.scene.i3dea.dirt_diffuse
                        if dirt:
                            material.i3d_attributes.shader_textures[1].source = dirt

        return {'FINISHED'}
