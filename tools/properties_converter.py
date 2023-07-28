# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

import bpy


class I3DEA_OT_properties_converter(bpy.types.Operator):
    bl_idname = "i3dea.properties_converter"
    bl_label = "Convert I3D properties.py.py"
    bl_description = "Converts I3D properties.py.py from Stjerne exporter to Giants exporter"
    bl_options = {'REGISTER', 'UNDO'}

    prop_conversion_map = {
        ("I3D_XMLconfigBool"): ("i3d_mapping", "is_mapped"),
        ("I3D_XMLconfigID"): ("i3d_mapping", "mapping_name"),

        ("I3D_static"): ("i3d_attributes", "rigid_body_type", "static"),
        ("I3D_dynamic"): ("i3d_attributes", "rigid_body_type", "dynamic"),
        ("I3D_kinematic"): ("i3d_attributes", "rigid_body_type", "kinematic"),
        ("I3D_compound"): ("i3d_attributes", "rigid_body_type", "compound"),
        ("I3D_compoundChild"): ("i3d_attributes", "rigid_body_type", "compound_child"),
        ("I3D_collision"): ("i3d_attributes", "collision"),
        ("I3D_collisionMask"): ("i3d_attributes", "collision_mask"),
        # ("I3D_solverIterationCount"): ("i3d_attributes", "collision_mask"),
        ("I3D_restitution"): ("i3d_attributes", "restitution"),
        ("I3D_staticFriction"): ("i3d_attributes", "static_friction"),
        ("I3D_dynamicFriction"): ("i3d_attributes", "dynamic_friction"),
        ("I3D_linearDamping"): ("i3d_attributes", "linear_damping"),
        ("I3D_angularDamping"): ("i3d_attributes", "angular_damping"),
        ("I3D_density"): ("i3d_attributes", "density"),

        # ("I3D_ccd"): ("i3d_attributes", "collision_mask"),
        ("I3D_trigger"): ("i3d_attributes", "trigger"),
        ("I3D_splitType"): ("i3d_attributes", "split_type"),
        ("I3D_splitMinU"): ("i3d_attributes", "split_uvs"),
        ("I3D_splitMinV"): ("i3d_attributes", "split_uvs"),
        ("I3D_splitMaxU"): ("i3d_attributes", "split_uvs"),
        ("I3D_splitMaxV"): ("i3d_attributes", "split_uvs"),
        ("I3D_splitUvWorldScale"): ("i3d_attributes", "split_uvs"),
        # ("I3D_joint"): ("i3d_attributes", "collision_mask"),
        # ("I3D_projection"): ("i3d_attributes", "collision_mask"),
        # ("I3D_projDistance"): ("i3d_attributes", "collision_mask"),
        # ("I3D_projAngle"): ("i3d_attributes", "collision_mask"),
        # ("I3D_xAxisDrive"): ("i3d_attributes", "collision_mask"),
        # ("I3D_yAxisDrive"): ("i3d_attributes", "collision_mask"),
        # ("I3D_zAxisDrive"): ("i3d_attributes", "collision_mask"),
        # ("I3D_drivePos"): ("i3d_attributes", "collision_mask"),
        # ("I3D_driveForceLimit"): ("i3d_attributes", "collision_mask"),
        # ("I3D_driveSpring"): ("i3d_attributes", "collision_mask"),
        # ("I3D_driveDamping"): ("i3d_attributes", "collision_mask"),
        # ("I3D_breakableJoint"): ("i3d_attributes", "collision_mask"),
        # ("I3D_jointBreakForce"): ("i3d_attributes", "collision_mask"),
        # ("I3D_jointBreakTorque"): ("i3d_attributes", "collision_mask"),
        # ("I3D_visibility"): ("i3d_attributes", "collision_mask"),
        ("I3D_oc"): ("data", "i3d_attributes", "is_occluder"),
        ("I3D_castsShadows"): ("data", "i3d_attributes", "casts_shadows"),
        ("I3D_receiveShadows"): ("data", "i3d_attributes", "receive_shadows"),
        ("I3D_nonRenderable"): ("data", "i3d_attributes", "non_renderable"),
        ("I3D_clipDistance"): ("i3d_attributes", "clip_distance"),
        # ("I3D_objectMask"): ("i3d_attributes", "collision_mask"),
        ("I3D_navMeshMask"): ("data", "i3d_attributes", "nav_mesh_mask"),
        ("I3D_decalLayer"): ("data", "i3d_attributes", "decal_layer"),
        ("I3D_mergeGroup"): ("i3d_merge_group", "group_id"),
        ("I3D_mergeGroupRoot"): ("i3d_merge_group", "is_root"),
        # ("I3D_boundingVolume"): ("data", "i3d_attributes", "bounding_volume_object"),
        ("I3D_cpuMesh"): ("data", "i3d_attributes", "cpu_mesh"),
        # ("I3D_mergeChildren"): ("i3d_attributes", "collision_mask"),
        # ("I3D_mergeChildrenFreezeRotation"): ("i3d_attributes", "collision_mask"),
        # ("I3D_mergeChildrenFreezeTranslation"): ("i3d_attributes", "collision_mask"),
        # ("I3D_mergeChildrenFreezeScale"): ("i3d_attributes", "collision_mask"),
        # ("I3D_objectDataFilePath"): ("i3d_attributes", "collision_mask"),

        ("I3D_lod"): ("i3d_attributes", "lod_distance"),
        ("I3D_lod1"): ("i3d_attributes", "lod_distance"),
        ("I3D_lod2"): ("i3d_attributes", "lod_distance"),
        ("I3D_lod3"): ("i3d_attributes", "lod_distance"),

        # ("I3D_alphaBlending"): ("i3d_attributes", "collision_mask"),

        ("I3D_minuteOfDayStart"): ("i3d_attributes", "minute_of_day_start"),
        ("I3D_minuteOfDayEnd"): ("i3d_attributes", "minute_of_day_end"),
        ("I3D_dayOfYearStart"): ("i3d_attributes", "day_of_year_start"),
        ("I3D_dayOfYearEnd"): ("i3d_attributes", "day_of_year_end"),
        ("I3D_weatherMask"): ("i3d_attributes", "weather_required_mask"),
        # ("I3D_viewerSpacialityMask"): ("i3d_attributes", "collision_mask"),
        ("I3D_weatherPreventMask"): ("i3d_attributes", "weather_prevent_mask"),
        # ("I3D_viewerSpacialityPreventMask"): ("i3d_attributes", "collision_mask"),
        # ("I3D_renderInvisible"): ("i3d_attributes", "collision_mask"),
        # ("I3D_visibleShaderParam"): ("i3d_attributes", "collision_mask"),
        # ("I3D_forceVisibilityCondition"): ("i3d_attributes", "collision_mask"),

        # Export settings
        # ("I3D_UIexportSettings", "I3D_exportApplyModifiers"): ("i3d_attributes", "collision_mask"),
        # ("I3D_UIexportSettings", "I3D_exportLights"): ("i3d_attributes", "collision_mask"),
        # ("I3D_UIexportSettings", "I3D_exportShapes"): ("i3d_attributes", "collision_mask"),
        # ("I3D_UIexportSettings", "I3D_exportMergeGroups"): ("i3d_attributes", "collision_mask"),
        # ("I3D_UIexportSettings", "I3D_exportSkinWeigths"): ("i3d_attributes", "collision_mask"),

    }

    reversed = {v: k for k, v in prop_conversion_map.items()}

    def convert_obj_props(self, context, obj, forward=True, merge_groups=None):
        '''Converts the obj properties from the Stjerne I3D Exporter to the Giants I3D Exporter
        :param context: The context of the scene
        :param obj: The object to convert the properties of
        :param forward: If the conversion should be from Stjerne to Giants or the other way around
        :param merge_groups: The merge groups to convert
        '''
        prop_map = self.prop_conversion_map if forward else self.reversed

        for giants, stjerne in prop_map.items():
            # print(f"{obj}{[stjerne[0]]}{[stjerne[1]]}")
            if stjerne[0] in obj and stjerne[1] in obj[stjerne[0]]:
                if obj[stjerne[0]][stjerne[1]]:
                    # print(obj[giants])
                    # print(f"Top of if: {obj[giants]} -> {obj[stjerne[0]][stjerne[1]]}")

                    # Need to check if rigid_body_type exists to be able to split up the enumprop from stjerne exporter
                    if stjerne[1] == "rigid_body_type":
                        rigid_type = obj[stjerne[0]][stjerne[1]]
                        if rigid_type == 1:
                            obj['I3D_static'] = True
                        elif rigid_type == 2:
                            obj['I3D_dynamic'] = True
                        elif rigid_type == 3:
                            obj['I3D_kinematic'] = True
                        elif rigid_type == 4:
                            obj['I3D_compoundChild'] = True
                        else:
                            # In case the enumprop is none and giants exporter has a set value
                            obj['I3D_static'] = False
                            obj['I3D_dynamic'] = False
                            obj['I3D_kinematic'] = False
                            obj['I3D_compoundChild'] = False

                    # Need to check if split_uvs exists to be able to split up the int array from stjerne exporter
                    elif stjerne[1] == "split_uvs":
                        obj['I3D_splitMinU'] = obj[stjerne[0]][stjerne[1]][0]
                        obj['I3D_splitMinV'] = obj[stjerne[0]][stjerne[1]][1]
                        obj['I3D_splitMaxU'] = obj[stjerne[0]][stjerne[1]][2]
                        obj['I3D_splitMaxV'] = obj[stjerne[0]][stjerne[1]][3]
                        obj['I3D_splitUvWorldScale'] = obj[stjerne[0]][stjerne[1]][4]

                    # Need to check if lod_distance exists to be able to split up the string from stjerne exporter
                    # and store it in the correct way (seperate float) for giants exporter
                    elif stjerne[1] == "lod_distance":
                        if obj[stjerne[0]][stjerne[1]]:
                            obj['I3D_lod'] = True
                            splitted = obj[stjerne[0]][stjerne[1]].split()

                            # loop to set the correct lod distance from stjerne exporter to giants exporter
                            # Max 4 lod distances allowed in giants exporter (lod0 should be 0)
                            for i, lod in enumerate(splitted):
                                if i == 4:
                                    break
                                obj[f'I3D_lod{i}'] = lod

                    else:
                        if "group_id" in obj[stjerne[0]]:
                            # loop to set the new correct merge group ID as stjerne exporter and giants exporter
                            # stores the merge group in different ways
                            for mg, new_id in merge_groups:
                                if mg == obj[stjerne[0]][stjerne[1]]:
                                    obj['I3D_mergeGroup'] = new_id
                        else:
                            obj[giants] = obj[stjerne[0]][stjerne[1]]
                            print(f"Else state: {obj[giants]} -> {obj[stjerne[0]][stjerne[1]]}")
            elif isinstance(stjerne, tuple):
                if stjerne[1] in obj.data:
                    # print(obj.data[stjerne[1]])
                    if stjerne[2] in obj.data[stjerne[1]]:
                        obj[giants] = obj.data[stjerne[1]][stjerne[2]]
                        print(f"Key {stjerne[2]} transferred correctly, object: {obj.name}")
                    else:
                        print(f"Key {stjerne[2]} not found in object.data. in object: {obj.name}")
            else:
                print(f"Key {stjerne[0]} or {stjerne[1]} not found in object.")

    def mg_string_to_int(self, context, merge_groups) -> list:
        '''Converts the stjerne string merge groups to int merge groups to be used in Giants I3D Exporter
        :param context: The context of the scene
        :param merge_groups: The merge groups to convert'''

        # Get the unique strings from merge_groups
        unique_strings = list(set(merge_groups))
        # Create a dictionary mapping each string to a unique integer
        string_to_int = {s: i+1 for i, s in enumerate(unique_strings)}

        # Create the new list with tuples, each tuple contains the string and its corresponding integer
        mg_list = [(mg, string_to_int[mg]) for mg in merge_groups]
        return mg_list

    def convert_material_props(self, context, mat):
        for attr in mat.keys():
            if attr == 'i3d_attributes':
                source = mat[attr].get('source')
                mat['customShader'] = source
                variation_idx = mat[attr].get('variation')
                if variation_idx:
                    variation_name = mat[attr]['variations'][variation_idx]['name']
                    mat['customShaderVariation'] = variation_name
                    # print(f"Variation name: {variation_name}")

                # mat['customShaderVariation'] = variation
        # print(f"Material: {mat.name}")

    def execute(self, context):
        # Get the merge groups from the objects
        merge_groups = [mg.i3d_merge_group.group_id for mg in bpy.data.objects if mg.i3d_merge_group.group_id]
        mg_list = self.mg_string_to_int(context, merge_groups)

        for obj in bpy.data.objects:
            self.convert_obj_props(context, obj, True, mg_list)

        for mat in bpy.data.materials:
            self.convert_material_props(context, mat)
        return {'FINISHED'}
