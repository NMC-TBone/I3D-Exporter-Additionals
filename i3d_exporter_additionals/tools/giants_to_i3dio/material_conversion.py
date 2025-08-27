from pathlib import Path
import bpy
from .logging_config import logger
from .mappings import OLD_TO_NEW_PARAMETERS, OLD_TO_NEW_CUSTOM_TEXTURES


class MaterialMigrationContext:
    def __init__(self):
        self.found_legacy_vehicle_shader = False
        self.migrated_count = 0
        self.skipped_count = 0
        self.material_props_updated = 0

    def mark_legacy_vehicle(self):
        self.found_legacy_vehicle_shader = True

    def summary(self):
        return (f"Materials migrated: {self.migrated_count}, "
                f"Legacy vehicleShader: {'yes' if self.found_legacy_vehicle_shader else 'no'}")


def migrate_materials() -> MaterialMigrationContext:
    ctx = MaterialMigrationContext()
    for mat in bpy.data.materials:
        if migrate_material_shader(mat, ctx):
            ctx.migrated_count += 1
        if migrate_giants_material_properties(mat):
            ctx.material_props_updated += 1
    return ctx


def migrate_giants_material_properties(mat: bpy.types.Material) -> bool:
    changed = False

    # shadingRate: string -> enum
    if "shadingRate" in mat:
        mat.i3d_attributes.shading_rate = mat["shadingRate"]
        del mat["shadingRate"]
        changed = True

    # materialSlotName: string, must also set use_material_slot_name if present
    if "materialSlotName" in mat and mat["materialSlotName"]:
        mat.i3d_attributes.material_slot_name = mat["materialSlotName"]
        mat.i3d_attributes.use_material_slot_name = True
        del mat["materialSlotName"]
        changed = True

    # surface_render_method: BLENDED -> True, else False
    if hasattr(mat, "surface_render_method"):
        mat.i3d_attributes.alpha_blending = (mat.surface_render_method == "BLENDED")
        changed = True

    return changed


def _is_giants_legacy_vehicle_shader(path_str: str) -> bool:
    return any(v in path_str for v in ("19", "22")) and "vehicleShader" in path_str


def migrate_material_shader(mat: bpy.types.Material, ctx: MaterialMigrationContext) -> bool:
    if not (shader_path := mat.get("customShader")):
        ctx.skipped_count += 1
        logger.debug(f"{mat.name}: No customShader found; skipped.")
        return False
    shader_stem = Path(shader_path).stem
    # Giants legacy FS19/22 vehicleShader: special handling
    if _is_giants_legacy_vehicle_shader(shader_path):
        if convert_giants_legacy_vehicle_shader_to_i3dio(mat, shader_stem):
            ctx.mark_legacy_vehicle()
            logger.info(f"Converted {mat.name!r} (Giants FS19/22 vehicleShader) to legacy format.")
            return True
        else:
            ctx.skipped_count += 1
            logger.warning(f"{mat.name}: vehicleShader detected but migration failed/skipped")
            return False

    # All other shaders: direct/sloppy migration
    if migrate_giants_standard_shader(mat, shader_stem):
        logger.info(f"Converted {mat.name!r} to standard shader format ({shader_stem}).")
        return True
    else:
        ctx.skipped_count += 1
        logger.warning(f"{mat.name}: standard shader migration failed/skipped.")
        return False


