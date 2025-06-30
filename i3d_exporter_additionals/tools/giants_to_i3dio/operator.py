import bpy
from .dispatcher import migrate_all
from ...helper_functions import check_i3d_exporter_type


class I3DEA_OT_migrate_giants_to_i3dio(bpy.types.Operator):
    bl_idname = "i3dea.migrate_giants_to_i3dio"
    bl_label = "Migrate from Giants to Community Exporter"
    bl_description = "Convert all Giants exporter properties and materials to the i3dio community exporter format"
    bl_options = {'INTERNAL', 'UNDO'}

    @classmethod
    def poll(cls, _context):
        _, i3dio_enabled = check_i3d_exporter_type()
        return i3dio_enabled

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width=475)

    def draw(self, _context):
        col = self.layout.column()
        col.label(text="Migration Warning", icon='ERROR')
        col.label(text="This operation will convert all Giants exporter properties and materials to the i3dio format.")
        col.separator()
        col.label(text="• After migration, your file may no longer work with the Giants exporter.")
        col.label(text="• Some settings or properties might be changed, lost, or not fully supported.")
        col.label(text="• You can undo this operation (Ctrl+Z).")
        col.label(text="However, for full safety, make a backup before migrating!", icon='INFO')
        col.label(text="• Especially if you intend to keep using the Giants exporter or might want to revert.")

    def execute(self, _context):
        migrate_all()
        self.report({'INFO'}, "Migration complete! Check console/log for details.")
        return {'FINISHED'}


class I3DEA_OT_disable_giants_exporter(bpy.types.Operator):
    bl_idname = "i3dea.disable_giants_exporter"
    bl_label = "Disable Giants I3D Exporter"
    bl_description = "Disable Giants I3D Exporter addon"
    bl_options = {'INTERNAL', 'UNDO'}

    def execute(self, context):
        import addon_utils
        giants_modules = ["io_export_i3d", "io_export_i3d_10_0_0"]
        for module in giants_modules:
            if addon_utils.check(module)[1]:
                addon_utils.disable(module, default_set=True)
                self.report({'INFO'}, f"{module} disabled.")
            else:
                self.report({'WARNING'}, f"{module} is not enabled.")
        self.report({'INFO'}, "Giants I3D Exporter disabled.")
        return {'FINISHED'}
