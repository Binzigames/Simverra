#IMPORTING SASSY LIBS
from SandEngine.Libs import *
from SandEngine.Visuals.VisualEngine import visuals_root , get_world , draw_loading_screen
from SandEngine.LogicsEngine import handle_controls , handle_ui_buttons
from SandEngine.Debuger import *
from SandEngine.Physics.PhysicsEngine import update_materials , activate_world
from SandEngine.DATA.GameConfig import *
from SandEngine.Audio.AudioEngine import *

#=====================
# root layers
#=====================
def visuals():
    pr.begin_drawing()
    visuals_root()
    handle_ui_buttons()
    pr.end_drawing()
def physics():
    activate_world(get_world())
    update_materials(get_world())
def logics():
    handle_controls()
    audio_system_update()
def exit():
    print_message("Exitting game...")
    audio_system_close()
    pr.close_window()
    sys.exit()
#=====================
# root
#=====================

def init_root():
    pr.init_window(w_x, w_y, w_title)
    audio_system_init()
    print_init()
    pr.set_target_fps(w_fps_lock)

    pr.begin_drawing()
    draw_loading_screen()
    pr.end_drawing()

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
