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

# --------------------------------------------------------------------------------------
#  Converted/inspired from skeletons script in maya i3d exporter, plugins/Skeletons.py
# --------------------------------------------------------------------------------------

# skeletons.py contains skeleton setup for vehicles, tools and placeables

import bpy
import math

from ..helper_functions import check_i3d_exporter_type

giants_i3d, stjerne_i3d = check_i3d_exporter_type()


class I3DEA_OT_skeletons(bpy.types.Operator):
    bl_label = "Create Button"
    bl_idname = "i3dea.skeletons"
    bl_description = "Creates the selected skeleton from the dropdown menu."
    bl_options = {'REGISTER', 'UNDO'}

    def create_skel_node(self, name, parent, display_handle=False, translate=(0, 0, 0), rotation=(0, 0, 0)):
        bpy.ops.object.empty_add(radius=0)
        node = bpy.context.active_object
        node.name = name
        node.parent = parent
        node.location = translate
        translate = (0, 0, 0)
        node.rotation_euler = rotation
        rotation = (0, 0, 0)
        if display_handle:
            self.set_display_handle(node)
        return node

    def set_display_handle(self, node):
        node = bpy.context.object
        node.empty_display_type = 'ARROWS'
        node.empty_display_size = 0.25

    def create_base_vehicle(self):
        self.create_base_vec(False)
        return

    def create_base_harvester(self):
        self.create_base_vec(True)
        return

    def create_attacher_joints(self):
        return self.create_vehicle_attacher_joints(False)

    def create_base_vec(self, is_harvester):
        self.create_vehicle_component("vehicleName_main_component1", "vehicleName_main_component1")
        vehicle = bpy.context.active_object
        vehicle_vis = self.create_skel_node("1_vehicleName_root(REPLACE_WITH_MESH)", vehicle)
        self.create_skel_node("1_wheels", vehicle_vis)
        cameras = ""
        if is_harvester:
            cameras = self.create_cameras_harvester()
        else:
            cameras = self.create_cameras_vehicle()
        cameras = bpy.context.active_object
        cameras.parent = vehicle_vis
        self.create_lights()
        create_lights = bpy.context.active_object
        create_lights.parent = vehicle_vis
        self.create_skel_node("4_exitPoint", vehicle_vis)
        cabin = self.create_skel_node("5_cabin_REPLACE_WITH_MESH", vehicle_vis)
        steering_base = self.create_skel_node("1_steeringBase", cabin)
        steering_wheel = self.create_skel_node("steeringWheel_REPLACE_WITH_MESH", steering_base)
        self.create_skel_node("playerRightHandTarget", steering_wheel, True, translate=(-0.189, 0.023, 0.03), rotation=(math.radians(-4.70569), math.radians(-50.8809), math.radians(-7.47474)))
        self.create_skel_node("playerLeftHandTarget", steering_wheel, True, translate=(0.189, 0.023, 0.03), rotation=(math.radians(-16.3303), math.radians(50.8809), math.radians(-7.47473)))
        seat = self.create_skel_node("2_seat_REPLACE_WITH_MESH", cabin)
        self.create_skel_node("playerSkin", seat, True)
        self.create_skel_node("3_lights_cabin", cabin)
        self.create_skel_node("4_wipers", cabin)
        self.create_skel_node("5_dashboards", cabin)
        self.create_skel_node("6_levers", cabin)
        self.create_skel_node("7_pedals", cabin)
        character_targets = self.create_skel_node("8_characterTargets", cabin, False)
        self.create_skel_node("playerRightFootTarget", character_targets, True)
        self.create_skel_node("playerLeftFootTarget", character_targets, True)
        self.create_skel_node("9_mirrors_cabin", cabin)
        self.create_skel_node("10_visuals_cabin", cabin)
        attacher_joints = None
        if is_harvester:
            attacher_joints = self.create_vehicle_attacher_joints(True)
        else:
            attacher_joints = self.create_vehicle_attacher_joints(False)
        attacher_joints = bpy.context.active_object
        attacher_joints.parent = vehicle_vis
        ai = self.create_skel_node("7_ai", vehicle_vis)
        self.create_skel_node("aiCollisionTrigger_REPLACE_WITH_MESH", ai)
        exhaust_particles = None
        if is_harvester:
            exhaust_particles = self.create_skel_node("particles", vehicle_vis)
        else:
            exhaust_particles = self.create_skel_node("8_exhaustParticles", vehicle_vis)
        self.create_skel_node("exhaustParticle1", exhaust_particles, True)
        self.create_skel_node("exhaustParticle2", exhaust_particles, True)
        if is_harvester:
            self.create_skel_node("movingParts", vehicle_vis)
        self.create_skel_node("9_hydraulics", vehicle_vis)
        self.create_skel_node("10_mirrors", vehicle_vis)
        self.create_skel_node("11_configurations", vehicle_vis)
        if is_harvester:
            self.create_skel_node("fillVolume", vehicle_vis)
            work_areas = self.create_skel_node("workAreas", vehicle_vis)
            work_area_straw = self.create_skel_node("workAreaStraw", work_areas)
            self.create_skel_node("workAreaStrawStart", work_area_straw)
            self.create_skel_node("workAreaStrawWidth", work_area_straw)
            self.create_skel_node("workAreaStrawHeight", work_area_straw)
            work_area_chopper = self.create_skel_node("workAreaChopper", work_areas)
            self.create_skel_node("workAreaChopperStart", work_area_chopper)
            self.create_skel_node("workAreaChopperWidth", work_area_chopper)
            self.create_skel_node("workAreaChopperHeight", work_area_chopper)
        self.create_skel_node("12_visuals", vehicle_vis)
        self.create_skel_node("2_skinnedMeshes", vehicle)
        self.create_skel_node("3_collisions", vehicle)
        return vehicle

    def create_base_tool(self):
        self.create_vehicle_component("toolName_main_component1", "toolName_main_component1")
        tool = bpy.context.active_object
        vehicle_vis = self.create_skel_node("1_toolName_root", tool)
        attachable = self.create_skel_node("1_attachable", vehicle_vis)
        self.create_skel_node("attacherJoint", attachable)
        self.create_skel_node("topReferenceNode", attachable)
        self.create_skel_node("ptoInputNode", attachable)
        self.create_skel_node("support", attachable)
        self.create_skel_node("connectionHoses", attachable)
        self.create_skel_node("wheelChocks", attachable)
        self.create_skel_node("2_wheels", vehicle_vis)
        self.create_lights()
        create_lights = bpy.context.active_object
        create_lights.parent = vehicle_vis
        self.create_skel_node("4_movingParts", vehicle_vis)
        self.create_skel_node("5_fillUnit", vehicle_vis)
        work_area = self.create_skel_node("6_workArea", vehicle_vis)
        self.create_skel_node("workAreaStart", work_area)
        self.create_skel_node("workAreaWidth", work_area)
        self.create_skel_node("workAreaHeight", work_area)
        self.create_skel_node("7_effects", vehicle_vis)
        ai = self.create_skel_node("8_ai", vehicle_vis)
        ai_markers = self.create_skel_node("aiMarkers", ai)
        self.create_skel_node("aiMarkerLeft", ai_markers)
        self.create_skel_node("aiMarkerRight", ai_markers)
        self.create_skel_node("aiMarkerBack", ai_markers)
        size_markers = self.create_skel_node("sizeMarkers", ai)
        self.create_skel_node("sizeMarkerLeft", size_markers)
        self.create_skel_node("sizeMarkerRight", size_markers)
        self.create_skel_node("sizeMarkerBack", size_markers)
        self.create_skel_node("aiCollisionNode", ai)
        self.create_skel_node("9_visuals", vehicle_vis)
        self.create_skel_node("2_skinnedMeshes", tool)
        self.create_skel_node("3_collisions", tool)
        return tool

    def create_player(self, steering_wheel=None):
        bpy.ops.object.empty_add(radius=0)
        player_root = bpy.context.active_object
        player_root.name = 'playerRoot'
        self.create_skel_node("player_skin", player_root, True)
        self.create_skel_node("player_rightFoot", player_root, True, translate=(-0.184, -0.393, -0.514), rotation=(0, 0, math.radians(10)))
        self.create_skel_node("player_leftFoot", player_root, True, translate=(0.184, -0.393, -0.514), rotation=(0, 0, math.radians(-10)))
        if steering_wheel is not None and steering_wheel is not False:
            self.create_skel_node("playerRightHandTarget", player_root, True, translate=(-0.188, -0.022, 0.03), rotation=(math.radians(-10.518), math.radians(51.12), math.radians(-4.708)))
            self.create_skel_node("playerLeftHandTarget", player_root, True, translate=(0.189, -0.023, 0.03), rotation=(math.radians(-10.518), math.radians(-51.12), math.radians(-4.708)))
        return player_root

    def create_lights(self):
        bpy.ops.object.empty_add(radius=0)
        lights_group = bpy.context.active_object
        lights_group.name = '3_lights'
        self.create_skel_node("1_sharedLights", lights_group)
        self.create_skel_node("2_staticLights", lights_group)
        # default lights
        default_lights = self.create_skel_node("3_defaultLights", lights_group)
        # Blender
        # (self, name, parent, coneAngle, range, dropOff, rgb, translate=(0, 0, 0), rotation=(0, 0, 0), castShadowMap=False)
        # Maya
        # (self, name, parent, coneAngle, intensity, dropOff, rgb, locatorScale=50, rotation=['0deg', '0deg', '0deg'], translation=[0, 0, 0], castShadowMap=False, depthMapBias=0.001, depthMapResolution=256)
        self.create_light('frontLightLow', default_lights, math.radians(80), 20, 0.6, (0.85, 0.85, 1), rotation=(math.radians(-75), 0, 0))
        self.create_light('highBeamLow', default_lights, math.radians(70), 30, 0.4, (0.85, 0.85, 1), rotation=(math.radians(-80), 0, 0))
        front_light_high = self.create_light('frontLightHigh', default_lights, math.radians(70), 25, 0.6, (0.85, 0.85, 1), rotation=(math.radians(-75), 0, math.radians(8)))
        self.create_light('frontLightHigh1', front_light_high, math.radians(70), 25, 0.6, (0.85, 0.85, 1), rotation=(0, math.radians(16), 0))
        high_beam_high = self.create_light('highBeamHigh', default_lights, math.radians(30), 60, 0.5, (0.85, 0.85, 1), rotation=(math.radians(-80), 0, math.radians(5)))
        self.create_light('highBeamHigh2', high_beam_high, math.radians(30), 60, 0.5, (0.85, 0.85, 1), rotation=(0, math.radians(10), 0))
        self.create_light('licensePlateLightHigh', default_lights, 120, 0.5, 2, (1, 1, 1), rotation=(math.radians(90), 0, 0))
        bpy.ops.object.light_add(type='POINT')
        point_light = bpy.context.object.data
        point_light.name = "interiorScreenLight"
        point_light.cutoff_distance = 0.25
        point_light.color = (0.59, 0.653079, 1)
        bpy.context.active_object.parent = default_lights
        work_lights = self.create_skel_node("4_workLights", lights_group)
        self.create_light('workLightFrontLow', work_lights, math.radians(130), 20, 0.4, (0.85, 0.85, 1), rotation=(math.radians(-80), 0, 0))
        work_light_front_high1 = self.create_light('workLightFrontHigh', work_lights, math.radians(90), 25, 0.4, (0.85, 0.85, 1), rotation=(math.radians(-65), 0, math.radians(15)))
        self.create_light('workLightFrontHigh2', work_light_front_high1, math.radians(90), 25, 0.4, (0.85, 0.85, 1), rotation=(0, math.radians(30), 0))
        # work lights back
        self.create_light('workLightBackLow', work_lights, math.radians(130), 20, 0.4, (0.85, 0.85, 1), rotation=(math.radians(70), 0, 0))
        work_light_back_high1 = self.create_light('workLightBackHigh', work_lights, math.radians(90), 25, 0.4, (0.85, 0.85, 1), rotation=(math.radians(70), 0, math.radians(-20)))
        self.create_light('workLightBackHigh2', work_light_back_high1, math.radians(90), 25, 0.4, (0.85, 0.85, 1), rotation=(math.radians(5.41377), math.radians(37.1585), math.radians(16.0129)))
        # backlights
        back_lights = self.create_skel_node("5_backLights", lights_group)
        back_lights_high1 = self.create_light('backLightsHigh', back_lights, math.radians(130), 2.5, 0.4, (0.5, 0, 0), rotation=(math.radians(-75), 0, math.radians(-180)))
        self.create_light('backLightsHigh2', back_lights_high1, math.radians(130), 2.5, 0.4, (0.5, 0, 0), rotation=(0, 0, 0))
        # turn lights
        turn_lights = self.create_skel_node("6_turnLights", lights_group)
        turn_light_left_front = self.create_light('turnLightLeftFront', turn_lights, math.radians(120), 4, 0.6, (0.31, 0.14, 0), rotation=(math.radians(75), 0, math.radians(-180)))
        self.create_light('turnLightLeftBack', turn_light_left_front, math.radians(120), 4, 0.6, (0.31, 0.14, 0), rotation=(0, 0, 0))
        turn_light_right_front = self.create_light('turnLightRightFront', turn_lights, math.radians(120), 4, 0.6, (0.31, 0.14, 0), rotation=(math.radians(75), 0, 0))
        self.create_light('turnLightRightBack', turn_light_right_front, math.radians(120), 4, 0.6, (0.31, 0.14, 0), rotation=(0, 0, 0))
        # beacon lights
        beacon_lights = self.create_skel_node("7_beaconLights", lights_group)
        self.create_skel_node("beaconLight1", beacon_lights)
        # reverse lights
        reverse_lights = self.create_skel_node("8_reverseLights", lights_group)
        reverse_light1 = self.create_light('reverseLightHigh', reverse_lights, math.radians(130), 2.5, 0.6, (0.9, 0.9, 1), rotation=(math.radians(75), 0, 0))
        self.create_light('reverseLightHigh2', reverse_light1, math.radians(130), 2.5, 0.6, (0.9, 0.9, 1))
        bpy.ops.object.select_grouped(type='PARENT')
        bpy.ops.object.select_grouped(type='PARENT')
        bpy.ops.object.select_grouped(type='PARENT')
        return lights_group

    def create_vehicle_attacher_joints(self, is_harvester):
        bpy.ops.object.empty_add(radius=0)
        attacher_joint_group = bpy.context.active_object
        attacher_joint_group.name = '6_attacherJoints'
        tools = self.create_skel_node("1_tools", attacher_joint_group)
        trailers = self.create_skel_node("2_trailers", attacher_joint_group)
        ptos = self.create_skel_node("3_ptos", attacher_joint_group)
        self.create_skel_node("4_connectionHoses", attacher_joint_group)
        if not is_harvester:
            # attacherjointbackrot
            attacher_joint_back_rot = self.create_skel_node("attacherJointBackRot", tools, rotation=(math.radians(13), 0, math.radians(-180)))
            attacher_joint_back_rot2 = self.create_skel_node("attacherJointBackRot2", attacher_joint_back_rot, translate=(0, -1, 0), rotation=(math.radians(13), 0, math.radians(-180)))
            self.create_skel_node("attacherJointBack", attacher_joint_back_rot2, True, rotation=(0, 0, math.radians(-90)))
            # attacherjointbackbottomarm
            attacher_joint_back_arm_bottom = self.create_skel_node("attacherJointBackArmBottom", tools, rotation=(math.radians(13), 0, math.radians(-180)))
            attacher_joint_back_arm_bottom_trans = self.create_skel_node("attacherJointBackArmBottomTrans_REPLACE_WITH_MESH", attacher_joint_back_arm_bottom)
            self.create_skel_node("referencePointBackBottom", attacher_joint_back_arm_bottom_trans, translate=(0, -1, 0))
            # attacherjointbacktoparm
            self.create_skel_node("attacherJointBackArmTop", tools, rotation=(math.radians(67), 0, 0))
        # attacherjointfrontrot
        attacher_joint_front_rot = self.create_skel_node("attacherJointFrontRot", tools, rotation=(math.radians(-13), 0, 0))
        attacher_joint_front_rot2 = self.create_skel_node("attacherJointFrontRot2", attacher_joint_front_rot, translate=(0, -1, 0), rotation=(math.radians(13), 0, 0))
        self.create_skel_node("attacherJointFront", attacher_joint_front_rot2, True, rotation=(0, 0, math.radians(90)))
        # attacherjointfrontbottomarm
        attacher_joint_front_arm_bottom = self.create_skel_node("attacherJointFrontArmBottom", tools, rotation=(math.radians(-26), 0, 0))
        attacher_joint_front_arm_bottom_trans = self.create_skel_node("attacherJointFrontArmBottomTrans_REPLACE_WITH_MESH", attacher_joint_front_arm_bottom)
        self.create_skel_node("referencePointFrontBottom", attacher_joint_front_arm_bottom_trans, translate=(0, -1, 0))
        # attacherjointfronttoparm
        self.create_skel_node("attacherJointFrontArmTop", tools, True, rotation=(math.radians(-40), 0, 0))
        # trailer joints
        self.create_skel_node("trailerAttacherJointBack", trailers, True, rotation=(0, 0, math.radians(-90)))
        if not is_harvester:
            self.create_skel_node("trailerAttacherJointBackLow", trailers, True, rotation=(0, 0, math.radians(-90)))
        if not is_harvester:
            self.create_skel_node("trailerAttacherJointFront", trailers, True, rotation=(0, 0, math.radians(-90)))
        # ptos
        if not is_harvester:
            self.create_skel_node("ptoBack", ptos, True, rotation=(0, 0, math.radians(-180)))
        self.create_skel_node("ptoFront", ptos, True)
        if not is_harvester:
            self.create_skel_node("5_frontloader", attacher_joint_group, True)
        if not is_harvester:
            bpy.ops.object.select_grouped(type='PARENT')
        else:
            bpy.ops.object.select_grouped(type='PARENT')
            bpy.ops.object.select_grouped(type='PARENT')
        return attacher_joint_group

    def create_traffic_vehicle(self):
        bpy.ops.object.empty_add(radius=0)
        traffic_vehicle = bpy.context.active_object
        traffic_vehicle.name = 'trafficVehicle01'
        self.create_skel_node("1_wheels", traffic_vehicle)
        lights = self.create_skel_node("lights", traffic_vehicle)
        self.create_skel_node("staticLights", lights)
        real_lights = self.create_skel_node("realLights", lights)
        self.create_light('frontLightLow', real_lights, math.radians(80), 20, 0.6, (0.85, 0.85, 1), rotation=(math.radians(-80), 0, 0), translate=(0, -3.5, 0.6), cast_shadow_map=False)
        front_light_high1 = self.create_light('frontLightHigh1', real_lights, math.radians(70), 25, 0.4, (0.85, 0.85, 1), rotation=(math.radians(-80), 0, math.radians(8)), translate=(-0.5, -3.5, 0.6))
        self.create_light('frontLightHigh2', front_light_high1, math.radians(70), 25, 0.4, (0.85, 0.85, 1), rotation=(math.radians(-80), 0, math.radians(-8)), translate=(0.5, -3.5, 0.6))
        self.create_light('backLightHigh1', front_light_high1, math.radians(130), 2.5, 0.4, (0.5, 0, 0), rotation=(math.radians(160), 0, 0), translate=(-0.5, 1, 0.8))
        self.create_light('backLightHigh2', front_light_high1, math.radians(130), 2.5, 0.4, (0.5, 0, 0), rotation=(math.radians(160), 0, 0), translate=(0.5, 1, 0.8))
        self.create_skel_node("trafficCollisionNode", traffic_vehicle)
        self.create_skel_node("driver_TO_BE_REPLACED", traffic_vehicle)
        self.create_skel_node("vehicle_vis", traffic_vehicle)
        return traffic_vehicle

    def create_placeable(self):
        bpy.ops.object.empty_add(radius=0)
        placeable = bpy.context.active_object
        placeable.name = 'placeable'
        self.create_placeable_elements(placeable)
        return placeable

    def create_animal_husbandry(self):
        bpy.ops.object.empty_add(radius=0)
        animal_husbandry = bpy.context.active_object
        animal_husbandry.name = 'animalHusbandry'
        food = self.create_skel_node("1_1_food", animal_husbandry)
        self.create_skel_node("fillVolume", food)
        self.create_exact_fill_root_node("exactFillRootNodeFood", food)
        food_places = self.create_skel_node("foodPlaces", food)
        self.create_skel_node("foodPlace1", food_places)
        self.create_skel_node("foodPlace2", food_places)
        self.create_skel_node("foodPlace3", food_places)
        self.create_skel_node("1_2_storage", animal_husbandry)
        straw = self.create_skel_node("1_3_straw", animal_husbandry)
        self.create_plane("strawPlane", straw, (5, 5, 0))
        self.create_exact_fill_root_node("exactFillRootNodeStraw", straw)
        milktank = self.create_skel_node("1_4_milktank", animal_husbandry)
        self.create_trigger("milktankTrigger", 2097152, "200000", milktank)
        liquid_manure_tank = self.create_skel_node("1_5_liquidManureTank", animal_husbandry)
        self.create_trigger("liquidManureTankTrigger", 2097152, "200000", liquid_manure_tank)
        water_places = self.create_skel_node("6_waterPlaces", animal_husbandry)
        self.create_skel_node("waterPlace1", water_places)
        self.create_skel_node("waterPlace2", water_places)
        self.create_skel_node("waterPlace3", water_places)
        pallet_areas = self.create_skel_node("1_7_palletAreas", animal_husbandry)
        self.create_trigger("palletTrigger", 2097152, "200000", pallet_areas)
        pallet_area1_start = self.create_skel_node("palletArea1Start", pallet_areas)
        self.create_skel_node("palletArea1End", pallet_area1_start)
        pallet_area2_start = self.create_skel_node("palletArea2Start", pallet_areas)
        self.create_skel_node("palletArea2End", pallet_area2_start)
        nav_root_node = self.create_skel_node("1_8_navigationRootNode", animal_husbandry)
        self.create_plane("navigationMesh", nav_root_node)
        walking_plane = self.create_plane("walkingPlane", nav_root_node)
        if giants_i3d:
            walking_plane['I3D_collision'] = True
            walking_plane['I3D_static'] = True
            walking_plane['I3D_nonRenderable'] = True
            walking_plane['I3D_castsShadows'] = True
            walking_plane['I3D_receiveShadows'] = True
            walking_plane['I3D_collisionMask'] = 131072
        if stjerne_i3d:
            bpy.context.object.i3d_attributes.rigid_body_type = 'static'
            bpy.context.object.i3d_attributes.collision_mask = "20000"
            bpy.context.object.data.i3d_attributes.casts_shadows = True
            bpy.context.object.data.i3d_attributes.receive_shadows = True
            bpy.context.object.data.i3d_attributes.non_renderable = True
        fences = self.create_skel_node("1_9_fences", animal_husbandry)
        fence1 = self.create_skel_node("fence1", fences)
        self.create_skel_node("fence1Node1", fence1, True)
        self.create_skel_node("fence1Node2", fence1, True)
        self.create_skel_node("fence1Node3", fence1, True)
        self.create_skel_node("fence1Node4", fence1, True)
        self.create_skel_node("1_10_warningStripes", animal_husbandry)
        self.create_trigger("1_11_loadingTrigger", 3145728, "300000", animal_husbandry)
        self.create_placeable_elements(animal_husbandry)
        return animal_husbandry

    def create_placeable_elements(self, parent):
        clear_areas = self.create_skel_node("1_clearAreas", parent)
        clear_area1_start = self.create_skel_node("clearArea1Start", clear_areas, True)
        self.create_skel_node("clearArea1Width", clear_area1_start, True, translate=(0, -1, 0))
        self.create_skel_node("clearArea1Height", clear_area1_start, True, translate=(1, 0, 0))
        clear_area2_start = self.create_skel_node("clearArea2Start", clear_areas, True)
        self.create_skel_node("clearArea2Width", clear_area2_start, True, translate=(0, -1, 0))
        self.create_skel_node("clearArea2Height", clear_area2_start, True, translate=(1, 0, 0))
        clear_area3_start = self.create_skel_node("clearArea3Start", clear_areas, True)
        self.create_skel_node("clearArea3Width", clear_area3_start, True, translate=(0, -1, 0))
        self.create_skel_node("clearArea3Height", clear_area3_start, True, translate=(1, 0, 0))
        level_areas = self.create_skel_node("2_levelAreas", parent)
        level_area1_start = self.create_skel_node("levelArea1Start", level_areas, True)
        self.create_skel_node("levelArea1Width", level_area1_start, True, translate=(0, -1, 0))
        self.create_skel_node("levelArea1Height", level_area1_start, True, translate=(1, 0, 0))
        level_area2_start = self.create_skel_node("levelArea2Start", level_areas, True)
        self.create_skel_node("levelArea2Width", level_area2_start, True, translate=(0, -1, 0))
        self.create_skel_node("levelArea2Height", level_area2_start, True, translate=(1, 0, 0))
        level_area3_start = self.create_skel_node("levelArea3Start", level_areas, True)
        self.create_skel_node("levelArea3Width", level_area3_start, True, translate=(0, -1, 0))
        self.create_skel_node("levelArea3Height", level_area3_start, True, translate=(1, 0, 0))
        paint_areas = self.create_skel_node("3_paintAreas", parent)
        paint_area1_start = self.create_skel_node("paintArea1Start", paint_areas, True)
        self.create_skel_node("paintArea1Width", paint_area1_start, True, translate=(0, -1, 0))
        self.create_skel_node("paintArea1Height", paint_area1_start, True, translate=(1, 0, 0))
        paint_area2_start = self.create_skel_node("paintArea2Start", paint_areas, True)
        self.create_skel_node("paintArea2Width", paint_area2_start, True, translate=(0, -1, 0))
        self.create_skel_node("paintArea2Height", paint_area2_start, True, translate=(1, 0, 0))
        paint_area3_start = self.create_skel_node("paintArea3Start", paint_areas, True)
        self.create_skel_node("paintArea3Width", paint_area3_start, True, translate=(0, -1, 0))
        self.create_skel_node("paintArea3Height", paint_area3_start, True, translate=(1, 0, 0))
        indoor_areas = self.create_skel_node("4_indoorAreas", parent)
        indoor_area1_start = self.create_skel_node("indoorArea1Start", indoor_areas, True)
        self.create_skel_node("indoorArea1Width", indoor_area1_start, True, translate=(0, -1, 0))
        self.create_skel_node("indoorArea1Height", indoor_area1_start, True, translate=(1, 0, 0))
        test_areas = self.create_skel_node("5_testAreas", parent)
        test_area1_start = self.create_skel_node("testArea1Start", test_areas, True)
        self.create_skel_node("testArea1End", test_area1_start, True, translate=(1, -1, 0))
        test_area2_start = self.create_skel_node("testArea2Start", test_areas, True)
        self.create_skel_node("testArea2End", test_area2_start, True, translate=(1, -1, 0))
        test_area3_start = self.create_skel_node("testArea3Start", test_areas, True)
        self.create_skel_node("testArea3End", test_area3_start, True, translate=(1, -1, 0))
        tip_occlusion_update_areas = self.create_skel_node("6_tipOcclusionUpdateAreas", parent)
        tip_occlusion_update_area1_start = self.create_skel_node("tipOcclusionUpdateArea1Start", tip_occlusion_update_areas, True)
        self.create_skel_node("tipOcclusionUpdateArea1End", tip_occlusion_update_area1_start, True, translate=(1, -1, 0))
        self.create_trigger("7_infoTrigger", 1048576, "100000", parent, size=(10, 10, 5))
        visuals = self.create_skel_node("8_visuals", parent)
        self.create_skel_node("winter", visuals)
        collisions = self.create_skel_node("9_collisions", parent)
        self.create_collision("collision", 255, "ff", collisions)
        self.create_collision("tipCollision", 524288, "80000", collisions)
        self.create_collision("tipCollisionWall", 524288, "80000", collisions)
        if giants_i3d:
            prop_name = 'userAttribute_float_collisionHeight'
            bpy.context.object[prop_name] = 4.0
            bpy.context.object.id_properties_ensure()  # Make sure the manager is updated
            property_manager = bpy.context.object.id_properties_ui(prop_name)
            property_manager.update(min=-200, max=200)
        if stjerne_i3d:
            bpy.ops.i3dio_user_attribute_list.new_item()
            bpy.context.object.i3d_user_attributes.attribute_list[0].name = "collisionHeight"
            bpy.context.object.i3d_user_attributes.attribute_list[0].type = 'data_float'
            bpy.context.object.i3d_user_attributes.attribute_list[0].data_float = 4

        doors = self.create_skel_node("10_doors", parent)
        self.create_trigger("doorTrigger", 3145728, "300000", doors)
        lights = self.create_skel_node("11_lights", parent)
        real_lights = self.create_skel_node("realLights", lights)
        real_lights_low = self.create_skel_node("realLightsLow", real_lights)
        self.create_point_light("pointLightLow", real_lights_low)
        real_lights_high = self.create_skel_node("realLightsHigh", real_lights)
        self.create_spot_light("spotLightHigh", real_lights_high)
        self.create_skel_node("linkedLights", lights)
        self.create_skel_node("lightSwitch", lights)

    def create_cameras(self, fov):
        bpy.ops.object.empty_add(radius=0)
        camera_group = bpy.context.active_object
        camera_group.name = '2_cameras'
        bpy.ops.object.empty_add(radius=0)
        outdoor_camera_group = bpy.context.active_object
        outdoor_camera_group.name = 'outdoorCameraTarget'
        outdoor_camera_group.parent = camera_group
        outdoor_camera_group.rotation_euler = (math.radians(-24), 0, math.radians(-180))
        bpy.ops.object.camera_add()
        outdoor_camera = bpy.context.active_object
        outdoor_camera.name = 'outdoorCamera'
        outdoor_camera.parent = outdoor_camera_group
        outdoor_camera.rotation_euler = (math.radians(90), 0, 0)
        outdoor_camera.location = (0, -11, 0)
        outdoor_camera = bpy.context.object.data
        outdoor_camera.lens = 54.43
        outdoor_camera.clip_start = 0.3
        outdoor_camera.clip_end = 5000
        bpy.ops.object.camera_add()
        indoor_camera = bpy.context.active_object
        indoor_camera.name = 'indoorCamera'
        indoor_camera.parent = camera_group
        indoor_camera.rotation_euler = (math.radians(72), 0, math.radians(-180))
        indoor_camera = bpy.context.object.data
        indoor_camera.lens = fov
        indoor_camera.clip_end = 5000
        bpy.ops.object.empty_add(radius=0)
        camera_raycast_node1_group = bpy.context.active_object
        camera_raycast_node1_group.name = 'cameraRaycastNode1'
        camera_raycast_node1_group.parent = camera_group
        bpy.ops.object.empty_add(radius=0)
        camera_raycast_node2_group = bpy.context.active_object
        camera_raycast_node2_group.name = 'cameraRaycastNode2'
        camera_raycast_node2_group.parent = camera_group
        bpy.ops.object.empty_add(radius=0)
        camera_raycast_node3_group = bpy.context.active_object
        camera_raycast_node3_group.name = 'cameraRaycastNode3'
        camera_raycast_node3_group.parent = camera_group
        bpy.ops.object.select_grouped(type='PARENT')
        return camera_group

    def create_cameras_vehicle(self):
        return self.create_cameras(60)

    def create_cameras_harvester(self):
        return self.create_cameras(75)

    def create_light(self, name, parent, cone_angle, light_range, drop_off, rgb, translate=(0, 0, 0), rotation=(0, 0, 0), cast_shadow_map=False):
        bpy.ops.object.light_add(type='SPOT')
        light = bpy.context.object.data
        light.spot_size = cone_angle
        light.spot_blend = drop_off
        light.color = rgb
        light.cutoff_distance = light_range
        if cast_shadow_map is False:
            bpy.context.object.data.use_shadow = False
        bpy.context.active_object.location = translate
        translate = (0, 0, 0)
        bpy.context.active_object.rotation_euler = rotation
        rotation = (0, 0, 0)
        light_transform = bpy.context.active_object
        light_transform.parent = parent
        light_transform.name = name
        if giants_i3d:
            light_transform['I3D_collision'] = False
            light_transform['I3D_static'] = False
            light_transform['I3D_clipDistance'] = 75.00
        if stjerne_i3d:
            bpy.context.object.i3d_attributes.clip_distance = 75
        return light_transform

    def create_point_light(self, name, parent, light_range=18, rgb=(0.44, 0.4, 0.4), clip_distance=75.00):
        bpy.ops.object.light_add(type='POINT')
        light = bpy.context.object.data
        light.color = rgb
        light.cutoff_distance = light_range
        light.use_shadow = False
        light = bpy.context.active_object
        light.parent = parent
        light.name = name
        if giants_i3d:
            light['I3D_collision'] = False
            light['I3D_static'] = False
            light['I3D_clipDistance'] = clip_distance
        if stjerne_i3d:
            bpy.context.object.i3d_attributes.clip_distance = clip_distance
        return light

    def create_spot_light(self, name, parent, cone_angle=math.radians(120), light_range=18, drop_off=4, rgb=(0.55, 0.5, 0.5), clip_distance=75):
        bpy.ops.object.light_add(type='SPOT')
        light = bpy.context.object.data
        light.spot_size = cone_angle
        light.spot_blend = drop_off
        light.color = rgb
        light.cutoff_distance = light_range
        light.use_shadow = False
        light = bpy.context.active_object
        light.parent = parent
        light.name = name
        if giants_i3d:
            light['I3D_collision'] = False
            light['I3D_static'] = False
            light['I3D_clipDistance'] = clip_distance
        if stjerne_i3d:
            bpy.context.object.i3d_attributes.clip_distance = clip_distance
        return light

    def create_collision(self, name, col_mask, col_mask_stjerne, parent, size=(1.0, 1.0, 1.0)):
        bpy.ops.mesh.primitive_cube_add()
        bpy.context.active_object.name = name
        bpy.context.object.data.name = name
        bpy.context.object.dimensions = size
        bpy.ops.object.transform_apply(scale=True)
        bpy.context.active_object.parent = parent
        trigger = bpy.context.active_object
        if giants_i3d:
            trigger['I3D_collision'] = True
            trigger['I3D_static'] = True
            trigger['I3D_trigger'] = True
            trigger['I3D_nonRenderable'] = True
            trigger['I3D_castsShadows'] = True
            trigger['I3D_receiveShadows'] = True
            trigger['I3D_collisionMask'] = col_mask
        if stjerne_i3d:
            bpy.context.object.i3d_attributes.rigid_body_type = 'static'
            bpy.context.object.i3d_attributes.trigger = True
            bpy.context.object.i3d_attributes.collision_mask = col_mask_stjerne
            bpy.context.object.data.i3d_attributes.casts_shadows = True
            bpy.context.object.data.i3d_attributes.receive_shadows = True
            bpy.context.object.data.i3d_attributes.non_renderable = True
        return trigger

    def create_trigger(self, name, col_mask, col_mask_stjerne, parent, size=(1.0, 1.0, 1.0)):
        bpy.ops.mesh.primitive_cube_add()
        bpy.context.active_object.name = name
        bpy.context.object.data.name = name
        bpy.context.object.dimensions = size
        bpy.ops.object.transform_apply(scale=True)
        bpy.context.active_object.parent = parent
        trigger = bpy.context.active_object
        if giants_i3d:
            trigger['I3D_collision'] = True
            trigger['I3D_static'] = True
            trigger['I3D_trigger'] = True
            trigger['I3D_nonRenderable'] = True
            trigger['I3D_castsShadows'] = True
            trigger['I3D_receiveShadows'] = True
            trigger['I3D_collisionMask'] = col_mask
        if stjerne_i3d:
            bpy.context.object.i3d_attributes.rigid_body_type = 'static'
            bpy.context.object.i3d_attributes.trigger = True
            bpy.context.object.i3d_attributes.collision_mask = col_mask_stjerne
            bpy.context.object.data.i3d_attributes.casts_shadows = True
            bpy.context.object.data.i3d_attributes.receive_shadows = True
            bpy.context.object.data.i3d_attributes.non_renderable = True
        return trigger

    def create_exact_fill_root_node(self, name, parent, size=(1.0, 1.0, 1.0)):
        bpy.ops.mesh.primitive_cube_add()
        bpy.context.active_object.name = name
        bpy.context.object.data.name = name
        bpy.context.object.dimensions = size
        bpy.ops.object.transform_apply(scale=True)
        bpy.context.active_object.parent = parent
        bpy.ops.object.parent_set(type='OBJECT', keep_transform=False)
        exact_fill_root_node = bpy.context.active_object
        if giants_i3d:
            exact_fill_root_node['I3D_collision'] = True
            exact_fill_root_node['I3D_static'] = True
            exact_fill_root_node['I3D_trigger'] = True
            exact_fill_root_node['I3D_nonRenderable'] = True
            exact_fill_root_node['I3D_castsShadows'] = True
            exact_fill_root_node['I3D_receiveShadows'] = True
            exact_fill_root_node['I3D_collisionMask'] = 1073741824
        if stjerne_i3d:
            bpy.context.object.i3d_attributes.rigid_body_type = 'static'
            bpy.context.object.i3d_attributes.collision_mask = "40000000"
            bpy.context.object.i3d_attributes.trigger = True
            bpy.context.object.data.i3d_attributes.casts_shadows = True
            bpy.context.object.data.i3d_attributes.receive_shadows = True
            bpy.context.object.data.i3d_attributes.non_renderable = True
        return exact_fill_root_node.name

    def create_plane(self, name, parent, size=(1.0, 1.0, 1.0)):
        bpy.ops.mesh.primitive_plane_add()
        bpy.context.active_object.name = name
        bpy.context.object.data.name = name
        bpy.context.object.dimensions = size
        bpy.ops.object.transform_apply(scale=True)
        bpy.context.active_object.parent = parent
        plane = bpy.context.active_object.name
        return plane

    def create_vehicle_component(self, name, data_name, size=(1.0, 1.0, 1.0), translate=(0, 0, 0)):
        bpy.ops.mesh.primitive_cube_add()
        bpy.context.active_object.name = name
        bpy.context.object.data.name = name
        bpy.context.object.data.name = data_name
        bpy.context.object.dimensions = size
        bpy.ops.object.transform_apply(scale=True)
        bpy.context.active_object.location = translate
        translate = (0, 0, 0)
        component = bpy.context.active_object
        if giants_i3d:
            component['I3D_dynamic'] = True
            component['I3D_collision'] = True
            component['I3D_compound'] = True
            component['I3D_collisionMask'] = 2109442.0
            component['I3D_clipDistance'] = 300.0
            component['I3D_castsShadows'] = True
            component['I3D_receiveShadows'] = True
            component['I3D_nonRenderable'] = True
        if stjerne_i3d:
            bpy.context.object.i3d_attributes.rigid_body_type = 'dynamic'
            bpy.context.object.i3d_attributes.compound = True
            bpy.context.object.i3d_attributes.collision_mask = "203002"
            bpy.context.object.i3d_attributes.clip_distance = 300
            bpy.context.object.data.i3d_attributes.casts_shadows = True
            bpy.context.object.data.i3d_attributes.receive_shadows = True
            bpy.context.object.data.i3d_attributes.non_renderable = True

    def execute(self, context):
        if len(bpy.context.selected_objects) > 0:
            mode = bpy.context.object.mode
            for obj in bpy.context.selected_objects:
                if not obj.type == "MESH":
                    continue
                if not mode == 'OBJECT':
                    bpy.ops.object.mode_set(mode='OBJECT')

        name = context.scene.i3dea.skeletons_dropdown
        getattr(I3DEA_OT_skeletons, name)(self)
        self.report({'INFO'}, name + " skeleton added")
        return {'FINISHED'}
