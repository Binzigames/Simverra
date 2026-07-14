# VISUAL ENGINE DRAWS SOME SHIT ON SCREEN
#importing for you honey ~
from SandEngine.Libs import *
from SandEngine.DATA.TMP import *
from SandEngine.Debuger import *

#camera
camera = pr.Camera2D()

camera.target = pr.Vector2(0, 0)
camera.offset = pr.Vector2(0, 0)
camera.rotation = 0.0
camera.zoom = 1.0

# ===== MAP =====
MAP_W = 256
MAP_H = 256
PIXEL_SIZE = 4

MAP_PATH = "SandEngine/DATA/map.json"

world = None

def load_map():
    global world

    os.makedirs("SandEngine/DATA", exist_ok=True)

    if not os.path.exists(MAP_PATH):

        world = [[0 for x in range(MAP_W)] for y in range(MAP_H)]

        for y in range(MAP_H // 2, MAP_H):
            for x in range(MAP_W):
                world[y][x] = 1

        save_map()
        print_message("Loading map...", 0)

    else:

        with open(MAP_PATH, "r") as f:
            world = json.load(f)


def save_map():
    global world

    with open(MAP_PATH, "w") as f:
        json.dump(world, f)
    print_message("Saving map...", 0)


def draw_map():
    global world

    if world is None:
        load_map()

    for y, row in enumerate(world):
        for x, cell in enumerate(row):

            if cell == 0:
                continue

            color = pr.BROWN

            if cell == 2:
                color = pr.YELLOW
            elif cell == 3:
                color = pr.BLUE
            elif cell == 4:
                color = pr.RED

            pr.draw_rectangle(
                x * PIXEL_SIZE,
                y * PIXEL_SIZE,
                PIXEL_SIZE,
                PIXEL_SIZE,
                color
            )


# WORLD EDIT

def get_world():

    global world

    if world is None:
        load_map()

    return world

def world_set(x, y, material=1):
    global world

    if world is None:
        load_map()

    if 0 <= x < MAP_W and 0 <= y < MAP_H:
        world[y][x] = material


def world_erase(x, y):
    world_set(x, y, 0)
    print_message(f"assassinated on {x} , {y}", 2)


def world_get(x, y):
    global world

    if world is None:
        load_map()

    if 0 <= x < MAP_W and 0 <= y < MAP_H:
        return world[y][x]

    return None


def world_fill(x, y, w, h, material=1):
    for yy in range(y, y + h):
        for xx in range(x, x + w):
            world_set(xx, yy, material)


def world_clear(x, y, w, h):
    world_fill(x, y, w, h, 0)
    print_message("cleaning world..." , 2)

def get_wheel_rotation():
    global TMP_cursor_scale
    wheel = pr.get_mouse_wheel_move()
    if wheel != 0:
        TMP_cursor_scale += wheel * 0.5

    # Artem: My scroll bar is broken. It's will be pain if don't add keys :(
    if pr.is_key_pressed(pr.KeyboardKey.KEY_KP_ADD):
        TMP_cursor_scale += 0.5
    elif pr.is_key_pressed(pr.KeyboardKey.KEY_KP_SUBTRACT):
        TMP_cursor_scale -= 0.5

    TMP_cursor_scale = max(0.1, min(TMP_cursor_scale, 20.0))
    
    return TMP_cursor_scale
#its "UI" my honey
Welcome_screen_shown = False
debug_menu = False
def draw_ui():
    global Welcome_screen_shown , debug_menu
    mouse = pr.get_mouse_position()
    world_mouse = pr.get_screen_to_world_2d(mouse, camera)

    pr.draw_circle_lines(
        int(world_mouse.x),
        int(world_mouse.y),
        get_wheel_rotation() * 5,
        pr.RAYWHITE
    )
    if not  Welcome_screen_shown:
        pr.draw_text(
            "SIMULATED BOX",
            80,
            180,
            42,
            pr.GREEN
        )

        pr.draw_text(
            "PHYSICS SANDBOX v1.0",
            80,
            235,
            22,
            pr.DARKGREEN
        )

        if int(pr.get_time() * 2) % 2:
            pr.draw_text(
                "PRESS LEFT MOUSE BUTTON TO START",
                80,
                320,
                22,
                pr.GREEN
            )

        pr.draw_text(
            "LMB  CREATE OBJECT",
            80,
            380,
            18,
            pr.DARKGREEN
        )

        pr.draw_text(
            "RMB  DELETE OBJECT",
            80,
            405,
            18,
            pr.DARKGREEN
        )
        if pr.is_mouse_button_down(pr.MouseButton.MOUSE_BUTTON_LEFT):
            Welcome_screen_shown = True
    elif debug_menu:

        panel = pr.Rectangle(
            pr.get_screen_width() - 340,
            20,
            320,
            230
        )

        pr.draw_rectangle_rec(panel, pr.Color(15, 18, 15, 255))

        pr.draw_rectangle_lines_ex(
            panel,
            2,
            pr.GREEN
        )

        pr.draw_rectangle(
            int(panel.x),
            int(panel.y),
            int(panel.width),
            28,
            pr.GREEN
        )

        pr.draw_text(
            " DEBUG TERMINAL ",
            int(panel.x + 8),
            int(panel.y + 6),
            18,
            pr.BLACK
        )

        mouse = pr.get_mouse_position()

        info = [
            f"FPS        : {pr.get_fps()}",
            f"MOUSE X    : {int(mouse.x)}",
            f"MOUSE Y    : {int(mouse.y)}"
        ]

        y = panel.y + 45

        for line in info:
            pr.draw_text(
                line,
                int(panel.x + 12),
                int(y),
                18,
                pr.GREEN
            )
            y += 22

        if int(pr.get_time() * 2) % 2:
            pr.draw_text(
                "_",
                int(panel.x + 12),
                int(y + 5),
                18,
                pr.GREEN
            )
    else:

        panel = pr.Rectangle(15, 15, 300, 90)

        pr.draw_rectangle_rec(panel, pr.Color(15, 15, 15, 220))
        pr.draw_rectangle_lines_ex(panel, 2, pr.GREEN)

        pr.draw_text(
            "SIMULATED BOX v1.0",
            28,
            28,
            20,
            pr.GREEN
        )
        pr.draw_text(
            f"FPS : {pr.get_fps()}",
            28,
            75,
            18,
            pr.GREEN
        )

    if pr.is_key_pressed(pr.KeyboardKey.KEY_TAB):
        debug_menu = not debug_menu

# drawer function
def visuals_root():
    global camera
    pr.begin_mode_2d(camera)

    pr.clear_background(pr.BLACK)
    draw_map()
    draw_ui()

    pr.end_mode_2d()

