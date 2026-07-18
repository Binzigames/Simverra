# VISUAL ENGINE DRAWS SOME SHIT ON SCREEN
#importing for you honey ~

from SandEngine.Libs import *
from SandEngine.DATA.TMP import *
from SandEngine.Debuger import *
from SandEngine.Visuals.Materials import *
from SandEngine.Physics.objects import *
from SandEngine.Physics.PhysicsEngine import *
from SandEngine.DATA.GameConfig import *

#=====================
#camera
#=====================

#camera
camera = pr.Camera2D()

camera.target = pr.Vector2(0, 0)
camera.offset = pr.Vector2(0, 0)
camera.rotation = 0.0
camera.zoom = 1.0


#=====================
# map functions
#=====================
def load_map():
    global world

    os.makedirs("SandEngine/DATA", exist_ok=True)

    if not os.path.exists(MAP_PATH):

        world = [[0 for x in range(MAP_W)] for y in range(MAP_H)]

        for y in range(MAP_H // 2, MAP_H):
            for x in range(MAP_W):
                world[y][x] = 4

        save_map()
        print_message("map loaded", 0)
    else:

        with open(MAP_PATH, "r") as f:
            world = json.load(f)
            print_message("Map opened", 0)

def load_map_return():
    global world

    os.makedirs("SandEngine/DATA", exist_ok=True)

    if not os.path.exists(MAP_PATH):

        world = [[0 for x in range(MAP_W)] for y in range(MAP_H)]

        for y in range(MAP_H // 2, MAP_H):
            for x in range(MAP_W):
                world[y][x] = 4

        save_map()
        print_message("Loading map with return...", 0)
        return world

    else:

        with open(MAP_PATH, "r") as f:
            world = json.load(f)
            return world


def save_map():
    global world

    with open(MAP_PATH, "w") as f:
        json.dump(world, f)
    print_message("map was saved", 0)

def draw_map():
    global map_texture

    if map_texture is None:
        create_map_texture()

    pr.draw_texture(
        map_texture,
        0,
        0,
        pr.WHITE
    )

#=====================
# map texture and  optimize stuff
#=====================
def create_map_texture():
    global world, map_texture, map_image

    if world is None:
        load_map()

    width = len(world[0]) * PIXEL_SIZE
    height = len(world) * PIXEL_SIZE

    map_image = pr.gen_image_color(
        width,
        height,
        pr.BLANK
    )

    update_map_texture()

    map_texture = pr.load_texture_from_image(map_image)
    print_message("Map was created", 0)


def update_map_texture():
    global map_image

    for y, row in enumerate(world):
        for x, cell in enumerate(row):

            if cell == 0:
                continue

            color = pr.BROWN

            if cell == 2:
                color = M_Sand(color, x, y)

            elif cell == 3:
                color = M_Water(color, x, y, get_world())

            elif cell == 4:
                color = M_Wall(color, x, y)

            elif cell == 5:
                color = M_graviy(color, x, y)


            for py in range(PIXEL_SIZE):
                for px in range(PIXEL_SIZE):

                    pr.image_draw_pixel(
                        map_image,
                        x * PIXEL_SIZE + px,
                        y * PIXEL_SIZE + py,
                        color
                    )


def update_cell_texture(x, y):
    global map_texture

    cell = world[y][x]

    color = pr.BLANK

    if cell == 2:
        color = M_Sand(pr.BROWN, x, y)

    elif cell == 3:
        color = M_Water(pr.BLUE, x, y, get_world())

    elif cell == 4:
        color = M_Wall(pr.GRAY, x, y)

    elif cell == 5:
        color = M_graviy(pr.GRAY, x, y)


    for py in range(PIXEL_SIZE):
        for px in range(PIXEL_SIZE):

            pr.image_draw_pixel(
                map_image,
                x * PIXEL_SIZE + px,
                y * PIXEL_SIZE + py,
                color
            )

    pr.update_texture(
        map_texture,
        map_image.data
    )

#=====================
# dirty textures
#=====================

def update_dirty_texture():

    cells = get_dirty_cells()

    if not cells:
        return


    for x, y in cells:

        cell = world[y][x]

        color = pr.BLANK


        if cell == 2:
            color = M_Sand(pr.BROWN, x, y)

        elif cell == 3:
            color = M_Water(pr.BLUE, x, y, world)

        elif cell == 4:
            color = M_Wall(pr.GRAY, x, y)

        elif cell == 5:
            color = M_graviy(pr.GRAY, x, y)



        for py in range(PIXEL_SIZE):

            for px in range(PIXEL_SIZE):

                pr.image_draw_pixel(
                    map_image,
                    x * PIXEL_SIZE + px,
                    y * PIXEL_SIZE + py,
                    color
                )


    pr.update_texture(
        map_texture,
        map_image.data
    )


#=====================
# world edit stuff
#=====================


def get_world():

    global world

    if world is None:
        load_map()

    return world

def world_set(x,y,material=1):
    global world

    if world is None:
        load_map()

    if 0 <= x < MAP_W and 0 <= y < MAP_H:
        world[y][x] = material

        if map_texture:
            update_cell_texture(x,y)
            print_message(f"set material on {x} , {y}", 2)

def world_erase(x, y):
    global world
    world_set(x, y, 0)
    update_materials(world)
    print_message(f"assassinated material on {x} , {y}", 2)


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
    update_cell_texture(x, y)
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

#=====================
#its "UI" my honey
#=====================

def draw_ui():
    global Welcome_screen_shown , debug_menu , object_mode , selected_object , object_menu
    mouse = pr.get_mouse_position()
    world_mouse = pr.get_screen_to_world_2d(mouse, camera)
    if not object_mode:
        pr.draw_circle_lines(
            int(world_mouse.x),
            int(world_mouse.y),
            max(1, min(int(get_wheel_rotation()), 5)) * 5,
            pr.RAYWHITE
        )
    if not  Welcome_screen_shown:
        pr.draw_text(
            "Simverra",
            80,
            180,
            42,
            pr.GREEN
        )

        pr.draw_text(
            "PHYSICS SANDBOX v1.0 / developed by : @porko_dev , @krakenschwester",
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
        pr.draw_text(
            "POWERED BY SAND ENGINE...",
            80,
            450,
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

        pr.draw_rectangle_rounded(panel, 0.1, 3,pr.Color(15, 18, 15, 255))

        pr.draw_rectangle_rounded_lines_ex(panel, 0.1, 3, 2, pr.GREEN)

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

        pr.draw_rectangle_rounded(panel, 0.1, 3, pr.Color(15, 15, 15, 220))
        pr.draw_rectangle_rounded_lines_ex(panel, 0.1, 3, 2, pr.GREEN)

        pr.draw_text(
            "Simverra v1.0",
            28,
            28,
            20,
            pr.GREEN
        )
        # =========================
        # OBJECT SPAWN SYSTEM
        # =========================

        mouse = pr.get_mouse_position()

        world_mouse = pr.get_screen_to_world_2d(
            mouse,
            camera
        )

        # OBJECT MODE BUTTON

        pr.draw_rectangle_rounded(
            pr.Rectangle(20, 120, 170, 35),
            0.2,
            3,
            pr.DARKGREEN
        )

        pr.draw_text(
            "OBJECT MODE",
            30,
            128,
            18,
            pr.WHITE
        )

        if pr.is_mouse_button_pressed(
                pr.MouseButton.MOUSE_BUTTON_LEFT
        ):

            if (
                    mouse.x > 20 and
                    mouse.x < 190 and
                    mouse.y > 120 and
                    mouse.y < 155
            ):
                object_mode = not object_mode
                object_menu = object_mode

        # OBJECT MENU

        if object_menu:

            panel = pr.Rectangle(
                20,
                170,
                240,
                220
            )

            pr.draw_rectangle_rec(
                panel,
                pr.Color(10, 10, 10, 230)
            )

            pr.draw_rectangle_lines_ex(
                panel,
                2,
                pr.GREEN
            )

            pr.draw_text(
                "SPAWNER",
                35,
                185,
                22,
                pr.GREEN
            )
            pr.draw_text(
                "RPESS MMB TO SPAWN",
                35,
                400,
                22,
                pr.GREEN
            )

            y = 230

            for name in OBJECTS:

                color = pr.WHITE

                if name == selected_object:
                    color = pr.YELLOW

                pr.draw_text(
                    name,
                    45,
                    y,
                    20,
                    color
                )

                if pr.is_mouse_button_pressed(
                        pr.MouseButton.MOUSE_BUTTON_RIGHT
                ):

                    if (
                            mouse.x > 35 and
                            mouse.x < 220 and
                            mouse.y > y and
                            mouse.y < y + 25
                    ):
                        selected_object = name

                y += 35

        # PREVIEW CIRCLE

        if object_mode:

            data = OBJECTS[selected_object]

            pr.draw_rectangle_lines(
                int(world_mouse.x),
                int(world_mouse.y),
                data["size"][0],
                data["size"][1],
                pr.YELLOW
            )

            if pr.is_mouse_button_pressed(
                    pr.MouseButton.MOUSE_BUTTON_MIDDLE
            ):
                obj = GameObject(
                    world_mouse.x,
                    world_mouse.y,
                    data["size"][0],
                    data["size"][1],
                    data["color"]
                )

                objects.append(obj)

    if pr.is_key_pressed(pr.KeyboardKey.KEY_TAB):
        debug_menu = not debug_menu


#=====================
# root
#=====================
def visuals_root():

    global camera


    dt = pr.get_frame_time()


    update_objects(
        world,
        dt
    )



    update_dirty_texture()

    pr.begin_mode_2d(camera)


    M_Background()


    draw_map()

    draw_objects()

    draw_ui()


    pr.end_mode_2d()
