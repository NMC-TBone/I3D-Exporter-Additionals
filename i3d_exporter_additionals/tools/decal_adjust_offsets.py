from dataclasses import dataclass

import bpy
from mathutils import Vector

from ..helper_functions import check_i3d_exporter_type


@dataclass(frozen=True)
class HitResult:
    distance: float
    hit_world: Vector
    face_index: int


TARGET_OFFSET = 0.0002  # desired decal offset in meters
START_OFFSET = 0.001  # how far above vertex to start raycast (meters)
MAX_RAY_DISTANCE = 0.075  # max ray length in meters


def is_valid_target(obj: bpy.types.Object, decals_set: set[bpy.types.Object], i3dio_enabled: bool) -> bool:
    """Check if object is a valid raycast target for decals."""
    if obj in decals_set or obj.type != "MESH" or not obj.visible_get():
        return False
    name_lower = obj.name.lower()
    if any(s in name_lower for s in ("decal", "alpha", "effect")) or name_lower.endswith("_ignore"):
        return False
    if obj.get("i3D_nonRenderable"):
        return False
    if i3dio_enabled:
        if obj.i3d_attributes.exclude_from_export or obj.data.i3d_attributes.non_renderable:
            return False
    return True


def collect_targets_for_decals(context: bpy.types.Context, decals: list[bpy.types.Object]) -> set[bpy.types.Object]:
    i3dio_enabled = check_i3d_exporter_type()[1]
    decals_set = set(decals)
    return {obj for obj in context.view_layer.objects if is_valid_target(obj, decals_set, i3dio_enabled)}


def raycast_world_to_object(eval_obj: bpy.types.Object, start_world: Vector, dir_world: Vector) -> HitResult | None:
    """Raycast from world space start along direction to an evaluated object."""
    mw = eval_obj.matrix_world
    mw_inv = mw.inverted()

    origin_local = mw_inv @ start_world
    direction_local = (mw_inv.to_3x3() @ dir_world).normalized()

    hit, loc_local, _normal_local, face_index = eval_obj.ray_cast(origin_local, direction_local)
    if not hit:
        return None
    hit_world = mw @ loc_local
    distance = (hit_world - start_world).length
    if distance > MAX_RAY_DISTANCE:
        return None
    return HitResult(distance, hit_world, face_index)


def scan_decal_vertices(
    context: bpy.types.Context,
    decals: list[bpy.types.Object],
    targets: set[bpy.types.Object],
) -> dict[str, dict]:
    """
    Scan all vertices of the given decals against target objects.

    Returns:
        A mapping from decal object name to scan data, including:
        hits, misses, distances, total_verts, and vertex_hits.
    """
    depsgraph = context.evaluated_depsgraph_get()
    evaluated_targets = {t: t.evaluated_get(depsgraph) for t in targets}

    scan_results = {}

    for decal in decals:
        me = decal.data
        mw = decal.matrix_world
        hits = misses = 0
        distances = []
        vertex_hits: dict[int, HitResult] = {}
        for vert in me.vertices:
            pos_world = mw @ vert.co
            normal_world = (mw.to_3x3() @ vert.normal).normalized()
            start = pos_world + normal_world * START_OFFSET
            direction = -normal_world

            best_hit = None
            for original_target, eval_target in evaluated_targets.items():
                hit_result = raycast_world_to_object(eval_target, start, direction)
                if hit_result and (best_hit is None or hit_result.distance < best_hit.distance):
                    best_hit = hit_result

            if best_hit is None:
                misses += 1
            else:
                hits += 1
                adjusted_distance = best_hit.distance - START_OFFSET
                distances.append(adjusted_distance)
                vertex_hits[vert.index] = HitResult(adjusted_distance, best_hit.hit_world, best_hit.face_index)

        # Store all results for this decal
        scan_results[decal.name] = {
            "hits": hits,
            "misses": misses,
            "distances": distances,
            "total_verts": len(me.vertices),
            "vertex_hits": vertex_hits,
        }

    return scan_results


def adjust_decal_object_vertices(decal: bpy.types.Object, scan_data: dict) -> None:
    """Adjusts a single decal's vertices based on pre-computed scan data."""
    me = decal.data
    mw = decal.matrix_world
    mw_inv3 = mw.inverted().to_3x3()
    vertex_hits = scan_data.get("vertex_hits", {})

    if not me.vertices or not vertex_hits:
        return

    for vert in me.vertices:
        if not (hit_result := vertex_hits.get(vert.index)):
            continue  # vertex had no hit
        move_amount = TARGET_OFFSET - hit_result.distance
        if abs(move_amount) < 1e-5:
            continue  # already close enough
        normal_world = (mw.to_3x3() @ vert.normal).normalized()
        offset_world = normal_world * move_amount
        offset_local = mw_inv3 @ offset_world
        vert.co += offset_local
    me.update()


