#imports assets like fonts or graphics or sounds
from SandEngine.Libs import *

#=====================
#FONTS
#=====================
FONT = None

def get_font():
    global FONT

    if FONT is None:
        FONT = pr.load_font("Assets/Inter.ttf")

    return FONT
#=====================
#SHADERS
#=====================

#=====================
#VISUALS
#=====================
def set_icon():
    icon = pr.load_image("Assets/icon.png")
    pr.set_window_icon(icon)
    pr.unload_image(icon)
