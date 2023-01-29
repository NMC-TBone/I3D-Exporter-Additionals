import math

import bpy
from ..helper_functions import check_i3d_exporter_type, get_curve_length

giants_i3d, stjerne_i3d = check_i3d_exporter_type()


class PoseAddOperator(bpy.types.Operator):
    bl_label = "Add Pose"
    bl_idname = "i3dea.add_pose"

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

    def execute(self, context):
        pose_list = context.scene.i3dea.pose_list
        selected_pose = pose_list[context.scene.i3dea.pose_count]
        sub_pose_list = selected_pose.sub_pose_list
        for obj in context.selected_objects:
            if obj.type == 'CURVE':
                if not any(sub_pose.curve == obj for sub_pose in sub_pose_list):
                    sub_pose = sub_pose_list.add()
                    sub_pose.curve = obj
        return {'FINISHED'}


class RemoveCurveOperator(bpy.types.Operator):
    bl_label = "Remove Curve"
    bl_idname = "i3dea.remove_curve"
    remove_all: bpy.props.BoolProperty()

    @classmethod
    def poll(cls, context):
        pose_list = context.scene.i3dea.pose_list
        selected_pose = pose_list[context.scene.i3dea.pose_count]
        return selected_pose.sub_pose_list

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
        bpy.ops.object.empty_add(type=empty_type, radius=0.25, location=location)
        empty = bpy.context.object
        empty.name = name
        return empty

    def __create_empties_on_curve(self, hierarchy=""):
        """Creates empty objects along each selected curve object"""
        # Create empty object "pose1"
        hierarchy_empty = self.__create_empty(name=hierarchy)

        if giants_i3d:
            hierarchy_empty['I3D_objectDataFilePath'] = hierarchy + ".dds"
            hierarchy_empty['I3D_objectDataHierarchicalSetup'] = True
            hierarchy_empty['I3D_objectDataHideFirstAndLastObject'] = True
            hierarchy_empty['I3D_objectDataExportPosition'] = True
            hierarchy_empty['I3D_objectDataExportOrientation'] = True
            hierarchy_empty['I3D_objectDataExportScale'] = True

        # for curve in bpy.context.scene.i3dea.pose_list.sub_pose_list:
        #     pass

        for pose in bpy.context.scene.i3dea.pose_list:
            pose_empty = self.__create_empty(name=pose.name)
            pose_empty.parent = hierarchy_empty

            # For AMOUNT_FIX
            longest_curve_length = 0
            for curve in pose.sub_pose_list:
                curve_length = get_curve_length(curve.curve.name)
                if curve_length > longest_curve_length:
                    longest_curve_length = curve_length

            for curve in pose.sub_pose_list:
                curve_empty = self.__create_empty(name=curve.curve.name + "_Y")
                curve_empty.parent = pose_empty
                amount = 0
                if bpy.context.scene.i3dea.motion_type == "AMOUNT_REL":
                    amount = bpy.context.scene.i3dea.motion_amount_rel
                elif bpy.context.scene.i3dea.motion_type == "DISTANCE":
                    c_length = get_curve_length(curve.curve.name)
                    amount = math.ceil(c_length / bpy.context.scene.i3dea.motion_distance)
                elif bpy.context.scene.i3dea.motion_type == "AMOUNT_FIX":
                    c_length = get_curve_length(curve.curve.name)
                    distance = longest_curve_length / bpy.context.scene.i3dea.motion_amount_fix
                    amount = math.ceil(c_length / distance)
                for i in range(amount):
                    x_empty = self.__create_empty(empty_type='ARROWS', name=f"{curve.curve.name}_X_{i:03d}")
                    # Set object constraint to follow curve
                    x_empty.constraints.new('FOLLOW_PATH')
                    x_empty.constraints['Follow Path'].target = bpy.data.objects[curve.curve.name]
                    x_empty.constraints['Follow Path'].use_curve_radius = False
                    x_empty.constraints['Follow Path'].use_fixed_location = True
                    x_empty.constraints['Follow Path'].use_curve_follow = True
                    x_empty.constraints['Follow Path'].forward_axis = 'TRACK_NEGATIVE_Y'
                    x_empty.constraints['Follow Path'].up_axis = 'UP_Z'

                    # Set object parent based on curve name
                    x_empty.parent = curve_empty

                    # Set offset factor for empty along curve
                    x_empty.constraints['Follow Path'].offset_factor = i / (amount - 1)

                    # Apply the constraint
                    bpy.ops.constraint.apply({'constraint': x_empty.constraints["Follow Path"]}, constraint='Follow Path')

    def execute(self, context):
        i3dea = context.scene.i3dea
        self.__create_empties_on_curve(hierarchy=i3dea.motion_hierarchy_name)
        self.report({'INFO'}, "Generated empties a long selected curves")
        return {'FINISHED'}
