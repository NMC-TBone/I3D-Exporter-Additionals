"""skeletons.py contains skeleton setup for vehicles, tools and placeables"""

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

#--------------------------------------------------------------------------------------
#  Converted/inspired from skeletons script in maya i3d exporter, plugins/Skeletons.py
#--------------------------------------------------------------------------------------

import bpy
import math

from .. import checkI3DexporterType

giantsI3D, stjerneI3D, dcc, I3DRemoveAttributes = checkI3DexporterType()

class TOOLS_OT_skeletons(bpy.types.Operator):
    bl_label = "Create Button"
    bl_idname = "tools.skeletons_create"
    bl_description = "Creates the selected skeleton from the dropdown menu."
    bl_options = {'REGISTER', 'UNDO'}

    def createSkelNode(self, name, parent, displayHandle=False, translate=(0, 0, 0), rotation=(0, 0, 0)):
        bpy.ops.object.empty_add(radius=0)
        node = bpy.context.active_object
        node.name = name
        node.parent = parent
        node.location = translate
        translate = (0, 0, 0)
        node.rotation_euler = rotation
        rotation = (0, 0, 0)
        if displayHandle:
            self.setDisplayHandle(node)
        return node

    def createBaseVehicle(self):
        self.createBaseVec(False)
        return

    def createBaseHarvester(self):
        self.createBaseVec(True)
        return

    def createAttacherJoints(self):
        return self.createVehicleAttacherJoints(False)
        
    def createBaseVec(self, isHarvester):
        self.createVehicleComponent("vehicleName_main_component1", "vehicleName_main_component1")
        vehicle = bpy.context.active_object
        vehicle_vis = self.createSkelNode("1_vehicleName_root(REPLACE_WITH_MESH)", vehicle)
        self.createSkelNode("1_wheels", vehicle_vis)
        cameras = ""
        if isHarvester:
            cameras = self.createCamerasHarvester()
        else:
            cameras = self.createCamerasVehicle()
        cameras = bpy.context.active_object
        cameras.parent = vehicle_vis
        self.createLights()
        createLights = bpy.context.active_object
        createLights.parent = vehicle_vis
        self.createSkelNode("4_exitPoint", vehicle_vis)
        cabin = self.createSkelNode("5_cabin_REPLACE_WITH_MESH", vehicle_vis)
        steeringBase = self.createSkelNode("1_steeringBase", cabin)
        steeringWheel = self.createSkelNode("steeringWheel_REPLACE_WITH_MESH", steeringBase)
        self.createSkelNode("playerRightHandTarget", steeringWheel, True, translate=(-0.189, 0.023, 0.03), rotation=(math.radians(-4.70569), math.radians(-50.8809), math.radians(-7.47474)))
        self.createSkelNode("playerLeftHandTarget", steeringWheel, True, translate=(0.189, 0.023, 0.03), rotation=(math.radians(-16.3303), math.radians(50.8809), math.radians(-7.47473)))
        seat = self.createSkelNode("2_seat_REPLACE_WITH_MESH", cabin)
        self.createSkelNode("playerSkin", seat, True)
        self.createSkelNode("3_lights_cabin", cabin)
        self.createSkelNode("4_wipers", cabin)
        self.createSkelNode("5_dashboards", cabin)
        self.createSkelNode("6_levers", cabin)
        self.createSkelNode("7_pedals", cabin)
        characterTargets = self.createSkelNode("8_characterTargets", cabin, False) 
        self.createSkelNode("playerRightFootTarget", characterTargets, True)
        self.createSkelNode("playerLeftFootTarget", characterTargets, True)
        self.createSkelNode("9_mirrors_cabin", cabin)
        self.createSkelNode("10_visuals_cabin", cabin)
        attacherJoints = ""
        if isHarvester:
            attacherJoints = self.createVehicleAttacherJoints(True)
        else:
            attacherJoints = self.createVehicleAttacherJoints(False)
        attacherJoints = bpy.context.active_object
        attacherJoints.parent = vehicle_vis
        ai = self.createSkelNode("7_ai", vehicle_vis)
        self.createSkelNode("aiCollisionTrigger_REPLACE_WITH_MESH", ai)
        exhaustParticles = None
        if isHarvester:
            exhaustParticles = self.createSkelNode("particles", vehicle_vis)
        else:
            exhaustParticles = self.createSkelNode("8_exhaustParticles", vehicle_vis)
        self.createSkelNode("exhaustParticle1", exhaustParticles, True)
        self.createSkelNode("exhaustParticle2", exhaustParticles, True)
        if isHarvester:
            self.createSkelNode("movingParts", vehicle_vis)
        self.createSkelNode("9_hydraulics", vehicle_vis)
        self.createSkelNode("10_mirrors", vehicle_vis)
        self.createSkelNode("11_configurations", vehicle_vis)
        if isHarvester:
            self.createSkelNode("fillVolume", vehicle_vis)
            workAreas = self.createSkelNode("workAreas", vehicle_vis)
            workAreaStraw = self.createSkelNode("workAreaStraw", workAreas)
            self.createSkelNode("workAreaStrawStart", workAreaStraw)
            self.createSkelNode("workAreaStrawWidth", workAreaStraw)
            self.createSkelNode("workAreaStrawHeight", workAreaStraw)
            workAreaChopper = self.createSkelNode("workAreaChopper", workAreas)
            self.createSkelNode("workAreaChopperStart", workAreaChopper)
            self.createSkelNode("workAreaChopperWidth", workAreaChopper)
            self.createSkelNode("workAreaChopperHeight", workAreaChopper)
        self.createSkelNode("12_visuals", vehicle_vis)
        self.createSkelNode("2_skinnedMeshes", vehicle)
        self.createSkelNode("3_collisions", vehicle)
        return vehicle
    
    def createBaseTool(self):
        self.createVehicleComponent("toolName_main_component1", "toolName_main_component1")
        tool = bpy.context.active_object
        vehicle_vis = self.createSkelNode("1_toolName_root", tool)
        attachable = self.createSkelNode("1_attachable", vehicle_vis)
        self.createSkelNode("attacherJoint", attachable)
        self.createSkelNode("topReferenceNode", attachable)
        self.createSkelNode("ptoInputNode", attachable)
        self.createSkelNode("support", attachable)
        self.createSkelNode("connectionHoses", attachable)
        self.createSkelNode("wheelChocks", attachable)
        self.createSkelNode("2_wheels", vehicle_vis)
        self.createLights()
        createLights = bpy.context.active_object
        createLights.parent = vehicle_vis
        self.createSkelNode("4_movingParts", vehicle_vis)
        self.createSkelNode("5_fillUnit", vehicle_vis)
        workArea = self.createSkelNode("6_workArea", vehicle_vis)
        self.createSkelNode("workAreaStart", workArea)
        self.createSkelNode("workAreaWidth", workArea)
        self.createSkelNode("workAreaHeight", workArea)
        self.createSkelNode("7_effects", vehicle_vis)
        ai = self.createSkelNode("8_ai", vehicle_vis)
        aiMarkers = self.createSkelNode("aiMarkers", ai)
        self.createSkelNode("aiMarkerLeft", aiMarkers)
        self.createSkelNode("aiMarkerRight", aiMarkers)
        self.createSkelNode("aiMarkerBack", aiMarkers)
        sizeMarkers = self.createSkelNode("sizeMarkers", ai)
        self.createSkelNode("sizeMarkerLeft", sizeMarkers)
        self.createSkelNode("sizeMarkerRight", sizeMarkers)
        self.createSkelNode("sizeMarkerBack", sizeMarkers)
        self.createSkelNode("aiCollisionNode", ai)
        self.createSkelNode("9_visuals", vehicle_vis)
        self.createSkelNode("2_skinnedMeshes", tool)
        self.createSkelNode("3_collisions", tool)
        return tool
    
    def createPlayer(self, steeringWheel=None):
        bpy.ops.object.empty_add(radius=0)
        playerRoot = bpy.context.active_object
        playerRoot.name = 'playerRoot'
        self.createSkelNode("player_skin", playerRoot, True)
        self.createSkelNode("player_rightFoot", playerRoot, True, translate=(-0.184, -0.393, -0.514), rotation=(0, 0, math.radians(10)))
        self.createSkelNode("player_leftFoot", playerRoot, True, translate=(0.184, -0.393, -0.514), rotation=(0, 0, math.radians(-10)))
        if steeringWheel is not None and steeringWheel is not False:
            self.createSkelNode("playerRightHandTarget", playerRoot, True, translate=(-0.188, -0.022, 0.03), rotation=(math.radians(-10.518), math.radians(51.12), math.radians(-4.708)))
            self.createSkelNode("playerLeftHandTarget", playerRoot, True, translate=(0.189, -0.023, 0.03), rotation=(math.radians(-10.518), math.radians(-51.12), math.radians(-4.708)))
        return playerRoot

    def setDisplayHandle(self, node):
        node = bpy.context.object
        node.empty_display_type = 'ARROWS'
        node.empty_display_size = 0.25

    def createCamerasVehicle(self):
        return self.createCameras(60)

    def createCamerasHarvester(self):
        return self.createCameras(75)

    def createCameras(self, fov):
        bpy.ops.object.empty_add(radius=0)
        cameraGroup = bpy.context.active_object
        cameraGroup.name = '2_cameras'
        bpy.ops.object.empty_add(radius=0)
        outdoorCameraGroup = bpy.context.active_object
        outdoorCameraGroup.name = 'outdoorCameraTarget'
        outdoorCameraGroup.parent = cameraGroup
        outdoorCameraGroup.rotation_euler = (math.radians(-24), 0, math.radians(-180))
        bpy.ops.object.camera_add()
        outdoorCamera = bpy.context.active_object
        outdoorCamera.name = 'outdoorCamera'
        outdoorCamera.parent = outdoorCameraGroup
        outdoorCamera.rotation_euler = (math.radians(90), 0, 0)
        outdoorCamera.location = (0, -11, 0)
        outdoorCamera = bpy.context.object.data
        outdoorCamera.lens = 54.43
        outdoorCamera.clip_start = 0.3
        outdoorCamera.clip_end = 5000
        bpy.ops.object.camera_add()
        indoorCamera = bpy.context.active_object
        indoorCamera.name = 'indoorCamera'
        indoorCamera.parent = cameraGroup
        indoorCamera.rotation_euler = (math.radians(72), 0, math.radians(-180))
        indoorCamera = bpy.context.object.data
        indoorCamera.lens = fov
        indoorCamera.clip_end = 5000
        bpy.ops.object.empty_add(radius=0)
        cameraRaycastNode1Group = bpy.context.active_object
        cameraRaycastNode1Group.name = 'cameraRaycastNode1'
        cameraRaycastNode1Group.parent = cameraGroup
        bpy.ops.object.empty_add(radius=0)
        cameraRaycastNode2Group = bpy.context.active_object
        cameraRaycastNode2Group.name = 'cameraRaycastNode2'
        cameraRaycastNode2Group.parent = cameraGroup
        bpy.ops.object.empty_add(radius=0)
        cameraRaycastNode3Group = bpy.context.active_object
        cameraRaycastNode3Group.name = 'cameraRaycastNode3'
        cameraRaycastNode3Group.parent = cameraGroup
        bpy.ops.object.select_grouped(type='PARENT')
        return cameraGroup

        # ------------------- LIGHTS VEHICLE -------------------
    def createLights(self):
        bpy.ops.object.empty_add(radius=0)
        lightsGroup = bpy.context.active_object
        lightsGroup.name = '3_lights'
        self.createSkelNode("1_sharedLights", lightsGroup)
        self.createSkelNode("2_staticLights", lightsGroup)
        # default lights
        defaultLights = self.createSkelNode("3_defaultLights", lightsGroup)
        # Blender
        # (self, name, parent, coneAngle, range, dropOff, rgb, translate=(0, 0, 0), rotation=(0, 0, 0), castShadowMap=False)
        # Maya
        # (self, name, parent, coneAngle, intensity, dropOff, rgb, locatorScale=50, rotation=['0deg', '0deg', '0deg'], translation=[0, 0, 0], castShadowMap=False, depthMapBias=0.001, depthMapResolution=256)
        self.createLight('frontLightLow', defaultLights, math.radians(80), 20, 0.6, (0.85, 0.85, 1), rotation=(math.radians(-75), 0, 0))
        self.createLight('highBeamLow', defaultLights, math.radians(70), 30, 0.4, (0.85, 0.85, 1), rotation=(math.radians(-80), 0, 0))
        frontLightHigh = self.createLight('frontLightHigh', defaultLights, math.radians(70), 25, 0.6, (0.85, 0.85, 1), rotation=(math.radians(-75), 0, math.radians(8)))
        self.createLight('frontLightHigh1', frontLightHigh, math.radians(70), 25, 0.6, (0.85, 0.85, 1), rotation=(0, math.radians(16), 0))
        highBeamHigh = self.createLight('highBeamHigh', defaultLights, math.radians(30), 60, 0.5, (0.85, 0.85, 1), rotation=(math.radians(-80), 0, math.radians(5)))
        self.createLight('highBeamHigh2', highBeamHigh, math.radians(30), 60, 0.5, (0.85, 0.85, 1), rotation=(0, math.radians(10), 0))
        self.createLight('licensePlateLightHigh', defaultLights, 120, 0.5, 2, (1, 1, 1), rotation=(math.radians(90), 0, 0))
        bpy.ops.object.light_add(type='POINT')
        pointLight = bpy.context.object.data
        pointLight.name = "interiorScreenLight"
        pointLight.cutoff_distance = 0.25
        pointLight.color = (0.59, 0.653079, 1)
        bpy.context.active_object.parent = defaultLights
        workLights = self.createSkelNode("4_workLights", lightsGroup)
        self.createLight('workLightFrontLow', workLights, math.radians(130), 20, 0.4, (0.85, 0.85, 1), rotation=(math.radians(-80), 0, 0))
        workLightFrontHigh1 = self.createLight('workLightFrontHigh', workLights, math.radians(90), 25, 0.4, (0.85, 0.85, 1), rotation=(math.radians(-65), 0, math.radians(15)))
        self.createLight('workLightFrontHigh2', workLightFrontHigh1, math.radians(90), 25, 0.4, (0.85, 0.85, 1), rotation=(0, math.radians(30), 0))
        # work lights back
        self.createLight('workLightBackLow', workLights, math.radians(130), 20, 0.4, (0.85, 0.85, 1), rotation=(math.radians(70), 0, 0))
        workLightBackHigh1 = self.createLight('workLightBackHigh', workLights, math.radians(90), 25, 0.4, (0.85, 0.85, 1), rotation=(math.radians(70), 0, math.radians(-20)))
        self.createLight('workLightBackHigh2', workLightBackHigh1, math.radians(90), 25, 0.4, (0.85, 0.85, 1), rotation=(math.radians(5.41377), math.radians(37.1585), math.radians(16.0129)))
        # back lights
        backLights = self.createSkelNode("5_backLights", lightsGroup)
        backLightsHigh1 = self.createLight('backLightsHigh', backLights, math.radians(130), 2.5, 0.4, (0.5, 0, 0), rotation=(math.radians(-75), 0, math.radians(-180)))
        self.createLight('backLightsHigh2', backLightsHigh1, math.radians(130), 2.5, 0.4, (0.5, 0, 0), rotation=(0, 0, 0))
        # turn lights
        turnLights = self.createSkelNode("6_turnLights", lightsGroup)
        turnLightLeftFront = self.createLight('turnLightLeftFront', turnLights, math.radians(120), 4, 0.6, (0.31, 0.14, 0), rotation=(math.radians(75), 0, math.radians(-180)))
        self.createLight('turnLightLeftBack', turnLightLeftFront, math.radians(120), 4, 0.6, (0.31, 0.14, 0), rotation=(math.radians(-30), 0, math.radians(-180)))
        turnLightRightFront = self.createLight('turnLightRightFront', turnLights, math.radians(120), 4, 0.6, (0.31, 0.14, 0), rotation=(math.radians(75), 0, 0))
        self.createLight('turnLightRightBack', turnLightRightFront, math.radians(120), 4, 0.6, (0.31, 0.14, 0), rotation=(math.radians(-30), 0, math.radians(-180)))
        # beacon lights
        beaconLights = self.createSkelNode("7_beaconLights", lightsGroup)
        self.createSkelNode("beaconLight1", beaconLights)
        # reverse lights
        reverseLights = self.createSkelNode("8_reverseLights", lightsGroup)
        reverseLight1 = self.createLight('reverseLightHigh', reverseLights, math.radians(130), 2.5, 0.6, (0.9, 0.9, 1), rotation=(math.radians(75), 0, 0))
        self.createLight('reverseLightHigh2', reverseLight1, math.radians(130), 2.5, 0.6, (0.9, 0.9, 1))
        bpy.ops.object.select_grouped(type='PARENT')
        bpy.ops.object.select_grouped(type='PARENT')
        bpy.ops.object.select_grouped(type='PARENT')
        return lightsGroup

        # vehicle
    def createLight(self, name, parent, coneAngle, range, dropOff, rgb, translate=(0, 0, 0), rotation=(0, 0, 0), castShadowMap=False):
        bpy.ops.object.light_add(type='SPOT')
        light = bpy.context.object.data
        light.spot_size = coneAngle
        light.spot_blend = dropOff
        light.color = rgb
        light.cutoff_distance = range
        if castShadowMap is False:
            bpy.context.object.data.use_shadow = False
        bpy.context.active_object.location = translate
        translate = (0, 0, 0)
        bpy.context.active_object.rotation_euler = rotation
        rotation = (0, 0, 0)
        lightTransform = bpy.context.active_object
        lightTransform.parent = parent
        lightTransform.name = name
        light = lightTransform.name
        if giantsI3D == True:
            dcc.I3DSetAttrBool(light,'I3D_collision',False)
            dcc.I3DSetAttrBool(light,'I3D_static',False)
            dcc.I3DSetAttrFloat(light,'I3D_clipDistance',75)
        if stjerneI3D == True:
            bpy.context.object.i3d_attributes.clip_distance = 75
        return lightTransform
    
    # placeable, low
    def createPointLight(self, name, parent, range=18, rgb=(0.44, 0.4, 0.4), clipDistance=75):
        bpy.ops.object.light_add(type='POINT')
        light = bpy.context.object.data
        light.color = rgb
        light.cutoff_distance = range
        light.use_shadow = False
        light = bpy.context.active_object
        light.parent = parent
        light.name = name
        light = light.name
        if giantsI3D == True:
            dcc.I3DSetAttrBool(light,'I3D_collision',False)
            dcc.I3DSetAttrBool(light,'I3D_static',False)
            dcc.I3DSetAttrFloat(light,'I3D_clipDistance',clipDistance)
        if stjerneI3D == True:
            bpy.context.object.i3d_attributes.clip_distance = clipDistance
        return light

    # placeable, high
    def createSpotLight(self, name, parent, coneAngle=math.radians(120), range=18, dropOff=4, rgb=(0.55, 0.5, 0.5), clipDistance=75):
        bpy.ops.object.light_add(type='SPOT')
        light = bpy.context.object.data
        light.spot_size = coneAngle
        light.spot_blend = dropOff
        light.color = rgb
        light.cutoff_distance = range
        light.use_shadow = False
        light = bpy.context.active_object
        light.parent = parent
        light.name = name
        light = light.name
        if giantsI3D == True:
            dcc.I3DSetAttrBool(light,'I3D_collision',False)
            dcc.I3DSetAttrBool(light,'I3D_static',False)
            dcc.I3DSetAttrFloat(light,'I3D_clipDistance',clipDistance)
        if stjerneI3D == True:
            bpy.context.object.i3d_attributes.clip_distance = clipDistance
        return light

    def createVehicleAttacherJoints(self, isHarvester):
        bpy.ops.object.empty_add(radius=0)
        attacherJointGroup = bpy.context.active_object
        attacherJointGroup.name = '6_attacherJoints'
        tools = self.createSkelNode("1_tools", attacherJointGroup)
        trailers = self.createSkelNode("2_trailers", attacherJointGroup)
        ptos = self.createSkelNode("3_ptos", attacherJointGroup)
        self.createSkelNode("4_connectionHoses", attacherJointGroup)
        if not isHarvester:
            # attacherjointbackrot
            attacherJointBackRot = self.createSkelNode("attacherJointBackRot", tools, rotation=(math.radians(13), 0, math.radians(-180)))
            attacherJointBackRot2 = self.createSkelNode("attacherJointBackRot2", attacherJointBackRot, translate=(0, -1, 0), rotation=(math.radians(13), 0, math.radians(-180)))
            self.createSkelNode("attacherJointBack", attacherJointBackRot2, True, rotation=(0, 0, math.radians(-90)))
            # attacherjointbackbottomarm
            attacherJointBackArmBottom = self.createSkelNode("attacherJointBackArmBottom", tools, rotation=(math.radians(13), 0, math.radians(-180)))
            attacherJointBackArmBottomTrans = self.createSkelNode("attacherJointBackArmBottomTrans_REPLACE_WITH_MESH", attacherJointBackArmBottom)
            self.createSkelNode("referencePointBackBottom", attacherJointBackArmBottomTrans, translate=(0, -1, 0))
            # attacherjointbacktoparm
            self.createSkelNode("attacherJointBackArmTop", tools, rotation=(math.radians(67), 0, 0))
        # attacherjointfrontrot
        attacherJointFrontRot = self.createSkelNode("attacherJointFrontRot", tools, rotation=(math.radians(-13), 0, 0))
        attacherJointFrontRot2 = self.createSkelNode("attacherJointFrontRot2", attacherJointFrontRot, translate=(0, -1, 0), rotation=(math.radians(13), 0, 0))
        self.createSkelNode("attacherJointFront", attacherJointFrontRot2, True, rotation=(0, 0, math.radians(90)))
        # attacherjointfrontbottomarm
        attacherJointFrontArmBottom = self.createSkelNode("attacherJointFrontArmBottom", tools, rotation=(math.radians(-26), 0, 0))
        attacherJointFrontArmBottomTrans = self.createSkelNode("attacherJointFrontArmBottomTrans_REPLACE_WITH_MESH", attacherJointFrontArmBottom)
        self.createSkelNode("referencePointFrontBottom", attacherJointFrontArmBottomTrans, translate=(0, -1, 0))
        # attacherjointfronttoparm
        self.createSkelNode("attacherJointFrontArmTop", tools, True, rotation=(math.radians(-40), 0, 0))
        # trailer joints
        self.createSkelNode("trailerAttacherJointBack", trailers, True, rotation=(0, 0, math.radians(-90)))
        if not isHarvester:
            self.createSkelNode("trailerAttacherJointBackLow", trailers, True, rotation=(0, 0, math.radians(-90)))
        if not isHarvester:
            self.createSkelNode("trailerAttacherJointFront", trailers, True, rotation=(0, 0, math.radians(-90)))
        # ptos
        if not isHarvester:
            self.createSkelNode("ptoBack", ptos, True, rotation=(0, 0, math.radians(-180)))
        self.createSkelNode("ptoFront", ptos, True)
        if not isHarvester:
            self.createSkelNode("5_frontloader", attacherJointGroup, True)
        if not isHarvester:
            bpy.ops.object.select_grouped(type='PARENT')
        else:
            bpy.ops.object.select_grouped(type='PARENT')
            bpy.ops.object.select_grouped(type='PARENT')
        return attacherJointGroup

    def createTrafficVehicle(self):
        bpy.ops.object.empty_add(radius=0)
        trafficVehicle = bpy.context.active_object
        trafficVehicle.name = 'trafficVehicle01'
        self.createSkelNode("1_wheels", trafficVehicle)
        lights = self.createSkelNode("lights", trafficVehicle)
        self.createSkelNode("staticLights", lights)
        realLights = self.createSkelNode("realLights", lights)
        self.createLight('frontLightLow', realLights, math.radians(80), 20, 0.6, (0.85, 0.85, 1), rotation=(math.radians(-80), 0, 0), translate=(0, -3.5, 0.6), castShadowMap=False)
        frontLightHigh1 = self.createLight('frontLightHigh1', realLights, math.radians(70), 25, 0.4, (0.85, 0.85, 1), rotation=(math.radians(-80), 0, math.radians(8)), translate=(-0.5, -3.5, 0.6))
        self.createLight('frontLightHigh2', frontLightHigh1, math.radians(70), 25, 0.4, (0.85, 0.85, 1), rotation=(math.radians(-80), 0, math.radians(-8)), translate=(0.5, -3.5, 0.6))
        self.createLight('backLightHigh1', frontLightHigh1, math.radians(130), 2.5, 0.4, (0.5, 0, 0), rotation=(math.radians(160), 0, 0), translate=(-0.5, 1, 0.8))
        self.createLight('backLightHigh2', frontLightHigh1, math.radians(130), 2.5, 0.4, (0.5, 0, 0), rotation=(math.radians(160), 0, 0), translate=(0.5, 1, 0.8))
        self.createSkelNode("trafficCollisionNode", trafficVehicle)
        self.createSkelNode("driver_TO_BE_REPLACED", trafficVehicle)
        self.createSkelNode("vehicle_vis", trafficVehicle)
        return trafficVehicle

    def createPlaceable(self):
        bpy.ops.object.empty_add(radius=0)
        placeable = bpy.context.active_object
        placeable.name = 'placeable'
        self.createPlaceableElements(placeable)
        return placeable
    
    def createAnimalHusbandry(self):
        bpy.ops.object.empty_add(radius=0)
        animalHusbandry = bpy.context.active_object
        animalHusbandry.name = 'animalHusbandry'
        food = self.createSkelNode("1_1_food", animalHusbandry)
        self.createSkelNode("fillVolume", food)
        self.createExactFillRootNode("exactFillRootNodeFood", food)
        foodPlaces = self.createSkelNode("foodPlaces", food)
        self.createSkelNode("foodPlace1", foodPlaces)
        self.createSkelNode("foodPlace2", foodPlaces)
        self.createSkelNode("foodPlace3", foodPlaces)
        self.createSkelNode("1_2_storage", animalHusbandry)
        straw = self.createSkelNode("1_3_straw", animalHusbandry)
        self.createPlane("strawPlane", straw, (5, 5, 0))
        self.createExactFillRootNode("exactFillRootNodeStraw", straw)
        milktank = self.createSkelNode("1_4_milktank", animalHusbandry)
        self.createTrigger("milktankTrigger", 2097152, "200000", milktank)
        lqiuidManureTank = self.createSkelNode("1_5_lqiuidManureTank", animalHusbandry)
        self.createTrigger("lqiuidManureTankTrigger", 2097152, "200000", lqiuidManureTank)
        waterPlaces = self.createSkelNode("6_waterPlaces", animalHusbandry)
        self.createSkelNode("waterPlace1", waterPlaces)
        self.createSkelNode("waterPlace2", waterPlaces)
        self.createSkelNode("waterPlace3", waterPlaces)
        palletAreas = self.createSkelNode("1_7_palletAreas", animalHusbandry)
        self.createTrigger("palletTrigger", 2097152, "200000", palletAreas)
        palletArea1Start = self.createSkelNode("palletArea1Start", palletAreas)
        self.createSkelNode("palletArea1End", palletArea1Start)
        palletArea2Start = self.createSkelNode("palletArea2Start", palletAreas)
        self.createSkelNode("palletArea2End", palletArea2Start)
        navRootNode = self.createSkelNode("1_8_navigationRootNode", animalHusbandry)
        self.createPlane("navigationMesh", navRootNode)
        walkingPlane = self.createPlane("walkingPlane", navRootNode)
        if giantsI3D == True:
            dcc.I3DSetAttrBool(walkingPlane,'I3D_collision',True)
            dcc.I3DSetAttrBool(walkingPlane,'I3D_static',True)
            dcc.I3DSetAttrBool(walkingPlane,'I3D_nonRenderable',True)
            dcc.I3DSetAttrBool(walkingPlane,'I3D_castsShadows',True)
            dcc.I3DSetAttrBool(walkingPlane,'I3D_receiveShadows',True)
            dcc.I3DSetAttrFloat(walkingPlane,'I3D_collisionMask',131072)
        if stjerneI3D == True:
            bpy.context.object.i3d_attributes.rigid_body_type = 'static'
            bpy.context.object.i3d_attributes.collision_mask = "20000"
            bpy.context.object.data.i3d_attributes.casts_shadows = True
            bpy.context.object.data.i3d_attributes.receive_shadows = True
            bpy.context.object.data.i3d_attributes.non_renderable = True
        fences = self.createSkelNode("1_9_fences", animalHusbandry)
        fence1 = self.createSkelNode("fence1", fences)
        self.createSkelNode("fence1Node1", fence1, True)
        self.createSkelNode("fence1Node2", fence1, True)
        self.createSkelNode("fence1Node3", fence1, True)
        self.createSkelNode("fence1Node4", fence1, True)
        self.createSkelNode("1_10_warningStripes", animalHusbandry)
        self.createTrigger("1_11_loadingTrigger", 3145728, "300000", animalHusbandry)
        self.createPlaceableElements(animalHusbandry)
        return animalHusbandry

    def createPlaceableElements(self, parent):
        clearAreas = self.createSkelNode("1_clearAreas", parent)
        clearArea1Start = self.createSkelNode("clearArea1Start", clearAreas, True)
        self.createSkelNode("clearArea1Width", clearArea1Start, True, translate=(0, -1, 0))
        self.createSkelNode("clearArea1Height", clearArea1Start, True, translate=(1, 0, 0))
        clearArea2Start = self.createSkelNode("clearArea2Start", clearAreas, True)
        self.createSkelNode("clearArea2Width", clearArea2Start, True, translate=(0, -1, 0))
        self.createSkelNode("clearArea2Height", clearArea2Start, True, translate=(1, 0, 0))
        clearArea3Start = self.createSkelNode("clearArea3Start", clearAreas, True)
        self.createSkelNode("clearArea3Width", clearArea3Start, True, translate=(0, -1, 0))
        self.createSkelNode("clearArea3Height", clearArea3Start, True, translate=(1, 0, 0))
        levelAreas = self.createSkelNode("2_levelAreas", parent)
        levelArea1Start = self.createSkelNode("levelArea1Start", levelAreas, True)
        self.createSkelNode("levelArea1Width", levelArea1Start, True, translate=(0, -1, 0))
        self.createSkelNode("levelArea1Height", levelArea1Start, True, translate=(1, 0, 0))
        levelArea2Start = self.createSkelNode("levelArea2Start", levelAreas, True)
        self.createSkelNode("levelArea2Width", levelArea2Start, True, translate=(0, -1, 0))
        self.createSkelNode("levelArea2Height", levelArea2Start, True, translate=(1, 0, 0))
        levelArea3Start = self.createSkelNode("levelArea3Start", levelAreas, True)
        self.createSkelNode("levelArea3Width", levelArea3Start, True, translate=(0, -1, 0))
        self.createSkelNode("levelArea3Height", levelArea3Start, True, translate=(1, 0, 0))
        paintAreas = self.createSkelNode("3_paintAreas", parent)
        paintArea1Start = self.createSkelNode("paintArea1Start", paintAreas, True)
        self.createSkelNode("paintArea1Width", paintArea1Start, True, translate=(0, -1, 0))
        self.createSkelNode("paintArea1Height", paintArea1Start, True, translate=(1, 0, 0))
        paintArea2Start = self.createSkelNode("paintArea2Start", paintAreas, True)
        self.createSkelNode("paintArea2Width", paintArea2Start, True, translate=(0, -1, 0))
        self.createSkelNode("paintArea2Height", paintArea2Start, True, translate=(1, 0, 0))
        paintArea3Start = self.createSkelNode("paintArea3Start", paintAreas, True)
        self.createSkelNode("paintArea3Width", paintArea3Start, True, translate=(0, -1, 0))
        self.createSkelNode("paintArea3Height", paintArea3Start, True, translate=(1, 0, 0))
        indoorAreas = self.createSkelNode("4_indoorAreas", parent)
        indoorArea1Start = self.createSkelNode("indoorArea1Start", indoorAreas, True)
        self.createSkelNode("indoorArea1Width", indoorArea1Start, True, translate=(0, -1, 0))
        self.createSkelNode("indoorArea1Height", indoorArea1Start, True, translate=(1, 0, 0))
        testAreas = self.createSkelNode("5_testAreas", parent)
        testArea1Start = self.createSkelNode("testArea1Start", testAreas, True)
        self.createSkelNode("testArea1End", testArea1Start, True, translate=(1, -1, 0))
        testArea2Start = self.createSkelNode("testArea2Start", testAreas, True)
        self.createSkelNode("testArea2End", testArea2Start, True, translate=(1, -1, 0))
        testArea3Start = self.createSkelNode("testArea3Start", testAreas, True)
        self.createSkelNode("testArea3End", testArea3Start, True, translate=(1, -1, 0))
        tipOcclusionUpdateAreas = self.createSkelNode("6_tipOcclusionUpdateAreas", parent)
        tipOcclusionUpdateArea1Start = self.createSkelNode("tipOcclusionUpdateArea1Start", tipOcclusionUpdateAreas, True)
        self.createSkelNode("tipOcclusionUpdateArea1End", tipOcclusionUpdateArea1Start, True, translate=(1, -1, 0))
        self.createTrigger("7_infoTrigger", 1048576, "100000", parent, size=(10, 10, 5))
        visuals = self.createSkelNode("8_visuals", parent)
        self.createSkelNode("winter", visuals)
        collisions = self.createSkelNode("9_collisions", parent)
        self.createCollision("collision", 255, "ff", collisions)
        self.createCollision("tipCollision", 524288, "80000", collisions)
        tipColWall = self.createCollision("tipCollisionWall", 524288, "80000", collisions)
        if giantsI3D == True:
            dcc.I3DSetAttrBool(tipColWall, 'collisionHeight', 4)
        doors = self.createSkelNode("10_doors", parent)
        self.createTrigger("doorTrigger", 3145728, "300000", doors)
        lights = self.createSkelNode("11_lights", parent)
        realLights = self.createSkelNode("realLights", lights)
        realLightsLow = self.createSkelNode("realLightsLow", realLights)
        self.createPointLight("pointLightLow", realLightsLow)
        realLightsHigh = self.createSkelNode("realLightsHigh", realLights)
        self.createSpotLight("spotLightHigh", realLightsHigh)
        self.createSkelNode("linkedLights", lights)
        self.createSkelNode("lightSwitch", lights)

    def createCollision(self, name, colMask, colMaskStjerne, parent, size=(1.0, 1.0, 1.0)):
        bpy.ops.mesh.primitive_cube_add()
        bpy.context.active_object.name = name
        bpy.context.object.data.name = name
        bpy.context.object.dimensions = size
        bpy.ops.object.transform_apply(scale=True)
        bpy.context.active_object.parent = parent
        trigger = bpy.context.active_object.name
        if giantsI3D == True:
            dcc.I3DSetAttrBool(trigger,'I3D_collision',True)
            dcc.I3DSetAttrBool(trigger,'I3D_static',True)
            dcc.I3DSetAttrBool(trigger,'I3D_trigger',True)
            dcc.I3DSetAttrBool(trigger,'I3D_nonRenderable',True)
            dcc.I3DSetAttrBool(trigger,'I3D_castsShadows',True)
            dcc.I3DSetAttrBool(trigger,'I3D_receiveShadows',True)
            dcc.I3DSetAttrBool(trigger,'I3D_collisionMask',colMask)
        if stjerneI3D == True:
            bpy.context.object.i3d_attributes.rigid_body_type = 'static'
            bpy.context.object.i3d_attributes.trigger = True
            bpy.context.object.i3d_attributes.collision_mask = colMaskStjerne
            bpy.context.object.data.i3d_attributes.casts_shadows = True
            bpy.context.object.data.i3d_attributes.receive_shadows = True
            bpy.context.object.data.i3d_attributes.non_renderable = True
        return trigger

    def createTrigger(self, name, colMask, colMaskStjerne, parent, size=(1.0, 1.0, 1.0)):
        bpy.ops.mesh.primitive_cube_add()
        bpy.context.active_object.name = name
        bpy.context.object.data.name = name
        bpy.context.object.dimensions = size
        bpy.ops.object.transform_apply(scale=True)
        bpy.context.active_object.parent = parent
        trigger = bpy.context.active_object.name
        if giantsI3D == True:
            dcc.I3DSetAttrBool(trigger,'i3D_collision',True)
            dcc.I3DSetAttrBool(trigger,'I3D_static',True)
            dcc.I3DSetAttrBool(trigger,'I3D_trigger',True)
            dcc.I3DSetAttrBool(trigger,'I3D_nonRenderable',True)
            dcc.I3DSetAttrBool(trigger,'I3D_castsShadows',True)
            dcc.I3DSetAttrBool(trigger,'I3D_receiveShadows',True)
            dcc.I3DSetAttrFloat(trigger,'I3D_collisionMask',colMask)
        if stjerneI3D == True:
            bpy.context.object.i3d_attributes.rigid_body_type = 'static'
            bpy.context.object.i3d_attributes.trigger = True
            bpy.context.object.i3d_attributes.collision_mask = colMaskStjerne
            bpy.context.object.data.i3d_attributes.casts_shadows = True
            bpy.context.object.data.i3d_attributes.receive_shadows = True
            bpy.context.object.data.i3d_attributes.non_renderable = True
        return trigger

    def createExactFillRootNode(self, name, parent, size=(1.0, 1.0, 1.0)):
        bpy.ops.mesh.primitive_cube_add()
        bpy.context.active_object.name = name
        bpy.context.object.data.name = name
        bpy.context.object.dimensions = size
        bpy.ops.object.transform_apply(scale=True)
        bpy.context.active_object.parent = parent
        bpy.ops.object.parent_set(type='OBJECT', keep_transform=False)
        exactFillRootNode = bpy.context.active_object.name
        if giantsI3D == True:
            dcc.I3DSetAttrBool(exactFillRootNode,'I3D_collision',True)
            dcc.I3DSetAttrBool(exactFillRootNode,'I3D_static',True)
            dcc.I3DSetAttrBool(exactFillRootNode,'I3D_trigger',True)
            dcc.I3DSetAttrBool(exactFillRootNode,'I3D_nonRenderable',True)
            dcc.I3DSetAttrBool(exactFillRootNode,'I3D_castsShadows',True)
            dcc.I3DSetAttrBool(exactFillRootNode,'I3D_receiveShadows',True)
            dcc.I3DSetAttrFloat(exactFillRootNode,'I3D_collisionMask',1073741824)
        if stjerneI3D == True:
            bpy.context.object.i3d_attributes.rigid_body_type = 'static'
            bpy.context.object.i3d_attributes.collision_mask = "40000000"
            bpy.context.object.i3d_attributes.trigger = True
            bpy.context.object.data.i3d_attributes.casts_shadows = True
            bpy.context.object.data.i3d_attributes.receive_shadows = True
            bpy.context.object.data.i3d_attributes.non_renderable = True
        return exactFillRootNode

    def createPlane(self, name, parent, size=(1.0, 1.0, 1.0)):
        bpy.ops.mesh.primitive_plane_add()
        bpy.context.active_object.name = name
        bpy.context.object.data.name = name
        bpy.context.object.dimensions = size
        bpy.ops.object.transform_apply(scale=True)
        bpy.context.active_object.parent = parent
        plane = bpy.context.active_object.name
        if giantsI3D == True:
            I3DRemoveAttributes(plane)
        return plane

    def createVehicleComponent(self, name, dataName, size=(1.0, 1.0, 1.0), translate=(0, 0, 0)):
        bpy.ops.mesh.primitive_cube_add()
        bpy.context.active_object.name = name
        bpy.context.object.data.name = name
        bpy.context.object.data.name = dataName
        bpy.context.object.dimensions = size
        bpy.ops.object.transform_apply(scale=True)
        bpy.context.active_object.location = translate
        translate = (0, 0, 0)
        component = bpy.context.active_object.name
        if giantsI3D == True:
            dcc.I3DSetAttrBool(component,'I3D_dynamic',True)
            dcc.I3DSetAttrBool(component,'I3D_collision',True)
            dcc.I3DSetAttrBool(component,'I3D_compound',True)
            dcc.I3DSetAttrFloat(component,'I3D_collisionMask',2109442)
            dcc.I3DSetAttrFloat(component,'I3D_clipDistance',300.0)
            dcc.I3DSetAttrBool(component,'I3D_castsShadows',True)
            dcc.I3DSetAttrBool(component,'I3D_receiveShadows',True)
            dcc.I3DSetAttrBool(component,'I3D_nonRenderable',True)
        if stjerneI3D == True:
            bpy.context.object.i3d_attributes.rigid_body_type = 'dynamic'
            bpy.context.object.i3d_attributes.compound = True
            bpy.context.object.i3d_attributes.collision_mask = "203002"
            bpy.context.object.i3d_attributes.clip_distance = 300
            bpy.context.object.data.i3d_attributes.casts_shadows = True
            bpy.context.object.data.i3d_attributes.receive_shadows = True
            bpy.context.object.data.i3d_attributes.non_renderable = True

    def execute(self, context):
        name = context.scene.i3deapg.skeletons_dropdown
        getattr(TOOLS_OT_skeletons, name)(self)
        self.report({'INFO'}, name + " skeleton added")
        return {'FINISHED'}
