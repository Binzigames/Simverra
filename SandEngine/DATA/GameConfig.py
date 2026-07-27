#config for everything in game... almost...
from SandEngine.Libs import *


#=====================
#SAND ENGINE
#=====================

#ui_colors
UI_C_BG      = pr.Color(15, 10, 28, 235)
UI_C_PANEL   = pr.Color(35, 20, 55, 245)
UI_C_BORDER  = pr.Color(100, 55, 150, 255)

UI_C_TEXT    = pr.Color(230, 220, 255, 255)
UI_C_MUTED   = pr.Color(145, 125, 180, 255)

UI_C_MAIN    = pr.Color(155, 80, 255, 255)
UI_C_ACCENT  = pr.Color(255, 190, 90, 255)

#window
w_fps_lock = 60
w_x = 1000
w_y = 800
w_title = "Simverra 1.1"

#debuger
d_show_logs = False

#extentions
WORLD_EXTENSION = ".simvworld"


# loading screen
loading_texts = [
    "Change now its time for change, nothing stays the same",
    "Losing my religion , trying to keep up with you",
    "All my life, i fight to survive",
    "The silence before the adventure begins",
    "Chasing shadows, building memories",
    "Somewhere far away, a story is waiting",
    "Turning pixels into emotions",
    "The journey starts with a single step",
    "Loading the impossible...",
    "Almost there, don't blink"
]


# =====================
# SCREEN FADE
# =====================

fade_alpha = 255
fade_speed = 20
fade_active = False
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
show_ui = True

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

DYNAMIC_MATERIALS = {
    3,
    8,
    9
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
BOMB = 6
SOIL = 7
GAS = 8
FIRE = 9
WOOD = 10
BLACK_HOLE = 11



#options
fire_life = {}

explosions = []
EXPLOSION_RADIUS = 15
# DIRTY PIXELS

dirty_cells = set()

# optimization
MAX_MATERIAL_UPDATES = 15000

#=====================
#OBJECTS
#=====================
objects = []

GRAVITY = 600


#=====================
#AUDIO ENGINE
#=====================
Music_Loudnes = 0.2
SFX_Loudnes = 0.1

#=====================
#TOGLES
#=====================
def togle_ui():
    global show_ui
    show_ui = not show_ui

def get_togle_ui():
    global show_ui
    return show_ui