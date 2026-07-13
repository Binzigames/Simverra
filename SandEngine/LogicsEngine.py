# LOGIC ENGINE COUNTS MATH ETC
#importing for you honey ~
from SandEngine.Libs import *
from SandEngine.DATA.TMP import *
from SandEngine.Visuals.VisualEngine import *

mouse = pr.get_mouse_position()
world_mouse = pr.get_screen_to_world_2d(mouse, camera)

# Controls
def handle_controls():
    global TMP_cursor_scale
    wheel = pr.get_mouse_wheel_move()

    if wheel != 0:
        TMP_cursor_scale += int(wheel +1)
        print(TMP_cursor_scale)

        if TMP_cursor_scale < 0.1:
            TMP_cursor_scale = 0.1

        if TMP_cursor_scale > 20:
            TMP_cursor_scale = 20
