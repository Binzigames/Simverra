# LOGIC ENGINE COUNTS MATH ETC
#importing for you honey ~
from SandEngine.Libs import *
from SandEngine.DATA.TMP import *
from SandEngine.Visuals.VisualEngine import *
from SandEngine.Debuger import *

Curent_material = 2
Fullscreen = False
def handle_controls():
    global Curent_material , Fullscreen
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

    if pr.is_key_pressed(pr.KeyboardKey.KEY_ONE):
        Curent_material = 2
    if pr.is_key_pressed(pr.KeyboardKey.KEY_TWO):
        Curent_material = 3
    if pr.is_key_pressed(pr.KeyboardKey.KEY_THREE):
        Curent_material = 4
    if pr.is_key_pressed(pr.KeyboardKey.KEY_F11):
        Fullscreen = not Fullscreen

        if Fullscreen:
            pr.toggle_fullscreen()
        else:
            pr.toggle_fullscreen()
            pr.set_window_size(800, 900)


def handle_ui_buttons():
    global Curent_material

    button_width = 150
    button_height = 45
    spacing = 15

    # RETRO PANEL
    panel_height = 75

    panel = pr.Rectangle(
        20,
        pr.get_screen_height() - panel_height - 15,
        pr.get_screen_width() - 40,
        panel_height
    )

    # background
    pr.draw_rectangle_rec(
        panel,
        pr.Color(10, 15, 10, 230)
    )

    # border
    pr.draw_rectangle_lines_ex(
        panel,
        2,
        pr.GREEN
    )

    # title
    pr.draw_text(
        " MATERIAL SELECT >",
        int(panel.x + 15),
        int(panel.y + 8),
        18,
        pr.GREEN
    )


    y = panel.y + 28

    buttons = [
        (
            pr.Rectangle(50, y, button_width, button_height),
            "[1] SAND",
            2,
            pr.Color(210,180,70,255)
        ),

        (
            pr.Rectangle(
                50 + button_width + spacing,
                y,
                button_width,
                button_height
            ),
            "[2] WATER",
            3,
            pr.Color(50,140,220,255)
        ),

        (
            pr.Rectangle(
                50 + (button_width + spacing)*2,
                y,
                button_width,
                button_height
            ),
            "[3] WALL",
            4,
            pr.Color(120,120,120,255)
        ),

        (
            pr.Rectangle(
                50 + (button_width + spacing) * 3,
                y,
                button_width,
                button_height,
            ),
            "[4] GRAVIY",
            5,
            pr.Color(100, 100, 100, 255)
        )
    ]


    mouse = pr.get_mouse_position()


    for rect, text, material, color in buttons:

        hovered = pr.check_collision_point_rec(
            mouse,
            rect
        )


        # button background
        if hovered:
            color = pr.Color(
                min(color.r+40,255),
                min(color.g+40,255),
                min(color.b+40,255),
                255
            )


        pr.draw_rectangle_rec(
            rect,
            pr.Color(
                5,
                5,
                5,
                255
            )
        )


        pr.draw_rectangle_lines_ex(
            rect,
            2,
            color
        )


        pr.draw_text(
            text,
            int(rect.x + 12),
            int(rect.y + 12),
            18,
            color
        )


        if hovered and pr.is_mouse_button_pressed(
            pr.MouseButton.MOUSE_BUTTON_LEFT
        ):
            Curent_material = material



    # RESET BUTTON

    reset_rect = pr.Rectangle(
        pr.get_screen_width()-230,
        y,
        200,
        button_height
    )


    hovered = pr.check_collision_point_rec(
        mouse,
        reset_rect
    )


    reset_color = pr.RED

    if hovered:
        reset_color = pr.Color(
            255,
            80,
            80,
            255
        )


    pr.draw_rectangle_rec(
        reset_rect,
        pr.Color(10,5,5,255)
    )


    pr.draw_rectangle_lines_ex(
        reset_rect,
        2,
        reset_color
    )


    pr.draw_text(
        "[R] RESET MAP",
        int(reset_rect.x+18),
        int(reset_rect.y+12),
        18,
        reset_color
    )


    if hovered and pr.is_mouse_button_pressed(
        pr.MouseButton.MOUSE_BUTTON_LEFT
    ):
        load_map()
