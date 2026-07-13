# VISUAL ENGINE DRAWS SOME SHIT ON SCREEN
#importing for you honey ~
from SandEngine.Libs import *
from SandEngine.DATA.TMP import *

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

    else:

        with open(MAP_PATH, "r") as f:
            world = json.load(f)


def save_map():
    global world

    with open(MAP_PATH, "w") as f:
        json.dump(world, f)


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

def world_set(x, y, material=1):
    global world

    if world is None:
        load_map()

    if 0 <= x < MAP_W and 0 <= y < MAP_H:
        world[y][x] = material


def world_erase(x, y):
    world_set(x, y, 0)


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


#its "UI" my honey
def draw_ui():
    mouse = pr.get_mouse_position()
    world_mouse = pr.get_screen_to_world_2d(mouse, camera)
    pr.draw_circle_lines(int(world_mouse.x), int(world_mouse.y), TMP_cursor_scale * 10, pr.RED)

# drawer function
def visuals_root():
    global camera

    pr.begin_drawing()
    pr.begin_mode_2d(camera)

    pr.clear_background(pr.BLACK)
    draw_map()
    draw_ui()

    pr.end_mode_2d()
    pr.end_drawing()
