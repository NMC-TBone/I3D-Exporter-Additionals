from .logging_config import logger
from .material_conversion import clean_giants_material_properties, migrate_materials
from .object_conversion import clean_giants_object_properties, migrate_objects


def migrate_all(*, preserve_old_properties: bool = False, migrate_visibility: bool = True) -> None:
    logger.info("Starting Giants -> i3dio migration...")
    migrate_objects(migrate_visibility=migrate_visibility)
    mat_ctx = migrate_materials()

    if preserve_old_properties:
        logger.info("Preserving Giants exporter properties.")
    else:
        clean_giants_object_properties()
        clean_giants_material_properties()

    if mat_ctx.found_legacy_vehicle_shader:
        import bpy

        bpy.ops.i3dio.udim_to_mat_template("EXEC_DEFAULT")  # EXEC_DEFAULT to run without opening the warning dialog
        logger.info("Ran UDIM to material template conversion to handle legacy vehicle shaders.")
    else:
        logger.info("No legacy vehicle shaders found, skipping UDIM to material template conversion.")
