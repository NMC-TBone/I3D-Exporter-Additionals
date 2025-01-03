import bpy
from bpy.types import (
    Panel,
    UIList
)
from .helper_functions import check_i3d_exporter_type, is_blend_saved


class I3DEA_UL_pose_curves(UIList):
    def draw_item(self, _context, layout, data, item, icon, active_data, active_propname, index):
        curve_ob = item.curve
        curve_icon = 'OUTLINER_OB_CURVE'
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            layout.prop(curve_ob, "name", text="", emboss=False, icon=curve_icon)
        elif self.layout_type == 'GRID':
            layout.alignment = 'CENTER'
            layout.label(text="", icon_value=icon)


class I3DEA_PT_MainPanel(Panel):
    bl_idname = 'I3DEA_PT_MainPanel'
    bl_label = 'I3D Exporter Additionals'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'I3D Exporter Additionals'

    def draw(self, context):
        giants_i3d, stjerne_i3d = check_i3d_exporter_type()
        layout = self.layout
        if giants_i3d and stjerne_i3d:
            # "Exporter selection" box
            layout.label(text="Both Giants & Stjerne I3D exporter is enabled", icon='ERROR')
            layout.label(text="Recommend to disable one of them as it can cause unexpected issues")

        draw_general_tools(layout, context, giants_i3d, stjerne_i3d)
        if giants_i3d:
            draw_user_attributes(layout, context)
        draw_skeletons(layout, context)
        draw_material_tools(layout, context)
        draw_asset_importer(layout, context)
        draw_track_tools(layout, context)
        draw_motion_path(layout, context)


def draw_general_tools(layout: bpy.types.UILayout, context: bpy.types.Context,
                       giants_i3d: bool, stjerne_i3d: bool) -> None:
    header, panel = layout.panel("I3DEA_general_tools", default_closed=True)
    header.label(text="General Tools")
    if panel:
        col = panel.column(align=True)
        row = col.row(align=True)
        row.operator("i3dea.copy_transform", text="Copy Location").state = 1
        row.operator("i3dea.copy_transform", text="Copy Rotation").state = 2
        row = col.row(align=True)
        row.operator("i3dea.mirror_orientation", text="Set mirror orientation")
        row.operator("i3dea.remove_doubles", text="Clean Meshes")
        row = col.row(align=True)
        row.operator("i3dea.mesh_name", text="Set Mesh Name")
        # row.operator("i3dea.fill_volume", text="Check Fill Volume") hidden for now
        if giants_i3d:
            row = col.row(align=True)
            row.operator("i3dea.xml_config", text="Enable export to i3dMappings")
            row.operator("i3dea.ignore", text="Add Suffix _ignore")
            row = col.row(align=True)
            row.operator("i3dea.verify_scene", text="Verify Scene")
            row.operator("i3dea.convert_skinnedmesh", text="Convert SkinnedMesh")

            prop_converter_header, prop_converter_panel = layout.panel("I3DEA_prop_converter", default_closed=True)
            prop_converter_header.label(text="Misc")
            if prop_converter_panel:
                def _get_toggle_icon(state: bool) -> str:
                    return 'CHECKBOX_HLT' if state else 'CHECKBOX_DEHLT'
                i3dea = context.scene.i3dea
                col = prop_converter_panel.column(align=True)
                col.label(text="Convert Settings:")
                row = col.row(align=True)
                row.prop(i3dea, "convert_user_attr", text="User Attributes", toggle=True,
                         icon=_get_toggle_icon(i3dea.convert_user_attr))
                row = col.row(align=True)
                row.prop(i3dea, "convert_lights", text="Lights", toggle=True,
                         icon=_get_toggle_icon(i3dea.convert_lights))
                row = col.row(align=True)
                row.prop(i3dea, "convert_materials", text="Materials", toggle=True,
                         icon=_get_toggle_icon(i3dea.convert_materials))
                if i3dea.convert_materials:
                    row = col.row(align=True)
                    row.prop(i3dea, "convert_nodes", text="Nodes", toggle=True,
                             icon=_get_toggle_icon(i3dea.convert_nodes))
                row = col.row(align=True)
                delete_row = col.row(align=True)
                if stjerne_i3d:
                    delete_row.enabled = False
                    row.label(text="Disabled when Stjerne I3D Exporter is enabled", icon='ERROR')
                    i3dea.property_unset('delete_old_props')
                delete_row.prop(i3dea, "delete_old_props", text="Delete Old Props", toggle=True,
                                icon=_get_toggle_icon(i3dea.delete_old_props))
                row = col.row(align=True)
                row.operator("i3dea.properties_converter", text="Convert Properties", icon='FILE_REFRESH')