class DecalObjectItem(bpy.types.PropertyGroup):
    object_name: bpy.props.StringProperty(name="Object Name")
    avg_distance: bpy.props.FloatProperty(name="Average Distance", precision=6)
    min_distance: bpy.props.FloatProperty(name="Min Distance", precision=6)
    max_distance: bpy.props.FloatProperty(name="Max Distance", precision=6)
    hit_count: bpy.props.IntProperty(name="Hit Count")
    miss_count: bpy.props.IntProperty(name="Miss Count")
    has_hits: bpy.props.BoolProperty(name="Has Hits")
    total_verts: bpy.props.IntProperty(name="Total Vertices")


class I3DEA_UL_DecalList(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        row = layout.row(align=True)
        total = item.total_verts or (item.hit_count + item.miss_count)
        row.label(text=f"verts {item.hit_count}/{total}")

        if item.has_hits:
            row.label(text=f"avg {item.avg_distance:.6f}")
            row.label(text=f"min {item.min_distance:.6f}")
            row.label(text=f"max {item.max_distance:.6f}")
        else:
            row.label(text="NO HITS")


class I3DEA_OT_adjust_decal_offsets(bpy.types.Operator):
    bl_idname = "i3dea.adjust_decal_offsets"
    bl_label = "Adjust Decal Offsets"
    bl_description = "Raycasts decal vertices against nearby geometry and adjusts them to the correct surface offset."
    bl_options = {"INTERNAL", "UNDO"}

    list_index: bpy.props.IntProperty(default=0)
    decal_items: bpy.props.CollectionProperty(type=DecalObjectItem)

    _scan_results: dict

    def invoke(self, context, event):
        self._scan_results = {}
        self.decal_items.clear()
        decals = [obj for obj in context.selected_objects if obj.type == "MESH"]
        if not decals:
            self.report({"WARNING"}, "No mesh objects selected.")
            return {"CANCELLED"}
        targets = collect_targets_for_decals(context, decals)
        if not targets:
            self.report({"WARNING"}, "No valid target objects found in the scene.")
            return {"CANCELLED"}

        scan_results = scan_decal_vertices(context, decals, targets)

        self._scan_results = scan_results
        for decal_name, data in scan_results.items():
            item = self.decal_items.add()
            item.object_name = decal_name
            item.hit_count = data["hits"]
            item.miss_count = data["misses"]
            item.total_verts = data["total_verts"]

            if data["hits"] > 0:
                distances = data["distances"]
                item.avg_distance = sum(distances) / len(distances)
                item.min_distance = min(distances)
                item.max_distance = max(distances)
                item.has_hits = True

        if not self.decal_items:
            self.report({"WARNING"}, "No decals had any valid hits against target objects.")
            return {"CANCELLED"}

        self.list_index = 0
        return context.window_manager.invoke_props_dialog(self, width=600)

    def draw(self, context):
        layout = self.layout

        layout.template_list("I3DEA_UL_DecalList", "", self, "decal_items", self, "list_index", rows=8)

        layout.separator()
        layout.label(text="Per-object distances calculated from vertex raycasts.")
        layout.label(text=f"Target surface offset: {TARGET_OFFSET:.6f} m")
        layout.label(text="All selected decals will be adjusted when you press OK.")

    def execute(self, context):
        original_mode = None
        active_object = context.view_layer.objects.active
        if active_object and active_object.mode != "OBJECT" and bpy.ops.object.mode_set.poll():
            original_mode = active_object.mode
            bpy.ops.object.mode_set(mode="OBJECT")

        scan_results = self._scan_results
        if not scan_results:
            self.report({"ERROR"}, "No scan results available.")
            return {"CANCELLED"}

        for decal_name, data in scan_results.items():
            decal_obj = context.view_layer.objects.get(decal_name)
            if decal_obj:
                adjust_decal_object_vertices(decal_obj, data)

        if active_object and original_mode and bpy.ops.object.mode_set.poll():
            bpy.ops.object.mode_set(mode=original_mode)
        self.report({"INFO"}, "Decal offsets adjusted.")
        return {"FINISHED"}


register, unregister = bpy.utils.register_classes_factory(
    (
        DecalObjectItem,
        I3DEA_UL_DecalList,
        I3DEA_OT_adjust_decal_offsets,
    )
)

if __name__ == "__main__":
    register()
