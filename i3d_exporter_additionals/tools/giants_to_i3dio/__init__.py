import bpy

from .operator import I3DEA_OT_disable_giants_exporter, I3DEA_OT_migrate_giants_to_i3dio

classes = (I3DEA_OT_migrate_giants_to_i3dio, I3DEA_OT_disable_giants_exporter)

register, unregister = bpy.utils.register_classes_factory(classes)
