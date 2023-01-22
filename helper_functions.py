import bpy


class Singleton:
    __instance = None

    def __init__(self):
        if Singleton.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            Singleton.__instance = self
            self.giants_i3d = False
            self.stjerne_i3d = False
            self.check_i3d_exporter_type()

    @classmethod
    def get_instance(cls):
        if Singleton.__instance is None:
            Singleton()
        return Singleton.__instance

    def check_i3d_exporter_type(self):
        if "io_export_i3d" in bpy.context.preferences.addons:
            self.giants_i3d = True
        else:
            self.giants_i3d = False
        if "i3dio" in bpy.context.preferences.addons:
            self.stjerne_i3d = True
        else:
            self.stjerne_i3d = False


def check_obj_type(obj):
    if len(bpy.context.selected_objects) > 0:
        mode = bpy.context.object.mode
        for obj in bpy.context.selected_objects:
            if not obj.type == "MESH":
                continue
            if not mode == 'OBJECT':
                bpy.ops.object.mode_set(mode='OBJECT')
