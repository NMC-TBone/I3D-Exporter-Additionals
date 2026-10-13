# I3D Exporter Additionals

![Blender minimum version](https://img.shields.io/badge/Blender-4.2%2B-orange?logo=blender&logoColor=white)
[![License](https://img.shields.io/badge/License-GPL--3.0--or--later-blue)](LICENSE)

A Blender toolbox for Farming Simulator modding: prepare meshes and materials, build starter hierarchies, work with tracks and curves, and move existing projects from the GIANTS exporter to the Community exporter.

This add-on works alongside an I3D exporter. The exporter creates the `.i3d` file used by GIANTS Editor and the game; Additionals helps you prepare the Blender scene.

**[Download](https://github.com/NMC-TBone/I3D-Exporter-Additionals/releases)** · **[Release notes](https://github.com/NMC-TBone/I3D-Exporter-Additionals/releases)** · **[Report a bug](https://github.com/NMC-TBone/I3D-Exporter-Additionals/issues)** · **[Discord](https://discord.gg/gBpCXYp)**

[Getting started](#getting-started) · [Tool guide](#tool-guide) · [Exporter migration](#exporter-migration) · [Troubleshooting](#troubleshooting) · [Help and feedback](#help-and-feedback)

## Getting started

### What you need

- **Blender 4.2 or newer**, the minimum version declared by this add-on.
- **An I3D exporter** for exporting and for tools that set exporter properties. General mesh and orientation tools can also be used without one.
- **Your game's data folder** configured in the Community exporter's preferences when working with game shaders, including mirror materials and material migration.

Both exporters are supported, with the **Community I3D Exporter preferred for this project**. Additionals includes Community-specific tools for migrating GIANTS projects and enabling material slot names across the file.

| Exporter | Downloads and documentation |
| --- | --- |
| **Community I3D Exporter** by StjerneIdioten (`i3dio`) | [Project and downloads](https://github.com/StjerneIdioten/I3D-Blender-Addon) · [Exporter documentation](https://stjerneidioten.github.io/I3D-Blender-Addon/) |
| **GIANTS I3D Exporter** | [GIANTS Developer Network downloads](https://gdn.giants-software.com/downloads.php) |

Choose an exporter version that supports your Blender version and the game you are modding. Enable one exporter at a time for normal use; Additionals displays a warning if both are enabled.

### Install the add-on

1. Open the [releases page](https://github.com/NMC-TBone/I3D-Exporter-Additionals/releases) and expand **Assets** for the release you want.
2. Download the add-on archive named `i3d_exporter_additionals-<version>.zip`. Keep it zipped. The **Source code** downloads are repository snapshots, so use the packaged add-on archive for installation.
3. Open Blender, then **drag the downloaded ZIP from your file manager into the Blender window**.
4. Follow the installation popup to install and enable the add-on.
5. Check that **I3D Exporter Additionals** is enabled under **Preferences → Add-ons**.

Alternatively, open **Edit → Preferences → Get Extensions**, use the drop-down menu in the top right, and choose **Install from Disk…** to select the ZIP.

See the [Blender manual's extension installation guide](https://docs.blender.org/manual/en/4.2/editors/preferences/extensions.html) for more on installing ZIP packages.

This README follows the current source code. An older release may have fewer tools; releases marked **Pre-release** contain development changes. Check the release notes when choosing a version.

### Find the tools

In the **3D Viewport** (the main area where you see your model), move your mouse over the viewport and press **N** to open the sidebar. Select the **I3D Exporter Additionals** tab on its right edge.

Click a section heading to expand it. Start in **Object Mode** unless a tool asks for Edit Mode. The guide below uses the names shown in the panel.

A few Blender terms used here:

- **Active object:** the main object in your selection, usually the one you selected last. Some tools use only this object even when several are selected.
- **Origin:** an object's pivot point and the reference point for its local X, Y, and Z axes.
- **Empty:** a helper object with no mesh, used for reference points or for grouping other objects.
- **Hierarchy:** objects arranged as parents and children, visible in the Outliner (the object list).
- **UV map:** the layout that tells Blender and the game where textures belong on a mesh. A second UV map provides another layout for the same geometry.

## Tool guide

### General Tools

| Tool | What it does and how to use it |
| --- | --- |
| **Copy Location / Copy Rotation** | Copies the active object's transform relative to its parent to the clipboard, converted to GIANTS Editor coordinates. Paste the three values into the corresponding field in GIANTS Editor. Also supports the active armature bone in **Edit Mode**. |
| **Set mirror orientation** | Select a **camera**, a **mirror mesh**, and a **reference empty**. Adjusts the mirror's local orientation using the camera and reference point. |
| **Clean Meshes** | Processes selected meshes: removes custom split normals, merges nearby vertices, marks sharp edges, applies smooth shading, and converts triangles to quads where possible. It changes mesh geometry and shading, so check the result before exporting. |
| **Set Mesh Name** | Renames mesh data throughout the **current scene** to match object names. Skips mesh data shared by several objects and removes any prefix before the last `:` in the object name. |
| **Align Hydraulic Pair** | Select two mesh objects: the cylinder housing and piston. Aligns their local axes to point towards each other while keeping the visible mesh geometry in place. See the steps below. |
| **Adjust Decal Offsets…** | Checks selected decal meshes against nearby visible surfaces, then adjusts vertices to a **0.0002 m (0.2 mm)** surface offset. Review the scan in the dialog before pressing **OK**. |
| **Set Origin to Face Normal** | In mesh **Edit Mode**, switch to **Face Select** and select a face (the last selected face is active). Aligns the object's local axes to the direction the face points, called its normal. Keeps visible geometry in place. Choose **Axis** and **Flip** in **Adjust Last Operation** (**F9**). |

For **Align Hydraulic Pair**, place each object's origin at its pivot or attachment point first. Select the piston, then Shift-select the housing to make the housing active, and run the tool. A name containing `punch` identifies the piston automatically; use **Swap Roles** in **F9** if the roles need reversing. The housing points along local **−Y**, and the piston along local **+Y**.

For **Adjust Decal Offsets…**, select only the decals and leave their underlying surfaces unselected and visible. Vertices that do not hit a valid surface stay unchanged. Decal, alpha, effect, ignored, and non-renderable objects are filtered out as target surfaces.

The following buttons appear when the **GIANTS exporter** is enabled:

| Tool | Purpose |
| --- | --- |
| **Add Suffix _ignore** | Adds `_ignore` to selected object names. This is the GIANTS exporter's naming convention for excluding an object and its children from export. |
| **Verify Scene** | Checks the scene using GIANTS exporter properties, including merge groups, bounding volumes, effect meshes, and vertex weights. Shows a summary; detailed messages are printed to Blender's console. |
| **Convert SkinnedMesh** | For the active mesh with **multiple Armature modifiers**. Combines the referenced armatures, sets up bone constraints, and parents the result under an existing `skinnedMeshes` or `skinnedMesh` object if present. Use it on a copy of an existing rig and check the result. |

### User Attributes

This section appears when the **GIANTS exporter** is enabled. It lets you add, edit, and delete named attributes on the **active object**. These are extra values the game or scripts can read from the exported object.

Enter a name, choose a type, and press **Add**. The panel offers `boolean` (on/off), `float` (decimal number), `integer` (whole number), `string` (text), and `scriptCallback`. For Community exporter projects, use the exporter's own user-attribute panel.

### Skeletons

Creates a starter object hierarchy with named helpers, cameras, lights, and collision or trigger placeholders where the chosen template includes them. Here, “skeleton” means a scene structure to build your mod around.

Choose a template from the drop-down and press **Create**:

| Starting point | Templates |
| --- | --- |
| Vehicles and equipment | Tractor, Combine, Tool, Traffic Vehicle |
| Vehicle helpers | Attacher Joints, Lights, Cameras (Tractor), Cameras (Combine), Player |
| Buildings and animals | Placeable, Husbandry |

The templates set exporter properties where supported by the enabled exporter. Replace placeholders such as `REPLACE_WITH_MESH`, move the reference points to fit your model, and adapt the hierarchy and the game's XML configuration to your mod.

### Material Tools

| Tool | What it does |
| --- | --- |
| **Add Mirror Material** | Creates or reuses `mirror_mat`, sets mirror shader metadata for the detected exporter, and assigns it to selected meshes by default. Assignment replaces existing material slots on affected meshes. With the Community exporter, set the **FS Data Folder** first. |
| **Enable Slot Names (All Materials)** | **Community exporter only.** Enables exported material slot names for every material in the file. Preserves existing custom slot names; newly enabled materials use their material name on export unless a custom name is set. |
| **Create Material** | Enter a material name and optional diffuse, specular, and normal texture paths, then press **Create …**. Creates connected material nodes and adds the material to selected meshes. **Alpha** connects the diffuse texture's alpha channel. If the name already exists, it reuses that material without rebuilding its nodes. |

**Create Material** sets up the Blender material nodes. Choose any game-specific shader and parameters in your exporter's material settings.

### Track Tools

Tools for preparing repeated track pieces, second UV maps, and previews of a track following a curve.

A curve object can contain multiple separate paths, called **splines**. Keep each curve to one path for these tools.

#### Manual Tools

| Tool | How to use it |
| --- | --- |
| **Create UVset 2** | Make a mesh with an existing UV map active. Choose **2x2** for four copies or **4x4** for sixteen copies. Each copy gets a second UV layout in a different grid tile. |
| **Add empties** | Choose a count from one to five, select the track-piece meshes, and press **Add**. Creates that many helper empties per selected mesh. |
| **Get Curve Length** | Make a curve active and press the button to display its length. Measures its first spline and applies the curve's scale if needed. Use a curve with a single spline for these tools. |
| **Calculate Amount** | Select two pieces to measure their separation along Blender's **Y axis**. Then make the curve active and run it again to estimate how many pieces fit using that distance. You can also enter the distance manually. |

#### Automatic

1. Prepare a track-piece mesh with an existing UV map and a single-spline curve representing the track path.
2. Make the **track-piece mesh active**, open **Automatic**, and choose the curve under **Manage and Create → Select Curve**.
3. Choose a name and either a **Fixed Amount** or a **Distance between links**. Creation starts with four or sixteen UV copies, so use a count at least as large as the chosen grid.
4. Enable the options you need: a second UV grid, extra objects for baking an ambient-occlusion mask (**Add Vmask Objects**), helper empties, or a bounding volume (a box describing the track's bounds). **Allow Curve Scale** can change the curve to fit the piece spacing.
5. Press **Create** to generate the duplicate pieces and parent hierarchy.

The curve is used to calculate the count; this operation does not place the generated pieces around it. Use **Track Visualization** to preview the wrapped result.

Automatic track creation writes its hierarchy and bounding-volume exporter settings for the **GIANTS exporter**. With the Community exporter, configure the equivalent export settings yourself, including excluding the `zzz_data_ignore` helper hierarchy.

#### Track Visualization

Select a track mesh and its curve, keeping the **mesh active**. Choose **Caterpillar** or **Rubber** and press **Track Visualization**. For Caterpillar, set the piece count and spacing first. The tool creates a curve-based animated preview; use **Delete** to remove the preview objects. **Bogie** is listed in the UI but is not implemented.

### Motion Path From Curves

Builds a hierarchy of empties sampled along curves, grouped into poses. This is useful when preparing path or object-array data.

1. Save your `.blend` file.
2. Press **+** to add a pose. Select the curves for that pose and press **Add Curves**.
3. Repeat for any additional poses, then choose a sampling method:

   - **Uniform Count:** the same number of empties on each curve.
   - **Adaptive Spacing:** uses the longest curve in each pose to calculate point counts for the other curves.
   - **Distance:** uses the requested distance to calculate point counts for each curve.
4. Set an **Array Name** and, for GIANTS object-data export, a **Save Location**.
5. Press **Create** to generate the hierarchy.

Use single-spline curves and settings that produce at least two points per curve. Generated empties keep their sampled positions and orientations; they do not stay linked to the curves.

With the GIANTS exporter enabled, the root receives object-data export properties and a `.dds` destination path. **Create** itself builds the Blender objects; it does not write a DDS file. With the Community exporter, configure object-data export separately.

## Exporter migration

**Migrate…** converts GIANTS exporter data to the **Community I3D Exporter** format. The Community exporter must be installed and enabled; the GIANTS exporter does not need to be enabled if its properties are already stored in the file.

Migration covers object and mesh properties, rigid-body settings, user attributes, merge groups, bounding-volume references, and material shader settings. Detected legacy FS19/FS22 vehicle shaders can also trigger the Community exporter's UDIM-to-material-template conversion.

1. **Save a backup of your `.blend` file.** Migration changes objects and materials throughout the file, including objects outside your current selection.
2. Enable the Community exporter and configure its **FS Data Folder** so game shaders are available.
3. Open Additionals and press **Migrate…** at the top of the panel.
4. Review the options, then confirm the migration.
5. Check materials and export settings, export with the Community exporter, and inspect the result in GIANTS Editor.

### Migration options and behavior

- **Keep Giants Exporter Properties** is **off by default**. Migration normally removes the old exporter properties after conversion. Enable it to retain those properties, but still keep a backup: other changes, such as material conversion and object renaming, can affect the old workflow.
- **Preserve Giants Visibility** is **on by default**. Copies the current Outliner **eye** state into fixed Community export visibility and turns off visibility tracking. Dynamic compound collision roots remain visible.
- Objects whose names end in `_ignore` are marked **Exclude from Export**, and that suffix is removed from their names.
- Meshes with existing color-attribute layers are set to **If Layer Exists**, preserving colors on effect meshes even when their material has no shader requiring vertex colors. Meshes without color layers keep their existing setting.

For those vertex-color settings to take effect, choose **Use Mesh Settings** for the global **Vertex Color** option when exporting with the Community exporter.

Some settings may have no equivalent in the other exporter. Review the converted file and the console messages before continuing work. If the GIANTS exporter is still enabled, the panel provides **Disable Giants I3D Exporter**.

## Troubleshooting

| Problem | What to check |
| --- | --- |
| No Additionals tab | Enable the add-on in Preferences, move the mouse over the **3D Viewport**, and press **N**. |
| A button is unavailable | Check the required selection and mode. **Set Origin to Face Normal** needs mesh Edit Mode; migration and slot names need the Community exporter. |
| A tool in this guide is missing | Compare your installed version with the release notes. GIANTS-specific controls appear only when that exporter is enabled. |
| “FS Data Folder is not set!” | Set the game data folder in the **Community exporter's** preferences. |
| Exporter helpers use the wrong exporter | After enabling or switching exporters, restart Blender so all helpers detect the enabled exporter. |
| Decal scan reports no hits | Keep the underlying surface visible and unselected, check decal normals, and ensure the decals are close to a valid target surface. |

On Windows, **Window → Toggle System Console** opens the console used by scene verification and migration messages.

## Help and feedback

For questions, join the [Discord server](https://discord.gg/gBpCXYp). For bugs or feature requests, use the [issue tracker](https://github.com/NMC-TBone/I3D-Exporter-Additionals/issues).

A useful bug report includes your Blender version, Additionals version, exporter name and version, steps to reproduce the problem, and any error message. Screenshots or a small example `.blend` file also help.

For help with exporting itself, see the [Community exporter documentation](https://stjerneidioten.github.io/I3D-Blender-Addon/) or the [GIANTS Developer Network](https://gdn.giants-software.com/).

Licensed under **GPL-3.0-or-later**. See [LICENSE](LICENSE).
