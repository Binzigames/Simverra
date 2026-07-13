# LOGIC ENGINE COUNTS MATH ETC
#importing for you honey ~
from SandEngine.Libs import *
from SandEngine.DATA.TMP import *
from SandEngine.Visuals.VisualEngine import *
from SandEngine.Debuger import *

Curent_material = 2

def handle_controls():
    global Curent_material
    mouse = pr.get_mouse_position()
    world_mouse = pr.get_screen_to_world_2d(mouse, camera)

    X = int(world_mouse.x // 4)
    Y = int(world_mouse.y // 4)
    radius = int(get_wheel_rotation())

    if pr.is_mouse_button_down(pr.MouseButton.MOUSE_BUTTON_LEFT):
        for x in range(-radius, radius + 1):
            for y in range(-radius, radius + 1):

                if x*x + y*y <= radius*radius:
                    world_set(X + x, Y + y, Curent_material)

        print_message(f"painted area at {X}, {Y} with scale {int(get_wheel_rotation())}" , 2)

    if pr.is_mouse_button_down(pr.MouseButton.MOUSE_BUTTON_RIGHT):
 

        for x in range(-radius, radius + 1):
            for y in range(-radius, radius + 1):

                if x*x + y*y <= radius*radius:
                    world_erase(X + x, Y + y)