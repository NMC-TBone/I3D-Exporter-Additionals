import bpy
from ..helper_functions import check_i3d_exporter_type

giants_i3d, stjerne_i3d, dcc, I3DRemoveAttributes = check_i3d_exporter_type()


class I3DEA_UL_selected_curves(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        pg = data
        curve_icon = 'OUTLINER_OB_CURVE'
        layout.prop(item, "curve_ref", text="", emboss=False, translate=False, icon=curve_icon)


class I3DEA_UL_selected_curves2(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        pg = data
        curve_icon = 'OUTLINER_OB_CURVE'
        layout.prop(item, "curve_ref", text="", emboss=False, translate=False, icon=curve_icon)


class I3DEA_OT_empties_along_curves(bpy.types.Operator):
    bl_label = "Create empties along curves"
    bl_idname = "i3dea.add_empties_curves"
    bl_description = "Create empties evenly spread along selected curves"
    bl_options = {'UNDO'}
    state: bpy.props.IntProperty()

    # Store the selected objects (curves)
    selected_curves = [[], []]

    def load_curves(self, context, pose2=False):
        for curve in context.selected_objects:
            if curve.type == 'CURVE':
                if not pose2:
                    if curve.name not in self.selected_curves[0]:
                        self.selected_curves[0].append(curve.name)
                elif pose2:
                    if curve.name not in self.selected_curves[1]:
                        self.selected_curves[1].append(curve.name)

    def execute(self, context):
        if self.state == 1:
            self.load_curves(context)

            object_names = [item.name for item in context.scene.i3dea.object_collection]
            for curve_name in self.selected_curves[0]:
                curve = bpy.data.objects[curve_name]
                if curve.type == 'CURVE' and curve.name not in object_names:
                    my_curve = context.scene.i3dea.object_collection.add()
                    my_curve.name = curve.name
                    my_curve.curve_ref = curve

            context.scene.i3dea.active_obj_index = len(context.scene.i3dea.object_collection) - 1

        elif self.state == 2:
            context.scene.i3dea.object_collection.clear()
            context.scene.i3dea.active_obj_index = -1

            self.selected_curves[0].clear()

        elif self.state == 3:
            if len(context.scene.i3dea.object_collection) > 0:
                ob_list = context.scene.i3dea.object_collection
                active = context.scene.i3dea.active_obj_index
                active_obj = context.scene.i3dea.object_collection[context.scene.i3dea.active_obj_index].curve_ref.name

                self.selected_curves[0].remove(active_obj)

                ob_list.remove(active)
                context.scene.i3dea.active_obj_index = min(max(0, active - 1), len(ob_list) - 1)
            else:
                pass

        if self.state == 4:
            self.load_curves(context, pose2=True)

            object_names2 = [item.name for item in context.scene.i3dea.object_collection2]
            for curve_name in self.selected_curves[1]:
                curve = bpy.data.objects[curve_name]
                if curve.type == 'CURVE' and curve.name not in object_names2:
                    my_curve = context.scene.i3dea.object_collection2.add()
                    my_curve.name = curve.name
                    my_curve.curve_ref = curve

            context.scene.i3dea.active_obj_index2 = len(context.scene.i3dea.object_collection2) - 1

            print(self.selected_curves[1])

        elif self.state == 5:
            context.scene.i3dea.object_collection2.clear()
            context.scene.i3dea.active_obj_index2 = -1

            self.selected_curves[1].clear()

        elif self.state == 6:
            if len(context.scene.i3dea.object_collection2) > 0:
                ob_list = context.scene.i3dea.object_collection2
                active = context.scene.i3dea.active_obj_index2
                active_obj = context.scene.i3dea.object_collection2[context.scene.i3dea.active_obj_index2].curve_ref.name

                self.selected_curves[1].remove(active_obj)

                ob_list.remove(active)
                context.scene.i3dea.active_obj_index2 = min(max(0, active - 1), len(ob_list) - 1)
            else:
                pass

        elif self.state == 7:
            # Create empty objects along selected curves
            create_empties_on_curve(self.selected_curves, context.scene.i3dea.curve_array_name, num_empties=context.scene.i3dea.amount_curve)
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

    if giants_i3d:
        dcc.I3DSetAttrString(hierarchy_empty.name, 'I3D_objectDataFilePath', hierarchy_name + ".dds")
        dcc.I3DSetAttrBool(hierarchy_empty.name, 'I3D_objectDataHierarchicalSetup', True)
        dcc.I3DSetAttrBool(hierarchy_empty.name, 'I3D_objectDataHideFirstAndLastObject', True)
        dcc.I3DSetAttrBool(hierarchy_empty.name, 'I3D_objectDataExportPosition', True)
        dcc.I3DSetAttrBool(hierarchy_empty.name, 'I3D_objectDataExportOrientation', True)
        dcc.I3DSetAttrBool(hierarchy_empty.name, 'I3D_objectDataExportScale', True)

    # Create empty object "pose1"
    pose1 = create_empty(name="pose1")
    pose1.parent = hierarchy_empty

    # Create empty object "pose2"
    pose2 = None
    if bpy.context.scene.i3dea.use_pose2 and len(selected_curves[1]) > 1:
        pose2 = create_empty(name="pose2")
        pose2.parent = hierarchy_empty

    num1, num2 = -1, -1
    for curve1 in selected_curves[0]:
        # Create Y empties inside pose1
        # Set empty name based on curve name
        num1 += 1
        empty_name = f"pose1_Y_{num1:03d}"

        y_empty = create_empty(name=empty_name)

        # Set object parent to the pose1 empties
        y_empty.parent = pose1

        curve1_length = bpy.data.objects[curve1].data.splines[0].calc_length()

        for i in range(num_empties):
            # Set empty name based on curve name
            empty_x_name = f"pose1_X_{i:03d}"
            x_empty = create_empty(empty_type='ARROWS', name=empty_x_name)

            # Set object constraint to follow curve
            x_empty.constraints.new('FOLLOW_PATH')
            x_empty.constraints['Follow Path'].target = bpy.data.objects[curve1]
            x_empty.constraints['Follow Path'].use_curve_radius = False
            x_empty.constraints['Follow Path'].use_fixed_location = True
            x_empty.constraints['Follow Path'].use_curve_follow = True
            x_empty.constraints['Follow Path'].forward_axis = 'FORWARD_Y'
            x_empty.constraints['Follow Path'].up_axis = 'UP_Z'

            # Set object parent based on curve name
            x_empty.parent = y_empty

            # Set offset factor for empty along curve
            if bpy.context.scene.i3dea.use_amount:
                x_empty.constraints['Follow Path'].offset_factor = i / (num_empties - 1)
            elif bpy.context.scene.i3dea.use_distance:
                amount1 = bpy.context.scene.i3dea.distance_curve / curve1_length
                x_empty.constraints['Follow Path'].offset_factor = i / (amount1 - 1)

            # Apply the constraint
            bpy.ops.constraint.apply({'constraint': x_empty.constraints["Follow Path"]}, constraint='Follow Path')

    if bpy.context.scene.i3dea.use_pose2:
        for curve2 in selected_curves[1]:
            # Create Y empties inside pose2
            # Set empty name based on curve name
            num2 += 1
            empty2_name = f"pose2_Y_{num2:03d}"

            y_empty2 = create_empty(name=empty2_name)

            # Set object parent to pose2 empties
            y_empty2.parent = pose2

            curve2_length = bpy.data.objects[curve2].data.splines[0].calc_length()
            amount2 = bpy.context.scene.i3dea.distance_curve / curve2_length

            for i in range(num_empties):
                # Set empty name based on curve name
                empty2_x_name = f"pose2_X_{i:03d}"
                x_empty2 = create_empty(empty_type='ARROWS', name=empty2_x_name)

                # Set object constraint to follow curve
                x_empty2.constraints.new('FOLLOW_PATH')
                x_empty2.constraints['Follow Path'].target = bpy.data.objects[curve2]
                x_empty2.constraints['Follow Path'].use_curve_radius = False
                x_empty2.constraints['Follow Path'].use_fixed_location = True
                x_empty2.constraints['Follow Path'].use_curve_follow = True
                x_empty2.constraints['Follow Path'].forward_axis = 'FORWARD_Y'
                x_empty2.constraints['Follow Path'].up_axis = 'UP_Z'

                # Set object parent based on curve name
                x_empty2.parent = y_empty2

                # Set offset factor for empty along curve
                if bpy.context.scene.i3dea.use_amount:
                    x_empty2.constraints['Follow Path'].offset_factor = i / (num_empties - 1)
                elif bpy.context.scene.i3dea.use_distance:
                    x_empty2.constraints['Follow Path'].offset_factor = amount2

                # Apply the constraint
                bpy.ops.constraint.apply({'constraint': x_empty2.constraints["Follow Path"]}, constraint='Follow Path')
