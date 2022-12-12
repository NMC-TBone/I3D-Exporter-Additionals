import bpy


class I3DEA_OT_emties_along_curves(bpy.types.Operator):
    bl_label = "Create empties along curves"
    bl_idname = "i3dea.add_empties_curves"
    bl_description = "Create empties evenly spread along selected curves"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # Store the selected objects (curves)
        selected_objects = [obj for obj in bpy.context.selected_objects if obj.type == 'CURVE']

        # Create empty objects along selected curves
        create_empties_on_curve(selected_objects, context.scene.i3dea.curve_array_name, num_empties=context.scene.i3dea.amount_curve)
        self.report({'INFO'}, "Generated empties a long selected curves")
        return {'FINISHED'}


def create_empty(empty_type='PLAIN_AXES', location=(0, 0, 0), name="empty"):
    """Creates an empty object at the origin"""
    bpy.ops.object.empty_add(type=empty_type, radius=0.25, location=location)
    empty = bpy.context.object
    empty.name = name
    return empty


def create_empties_on_curve(selected_curves, hierarchy_name, num_empties=10):
    """Creates empty objects along each selected curve object"""
    # Create empty object "pose1"
    hierarchy_empty = create_empty(name=hierarchy_name)

    # Create empty object "pose1"
    pose1 = create_empty(name="pose1")
    pose1.parent = hierarchy_empty

    # Create empty object "pose2"
    pose2 = create_empty(name="pose2")
    pose2.parent = hierarchy_empty

    num1, num2 = -1, -1
    for obj in selected_curves:
        # Create Y empties inside pose1 & pose2
        # Set empty name based on curve name
        if obj.name.startswith("pose1"):
            num1 += 1
            empty_name = f"pose1_Y_{num1:03d}"
        elif obj.name.startswith("pose2"):
            num2 += 1
            empty_name = f"pose2_Y_{num2:03d}"
        else:
            empty_name = "empty"
        y_empty = create_empty(name=empty_name)

        # Set object parent to the pose1 and pose2 empties
        if obj.name.startswith("pose1"):
            y_empty.parent = pose1
        elif obj.name.startswith("pose2"):
            y_empty.parent = pose2

        for i in range(num_empties):
            # Set empty name based on curve name
            if obj.name.startswith("pose1"):
                empty_name = f"pose1_X_{i:03d}"
            elif obj.name.startswith("pose2"):
                empty_name = f"pose2_X_{i:03d}"
            else:
                empty_name = "empty"
            x_empty = create_empty(empty_type='ARROWS', name=empty_name)

            # Set object constraint to follow curve
            x_empty.constraints.new('FOLLOW_PATH')
            x_empty.constraints['Follow Path'].target = obj
            x_empty.constraints['Follow Path'].use_curve_radius = False
            x_empty.constraints['Follow Path'].use_fixed_location = True
            x_empty.constraints['Follow Path'].use_curve_follow = True
            x_empty.constraints['Follow Path'].forward_axis = 'FORWARD_Y'
            x_empty.constraints['Follow Path'].up_axis = 'UP_Z'

            # Set object parent based on curve name
            if obj.name.startswith("pose1"):
                x_empty.parent = y_empty
            elif obj.name.startswith("pose2"):
                x_empty.parent = y_empty

            # Set offset factor for empty along curve
            if bpy.context.scene.i3dea.use_amount:
                x_empty.constraints['Follow Path'].offset_factor = i / (num_empties - 1)
            elif bpy.context.scene.i3dea.use_distance:
                x_empty.constraints['Follow Path'].offset_factor = i / (bpy.context.scene.i3dea.distance_curve - 1)

            # Apply the constraint
            bpy.ops.constraint.apply({'constraint': x_empty.constraints["Follow Path"]}, constraint='Follow Path')
