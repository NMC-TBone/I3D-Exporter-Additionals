from math import radians

BASE_VEHICLE_SKELETON = {
    "name": "1:vehicleName_main_component1",
    "type": "mesh",  # We want a mesh for the main component.
    "data_name": "vehicleName_main_component1",
    "children": [
        {
            "name": "1:vehicleName_root(REPLACE_WITH_MESH)",
            "type": "empty",
            "children": [
                {"name": "1:wheels", "type": "empty"},
                # Include cameras from the common config:
                {"name": "cameras", "type": "include", "include": "CAMERAS_VEHICLE"},
                # Include lights:
                {"name": "lights", "type": "include", "include": "LIGHTS"},
                {"name": "4:exitPoint", "type": "empty"},
                {
                    "name": "5:cabin_REPLACE_WITH_MESH",
                    "type": "empty",
                    "children": [
                        {
                            "name": "1:steeringBase",
                            "type": "empty",
                            "children": [
                                {
                                    "name": "steeringWheel_REPLACE_WITH_MESH",
                                    "type": "empty",
                                    "children": [
                                        {
                                            "name": "playerRightHandTarget",
                                            "type": "empty",
                                            "display_handle": True,
                                            "location": (-0.189, 0.023, 0.03),
                                            "rotation": (radians(-4.70569), radians(-50.8809), radians(-7.47474)),
                                        },
                                        {
                                            "name": "playerLeftHandTarget",
                                            "type": "empty",
                                            "display_handle": True,
                                            "location": (0.189, 0.023, 0.03),
                                            "rotation": (radians(-16.3303), radians(50.8809), radians(-7.47473)),
                                        },
                                    ],
                                }
                            ],
                        },
                        {
                            "name": "2:seat_REPLACE_WITH_MESH",
                            "type": "empty",
                            "children": [{"name": "playerSkin", "type": "empty", "display_handle": True}],
                        },
                        {"name": "3:lights_cabin", "type": "empty"},
                        {"name": "4:wipers", "type": "empty"},
                        {"name": "5:dashboards", "type": "empty"},
                        {"name": "6:levers", "type": "empty"},
                        {"name": "7:pedals", "type": "empty"},
                        {
                            "name": "8:characterTargets",
                            "type": "empty",
                            "children": [
                                {"name": "playerRightFootTarget", "type": "empty", "display_handle": True},
                                {"name": "playerLeftFootTarget", "type": "empty", "display_handle": True},
                            ],
                        },
                        {"name": "9:mirrors_cabin", "type": "empty"},
                        {"name": "10:visuals_cabin", "type": "empty"},
                    ],
                },
                # Include attacher joints from the common config.
                {
                    "name": "attacher_joints",
                    "type": "include",
                    "include": "ATTACHER_JOINTS",
                    "params": {"is_harvester": False},
                },
                {
                    "name": "7:ai",
                    "type": "empty",
                    "children": [{"name": "aiCollisionTrigger_REPLACE_WITH_MESH", "type": "empty"}],
                },
                {
                    "name": "exhaust_particles",
                    "type": "empty",
                    "children": [
                        {"name": "exhaustParticle1", "type": "empty", "display_handle": True},
                        {"name": "exhaustParticle2", "type": "empty", "display_handle": True},
                    ],
                },
                {"name": "9:hydraulics", "type": "empty"},
                {"name": "10:mirrors", "type": "empty"},
                {"name": "11:configurations", "type": "empty"},
                {"name": "12:visuals", "type": "empty"},
            ],
        },
        # Additional nodes that are children of the main vehicle component:
        {"name": "2:skinnedMeshes", "type": "empty"},
        {"name": "3:collisions", "type": "empty"},
    ],
}
