#IMPORTING SASSY LIBS
from SandEngine.Visuals.VisualEngine import visuals_root , get_world , draw_loading_screen
from SandEngine.Additions.LogicsEngine import handle_controls , handle_ui_buttons , refresh_material_groups
from SandEngine.Debuger import *
from SandEngine.Physics.PhysicsEngine import update_materials , activate_world
from SandEngine.Audio.AudioEngine import *
from Assets.Assets_importer import *
from SandEngine.Additions.api_manager import *
from SandEngine.Additions.ModdingEngine import *

#=====================
# root layers
#=====================
def visuals():
    pr.begin_drawing()
    visuals_root()

    if get_togle_ui():
        handle_ui_buttons()

    if is_moded:
        render_mods()
        ui_mods()
    pr.end_drawing()
def physics():
    activate_world(get_world())
    update_materials(get_world())
def logics():
    handle_controls()
    audio_system_update()
    if is_moded:
        logic_mods()
        refresh_material_groups(mods)
def exit():
    print_message("Exitting game...")
    audio_system_close()
    terminate_apis()
    pr.close_window()
    sys.exit()
#=====================
# root
#=====================

def init_root():
    pr.init_window(w_x, w_y, w_title)
    set_icon()
    audio_system_init()
    print_init()
    pr.set_target_fps(w_fps_lock)

    pr.begin_drawing()
    draw_loading_screen()
    pr.end_drawing()

    try:
        init_apis()
    except Exception:
        pass
    init_mods()
    activate_world(get_world())
    update_materials(get_world())

    while not pr.window_should_close():
        root()
    else:
        exit()

def root():
    logics()
    physics()
    visuals()
