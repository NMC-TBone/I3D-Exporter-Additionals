
import bpy
import time
from bpy.app.handlers import persistent

CHECK_INTERVAL = 0.5
IMPORT_DELAY = 1.25

_known_i3d_objects = set()
_pending_i3d_objects = set()

_last_change_time = 0.0
_timer_running = False


def get_i3d_objects():
    objects = set()

    try:
        for obj in list(bpy.data.objects):
            try:
                if obj and "_i3d_nodeId" in obj:
                    objects.add(obj.as_pointer())
            except (ReferenceError, RuntimeError):
                continue
    except (ReferenceError, RuntimeError):
        return set()

    return objects
    

def check_for_new_i3d_objects():
    global _known_i3d_objects
    global _pending_i3d_objects
    global _last_change_time

    current_objects = get_i3d_objects()

    _known_i3d_objects.intersection_update(current_objects)

    new_objects = current_objects - _known_i3d_objects

    if new_objects:
        _known_i3d_objects.update(new_objects)
        _pending_i3d_objects.update(new_objects)
        _last_change_time = time.monotonic()

        print(
            f"[i3dio Auto] {len(new_objects)} neue "
            f"I3D-Objekte erkannt."
        )


def run_auto_migration():
    global _pending_i3d_objects

    if not _pending_i3d_objects:
        return

    elapsed = time.monotonic() - _last_change_time

    if elapsed < IMPORT_DELAY:
        return

    print("[i3dio Auto] Starte automatische Migration...")

    try:
        if not bpy.ops.i3dea.migrate_giants_to_i3dio.poll():
            print(
                "[i3dio Auto] Migration nicht möglich. "
                "Ist der Community Exporter aktiviert?"
            )
            _pending_i3d_objects.clear()
            return

        result = bpy.ops.i3dea.migrate_giants_to_i3dio(
            "EXEC_DEFAULT",
            preserve_old_properties=False,
            migrate_visibility=True,
        )

        if "FINISHED" in result:
            print(
                "[i3dio Auto] Migration erfolgreich abgeschlossen."
            )
        else:
            print(
                "[i3dio Auto] Migration wurde abgebrochen."
            )

    except Exception as exc:
        print(f"[i3dio Auto] Fehler: {exc}")

    finally:
        _pending_i3d_objects.clear()


    if hasattr(bpy.ops, "i3d_material_visualizer") and hasattr(bpy.ops.i3d_material_visualizer, "visualize_all"):
        bpy.ops.i3d_material_visualizer.visualize_all()


def auto_import_timer():
    check_for_new_i3d_objects()

    if _pending_i3d_objects:
        elapsed = time.monotonic() - _last_change_time

        if elapsed >= IMPORT_DELAY:
            run_auto_migration()

    return CHECK_INTERVAL


@persistent
def load_post_handler(_dummy):
    global _known_i3d_objects
    global _pending_i3d_objects
    global _last_change_time

    _known_i3d_objects = get_i3d_objects()
    _pending_i3d_objects.clear()
    _last_change_time = 0.0

    print("[i3dio Auto] Objekterkennung zurückgesetzt.")

    

def register_auto_import_detection():

    if load_post_handler not in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.append(load_post_handler)

    if not bpy.app.timers.is_registered(initialize_auto_import_detection):
        bpy.app.timers.register(
            initialize_auto_import_detection,
            first_interval=2.0,
            persistent=True,
        )

    print("[i3dio Auto] Initialisierung gestartet.")


def initialize_auto_import_detection():

    global _known_i3d_objects
    global _pending_i3d_objects
    global _last_change_time
    global _timer_running

    try:
        _known_i3d_objects = get_i3d_objects()
        _pending_i3d_objects.clear()
        _last_change_time = 0.0

        if not bpy.app.timers.is_registered(auto_import_timer):
            bpy.app.timers.register(
                auto_import_timer,
                first_interval=CHECK_INTERVAL,
                persistent=True,
            )

        _timer_running = True

        print(
            f"[i3dio Auto] Überwachung aktiv. "
            f"{len(_known_i3d_objects)} vorhandene I3D-Objekte."
        )

    except Exception as exc:
        print(f"[i3dio Auto] Initialisierungsfehler: {exc}")

    return None



def unregister_auto_import_detection():

    global _timer_running
    global _pending_i3d_objects

    if load_post_handler in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.remove(load_post_handler)

    for timer in (
        initialize_auto_import_detection,
        auto_import_timer,
    ):
        if bpy.app.timers.is_registered(timer):
            bpy.app.timers.unregister(timer)

    _pending_i3d_objects.clear()
    _timer_running = False

    print("[i3dio Auto] Automatische Erkennung deaktiviert.")
