# LOGIC ENGINE COUNTS MATH ETC
#importing for you honey ~
from SandEngine.Libs import *
from SandEngine.DATA.TMP import *
from SandEngine.Visuals.VisualEngine import *
from SandEngine.Physics.objects import *
from SandEngine.Debuger import *
from SandEngine.DATA.GameConfig import *

#=====================
#controls system
#=====================

def handle_controls():
    global Curent_material, Fullscreen

    mouse = pr.get_mouse_position()
    world_mouse = pr.get_screen_to_world_2d(mouse, camera)

    X = int(world_mouse.x // 4)
    Y = int(world_mouse.y // 4)

    radius = max(1, min(int(get_wheel_rotation()), 5))
    r2 = radius * radius

    left = pr.is_mouse_button_down(pr.MouseButton.MOUSE_BUTTON_LEFT)
    right = pr.is_mouse_button_down(pr.MouseButton.MOUSE_BUTTON_RIGHT)

    if left or right:

        for yy in range(-radius, radius + 1):

            yy2 = yy * yy

            for xx in range(-radius, radius + 1):

                if xx * xx + yy2 > r2:
                    continue

                wx = X + xx
                wy = Y + yy

                if left and not get_mouse_hovery():
                    world_set(wx, wy, Curent_material)
                else:
                    world_set(wx, wy, 0)

    if pr.is_key_pressed(pr.KeyboardKey.KEY_ONE):
        Curent_material = 2

    elif pr.is_key_pressed(pr.KeyboardKey.KEY_TWO):
        Curent_material = 3

    elif pr.is_key_pressed(pr.KeyboardKey.KEY_THREE):
        Curent_material = 4

    elif pr.is_key_pressed(pr.KeyboardKey.KEY_FOUR):
        Curent_material = 5

    if pr.is_key_pressed(pr.KeyboardKey.KEY_F11):

        Fullscreen = not Fullscreen

        pr.toggle_fullscreen()

        if not Fullscreen:
            pr.set_window_size(800, 900)

#=====================
# down-screen menu
#=====================
def select_sand():
    global Curent_material
    Curent_material = 2


def select_water():
    global Curent_material
    Curent_material = 3


def select_wall():
    global Curent_material
    Curent_material = 4


def select_gravity():
    global Curent_material
    Curent_material = 5


def reset_map():
    global world

    world = load_map_return()
    activate_world(world)
    create_map_texture()
    clear_all_objects()



def handle_ui_buttons():

    button_width = 150
    button_height = 45
    spacing = 15

    panel_height = 75


    panel = pr.Rectangle(
        20,
        pr.get_screen_height() - panel_height - 15,
        pr.get_screen_width() - 40,
        panel_height
    )


    # PANEL
    panel_ui(
        panel,
        " MATERIAL SELECT >"
    )


    y = panel.y + 28



    buttons = [

        (
            pr.Rectangle(
                50,
                y,
                button_width,
                button_height
            ),
            "[1] SAND",
            pr.Color(210,180,70,255),
            pr.Color(20,20,20,255),
            select_sand
        ),


        (
            pr.Rectangle(
                50 + button_width + spacing,
                y,
                button_width,
                button_height
            ),
            "[2] WATER",
            pr.Color(50,140,220,255),
            pr.Color(20,20,20,255),
            select_water
        ),


        (
            pr.Rectangle(
                50 + (button_width + spacing) * 2,
                y,
                button_width,
                button_height
            ),
            "[3] WALL",
            pr.Color(120,120,120,255),
            pr.Color(20,20,20,255),
            select_wall
        ),


        (
            pr.Rectangle(
                50 + (button_width + spacing) * 3,
                y,
                button_width,
                button_height
            ),
            "[4] GRAVITY",
            pr.Color(100,100,100,255),
            pr.Color(20,20,20,255),
            select_gravity
        )

    ]


    for rect, text, color, text_color, action in buttons:

        Button(
            rect,
            text,
            action
        )



    # RESET BUTTON

    reset_rect = pr.Rectangle(
        pr.get_screen_width() - 230,
        y,
        200,
        button_height
    )


    Button(
        reset_rect,
        "RESET MAP",
        pr.Color(10,5,5,255),
    )