def draw_user_attributes(layout: bpy.types.UILayout, context: bpy.types.Context) -> None:
    header, panel = layout.panel("I3DEA_user_attributes", default_closed=True)
    header.label(text="User Attributes")
    if panel:
        col = panel.column(align=True)
        row = col.row(align=True)
        if obj := context.active_object:
            row.label(text=f"Object Name: {obj.name}")
            row = col.row()
            attributes = [k for k in obj.keys() if 0 == k.find("userAttribute_")]
            if attributes:
                col2 = row.column()
                box2 = col2.box()
                row2 = box2.row()
                row2.label(text="Attributes:")
                row2 = box2.row()
                for k in attributes:
                    m_list = k.split("_", 2)
                    name = m_list[2]
                    row2.prop(obj, f'["{k}"]', text=name)
                    row2.operator("i3dea.delete_user_attribute", text="", icon='X').attribute_name = k
                    row2 = box2.row()
                row = col.row()
            row.label(text="Add new attributes:")
            row = col.row()
            row.prop(context.scene.i3dea, "user_attribute_name", text="Name")
            row = col.row()
            row.prop(context.scene.i3dea, "user_attribute_type", text="Type")
            row = col.row()
            row.operator("i3dea.create_user_attribute", text="Add")
        else:
            row.label(text="Object Name: None")


def draw_skeletons(layout: bpy.types.UILayout, context: bpy.types.Context) -> None:
    header, panel = layout.panel("I3DEA_skeletons", default_closed=True)
    header.label(text="Skeletons")
    if panel:
        col = panel.column(align=True)
        row = col.row(align=True)
        row.prop(context.scene.i3dea, "skeletons_dropdown", text="")
        row.operator("i3dea.skeletons", text="Create", icon='BONE_DATA')


def draw_material_tools(layout: bpy.types.UILayout, context: bpy.types.Context) -> None:
    header, panel = layout.panel("I3DEA_material_tools", default_closed=True)
    header.label(text="Material Tools")
    if panel:
        i3dea = context.scene.i3dea
        box = panel.box()
        col = box.column(align=True)
        col.label(text="Material operators")
        row = col.row(align=True)
        row.operator("i3dea.mirror_material", text="Add Mirror Material")
        row.operator("i3dea.remove_unused_material_slots")

        box = panel.box()
        col = box.column(align=True)
        col.label(text="Create a material")
        row = col.row(align=True)
        row.prop(i3dea, "diffuse_box", text="Diffuse")
        if i3dea.diffuse_box:
            row.prop(i3dea, "alpha_box", text="Alpha")
        col.prop(i3dea, "material_name", text="Material Name")
        if i3dea.diffuse_box:
            col.prop(i3dea, "diffuse_texture_path", text="Diffuse Texture")
        col.prop(i3dea, "spec_texture_path", text="Specular Texture")
        col.prop(i3dea, "normal_texture_path", text="Normal Texture")
        col.operator("i3dea.setup_material", text=f"Create {i3dea.material_name}")


def draw_asset_importer(layout: bpy.types.UILayout, context: bpy.types.Context) -> None:
    header, panel = layout.panel("I3DEA_asset_importer", default_closed=True)
    header.label(text="Asset Importer")
    if panel:
        row = panel.row(align=True)
        row.prop(context.scene.i3dea, "assets_dropdown", text="")
        row.operator("i3dea.assets", text="Import Asset")


