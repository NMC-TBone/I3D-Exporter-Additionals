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


class I3DEA_OT_properties_converter(bpy.types.Operator):
    bl_idname = "i3dea.properties_converter"
    bl_label = "Convert I3D properties"
    bl_description = "Converts I3D properties from Stjerne exporter to Giants exporter"
    bl_options = {'REGISTER', 'UNDO'}

    reversed = {v: k for k, v in prop_conversion_map.items()}

    def _handle_rigid_body_type(self, obj, stjerne):
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
        return 1

    def _handle_split_uvs(self, obj, stjerne):
        obj['I3D_splitMinU'] = obj[stjerne[0]][stjerne[1]][0]
        obj['I3D_splitMinV'] = obj[stjerne[0]][stjerne[1]][1]
        obj['I3D_splitMaxU'] = obj[stjerne[0]][stjerne[1]][2]
        obj['I3D_splitMaxV'] = obj[stjerne[0]][stjerne[1]][3]
        obj['I3D_splitUvWorldScale'] = obj[stjerne[0]][stjerne[1]][4]
        return 1

    def _handle_lod_distance(self, obj, stjerne):
        if obj[stjerne[0]][stjerne[1]]:
            obj['I3D_lod'] = True
            splitted = obj[stjerne[0]][stjerne[1]].split()

            # loop to set the correct lod distance from stjerne exporter to giants exporter
            # Max 4 lod distances allowed in giants exporter (lod0 should be 0)
            for i, lod in enumerate(splitted):
                if i == 4:
                    break
                obj[f'I3D_lod{i}'] = lod
            return 1

    def _handle_merge_group(self, obj, stjerne, merge_groups):
        for mg, new_id in merge_groups:
            if mg == obj[stjerne[0]][stjerne[1]]:
                obj['I3D_mergeGroup'] = new_id
        return 1

    def _handle_other_cases(self, obj, giants, stjerne):
        obj[giants] = obj[stjerne[0]][stjerne[1]]
        return 1

    def mg_string_to_int(self, context, merge_groups) -> list:
        """
        Converts the stjerne string merge groups to int merge groups to be used in Giants I3D Exporter
        :param context: The context of the scene
        :param merge_groups: The merge groups to convert
        """

        # Get the unique strings from merge_groups
        unique_strings = list(dict.fromkeys(merge_groups))

        # Create a dictionary mapping each string to a unique integer
        string_to_int = {s: i for i, s in enumerate(unique_strings)}

        # Create the new list with tuples, each tuple contains the string and its corresponding integer
        mg_list = [(s, string_to_int[s]) for s in unique_strings]
        return mg_list

    def convert_obj_props(self, context, obj, forward=True, merge_groups=None) -> int:
        """
        Converts the obj properties from the Stjerne I3D Exporter to the Giants I3D Exporter
        :param context: The context of the scene
        :param obj: The object to convert the properties of
        :param forward: If the conversion should be from Stjerne to Giants or the other way around
        :param merge_groups: The merge groups to convert
        """
        prop_map = prop_conversion_map if forward else self.reversed
        props_conv = 0

        for giants, stjerne in prop_map.items():
            if stjerne[0] in obj and stjerne[1] in obj[stjerne[0]]:
                if obj[stjerne[0]][stjerne[1]]:
                    if stjerne[1] == "rigid_body_type":
                        props_conv += self._handle_rigid_body_type(obj, stjerne)
                    elif stjerne[1] == "split_uvs":
                        props_conv += self._handle_split_uvs(obj, stjerne)
                    elif stjerne[1] == "lod_distance":
                        props_conv += self._handle_lod_distance(obj, stjerne)
                    else:
                        if "group_id" in obj[stjerne[0]]:
                            props_conv += self._handle_merge_group(obj, stjerne, merge_groups)
                        else:
                            props_conv += self._handle_other_cases(obj, giants, stjerne)
            elif isinstance(stjerne, tuple) and obj.type == 'MESH' and \
                    stjerne[1] in obj.data and stjerne[2] in obj.data[stjerne[1]]:

                obj[giants] = obj.data[stjerne[1]][stjerne[2]]
                props_conv += 1
        return props_conv

    def convert_user_attr(self, context, obj) -> int:
        count = 0
        if 'i3d_user_attributes' in obj and 'attribute_list' in obj['i3d_user_attributes']:
            for attr in obj['i3d_user_attributes']['attribute_list']:
                match attr.get('type'):
                    case 0:
                        attr_type = 'data_scriptCallback'
                    case 1:
                        attr_type = 'data_string'
                    case 2:
                        attr_type = 'data_float'
                    case 3:
                        attr_type = 'data_integer'
                    case _:
                        attr_type = 'data_boolean'
                giants_attr = f"userAttribute_{attr_type.removeprefix('data_')}_{attr['name']}"
                obj[giants_attr] = attr[attr_type]
                count += 1
        return count

    def convert_light_props(self, context, obj) -> int:
        count = 0
        if 'i3d_attributes' in obj.data and obj.data['i3d_attributes'] != {}:
            for attr in obj.data['i3d_attributes']:
                if attr == 'type_of_light':
                    obj['I3D_lightType'] = obj.data['i3d_attributes'][attr]
                    count += 1
                elif attr == 'light_color':
                    obj['I3D_lightColor'] = obj.data['i3d_attributes'][attr]
                    count += 1

        return count

    def convert_material_props(self, context, mat):
        """
        Converts the material properties from Stjerne to Giants
        :param context: The context of the scene
        :param mat: The material props to convert
        """

        keys = list(mat.keys())
        for attr in keys:
            # Check if its the correct mat property
            if attr == 'i3d_attributes':
                source = mat[attr].get('source')
                if source:
                    if 'Farming Simulator 19' in source:
                        source = source.replace('Farming Simulator 19', 'Farming Simulator 22')
                    mat['customShader'] = source
                    # print(f"Source: {source}")
                # Get the variation index
                variation_idx = mat[attr].get('variation')
                if variation_idx:
                    variation_name = mat[attr]['variations'][variation_idx].get('name')
                    mat['customShaderVariation'] = variation_name
                    # print(f"Variation: {variation_name}")
                shader_params = mat[attr].get('shader_parameters')
                if shader_params:
                    # Loop over all the shader parameters
                    for param in shader_params:
                        param_name = param.get('name')
                        param_type = param.get('type')
                        # Get different float values from the shader parameters
                        if param_type == 0:
                            data = param.get('data_float_1')
                        elif param_type == 1:
                            data = param.get('data_float_2')
                        elif param_type == 2:
                            data = param.get('data_float_3')
                        elif param_type == 3:
                            data = param.get('data_float_4')

                        # Set the new property name and value
                        new_property_name = f"customParameter_{param_name}"
                        data_string = " ".join(str(i) for i in data)
                        mat[new_property_name] = data_string
                shader_textures = mat[attr].get('shader_textures')
                if shader_textures:
                    for tex in shader_textures:
                        tex_name = tex.get('name')
                        tex_source = tex.get('source')
                        tex_default_source = tex.get('default_source')
                        if tex_source != tex_default_source:
                            new_property_name = f"customTexture_{tex_name}"
                            mat[new_property_name] = tex_source

    def convert_node_structure(self, context, mat):
        if mat.node_tree:
            bsdf = None
            tex_node = None
            sep_color_node = None

            # find the Principled BSDF and Glossmap nodes
            for node in mat.node_tree.nodes:
                if node.name == 'Principled BSDF':
                    bsdf = node
                elif node.name == 'Glossmap':
                    if node.type == 'TEX_IMAGE':
                        tex_node = node
                    elif node.type == 'SEPARATE_COLOR':
                        sep_color_node = node
                        if sep_color_node.inputs['Color'].is_linked:
                            tex_node = sep_color_node.inputs['Color'].links[0].from_node
                            if tex_node.type != 'TEX_IMAGE':
                                tex_node = None

            # if we didn't find the Principled BSDF node return
            if not bsdf:
                print(f"No Principled BSDF node found in material: {mat.name}")
                return

            # if we didn't find the Glossmap node return
            if not tex_node:
                print(f"No Glossmap node found in material: {mat.name}")
                return

            # if both nodes are found, link them together
            mat.node_tree.links.new(bsdf.inputs['Specular'], tex_node.outputs['Color'])
            if sep_color_node:
                mat.node_tree.nodes.remove(sep_color_node)

    def execute(self, context):
        total_props_conv = 0
        # Get the merge groups from the objects
        merge_groups = [mg['i3d_merge_group']['group_id'] for mg in bpy.data.objects if mg.type == 'MESH' and
                        'i3d_merge_group' in mg and 'group_id' in mg['i3d_merge_group'] and
                        mg['i3d_merge_group']['group_id'] != '']
        mg_list = self.mg_string_to_int(context, merge_groups)

        """Things to add for ui/options:
        - Option to convert material properties
        - Option to convert node structure
        - Option to convert user attributes"""

        for obj in bpy.data.objects:
            total_props_conv += self.convert_obj_props(context, obj, True, mg_list)
            # if context.convert_user_attr:
            total_props_conv += self.convert_user_attr(context, obj)
            if obj.type == 'LIGHT':
                total_props_conv += self.convert_light_props(context, obj)

        # if context.convert_mat_props:
        for mat in bpy.data.materials:
            self.convert_material_props(context, mat)
            # if context.convet_nodes:
            self.convert_node_structure(context, mat)
        self.report({'INFO'}, f"{total_props_conv} props converted")
        return {'FINISHED'}
