#config for everything in game... almost...
from SandEngine.Libs import *


#=====================
#SAND ENGINE
#=====================

#window
w_fps_lock = 60
w_x = 1000
w_y = 800
w_title = "Simverra 1.0"

#debuger
d_show_logs = False

#=====================
#VISUAL ENGINE
#=====================

# optimization settings
map_texture = None
map_image = None

# UI
Welcome_screen_shown = False
debug_menu = False
object_menu = False
object_mode = False

selected_object = "BOX"

OBJECTS = {
    "BOX": {
        "color": pr.RED,
        "size": (20,20)
    },

    "STONE BOX": {
        "color": pr.GRAY,
        "size": (35,35)
    },

    "BALL": {
        "color": pr.BLUE,
        "size": (25,25)
    }
}
#map options
MAP_W = 256
MAP_H = 256
PIXEL_SIZE = 4

MAP_PATH = "SandEngine/DATA/map.json"

world = None


#=====================
#LOGICS ENGINE
#=====================

Curent_material = 2
Fullscreen = False

#=====================
#PHYSICS ENGINE
#=====================

# MATERIAL IDS

AIR = 0
SAND = 2
WATER = 3
STONE = 4
GRAVIY = 5

# DIRTY PIXELS

dirty_cells = set()

# optimization
MAX_MATERIAL_UPDATES = 10000
