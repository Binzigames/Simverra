#IMPORTING SASSY LIBS
from SandEngine.Libs import *
from SandEngine.Visuals.VisualEngine import visuals_root , get_world
from SandEngine.LogicsEngine import handle_controls , handle_ui_buttons
from SandEngine.Debuger import *
from SandEngine.Physics.PhysicsEngine import update_materials
# root functions
def visuals():
    pr.begin_drawing()
    visuals_root()
    handle_ui_buttons()
    pr.end_drawing()
def physics():
    update_materials(world=get_world())
def logics():
    handle_controls()
def exit():
    print_message("Exitting game...")
    pr.close_window()
    sys.exit()

# root

def init_root():
    pr.init_window( 900 , 800 , "SandBoxProject")
    print_init()
    while not pr.window_should_close():
        root()
    else:
        exit()

def root():
    visuals()
    logics()
    physics()
