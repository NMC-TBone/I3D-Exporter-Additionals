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

# Test the whole scene to check if there is any issues in the setup before export to i3d

import bpy
from mathutils import Vector

# Numbers are taken from Giants Maya exporter
MAX_OBJECT_COUNT = 150
MAX_POLY_COUNT = 200000
MAX_MERGE_GROUP_MEMBERS = 60


class I3DEA_OT_verify_scene(bpy.types.Operator):
    bl_idname = "i3dea.verify_scene"
    bl_label = "Verify Scene"
    bl_description = "Control the scene for any issues before export to i3d"

    @staticmethod
    def get_children(parent_obj):
        children = []
        to_visit = [bpy.data.objects[parent_obj]]
        while to_visit:
            curr_ob = to_visit.pop()
            children.extend(curr_ob.children)
            to_visit.extend(curr_ob.children)
        return children

    def objects_to_check(self, context):
        ignored_obj_names = set()
        for obj in bpy.data.objects:
            if obj.name.lower().endswith("_ignore"):
                children_objs = self.get_children(obj.name)
                ignored_obj_names.update(obj.name for obj in children_objs)
        return [obj for obj in bpy.data.objects if obj.name not in ignored_obj_names]

    def check_placeable(self, obj):
        if "placeable" in obj.name.lower():
            return True
        for mat in obj.material_slots:
            if 'customShader' in mat.material:
                if "placeableShader" or "buildingShader" in mat.material['customShader']:
                    return True
        return False

    def initialize_counts(self):
        self.error_count = 0
        self.warning_count = 0
        self.info_count = 0
        self.total_object_count = 0
        self.total_poly_count = 0
        self.merge_group_members = {}
        self.bounding_volumes = {}
        self.component_number = 1
        self.messages = []

    def _add_message(self, type, content):
        self.messages.append({'type': type, 'content': content})
        if type == 'ERROR':
            self.error_count += 1
        elif type == 'WARNING':
            self.warning_count += 1
        elif type == 'INFO':
            self.info_count += 1

    def _check_objects(self, context, objects_list, is_placeable):
        dg = context.evaluated_depsgraph_get()
        for obj in objects_list:
            self.name_lower = obj.name.lower()
            if obj.type == 'MESH':
                self._check_mesh_object(obj, context, dg, is_placeable)

    def _check_mesh_object(self, obj, context, dg, is_placeable):
        has_armature = any(mo.type == "ARMATURE" for mo in obj.modifiers)

        eval_obj = obj.evaluated_get(dg)
        mesh = bpy.data.meshes.new_from_object(eval_obj)
        poly_count = len(mesh.polygons)

        is_non_renderable = obj.get('I3D_nonRenderable', False) is True
        merge_group = obj.get('I3D_mergeGroup', 0)
        merge_group_root = obj.get('I3D_mergeGroupRoot', False)
        bounding_volume = obj.get('I3D_boundingVolume', '')
        if poly_count > 0 and not is_non_renderable and merge_group == 0:
            self.total_object_count += 1
            self.total_poly_count += poly_count

            if len([o for o in bpy.data.objects if o.data == mesh]) > 1:
                self._add_message('INFO', f"Multiple shapes defined for {obj.name}!")
        bpy.data.meshes.remove(mesh)

        if merge_group > 0:
            member_count, has_root_object = self.merge_group_members.get(merge_group, (0, False))
            # Update the member count and root object flag
            self.merge_group_members[merge_group] = (member_count + 1, has_root_object or merge_group_root)

            merge_group_name = f"MERGEGROUP_{merge_group}"
            if merge_group_name not in self.bounding_volumes:
                self.bounding_volumes[merge_group_name] = False

        if bounding_volume not in ['', 'None']:
            self.bounding_volumes[bounding_volume] = True

        if obj.get("I3D_static", False) is True and not is_placeable:
            self._add_message('INFO', f"RigidBody: {obj.name} is marked as static!")

        clip_distance_conditions = [('I3D_nonRenderable', lambda v: v == 0),
                                    ('I3D_mergeGroup', lambda v: v == 0),
                                    ('I3D_clipDistance', lambda v: v == 0),
                                    ('I3D_boundingVolume', lambda v: v == '')]
        if all(key in obj and condition(obj[key]) for key, condition in clip_distance_conditions):
            self._add_message('INFO',
                              f"ClipDistance: {obj.name} has no clip distance set. This causes performance issues!")

        decal_layer = obj.get('I3D_decalLayer', 0)
        if 'decal' in self.name_lower and decal_layer == 0:
            self._add_message('INFO', f"Decal Layer: {obj.name}, has decal layer set to 0")
        elif decal_layer > 0 and 'decal' not in self.name_lower:
            self._add_message('INFO', f"Decal Layer: {obj.name} have to be pre-/postfixed by 'decal' "
                              "if decalLayer-attribute > 0")

        if 'fillvolume' in self.name_lower:
            if obj.get('I3D_cpuMesh', False) is False:
                self._add_message('WARNING', f"FillVolume: {obj.name} is not marked as CPU-Mesh!")

        collision = obj.get('I3D_collision', False)
        compound = obj.get('I3D_compound', False)
        trigger = obj.get('I3D_trigger', False)
        if collision is True:
            if compound is True and trigger is False and obj.parent is None:
                expected_suffix = "_main_component1" \
                    if self.component_number == 1 else f"_component{self.component_number}"
                self.component_number += 1
                if not obj.name.endswith(expected_suffix):
                    self._add_message('WARNING', f"Component: Object {obj.name} is marked as compound, "
                                      f"but name convention is wrong. Should be {expected_suffix}")

            if obj.scale != Vector((1, 1, 1)):
                self._add_message('WARNING, 'f"Scale: collision {obj.name} is not scaled 1 1 1, apply scale.")

        if 'effect' in self.name_lower:
            if not obj.data.color_attributes:
                self._add_message('WARNING',
                                  f"EffectMesh: {obj.name}, is a effect but doesn't have a Vertex Color layer")
            if not len(obj.data.uv_layers) == 2:
                self._add_message('WARNING', f"EffectMesh: {obj.name}, is a effect but doesn't have 2 UV layers")

        if has_armature and obj.modifiers and obj.modifiers[0].type != "ARMATURE":
            self._add_message('WARNING', f"Armature modifier: Object {obj.name} "
                              "has armature modifier, but it's not first modifier in the list.")
        if len(obj.vertex_groups) > 0:
            if not has_armature:
                self._add_message('WARNING', f"Vertex groups: Object {obj.name} "
                                  "has vertex groups, but no armature modifier.")

            uninfluenced_vertices = [v.index for v in obj.data.vertices if sum(group.weight for group in v.groups) == 0]
            if uninfluenced_vertices:
                vertices_str = ", ".join(map(str, uninfluenced_vertices))
                self._add_message('ERROR', f"Vertex groups: Object {obj.name} "
                                  "has vertex groups, but the following vertices "
                                  f"are not influenced by any group: {vertices_str}")

    def report_results(self):
        if self.total_poly_count > MAX_POLY_COUNT:
            self._add_message('ERROR', f"Poly count: {self.total_poly_count} is very high. "
                              "This cause performance issues. Try to reduce it")

        if self.total_object_count > MAX_OBJECT_COUNT:
            self._add_message('ERROR', f"Object count: {self.total_object_count} mesh objects is very high. "
                              "This cause performance issues. Consider merging some objects")

        if self.merge_group_members:
            for merge_group, (member_count, has_root_object) in self.merge_group_members.items():
                if member_count > MAX_MERGE_GROUP_MEMBERS:
                    self._add_message('WARNING', f"Merge group: {merge_group} has {member_count} members. "
                                      f"Max allowed is {MAX_MERGE_GROUP_MEMBERS}. "
                                      "Consider splitting it into multiple merge groups")
                if not has_root_object:
                    self._add_message('WARNING', f"Merge group: {merge_group} has no root object. "
                                      "First member will be set as root.")
        if self.bounding_volumes:
            for bv, used in self.bounding_volumes.items():
                if not used:
                    self._add_message('WARNING', f"No bounding-volume defined for {bv}. "
                                      "Bounding volume will be automatically calculated")

        print("--------------------")
        print("VERIFY SCENE RESULTS")
        print("--------------------")
        for message in self.messages:
            print(f"{message['type']}: {message['content']}")
        print("Errors:", self.error_count)
        print("Warnings:", self.warning_count)
        print("Info:", self.info_count)
        print("Poly count:", self.total_poly_count)
        print("Object count:", self.total_object_count)

    def execute(self, context):
        is_placeable = any(self.check_placeable(obj) for obj in bpy.data.objects)
        objects_list = self.objects_to_check(context)
        self.initialize_counts()
        self._check_objects(context, objects_list, is_placeable)
        self.report_results()

        self.report({'INFO'}, f'Errors: {self.error_count}, Warnings: {self.warning_count}, Info: {self.info_count} '
                    '(check console for details)')
        return {'FINISHED'}
