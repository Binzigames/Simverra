# LOGIC ENGINE COUNTS MATH ETC
#importing for you honey ~
from SandEngine.Libs import *
from SandEngine.DATA.TMP import *
from SandEngine.Visuals.VisualEngine import *

Curent_material = 2

def handle_controls():
    global Curent_material
    mouse = pr.get_mouse_position()
    world_mouse = pr.get_screen_to_world_2d(mouse, camera)

    X = int(world_mouse.x // 4)
    Y = int(world_mouse.y // 4)

    if pr.is_mouse_button_down(pr.MouseButton.MOUSE_BUTTON_LEFT):

        radius = TMP_cursor_scale

        for x in range(-radius, radius + 1):
            for y in range(-radius, radius + 1):

                if x*x + y*y <= radius*radius:
                    world_set(X + x, Y + y, Curent_material)

        print(f"painted area at {X}, {Y} with scale {TMP_cursor_scale}")