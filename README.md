# i3d_exporter_additionals


## Description

Some additional tools that work along with [Giants i3d Exporter](https://gdn.giants-software.com/download.php?downloadId=92) and [StjerneIdioten I3D-Blender-Addon](https://github.com/StjerneIdioten/I3D-Blender-Addon) for Blender.

## Included tools
### Mesh Tools
Clean meshes: Removes custom split normals, set shade smooth and auto smooth, merge vertices, remove triangulation on mesh.

Set mesh name: Copy object name to mesh data name

Get curve length: Calculate length of selected curve

Add suffix _ignore: This will add _ignore to the end of selected objects name. This will only work with the Giants i3d exporter, as this exporter got a built in function to ignore all objects and it's children when _ignore is used.

### UV-Tools
Create UVset2: Generates UVset2 for selected object (2x2, will create a grid of 4 and for separate objects and 4x4 will create grid of 16 and 16 seperate objects).

### Skeletons
Tool to generate simple skeleton structures of selected item. It will also add correct attributes for both Giants and Stjerne I3D exporter.

### Material-Tools
Add mirror material: Add mirror_mat to the blender file with correct material attributes. Unfortunetly the mirror material doesn't export correctly.

Remove duplicated materials: Currently just removes empty slots in the materials and clears Orphan Data.

### Assets Importer
It imports the in game assets into your blender file with correct rotation and translation. No lights added to it yet. (Keep in mind these objects are ment for reference only, if you deceide to export a mod with these objects you can expect issues with UV maps etc).

## How to install
Support for Blender 3.0.0 and up
Install it like any other Blender addon. Download the newest version from [releases page](https://github.com/NMC-TBone/i3d_exporter_additionals/releases).

## Need help?
Feel free to contact me on [discord](https://discord.gg/gBpCXYp)

If you find any issues with this addon create a [new issue](https://github.com/NMC-TBone/i3d_exporter_additionals/issues).

**Note**
*The mirror material don't export correctly to i3d yet, due to missing attributes within the i3d exporter.*
