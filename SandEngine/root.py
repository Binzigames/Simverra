#IMPORTING SASSY LIBS
from SandEngine.Libs import *
from SandEngine.Visuals.VisualEngine import visuals_root
from SandEngine.LogicsEngine import handle_controls

# root functions
def visuals():
    visuals_root()
def physics():
    pass
def logics():
    handle_controls()
def exit():
    pr.close_window()
    sys.exit()

# root

def init_root():
    pr.init_window( 900 , 800 , "SandBoxProject")
    while not pr.window_should_close():
        root()
    else:
        exit()

def root():
    physics()
    logics()
    visuals()
