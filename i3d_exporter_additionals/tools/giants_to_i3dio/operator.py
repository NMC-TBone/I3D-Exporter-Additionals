import bpy

from ...helper_functions import check_i3d_exporter_type, get_enabled_addons_by_prefix
from .dispatcher import migrate_all


class I3DEA_OT_migrate_giants_to_i3dio(bpy.types.Operator):
    bl_idname = "i3dea.migrate_giants_to_i3dio"
    bl_label = "Migrate from Giants to Community Exporter"
    bl_description = "Convert all Giants exporter properties and materials to the i3dio community exporter format"
    bl_options = {"INTERNAL", "UNDO"}

    preserve_old_properties: bpy.props.BoolProperty(
        name="Keep Giants Exporter Properties",
        description="Keep Giants exporter custom properties after copying them to the Community Exporter",
        default=False,
    )

    migrate_visibility: bpy.props.BoolProperty(
        name="Preserve Giants Visibility",
        description=(
            "Copy the current Outliner eye state to the Community Exporter's fixed Visibility property; "
            "dynamic compound collision roots remain visible"
        ),
        default=True,
    )

    convert_roughness_mask: bpy.props.BoolProperty(
        name="Convert Roughness Mask to Specular IOR",
        description=(
            "For every material's Principled BSDF node, move whatever is plugged into 'Roughness' "
            "over to 'Specular IOR Level' instead"
        ),
        default=True,
    )

    @classmethod
    def poll(cls, _context):
        _, i3dio_enabled = check_i3d_exporter_type()
        return i3dio_enabled

    def invoke(self, context, event):
        self.convert_roughness_mask = context.scene.i3dea.auto_convert_roughness_on_migration
        return context.window_manager.invoke_props_dialog(self, width=475)

    def draw(self, _context):
        col = self.layout.column()
        col.label(text="Migration Warning", icon="ERROR")
        col.label(text="This operation will convert all Giants exporter properties and materials to the i3dio format.")
        col.separator()
        col.label(text="• After migration, your file may no longer work with the Giants exporter.")
        col.label(text="• Some settings or properties might be changed, lost, or not fully supported.")
        col.label(text="• You can undo this operation (Ctrl+Z).")
        col.label(text="However, for full safety, make a backup before migrating!", icon="INFO")
        col.label(text="• Especially if you intend to keep using the Giants exporter or might want to revert.")
        col.separator()
        col.prop(self, "preserve_old_properties")
        col.prop(self, "migrate_visibility")
        col.prop(self, "convert_roughness_mask")

    def execute(self, context):
        migrate_all(
            preserve_old_properties=self.preserve_old_properties,
            migrate_visibility=self.migrate_visibility,
            convert_roughness_mask=self.convert_roughness_mask,
        )
        self.report({"INFO"}, "Migration complete! Check console/log for details.")
        return {"FINISHED"}


class I3DEA_OT_disable_giants_exporter(bpy.types.Operator):
    bl_idname = "i3dea.disable_giants_exporter"
    bl_label = "Disable Giants I3D Exporter"
    bl_description = "Disable Giants I3D Exporter addon"
    bl_options = {"INTERNAL", "UNDO"}

    def execute(self, context):
        import addon_utils

        for addon in get_enabled_addons_by_prefix("io_export_i3d"):
            addon_utils.disable(addon.module, default_set=True)
            self.report({"INFO"}, f"{addon.module} disabled.")
        self.report({"INFO"}, "Giants I3D Exporter disabled.")
        return {"FINISHED"}
