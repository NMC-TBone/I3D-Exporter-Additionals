import math

import bpy
from ..helper_functions import check_i3d_exporter_type, get_curve_length

giants_i3d, stjerne_i3d = check_i3d_exporter_type()


class PoseAddOperator(bpy.types.Operator):
    bl_label = "Add Pose"
    bl_idname = "i3dea.add_pose"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        pose_count = context.scene.i3dea.pose_count
        pose_list = context.scene.i3dea.pose_list
        while True:
            pose_count += 1
            name = "pose" + str(pose_count)
            existing = any(item.name == name for item in pose_list)
            if not existing:
                break
        item = pose_list.add()
        item.name = name
        return {'FINISHED'}


class PoseRemoveOperator(bpy.types.Operator):
    bl_label = "Remove Pose"
    bl_idname = "i3dea.remove_pose"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.scene.i3dea.pose_list

    def execute(self, context):
        pose_list = context.scene.i3dea.pose_list
        index = max(0, len(pose_list) - 1)
        pose_list.remove(index)
        context.scene.i3dea.pose_count = max(0, context.scene.i3dea.pose_count - 1)
        return {'FINISHED'}


class AddCurveOperator(bpy.types.Operator):
    bl_label = "Add Curve"
    bl_idname = "i3dea.add_curve"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        pose_list = context.scene.i3dea.pose_list
        selected_pose = pose_list[context.scene.i3dea.pose_count]
        sub_pose_list = selected_pose.sub_pose_list
        for obj in context.selected_objects:
            if obj.type == 'CURVE':
                if not any(sub_pose.curve == obj.name for sub_pose in sub_pose_list):
                    sub_pose = sub_pose_list.add()
                    sub_pose.curve = obj.name
        return {'FINISHED'}


class RemoveCurveOperator(bpy.types.Operator):
    bl_label = "Remove Curve"
    bl_idname = "i3dea.remove_curve"
    bl_options = {'REGISTER', 'UNDO'}
    remove_all: bpy.props.BoolProperty()

    @classmethod
    def poll(cls, context):
        pose_list = context.scene.i3dea.pose_list
        if pose_list:
            selected_pose = pose_list[context.scene.i3dea.pose_count]
            return selected_pose.sub_pose_list
        else:
            return False

    def execute(self, context):
        pose_list = context.scene.i3dea.pose_list
        selected_pose = pose_list[context.scene.i3dea.pose_count]

        if self.remove_all:
            selected_pose.sub_pose_list.clear()
        else:
            sub_pose_list = selected_pose.sub_pose_list
            index = selected_pose.sub_pose_count
            sub_pose_list.remove(index)
            selected_pose.sub_pose_count = min(max(0, index - 1), len(sub_pose_list) - 1)
        return {'FINISHED'}


class I3DEA_OT_empties_along_curves(bpy.types.Operator):
    bl_label = "Create empties along curves"
    bl_idname = "i3dea.add_empties_curves"
    bl_description = "Create empties evenly spread along selected curves"
    bl_options = {'UNDO'}

    def __create_empty(self, empty_type='PLAIN_AXES', location=(0, 0, 0), name="empty"):
        """Creates an empty object at the origin"""
        empty = bpy.data.objects.new(name, None)
        empty.empty_display_size = 0.25
        empty.empty_display_type = empty_type
        empty.location = location
        bpy.context.collection.objects.link(empty)
        return empty

    def __create_empties_on_curve(self, hierarchy="curveArray"):
        """Creates empty objects along each selected curve object"""
        # Create empty object "pose1"
        hierarchy_empty = self.__create_empty(name=hierarchy)

        if giants_i3d:
            hierarchy_empty['I3D_objectDataFilePath'] = f"{hierarchy}.dds"
            hierarchy_empty['I3D_objectDataHierarchicalSetup'] = True
            hierarchy_empty['I3D_objectDataHideFirstAndLastObject'] = True
            hierarchy_empty['I3D_objectDataExportPosition'] = True
            hierarchy_empty['I3D_objectDataExportOrientation'] = True
            hierarchy_empty['I3D_objectDataExportScale'] = True

        all_empties = []
        for pose in bpy.context.scene.i3dea.pose_list:
            if pose.sub_pose_list:
                pose_empty = self.__create_empty(name=pose.name)
                pose_empty.parent = hierarchy_empty
            else:
                pose_empty = None

            # For AMOUNT_FIX
            curve_lengths = {curve.curve: get_curve_length(curve.curve) for curve in pose.sub_pose_list}
            longest_curve_length = max(curve_lengths.values(), default=0)

            for ind, curve in enumerate(pose.sub_pose_list):
                split_name = curve.curve.split('.')[0]
                curve_empty = self.__create_empty(name=f"{split_name}_Y_{ind:03d}")
                curve_empty.parent = pose_empty
                c_length = curve_lengths[curve.curve]
                amount = 0
                if bpy.context.scene.i3dea.motion_type == "AMOUNT_REL":
                    amount = bpy.context.scene.i3dea.motion_amount_rel
                elif bpy.context.scene.i3dea.motion_type == "DISTANCE":
                    amount = math.ceil(c_length / bpy.context.scene.i3dea.motion_distance)
                elif bpy.context.scene.i3dea.motion_type == "AMOUNT_FIX":
                    distance = longest_curve_length / bpy.context.scene.i3dea.motion_amount_fix
                    amount = math.ceil(c_length / distance)
                for i in range(amount):
                    x_empty = self.__create_empty(empty_type='ARROWS', name=f"{split_name}_X_{i:03d}")
                    x_empty.parent = curve_empty

                    # Set object constraint to follow curve
                    follow_path = x_empty.constraints.new('FOLLOW_PATH')
                    follow_path.target = bpy.data.objects[curve.curve]
                    follow_path.use_curve_radius = False
                    follow_path.use_fixed_location = True
                    follow_path.use_curve_follow = True
                    follow_path.forward_axis = 'TRACK_NEGATIVE_Y'
                    follow_path.up_axis = 'UP_Z'
                    # Set offset factor for empty along curve
                    follow_path.offset_factor = i / (amount - 1)
                    all_empties.append(x_empty)

        # Update scene once to get empty matrix and set that after removing constraint
        bpy.context.view_layer.update()
        for x_empty in all_empties:
            transformation_matrix = x_empty.matrix_world.copy()
            x_empty.constraints.remove(x_empty.constraints['Follow Path'])
            x_empty.matrix_world = transformation_matrix

    def execute(self, context):
        import time
        start_time = time.time()
        if context.mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')
        i3dea = context.scene.i3dea
        self.__create_empties_on_curve(hierarchy=i3dea.motion_hierarchy_name)
        end_time = time.time()
        self.report({'INFO'}, f"Generated empties a long selected curves in {end_time - start_time:.2f} seconds")
        return {'FINISHED'}