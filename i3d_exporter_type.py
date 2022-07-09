import bpy


def check_i3d_exporter_type():
    giants_i3d = False
    I3DRemoveAttributes: any = {}
    dcc: any = {}
    stjerne_i3d = False

    for a in bpy.context.preferences.addons:
        if a.module == "io_export_i3d":
            giants_i3d = True
            from io_export_i3d.dcc import dccBlender as dcc
            from io_export_i3d.dcc import I3DRemoveAttributes
        if a.module == "i3dio":
            stjerne_i3d = True

    return giants_i3d, stjerne_i3d, dcc, I3DRemoveAttributes
