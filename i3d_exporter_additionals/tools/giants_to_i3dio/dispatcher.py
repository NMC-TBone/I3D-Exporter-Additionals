from .object_conversion import migrate_objects
from .material_conversion import migrate_materials
from .logging_config import logger


def migrate_all():
    logger.info("Starting Giants -> i3dio migration...")
    migrate_objects()
    mat_ctx = migrate_materials()
    if mat_ctx.found_legacy_vehicle_shader:
        import bpy
        bpy.ops.i3dio.udim_to_mat_template('EXEC_DEFAULT')  # EXEC_DEFAULT to run without opening the warning dialog
        logger.info("Ran UDIM to material template conversion to handle legacy vehicle shaders.")
    else:
        logger.info("No legacy vehicle shaders found, skipping UDIM to material template conversion.")
