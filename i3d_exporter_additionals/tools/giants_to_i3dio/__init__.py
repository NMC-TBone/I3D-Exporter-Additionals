
import bpy

from .operator import (
    I3DEA_OT_disable_giants_exporter,
    I3DEA_OT_migrate_giants_to_i3dio,
)

from .auto_import import (
    register_auto_import_detection,
    unregister_auto_import_detection,
)


classes = (
    I3DEA_OT_migrate_giants_to_i3dio,
    I3DEA_OT_disable_giants_exporter,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    try:
        register_auto_import_detection()
    except Exception:
        for cls in reversed(classes):
            bpy.utils.unregister_class(cls)
        raise


def unregister():
    unregister_auto_import_detection()

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