def draw_track_tools(layout: bpy.types.UILayout, context: bpy.types.Context) -> None:
    i3dea = context.scene.i3dea
    header, panel = layout.panel("I3DEA_track_tools", default_closed=True)
    header.label(text="Track Tools")
    if panel:
        col = panel.column(align=True)
        row = col.row(align=True)
        row.prop(i3dea, "track_mode", expand=True)

        if i3dea.track_mode == 'MANUAL':
            box = panel.box()
            box_col = box.column(align=True)
            box_col.label(text="Create Second UV")
            box_row = box_col.row(align=True)

            box_row.prop(i3dea, "size_dropdown", text="")
            box_row.operator("i3dea.make_uvset", text="Create UVset 2", icon="UV")

            box = panel.box()
            box_col = box.column(align=True)
            box_col.label(text="Add empties between selected objects")
            box_row = box_col.row(align=True)

            box_row.prop(i3dea, "add_empty_int", text="")
            box_row.operator("i3dea.add_empty", text="Add", icon='EMPTY_DATA')

            box = panel.box()
            box_col = box.column(align=True)
            box_col.label(text="Get length of selected curve")
            box_row = box_col.row(align=True)

            box_row.prop(i3dea, "curve_length_disp", text="")
            box_row.operator("i3dea.curve_length", text="Get Curve Length", icon='MOD_LENGTH')

            box = panel.box()
            box_col = box.column(align=True)
            box_col.label(text="Calculate the distance between 2 track pieces")
            box_row = box_col.row(align=True)

            box_row.prop(i3dea, "piece_distance", text="")
            box_row.operator("i3dea.calculate_amount", text="Calculate Amount")
            box_row = box_col.row(align=True)
            box_row.prop(i3dea, "track_piece_amount", text="")

        elif i3dea.track_mode == 'AUTOMATIC':
            header, panel = layout.panel("I3DEA_create_uv_set", default_closed=True)
            header.prop(i3dea, "auto_use_uvset", text="Create UV set")
            if panel:
                panel.use_property_split = True
                panel.use_property_decorate = False
                panel.active = i3dea.auto_use_uvset
                panel.prop(i3dea, "auto_uvset_dropdown", text="2nd uv size")
                panel.prop(i3dea, "auto_add_vmask")

            header, panel = layout.panel("I3DEA_fixed_amount", default_closed=True)
            header.prop(i3dea, "auto_fixed_amount", text="Fixed Amount")
            if panel:
                panel.use_property_split = True
                panel.use_property_decorate = False
                panel.active = i3dea.auto_fixed_amount
                panel.prop(i3dea, "auto_fxd_amount_int")

            header, panel = layout.panel("I3DEA_add_empties", default_closed=True)
            header.prop(i3dea, "auto_add_empties", text="Add Empties")
            if panel:
                panel.use_property_split = True
                panel.use_property_decorate = False
                panel.active = i3dea.auto_add_empties
                panel.prop(i3dea, "auto_empty_int")

            header, panel = layout.panel("I3DEA_create_auto_track", default_closed=True)
            header.label(text="Manage and Create")
            if panel:
                panel.use_property_split = True
                panel.use_property_decorate = False
                panel.prop(i3dea, "selected_curve")
                if i3dea.selected_curve and not i3dea.auto_fixed_amount:
                    panel.prop(i3dea, "auto_allow_curve_scale")
                panel.prop(i3dea, "auto_create_bbox")
                panel.prop(i3dea, "auto_name")
                if not i3dea.auto_fixed_amount:
                    panel.prop(i3dea, "auto_distance")
                panel.operator("i3dea.automatic_track_creation", text="Create")

        header, panel = layout.panel("I3DEA_track_visualization", default_closed=True)
        header.label(text="Track Visualization")
        if panel:
            col = panel.column(align=True)
            row = col.row(align=True)
            row.prop(i3dea, "track_type_method", expand=True)

            panel.use_property_split = True
            panel.use_property_decorate = False
            if i3dea.track_type_method == 'CATERPILLAR':
                col = panel.column(heading="Track Settings", align=True)
                col.prop(i3dea, "track_vis_amount")
                col.prop(i3dea, "track_vis_distance")
            row = panel.row(align=True)
            row.operator("i3dea.visualization", text="Track Visualization")
            row.operator("i3dea.visualization_del", text="Delete")


