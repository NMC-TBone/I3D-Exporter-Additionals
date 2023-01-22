import bpy

from bpy.types import Panel, UIList
from .helper_functions import Singleton

singleton_instance = Singleton.get_instance()


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
    bl_category = 'GIANTS I3D Exporter NEW'


class I3DEA_PT_MainPanel(I3deaPanel, Panel):
    bl_idname = 'I3DEA_PT_MainPanel'
    bl_label = 'I3D Exporter Additionals'

    def draw(self, context):
        layout = self.layout
        if singleton_instance.giants_i3d and singleton_instance.stjerne_i3d:
            # "Exporter selection" box
            layout.label(text="Both Giants & Stjerne I3D exporter is enabled", icon='ERROR')
            layout.label(text="Recommend to disable one of them as it can cause some issues")


class I3DEA_PT_GeneralTools(I3deaPanel, Panel):
    bl_idname = 'I3DEA_PT_GeneralTools'
    bl_label = 'General Tools'
    bl_parent_id = 'I3DEA_PT_MainPanel'

    def draw(self, context):
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
        row.operator("i3dea.fill_volume", text="Check Fill Volume")
        if singleton_instance.giants_i3d:
            row = col.row(align=True)
            row.operator("i3dea.xml_config", text="Enable export to i3dMappings")
            row.operator("i3dea.ignore", text="Add Suffix _ignore")
            row = col.row(align=True)
            row.operator("i3dea.verify_scene", text="Verify Scene")


class I3DEA_PT_UserAttributes(I3deaPanel, Panel):
    bl_idname = 'I3DEA_PT_UserAttributes'
    bl_label = 'User Attributes'
    bl_parent_id = 'I3DEA_PT_MainPanel'

    @classmethod
    def poll(cls, context):
        return singleton_instance.giants_i3d

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
