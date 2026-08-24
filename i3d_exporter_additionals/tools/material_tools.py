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
from bpy_extras.node_utils import connect_sockets

from ..helper_functions import check_i3d_exporter_type, get_addon_preferences

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
        if i3dio_enabled and get_addon_preferences("i3dio").fs_data_path == "":
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

    @staticmethod
    def load_image(image_path: str) -> bpy.types.Image | None:
        if not image_path:
            return None
        try:
            image_name = bpy.path.display_name_from_filepath(image_path)
            print(f"Loading image: {image_path} as {image_name}")
            if image := bpy.data.images.get(image_name):
                return image
            return bpy.data.images.load(image_path)
        except Exception as e:
            print(f"Failed to load image {image_path}: {e}")
            return None

    @staticmethod
    def apply_material_to_selected(context: bpy.types.Context, mat: bpy.types.Material) -> int:
        applied_count = 0
        for obj in context.selected_objects:
            if obj.type == "MESH":
                if mat.name not in obj.data.materials:
                    obj.data.materials.append(mat)
                applied_count += 1
        return applied_count

    def execute(self, context):
        i3dea = context.scene.i3dea
        created = False
        if not (mat := bpy.data.materials.get(i3dea.material_name)):
            mat = bpy.data.materials.new(name=i3dea.material_name)
            created = True

        if created:
            wrapper = PrincipledBSDFWrapper(mat, is_readonly=False)
            tex = wrapper.base_color_texture
            if img := self.load_image(i3dea.diffuse_texture_path):
                tex.image = img
            if i3dea.alpha_box:
                node_img = tex.node_image
                node_bsdf = wrapper.node_principled_bsdf
                if node_img is not None and node_bsdf is not None:
                    connect_sockets(node_img.outputs["Alpha"], node_bsdf.inputs["Alpha"])

            normal_tex = wrapper.normalmap_texture
            if img := self.load_image(i3dea.normal_texture_path):
                normal_tex.image = img

            spec_tex = wrapper.specular_texture
            if img := self.load_image(i3dea.spec_texture_path):
                spec_tex.image = img

        applied_count = self.apply_material_to_selected(context, mat)
        if applied_count > 0:
            if created:
                self.report({"INFO"}, f"{i3dea.material_name} created and applied to selected objects")
            else:
                self.report({"INFO"}, f"{i3dea.material_name} applied to selected objects")
        else:
            if created:
                self.report({"INFO"}, f"{i3dea.material_name} created (no mesh objects selected)")
            else:
                self.report({"INFO"}, f"{i3dea.material_name} already existed (no mesh objects selected)")

        return {"FINISHED"}


class I3DEA_OT_enable_all_material_slotnames(bpy.types.Operator):
    bl_idname = "i3dea.enable_all_material_slotnames"
    bl_label = "Enable All Material Slot Names"
    bl_description = (
        "Enables 'Material Slot Name' on every material in the blend file.\n"
        "Materials that already have it enabled keep their existing custom name.\n"
        "Materials that get newly enabled are left blank "
        "(the material's own name will be used on export)"
    )
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context) -> bool:
        return check_i3d_exporter_type()[1]  # Only makes sense with the Community (i3dio) exporter

    def execute(self, context: bpy.types.Context):
        newly_enabled = 0
        already_enabled = 0

        for mat in bpy.data.materials:
            if mat.i3d_attributes.use_material_slot_name:
                already_enabled += 1
                continue
            mat.i3d_attributes.use_material_slot_name = True
            newly_enabled += 1

        self.report(
            {"INFO"},
            f"Enabled Material Slot Name on {newly_enabled} material(s) "
            f"({already_enabled} already had it enabled).",
        )
        return {"FINISHED"}


def convert_roughness_to_specular_ior() -> int:
    """For every material's Principled BSDF node(s), moves whatever is plugged into the 'Roughness'
    input over to the 'Specular IOR Level' input instead (e.g. to reuse a roughness/gloss mask texture
    as the specular input). Materials with nothing linked to Roughness are left untouched.

    Returns the number of materials that were changed.
    """
    converted_count = 0
    for mat in bpy.data.materials:
        if not mat.use_nodes or not mat.node_tree:
            continue
        links = mat.node_tree.links
        material_changed = False

        for node in mat.node_tree.nodes:
            if node.type != "BSDF_PRINCIPLED":
                continue
            roughness_input = node.inputs.get("Roughness")
            specular_ior_input = node.inputs.get("Specular IOR Level")
            if not roughness_input or not specular_ior_input or not roughness_input.is_linked:
                continue

            # Move every link currently feeding Roughness over to Specular IOR Level instead
            for link in list(roughness_input.links):
                from_socket = link.from_socket
                links.remove(link)
                links.new(from_socket, specular_ior_input)
            material_changed = True

        if material_changed:
            converted_count += 1

    return converted_count


class I3DEA_OT_convert_roughness_to_specular_ior(bpy.types.Operator):
    bl_idname = "i3dea.convert_roughness_to_specular_ior"
    bl_label = "Roughness -> Specular IOR"
    bl_description = (
        "For every material's Principled BSDF node, moves whatever is currently plugged into 'Roughness' "
        "over to 'Specular IOR Level' instead (e.g. to reuse a roughness/gloss mask texture as the specular input).\n"
        "Only materials with something linked to Roughness are affected"
    )
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context: bpy.types.Context):
        converted_count = convert_roughness_to_specular_ior()
        self.report({"INFO"}, f"Converted Roughness -> Specular IOR Level on {converted_count} material(s).")
        return {"FINISHED"}


classes = (
    I3DEA_OT_mirror_material,
    I3DEA_OT_setup_material,
    I3DEA_OT_enable_all_material_slotnames,
    I3DEA_OT_convert_roughness_to_specular_ior,
)
register, unregister = bpy.utils.register_classes_factory(classes)
