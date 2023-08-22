from bpy.types import Panel, UIList
from .helper_functions import check_i3d_exporter_type


class I3DEA_UL_pose_curves(UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        curve_ob = item.curve
        curve_icon = 'OUTLINER_OB_CURVE'
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            layout.prop(curve_ob, "name", text="", emboss=False, icon=curve_icon)
        elif self.layout_type == 'GRID':
            layout.alignment = 'CENTER'
            layout.label(text="", icon_value=icon)


class I3deaPanel:
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'I3D Exporter Additionals'


class I3deaTrackSetupAuto(I3deaPanel):
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        i3dea = context.scene.i3dea
        return i3dea.track_mode == 'AUTOMATIC'


class I3DEA_PT_MainPanel(I3deaPanel, Panel):
    bl_idname = 'I3DEA_PT_MainPanel'
    bl_label = 'I3D Exporter Additionals'

    def draw(self, context):
        giants_i3d, stjerne_i3d = check_i3d_exporter_type()
        layout = self.layout
        if giants_i3d and stjerne_i3d:
            # "Exporter selection" box
            layout.label(text="Both Giants & Stjerne I3D exporter is enabled", icon='ERROR')
            layout.label(text="Recommend to disable one of them as it can cause unexpected issues")


class I3DEA_PT_GeneralTools(I3deaPanel, Panel):
    bl_idname = 'I3DEA_PT_GeneralTools'
    bl_label = 'General Tools'
    bl_parent_id = 'I3DEA_PT_MainPanel'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        giants_i3d, stjerne_i3d = check_i3d_exporter_type()
        layout = self.layout
        col = layout.column(align=True)
        row = col.row(align=True)
        row.operator("i3dea.copy_orientation", text="Copy Location").state = 1
        row.operator("i3dea.copy_orientation", text="Copy Rotation").state = 2
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


class I3DEA_PT_PropConverter(I3deaPanel, Panel):
    bl_idname = 'I3DEA_PT_PropConverterSub'
    bl_label = 'Misc'
    bl_parent_id = 'I3DEA_PT_GeneralTools'
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        giants_i3d, stjerne_i3d = check_i3d_exporter_type()
        return giants_i3d

    def draw(self, context):
        giants_i3d, stjerne_i3d = check_i3d_exporter_type()
        i3dea = context.scene.i3dea
        layout = self.layout
        layout.use_property_split = False
        layout.use_property_decorate = False
        col = layout.column(align=True)
        box = col.box()
        box.label(text="Convert Settings")
        subcol = box.column(align=True)
        subcol.prop(i3dea, "convert_user_attr", toggle=True,
                    icon='CHECKBOX_HLT' if i3dea.convert_user_attr else 'CHECKBOX_DEHLT')
        subcol.prop(i3dea, "convert_lights", toggle=True,
                    icon='CHECKBOX_HLT' if i3dea.convert_lights else 'CHECKBOX_DEHLT')
        subcol.prop(i3dea, "convert_materials", toggle=True,
                    icon='CHECKBOX_HLT' if i3dea.convert_materials else 'CHECKBOX_DEHLT')
        if i3dea.convert_materials:
            subcol.prop(i3dea, "convert_nodes", toggle=True,
                        icon='CHECKBOX_HLT' if i3dea.convert_nodes else 'CHECKBOX_DEHLT')
        subcol2 = subcol.column(align=True if giants_i3d and not stjerne_i3d else False)
        if stjerne_i3d:
            subcol2.enabled = False
            subcol2.label(text="Disabled when Stjerne I3D Exporter is enabled", icon='ERROR')
            i3dea.property_unset('delete_old_props')
        subcol2.prop(i3dea, "delete_old_props", toggle=True,
                     icon='CHECKBOX_HLT' if i3dea.delete_old_props else 'CHECKBOX_DEHLT')

        col.operator("i3dea.properties_converter", text="Convert Properties", icon='FILE_REFRESH')


class I3DEA_PT_UserAttributes(I3deaPanel, Panel):
    bl_idname = 'I3DEA_PT_UserAttributes'
    bl_label = 'User Attributes'
    bl_parent_id = 'I3DEA_PT_MainPanel'
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        giants_i3d, stjerne_i3d = check_i3d_exporter_type()
        return giants_i3d

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        row = col.row(align=True)
        obj = context.object
        if obj:
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


class I3DEA_PT_Skeletons(I3deaPanel, Panel):
    bl_idname = 'I3DEA_PT_Skeletons'
    bl_label = 'Skeletons'
    bl_parent_id = 'I3DEA_PT_MainPanel'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        i3dea = context.scene.i3dea
        layout = self.layout

        col = layout.column(align=True)
        row = col.row(align=True)
        row.prop(i3dea, "skeletons_dropdown", text="")
        row.operator("i3dea.skeletons", text="Create", icon='BONE_DATA')


class I3DEA_PT_MaterialTools(I3deaPanel, Panel):
    bl_idname = 'I3DEA_PT_MaterialTools'
    bl_label = 'Material Tools'
    bl_parent_id = 'I3DEA_PT_MainPanel'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        i3dea = context.scene.i3dea
        layout = self.layout

        box = layout.box()
        box_col = box.column(align=True)
        box_col.label(text="Material operators")
        box_col.label(text="Mirror material is currently not possible to export with I3D Exporter")
        box_row = box_col.row(align=True)

        box_row.operator("i3dea.mirror_material", text="Add Mirror Material")
        box_row.operator("i3dea.remove_duplicate_material", text="Remove Duplicate Materials")

        box = layout.box()
        box_col = box.column(align=True)
        box_col.label(text="Create a material")
        box_row = box_col.row(align=True)

        box_row.prop(i3dea, "diffuse_box", text="Diffuse")
        if i3dea.diffuse_box:
            box_row.prop(i3dea, "alpha_box", text="Alpha")
        box_row = box_col.row(align=True)
        box_row.prop(i3dea, "material_name", text="")
        if i3dea.diffuse_box:
            box_row = box_col.row(align=True)
            box_row.prop(i3dea, "diffuse_texture_path", text="Diffuse")
        box_row = box_col.row(align=True)
        box_row.prop(i3dea, "spec_texture_path", text="Specular")
        box_row = box_col.row(align=True)
        box_row.prop(i3dea, "normal_texture_path", text="Normal")
        box_row = box_col.row(align=True)
        box_row.operator("i3dea.setup_material", text="Create " + i3dea.material_name)


class I3DEA_PT_AssetImporter(I3deaPanel, Panel):
    bl_idname = 'I3DEA_PT_AssetImporter'
    bl_label = 'Asset Importer'
    bl_parent_id = 'I3DEA_PT_MainPanel'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        i3dea = context.scene.i3dea
        layout = self.layout

        col = layout.column(align=True)
        row = col.row(align=True)
        row.prop(i3dea, "assets_dropdown", text="")
        row.operator("i3dea.assets", text="Import Asset")


class I3DEA_PT_TrackTools(I3deaPanel, Panel):
    bl_idname = 'I3DEA_PT_TrackTools'
    bl_label = 'Track Tools'
    bl_parent_id = 'I3DEA_PT_MainPanel'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        pass


class I3DEA_PT_TrackSetup(I3deaPanel, Panel):
    bl_idname = 'I3DEA_PT_TrackSetup'
    bl_label = 'Track Setup'
    bl_parent_id = 'I3DEA_PT_TrackTools'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        i3dea = context.scene.i3dea
        layout = self.layout

        col = layout.column(align=True)
        row = col.row(align=True)
        row.prop(i3dea, "track_mode", expand=True)

        if i3dea.track_mode == 'MANUAL':
            box = layout.box()
            box_col = box.column(align=True)
            box_col.label(text="Create Second UV")
            box_row = box_col.row(align=True)

            box_row.prop(i3dea, "size_dropdown", text="")
            box_row.operator("i3dea.make_uvset", text="Create UVset 2", icon="UV")

            box = layout.box()
            box_col = box.column(align=True)
            box_col.label(text="Add empties between selected objects")
            box_row = box_col.row(align=True)

            box_row.prop(i3dea, "add_empty_int", text="")
            box_row.operator("i3dea.add_empty", text="Add", icon='EMPTY_DATA')

            box = layout.box()
            box_col = box.column(align=True)
            box_col.label(text="Get length of selected curve")
            box_row = box_col.row(align=True)

            box_row.prop(i3dea, "curve_length_disp", text="")
            box_row.operator("i3dea.curve_length", text="Get Curve Length", icon='MOD_LENGTH')

            box = layout.box()
            box_col = box.column(align=True)
            box_col.label(text="Calculate the distance between 2 track pieces")
            box_row = box_col.row(align=True)

            box_row.prop(i3dea, "piece_distance", text="")
            box_row.operator("i3dea.calculate_amount", text="Calculate Amount")
            box_row = box_col.row(align=True)
            box_row.prop(i3dea, "track_piece_amount", text="")

            """
            box_row.prop(i3dea, "auto_allow_curve_scale", text="Allow Curve Scale", toggle=True, icon='CHECKBOX_HLT'
            if i3dea.auto_allow_curve_scale else 'CHECKBOX_DEHLT')
            box_row = box_col.row(align=True)
            box_row.prop(i3dea, "auto_empty", text="Add empties", toggle=True, icon='CHECKBOX_HLT' if i3dea.auto_empty
            else 'CHECKBOX_DEHLT')
            if i3dea.auto_empty:
                box_row = box_col.row(align=True)
                box_row.prop(i3dea, "auto_empty_int", text="")"""


class I3DEA_PT_CreateUvSet(I3deaTrackSetupAuto, Panel):
    bl_idname = 'I3DEA_PT_CreateUvSet'
    bl_label = 'Create UV set'
    bl_parent_id = 'I3DEA_PT_TrackSetup'

    def draw_header(self, context):
        i3dea = context.scene.i3dea
        self.layout.prop(i3dea, "auto_use_uvset", text="")

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False

        i3dea = context.scene.i3dea

        col = layout.column()
        col.active = i3dea.auto_use_uvset
        col.prop(i3dea, "auto_uvset_dropdown", text="2nd uv size")
        col.prop(i3dea, "auto_add_vmask")


class I3DEA_PT_CalcAmount(I3deaTrackSetupAuto, Panel):
    bl_idname = 'I3DEA_PT_CalcAmount'
    bl_label = 'Fixed Amount'
    bl_parent_id = 'I3DEA_PT_TrackSetup'

    def draw_header(self, context):
        i3dea = context.scene.i3dea
        self.layout.prop(i3dea, "auto_fixed_amount", text="")

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False

        i3dea = context.scene.i3dea

        col = layout.column()
        col.active = i3dea.auto_fixed_amount
        col.prop(i3dea, "auto_fxd_amount_int")


class I3DEA_PT_AddEmpties(I3deaTrackSetupAuto, Panel):
    bl_idname = 'I3DEA_PT_AddEmpties'
    bl_label = 'Add Empties'
    bl_parent_id = 'I3DEA_PT_TrackSetup'

    def draw_header(self, context):
        i3dea = context.scene.i3dea
        self.layout.prop(i3dea, "auto_add_empties", text="")

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False

        i3dea = context.scene.i3dea

        col = layout.column()
        col.active = i3dea.auto_add_empties
        col.prop(i3dea, "auto_empty_int")


class I3DEA_PT_CreateAutoTrack(I3deaPanel, Panel):
    bl_idname = 'I3DEA_PT_CreateAutoTrack'
    bl_label = 'Manage and Create'
    bl_parent_id = 'I3DEA_PT_TrackSetup'

    @classmethod
    def poll(cls, context):
        i3dea = context.scene.i3dea
        return i3dea.track_mode == 'AUTOMATIC'

    def draw(self, context):
        layout = self.layout

        layout.use_property_split = True
        layout.use_property_decorate = False

        i3dea = context.scene.i3dea

        col = layout.column()
        col.prop(i3dea, "auto_all_curves")
        if i3dea.auto_all_curves != "None" and not i3dea.auto_fixed_amount:
            col.prop(i3dea, "auto_allow_curve_scale")
        else:
            i3dea.property_unset("auto_allow_curve_scale")
        col.prop(i3dea, "auto_create_bbox")
        col.prop(i3dea, "auto_name")
        if not i3dea.auto_fixed_amount:
            col.prop(i3dea, "auto_distance")
        col.operator("i3dea.automatic_track_creation", text="Create")


class I3DEA_PT_TrackVisualization(I3deaPanel, Panel):
    bl_idname = 'I3DEA_PT_TrackVisualization'
    bl_label = 'Track Visualization'
    bl_parent_id = 'I3DEA_PT_TrackTools'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        row = col.row(align=True)
        row.prop(context.scene.i3dea, "track_type_method", expand=True)

        layout.use_property_split = True
        layout.use_property_decorate = False
        if context.scene.i3dea.track_type_method == 'CATERPILLAR':
            col = layout.column(heading="Track Settings", align=True)
            col.prop(context.scene.i3dea, "track_vis_amount")
            col.prop(context.scene.i3dea, "track_vis_distance")
        row = layout.row(align=True)
        row.operator("i3dea.visualization", text="Track Visualization")
        row.operator("i3dea.visualization_del", text="Delete")


class I3DEA_UL_PoseList(UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
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


class I3DEA_PT_ArrayHierarchy(I3deaPanel, Panel):
    bl_idname = 'I3DEA_PT_ArrayHierarchy'
    bl_label = 'Motion Path From Curves'
    bl_parent_id = 'I3DEA_PT_MainPanel'
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        i3dea = context.scene.i3dea
        layout = self.layout

        col = layout.column(align=True)
        row = col.row(align=True)
        row.template_list("I3DEA_UL_PoseList", "", i3dea, "pose_list", i3dea, "pose_count", rows=1)
        col = row.column(align=True)
        col.operator("i3dea.add_pose", text="", icon='ADD')
        col.operator("i3dea.remove_pose", text="", icon='REMOVE')


class I3DEA_PT_SubArrayHierarchy(I3deaPanel, Panel):
    bl_label = "Sub Pose List"
    bl_parent_id = "I3DEA_PT_ArrayHierarchy"

    @classmethod
    def poll(cls, context):
        return context.scene.i3dea.pose_list

    def draw(self, context):
        i3dea = context.scene.i3dea
        layout = self.layout
        pose_list = context.scene.i3dea.pose_list
        if pose_list:
            selected_pose = pose_list[context.scene.i3dea.pose_count]
            layout.label(text=str(pose_list[context.scene.i3dea.pose_count].name))
            row = layout.row()
            row.template_list("I3DEA_UL_SubPoseCurveList", "", selected_pose, "sub_pose_list",
                              selected_pose, "sub_pose_count", rows=1)
            row = layout.row(align=True)
            row.operator("i3dea.add_curve", text="Add Curves", icon='ADD')
            row.operator("i3dea.remove_curve", text="Remove All", icon='CANCEL').remove_all = True
            row.operator("i3dea.remove_curve", text="Remove", icon='REMOVE').remove_all = False

            box = layout.box()
            box_col = box.column(align=True)
            box_col.label(text="Settings for array creation")
            box_row = box_col.row(align=True)

            box_row.prop(i3dea, "motion_type", expand=True)
            box_row = box_col.row(align=True)
            box_row.prop(i3dea, "motion_amount_rel")
            box_row.prop(i3dea, "motion_amount_fix")
            box_row.prop(i3dea, "motion_distance")
            box_row = box_col.row()
            box_row.label(text="")
            box_row = box_col.row(align=True)
            box_row.prop(i3dea, "motion_hierarchy_name")
            box_row = box_col.row(align=True)
            box_row.prop(i3dea, "motion_save_location")
            box_row = box_col.row(align=True)
            box_row.operator("i3dea.add_empties_curves", text="Create")