def convert_giants_legacy_vehicle_shader_to_i3dio(mat: bpy.types.Material, shader_name: str) -> bool:
    """
    Converts Giants FS19/22 exporter vehicleShader material keys to legacy i3dio format keys on mat.i3d_attributes.
    This is done for the udim_to_mat_template operator in i3dio addon do the actual conversion for vehicleShader.
    Returns True if shimed, False otherwise.
    """
    i3da = mat.i3d_attributes
    i3da["source"] = shader_name
    i3da["temp_old_variation_name"] = mat.get("customShaderVariation", "")

    # Collect all customParameter_* keys
    shader_parameters = []
    for k in mat.keys():
        if not k.startswith("customParameter_"):
            continue
        pname = k.replace("customParameter_", "")
        string_value = mat[k]

        # Giants store all parameters as space-separated strings: "1.0 0.5 0.0 1.0"
        vals = [float(v) for v in string_value.split()]
        # All their parameters are usually stored with 4 values, even if the parameter is something else.
        # So just to make it easy for ourselves, clip everything to 4 values.
        vals = (vals + [0.0] * 4)[:4]
        shader_parameters.append({'name': pname, 'data_float_4': vals})
    i3da["shader_parameters"] = shader_parameters

    # Collect all customTexture_* keys
    shader_textures = []
    for k in mat.keys():
        if not k.startswith("customTexture_"):
            continue
        tname = k.replace("customTexture_", "")
        texture_value = mat[k]
        shader_textures.append({'name': tname, 'source': texture_value})
    i3da["shader_textures"] = shader_textures

    _remove_giants_legacy_mat_keys(mat)
    logger.info(f"[Adapter] {mat.name}: Wrote {len(shader_parameters)} shader params, "
                f"{len(shader_textures)} textures for legacy operator.")
    return True


def migrate_giants_standard_shader(mat: bpy.types.Material, shader_name: str) -> bool:
    """Converts all Giants shaders to i3dio format. This includes FS25 vehicleShader and any other game shaders."""
    i3da = mat.i3d_attributes

    i3da.shader_name = ""  # Just a safety to make it update
    i3da.shader_name = shader_name  # The property will not set the shader name if it doesn't exist.

    if mat.get("customShaderVariation", "") not in i3da.shader_variations:
        return False
    i3da.shader_variation_name = mat.get("customShaderVariation", "")

    # Assign all customParameter_* keys to i3dio shader material parameters
    parameter_collection = i3da.shader_material_parameters
    for k in mat.keys():
        if not k.startswith("customParameter_"):
            continue
        pname: str = k.replace("customParameter_", "")
        if (new_pname := OLD_TO_NEW_PARAMETERS.get(pname, pname)) not in parameter_collection:
            continue
        string_value: str = mat[k]
        # Giants store all parameters as space-separated strings: "1.0 0.5 0.0 1.0"
        vals = [float(v) for v in string_value.split()]
        # All their parameters are usually stored with 4 values, even if the parameter is something else.
        # So we will have to slice it to match the "target" i3dio parameter property length.
        try:
            target_param = parameter_collection[new_pname]
            expected_length = len(target_param)
            sliced_vals = (vals + [0.0] * expected_length)[:expected_length]
            parameter_collection[new_pname] = sliced_vals
        except (TypeError, ValueError, KeyError) as e:
            logger.warning(f"{mat.name}: Error setting parameter {new_pname!r} with value {vals!r}: {e}")

    # Assign all customTexture_* keys to i3dio shader material textures
    texture_collection = i3da.shader_material_textures
    for k in mat.keys():
        if not k.startswith("customTexture_"):
            continue
        tname: str = k.replace("customTexture_", "")
        new_tname = OLD_TO_NEW_CUSTOM_TEXTURES.get(tname, tname)
        target_tex_slot = next((t for t in texture_collection if t.name == new_tname), None)
        if target_tex_slot:
            texture_value: str = mat[k]
            if texture_value and texture_value != target_tex_slot.default_source:
                # Only update if the texture value is not the default source
                target_tex_slot.source = texture_value

    _remove_giants_legacy_mat_keys(mat)


def _remove_giants_legacy_mat_keys(mat: bpy.types.Material) -> None:
    """
    Removes all Giants legacy material keys from the material.
    This is a cleanup function to ensure no old keys remain after migration.
    """
    for k in list(mat.keys()):
        if k.startswith("customParameter_") or k.startswith("customTexture_") \
                or k in {"customShader", "customShaderVariation"}:
            del mat[k]
    logger.debug(f"{mat.name}: Removed Giants legacy keys.")
