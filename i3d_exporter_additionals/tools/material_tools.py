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
from bpy_extras.node_shader_utils import PrincipledBSDFWrapper

from ..helper_functions import check_i3d_exporter_type, get_i3dio_preferences

giants_enabled, i3dio_enabled = check_i3d_exporter_type()


class I3DEA_OT_mirror_material(bpy.types.Operator):
    bl_idname = "i3dea.mirror_material"
    bl_label = "Add Mirror Material"
    bl_description = "Adds mirror_mat to materials and assigns it to selected objects"
    bl_options = {"REGISTER", "UNDO"}

    assign_to_selected: bpy.props.BoolProperty(
        name="Assign to selected",
        description="Assign the mirror material to selected objects",
        default=True,
    )

    @staticmethod
    def set_exporter_metadata(mat: bpy.types.Material) -> None:
        if giants_enabled:
            mat["customShader"] = "$data\\shaders\\mirrorShader.xml"
            mat["shadingRate"] = "1x1"
        if i3dio_enabled:
            mat.i3d_attributes.shader_name = "mirrorShader"

    @staticmethod
    def get_or_create_mirror_material() -> bpy.types.Material:
        if mat := bpy.data.materials.get("mirror_mat"):
            return mat
        mat = bpy.data.materials.new(name="mirror_mat")
        wrapper = PrincipledBSDFWrapper(mat, is_readonly=False)
        wrapper.base_color = (0.0, 0.0, 0.0)
        wrapper.metallic = 1.0
        wrapper.specular = 1.0
        wrapper.roughness = 1.0
        return mat

    def execute(self, context: bpy.types.Context):
        if i3dio_enabled and get_i3dio_preferences().fs_data_path == "":
            self.report({"ERROR"}, "FS Data Folder is not set!")
            return {"CANCELLED"}

        mirror_mat = self.get_or_create_mirror_material()
        self.set_exporter_metadata(mirror_mat)

        selected_objs = context.selected_objects
        if not self.assign_to_selected or not selected_objs:
            self.report({"INFO"}, "Skipped assignment due to no selected objects.")
            return {"FINISHED"}

        assigned_count = 0

        for obj in selected_objs:
            if obj.type != "MESH" or any(m is mirror_mat for m in obj.data.materials):
                continue
            obj.data.materials.clear()
            obj.data.materials.append(mirror_mat)
            assigned_count += 1

        self.report({"INFO"}, f"Added mirror_mat and assigned to {assigned_count} objects.")
        return {"FINISHED"}


class I3DEA_OT_setup_material(bpy.types.Operator):
    bl_idname = "i3dea.setup_material"
    bl_label = "Make Material"
    bl_description = "Set up a material with all the material nodes correctly connected"
    bl_options = {"REGISTER", "UNDO"}

    def create_material(self, mat_name):
        mat = bpy.data.materials.get(mat_name)
        if not mat:
            mat = bpy.data.materials.new(name=mat_name)
            mat.use_nodes = True
        return mat

    def load_image_to_node(self, node, image_path, color_space="sRGB"):
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
        self.load_image_to_node(img_tex_normal, image_path, "Non-Color")

    def setup_specular_map(self, nodes, links, image_path):
        img_tex_spec = nodes.new("ShaderNodeTexImage")
        img_tex_spec.location = (-510, 32)
        if giants_enabled:
            links.new(img_tex_spec.outputs["Color"], nodes.get("Principled BSDF").inputs["Specular IOR Level"])
        elif i3dio_enabled:
            sep_rgb = nodes.new("ShaderNodeSeparateRGB")
            sep_rgb.name = "Glossmap"
            sep_rgb.location = (-210, 90)
            links.new(img_tex_spec.outputs["Color"], sep_rgb.inputs["Image"])
        self.load_image_to_node(img_tex_spec, image_path, "Non-Color")

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
            self.report({"INFO"}, f"{i3dea.material_name} applied to selected objects")
        else:
            self.report({"INFO"}, f"{i3dea.material_name} created")

        return {"FINISHED"}


classes = (
    I3DEA_OT_mirror_material,
    I3DEA_OT_setup_material,
)
register, unregister = bpy.utils.register_classes_factory(classes)