def draw_motion_path(layout: bpy.types.UILayout, context: bpy.types.Context) -> None:
    i3dea = context.scene.i3dea
    header, panel = layout.panel("I3DEA_motion_path", default_closed=True)
    header.label(text="Motion Path From Curves")
    if panel:
        col = panel.column(align=True)
        row = col.row(align=True)
        row.template_list("I3DEA_UL_PoseList", "", i3dea, "pose_list", i3dea, "pose_count", rows=1)
        col = row.column(align=True)
        col.operator("i3dea.add_pose", text="", icon='ADD')
        col.operator("i3dea.remove_pose", text="", icon='REMOVE')

        if pose_list := i3dea.pose_list:
            header, panel = layout.panel("I3DEA_sub_pose_list", default_closed=False)
            header.label(text="Sub Pose List")
            if panel:
                selected_pose = pose_list[i3dea.pose_count]
                panel.label(text=f"{pose_list[i3dea.pose_count].name}")
                row = panel.row()
                row.template_list("I3DEA_UL_SubPoseCurveList", "", selected_pose, "sub_pose_list", selected_pose,
                                  "sub_pose_count", rows=1)
                row = panel.row(align=True)
                row.operator("i3dea.add_curve", text="Add Curves", icon='ADD')
                row.operator("i3dea.remove_curve", text="Remove All", icon='CANCEL').remove_all = True
                row.operator("i3dea.remove_curve", text="Remove", icon='REMOVE').remove_all = False

                box = panel.box()
                box.enabled = bool(selected_pose.sub_pose_list)
                box_col = box.column(align=True)
                box_col.label(text="Settings for array creation")
                box_row = box_col.row(align=True)

                box_row.prop(i3dea, "motion_type", expand=True)
                box_row = box_col.row(align=True)
                box_row_uniform = box_row.row(align=True)
                box_row_uniform.enabled = i3dea.motion_type == 'UNIFORM'
                box_row_uniform.prop(i3dea, "motion_uniform")
                box_row_adaptive = box_row.row(align=True)
                box_row_adaptive.enabled = i3dea.motion_type == 'ADAPTIVE'
                box_row_adaptive.prop(i3dea, "motion_adaptive")
                box_row_distance = box_row.row(align=True)
                box_row_distance.enabled = i3dea.motion_type == 'DISTANCE'
                box_row_distance.prop(i3dea, "motion_distance")
                box_row = box_col.row()
                box_row.label(text="")
                box_row = box_col.row(align=True)
                box_row.prop(i3dea, "motion_hierarchy_name")
                box_row = box_col.row(align=True)
                if not is_blend_saved():
                    box_row.label(text="Save blend file to enable save location", icon='ERROR')
                box_row = box_col.row(align=True)
                box_row.enabled = is_blend_saved()
                box_row.prop(i3dea, "motion_save_location")
                box_row = box_col.row(align=True)
                box_row.operator("i3dea.add_empties_curves", text="Create")


class I3DEA_UL_PoseList(UIList):
    def draw_item(self, _context, layout, data, item, icon, active_data, active_propname, index):
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            layout.label(text=item.name)
        elif self.layout_type == 'GRID':
            layout.alignment = 'CENTER'
            layout.label(text=item.name)


class I3DEA_UL_SubPoseCurveList(UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        curve_ob = item.curve
        curve_icon = 'OUTLINER_OB_CURVE'
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            layout.label(text=str(curve_ob), translate=False, icon=curve_icon)
        elif self.layout_type == 'GRID':
            layout.alignment = 'CENTER'
            layout.label(text="", icon_value=icon)


classes = (
    I3DEA_PT_MainPanel,
    I3DEA_UL_pose_curves,
    I3DEA_UL_PoseList,
    I3DEA_UL_SubPoseCurveList,
)

register, unregister = bpy.utils.register_classes_factory(classes)
