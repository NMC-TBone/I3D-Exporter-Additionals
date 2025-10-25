import math

import bpy

from ..helper_functions import check_i3d_exporter_type, get_curve_length

giants_enabled, i3dio_enabled = check_i3d_exporter_type()


class PoseAddOperator(bpy.types.Operator):
    bl_label = "Add Pose"
    bl_idname = "i3dea.add_pose"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        pose_count = context.scene.i3dea.pose_count
        pose_list = context.scene.i3dea.pose_list
        while True:
            pose_count += 1
            name = f"pose{pose_count}"
            existing = any(item.name == name for item in pose_list)
            if not existing:
                break
        item = pose_list.add()
        item.name = name
        return {"FINISHED"}


class PoseRemoveOperator(bpy.types.Operator):
    bl_label = "Remove Pose"
    bl_idname = "i3dea.remove_pose"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.scene.i3dea.pose_list

    def execute(self, context):
        pose_list = context.scene.i3dea.pose_list
        index = max(0, len(pose_list) - 1)
        pose_list.remove(index)
        context.scene.i3dea.pose_count = max(0, context.scene.i3dea.pose_count - 1)
        return {"FINISHED"}


class AddCurveOperator(bpy.types.Operator):
    bl_label = "Add Curve"
    bl_idname = "i3dea.add_curve"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        pose_list = context.scene.i3dea.pose_list
        selected_pose = pose_list[context.scene.i3dea.pose_count]
        sub_pose_list = selected_pose.sub_pose_list
        for obj in context.selected_objects:
            if obj.type == "CURVE":
                if not any(sub_pose.curve == obj.name for sub_pose in sub_pose_list):
                    sub_pose = sub_pose_list.add()
                    sub_pose.curve = obj.name
        return {"FINISHED"}


class RemoveCurveOperator(bpy.types.Operator):
    bl_label = "Remove Curve"
    bl_idname = "i3dea.remove_curve"
    bl_options = {"REGISTER", "UNDO"}
    remove_all: bpy.props.BoolProperty()

    @classmethod
    def poll(cls, context):
        pose_list = context.scene.i3dea.pose_list
        if pose_list:
            selected_pose = pose_list[context.scene.i3dea.pose_count]
            return selected_pose.sub_pose_list
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
        return {"FINISHED"}


class I3DEA_OT_empties_along_curves(bpy.types.Operator):
    bl_label = "Create empties along curves"
    bl_idname = "i3dea.add_empties_curves"
    bl_description = "Create empties evenly spread along selected curves"
    bl_options = {"REGISTER", "UNDO"}

    def _create_empty(self, context, empty_type="PLAIN_AXES", location=(0, 0, 0), name="empty") -> bpy.types.Object:
        """Creates an empty object at the origin"""
        empty = bpy.data.objects.new(name, None)
        empty.empty_display_size = 0.25
        empty.empty_display_type = empty_type
        empty.location = location
        context.collection.objects.link(empty)
        return empty

    def _create_empties_on_curve(self, context, hierarchy="curveArray"):
        """Creates empty objects along each selected curve object"""
        i3dea = context.scene.i3dea
        # Create empty object "pose1"
        hierarchy_empty = self._create_empty(context, name=hierarchy)

        if giants_enabled:
            from pathlib import Path

            blend_file_path = Path(bpy.data.filepath).parent
            target_path = Path(i3dea.motion_save_location or "")

            if blend_file_path.anchor == target_path.anchor:
                try:
                    relative_path = target_path.relative_to(blend_file_path)
                    final_path = f"{relative_path.as_posix()}/{hierarchy}.dds"
                except ValueError:
                    # Fallback to absolute path if relative fails
                    final_path = f"{target_path.as_posix()}/{hierarchy}.dds"
            else:
                # Use absolute path if paths are on different mounts
                final_path = f"{target_path.as_posix()}/{hierarchy}.dds"

            final_path = final_path.replace("\\", "/").replace("//", "/")

            if not final_path.startswith((".", "/")):
                final_path = "./" + final_path

            hierarchy_empty["i3D_objectDataFilePath"] = final_path

            hierarchy_empty["i3D_objectDataHierarchicalSetup"] = True
            hierarchy_empty["i3D_objectDataHideFirstAndLastObject"] = True
            hierarchy_empty["i3D_objectDataExportPosition"] = True
            hierarchy_empty["i3D_objectDataExportOrientation"] = True
            hierarchy_empty["i3D_objectDataExportScale"] = True

        all_empties = []
        for pose in i3dea.pose_list:
            if pose.sub_pose_list:
                pose_empty = self._create_empty(context, name=pose.name)
                pose_empty.parent = hierarchy_empty
            else:
                pose_empty = None

            # For AMOUNT_FIX
            curve_lengths = {
                curve.curve: get_curve_length(context.scene.objects[curve.curve]) for curve in pose.sub_pose_list
            }
            longest_curve_length = max(curve_lengths.values(), default=0)

            for idx, curve in enumerate(pose.sub_pose_list):
                split_name = curve.curve.split(".")[0]
                curve_empty = self._create_empty(context, name=f"{split_name}_Y_{idx:03d}")
                curve_empty.parent = pose_empty
                c_length = curve_lengths[curve.curve]
                amount = 0
                if i3dea.motion_type == "UNIFORM":
                    amount = i3dea.motion_uniform
                elif i3dea.motion_type == "ADAPTIVE":
                    distance = longest_curve_length / i3dea.motion_adaptive
                    amount = math.ceil(c_length / distance)
                elif i3dea.motion_type == "DISTANCE":
                    amount = math.ceil(c_length / i3dea.motion_distance)
                for i in range(amount):
                    x_empty = self._create_empty(context, empty_type="ARROWS", name=f"{split_name}_X_{i:03d}")
                    x_empty.parent = curve_empty

                    # Set object constraint to follow curve
                    follow_path = x_empty.constraints.new("FOLLOW_PATH")
                    follow_path.target = bpy.data.objects[curve.curve]
                    follow_path.use_curve_radius = False
                    follow_path.use_fixed_location = True
                    follow_path.use_curve_follow = True
                    follow_path.forward_axis = "TRACK_NEGATIVE_Y"
                    follow_path.up_axis = "UP_Z"
                    # Set offset factor for empty along curve
                    follow_path.offset_factor = i / (amount - 1)
                    all_empties.append(x_empty)

        # Update scene once to get empty matrix and set that after removing constraint
        context.view_layer.update()
        for x_empty in all_empties:
            transformation_matrix = x_empty.matrix_world.copy()
            x_empty.constraints.remove(x_empty.constraints["Follow Path"])
            x_empty.matrix_world = transformation_matrix

    def execute(self, context):
        import time

        start_time = time.time()
        i3dea = context.scene.i3dea
        self._create_empties_on_curve(context, hierarchy=i3dea.motion_hierarchy_name)
        end_time = time.time()
        self.report({"INFO"}, f"Generated empties a long selected curves in {end_time - start_time:.2f} seconds")
        return {"FINISHED"}


classes = (
    PoseAddOperator,
    PoseRemoveOperator,
    AddCurveOperator,
    RemoveCurveOperator,
    I3DEA_OT_empties_along_curves,
)
register, unregister = bpy.utils.register_classes_factory(classes)
