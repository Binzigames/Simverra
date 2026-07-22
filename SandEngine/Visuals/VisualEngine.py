# VISUAL ENGINE DRAWS SOME SHIT ON SCREEN
#importing for you honey ~
from SandEngine.Libs import *
from SandEngine.DATA.TMP import *
from SandEngine.Debuger import *
from SandEngine.Visuals.Materials import *
from SandEngine.Physics.objects import *
from SandEngine.Physics.PhysicsEngine import *
from SandEngine.DATA.GameConfig import *
from Assets.Assets_importer import *
from SandEngine.Audio.AudioEngine import *

#=====================
#camera
#=====================

#camera
camera = pr.Camera2D()

camera.target = pr.Vector2(0, 0)
camera.offset = pr.Vector2(0, 0)
camera.rotation = 0.0
camera.zoom = 1.0

# =====================
# SAVE USER WORLD
# =====================

def save_world_as():
    global world

    root = tk.Tk()
    root.withdraw()

    path = filedialog.asksaveasfilename(
        title="Save SimWorld",
        defaultextension=WORLD_EXTENSION,
        filetypes=[
            ("SimWorld map", "*.simvworld"),
            ("All files", "*.*")
        ]
    )

    root.destroy()

    if not path:
        return

    data = {
        "format": "SimVWorld",
        "version": 1,
        "width": MAP_W,
        "height": MAP_H,
        "world": world
    }

    with open(path, "w") as f:
        json.dump(data, f)

    print_message("World exported", 0)



# =====================
# LOAD USER WORLD
# =====================

def load_world_from_file():
    global world
    global map_texture

    root = tk.Tk()
    root.withdraw()

    path = filedialog.askopenfilename(
        title="Open SimWorld",
        filetypes=[
            ("SimWorld map", "*.simvworld"),
            ("All files", "*.*")
        ]
    )

    root.destroy()

    if not path:
        return

    try:

        with open(path, "r") as f:
            data = json.load(f)


        if data.get("format") != "SimVWorld":
            print_message("Wrong world format", 1)
            return


        world = data["world"]

        # оновити текстуру карти
        map_texture = None

        print_message("World loaded", 0)


    except Exception as e:
        print_message(str(e), 1)
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

    if pr.is_window_fullscreen():
        scale = pr.get_screen_width() / map_texture.width

        pr.draw_texture_pro(
            map_texture,
            pr.Rectangle(0, 0, map_texture.width, map_texture.height),
            pr.Rectangle(
                0,
                0,
                map_texture.width * scale,
                map_texture.height * scale
            ),
            pr.Vector2(0, 0),
            0.0,
            pr.WHITE
        )
    else:
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

            elif cell == 6 :
                color = M_bomb(color, x, y)

            elif cell == 7:
                color = M_soil(color, x, y, get_world())

            elif cell == 8:
                color = M_Gas()


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

    elif cell == 6:
        color = M_bomb(color, x, y)

    elif cell == 7:
        color = M_soil(color, x, y, get_world())

    elif cell == 8:
        color = M_Gas()


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

        elif cell == 6:
            color = M_bomb(color, x, y)

        elif cell == 7:
            color = M_soil(color, x, y, get_world())

        elif cell == 8:
            color = M_Gas()



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
is_hovered = False
#widgets
#text
def ui_text(text, x, y, size=24, color=UI_C_TEXT):

    # Shadow
    pr.draw_text_ex(
        get_font(),
        str(text),
        pr.Vector2(x + 1, y + 1),
        float(size),
        1,
        pr.Color(0, 0, 0, 90)
    )

    # Text
    pr.draw_text_ex(
        get_font(),
        str(text),
        pr.Vector2(x, y),
        float(size),
        1,
        color
    )

#buttons
def Button(rect, text, action=None):
    global is_hovered

    mouse = pr.get_mouse_position()

    hovered = pr.check_collision_point_rec(
        mouse,
        rect
    )

    if hovered:
        is_hovered = True

    color = UI_C_BG

    if hovered:
        color = pr.Color(58, 63, 72, 255)

        if pr.is_mouse_button_down(
            pr.MouseButton.MOUSE_BUTTON_LEFT
        ):
            color = UI_C_MAIN


    shadow = pr.Rectangle(
        rect.x,
        rect.y + 3,
        rect.width,
        rect.height
    )

    pr.draw_rectangle_rounded(
        shadow,
        0.35,
        8,
        pr.Color(0,0,0,60)
    )


    pr.draw_rectangle_rounded(
        rect,
        0.35,
        8,
        color
    )


    pr.draw_rectangle_rounded_lines_ex(
        rect,
        0.35,
        8,
        1,
        UI_C_BORDER
    )


    size = int(rect.height * 0.55)

    tw = pr.measure_text_ex(
        get_font(),
        text,
        float(size),
        1
    ).x


    ui_text(
        text,
        rect.x + (rect.width - tw) / 2,
        rect.y + (rect.height-size)/2,
        size
    )


    if hovered:

        pr.draw_rectangle_rounded_lines_ex(
            rect,
            0.35,
            8,
            2,
            UI_C_MAIN
        )


        if pr.is_mouse_button_pressed(
            pr.MouseButton.MOUSE_BUTTON_LEFT
        ):

            if action:
                play_sound(1)
                action()

def object_select_button(name, x, y):
    global selected_object

    mouse = pr.get_mouse_position()

    rect = pr.Rectangle(
        x,
        y,
        240,
        28
    )

    hover = pr.check_collision_point_rec(
        mouse,
        rect
    )

    selected = name == selected_object

    if selected:

        pr.draw_rectangle_rounded(
            rect,
            0.4,
            6,
            pr.Color(60,90,140,180)
        )

    elif hover:

        pr.draw_rectangle_rounded(
            rect,
            0.4,
            6,
            pr.Color(255,255,255,18)
        )

    icon = ">" if selected else "*"

    ui_text(
        f"{icon} {name.title()}",
        x + 10,
        y + 5,
        18,
        UI_C_TEXT if selected else UI_C_MUTED
    )

    if hover and pr.is_mouse_button_pressed(
        pr.MouseButton.MOUSE_BUTTON_LEFT
    ):
        selected_object = name

def get_mouse_hovery():
    global is_hovered
    return is_hovered



#buttons functions
def toggle_object_mode():
    global object_mode, object_menu

    object_mode = not object_mode
    object_menu = object_mode

def draw_object_mode_panel():

    panel = pr.Rectangle(
        20,
        300,
        300,
        250
    )


    panel_ui(
        panel,
        "OBJECT SELECT"
    )


    y = panel.y + 45


    for obj in OBJECTS:

        object_select_button(
            obj,
            panel.x + 15,
            y
        )

        y += 30

def object_select_button(name, x, y):
    global selected_object

    color = pr.YELLOW if name == selected_object else pr.WHITE

    ui_text(
        name,
        x,
        y,
        20,
        color
    )

    mouse = pr.get_mouse_position()

    if (
        pr.is_mouse_button_pressed(
            pr.MouseButton.MOUSE_BUTTON_RIGHT
        )
        and
        mouse.x > x and
        mouse.x < x + 180
        and
        mouse.y > y
        and
        mouse.y < y + 25
    ):
        selected_object = name


# Panel
def panel_ui(rect, title=None):
    global is_hovered

    mouse = pr.get_mouse_position()


    hovered = pr.check_collision_point_rec(
        mouse,
        rect
    )


    if hovered:
        is_hovered = True


    shadow = pr.Rectangle(
        rect.x + 5,
        rect.y + 5,
        rect.width,
        rect.height
    )


    pr.draw_rectangle_rounded(
        shadow,
        0.30,
        8,
        pr.Color(0,0,0,70)
    )


    pr.draw_rectangle_rounded(
        rect,
        0.30,
        8,
        UI_C_PANEL
    )


    pr.draw_rectangle_rounded_lines_ex(
        rect,
        0.30,
        8,
        1,
        UI_C_BORDER
    )


    if title:

        ui_text(
            title,
            rect.x + 18,
            rect.y + 14,
            20,
            UI_C_TEXT
        )

def draw_preview(world_mouse):

    data = OBJECTS[selected_object]

    pr.draw_rectangle(
        int(world_mouse.x),
        int(world_mouse.y),
        data["size"][0],
        data["size"][1],
        pr.fade(
            data["color"],
            0.25
        )
    )

    pr.draw_rectangle_lines(
        int(world_mouse.x),
        int(world_mouse.y),
        data["size"][0],
        data["size"][1],
        UI_C_ACCENT
    )

def draw_cursor():

    mouse = pr.get_mouse_position()

    world = pr.get_screen_to_world_2d(
        mouse,
        camera
    )

    r = max(
        1,
        min(int(get_wheel_rotation()),5)
    ) * 5

    pr.draw_circle(
        int(world.x),
        int(world.y),
        2,
        UI_C_ACCENT
    )

    pr.draw_circle_lines(
        int(world.x),
        int(world.y),
        r,
        UI_C_ACCENT
    )

    pr.draw_circle_lines(
        int(world.x),
        int(world.y),
        r + 5,
        pr.fade(UI_C_ACCENT,0.3)
    )

# global ui draw
def draw_ui():
    global Welcome_screen_shown, debug_menu, object_mode , is_hovered
    is_hovered = False
    mouse = pr.get_mouse_position()
    world_mouse = pr.get_screen_to_world_2d(mouse, camera)

    # ==========================
    # CURSOR
    # ==========================

    if not object_mode:
        draw_cursor()

    # ==========================
    # WELCOME SCREEN
    # ==========================

    if not Welcome_screen_shown:

        sw = pr.get_screen_width()
        sh = pr.get_screen_height()

        panel = pr.Rectangle(
            sw / 2 - 310,
            sh / 2 - 180,
            620,
            360
        )

        panel_ui(panel)

        ui_text(
            w_title,
            panel.x + 40,
            panel.y + 45,
            54,
            UI_C_TEXT
        )

        ui_text(
            "Physics Sandbox / all rights reserved!",
            panel.x + 42,
            panel.y + 105,
            22,
            UI_C_MUTED
        )

        ui_text(
            "Powered by Sand Engine",
            panel.x + 42,
            panel.y + 140,
            18,
            UI_C_MAIN
        )
        ui_text(
            "developed by @Porko_dev(YK) , @Krakenschwester",
            panel.x + 42,
            panel.y + 167,
            18,
            UI_C_MAIN
        )

        pr.draw_line(
            int(panel.x + 40),
            int(panel.y + 190),
            int(panel.x + panel.width - 40),
            int(panel.y + 190),
            UI_C_BORDER
        )

        ui_text(
            "LMB   Create Object",
            panel.x + 42,
            panel.y + 200,
            18
        )

        ui_text(
            "RMB   Delete Object",
            panel.x + 42,
            panel.y + 228,
            18
        )

        ui_text(
            "MMB   Spawn Selected Object",
            panel.x + 42,
            panel.y + 256,
            18
        )

        if int(pr.get_time() * 2) % 2:

            ui_text(
                "Click anywhere to begin",
                panel.x + 42,
                panel.y + 310,
                22,
                UI_C_ACCENT
            )

        if pr.is_mouse_button_pressed(
                pr.MouseButton.MOUSE_BUTTON_LEFT):
            Welcome_screen_shown = True

        return

    # ==========================
    # DEBUG
    # ==========================

    if debug_menu:

        panel = pr.Rectangle(
            pr.get_screen_width() - 340,
            20,
            320,
            210
        )

        panel_ui(
            panel,
            "Debug"
        )

        info = [

            ("FPS", pr.get_fps()),
            ("Mouse X", int(mouse.x)),
            ("Mouse Y", int(mouse.y)),
            ("Objects", len(objects)),
            ("Zoom", round(camera.zoom, 2))

        ]

        y = panel.y + 48

        for name, value in info:

            ui_text(
                f"{name:<10}",
                panel.x + 18,
                y,
                18,
                UI_C_MUTED
            )

            ui_text(
                str(value),
                panel.x + 170,
                y,
                18,
                UI_C_TEXT
            )

            y += 26

    # ==========================
    # TOP BAR
    # ==========================

    panel = pr.Rectangle(
        15,
        15,
        300,
        90
    )

    panel_ui(panel)

    ui_text(
        "Simverra",
        30,
        30,
        26
    )

    ui_text(
        "Physics Sandbox",
        30,
        58,
        16,
        UI_C_MUTED
    )

    # ==========================
    # TOOLBAR
    # ==========================

    Button(
        pr.Rectangle(
            20,
            120,
            180,
            40
        ),
        "Object Mode",
        toggle_object_mode
    )

    # ==========================
    # OBJECT PANEL
    # ==========================

    if object_menu:
        draw_object_mode_panel()

    # ==========================
    # PREVIEW
    # ==========================

    if object_mode:

        draw_preview(world_mouse)

        data = OBJECTS[selected_object]

        if pr.is_mouse_button_pressed(
                pr.MouseButton.MOUSE_BUTTON_MIDDLE):

            obj = GameObject(
                world_mouse.x,
                world_mouse.y,
                data["size"][0],
                data["size"][1],
                data["color"]
            )

            objects.append(obj)
            play_sound(1)

    # ==========================
    # DEBUG TOGGLE
    # ==========================

    if pr.is_key_pressed(
            pr.KeyboardKey.KEY_TAB):
        debug_menu = not debug_menu



#=====================
#loading srcreen
#=====================
def draw_loading_screen():
    M_Background()
    quote = random.choice(loading_texts)
    sw = pr.get_screen_width()
    sh = pr.get_screen_height()

    panel = pr.Rectangle(
        sw / 2 - 310,
        sh / 2 - 180,
        620,
        360
    )

    panel_ui(panel)

    ui_text(
        "Simverra",
        panel.x + 40,
        panel.y + 45,
        54,
        UI_C_TEXT
    )

    ui_text(
        "Physics Sandbox / all rights reserved!",
        panel.x + 42,
        panel.y + 105,
        22,
        UI_C_MUTED
    )

    ui_text(
        "Powered by Sand Engine",
        panel.x + 42,
        panel.y + 140,
        18,
        UI_C_MAIN
    )
    ui_text(
        quote,
        panel.x + 42,
        panel.y + 167,
        18,
        UI_C_MAIN
    )

    pr.draw_line(
        int(panel.x + 40),
        int(panel.y + 190),
        int(panel.x + panel.width - 40),
        int(panel.y + 190),
        UI_C_BORDER
    )
    ui_text(
        "loading you sandbox...",
        panel.x + 42,
        panel.y + 310,
        22,
        UI_C_ACCENT
     )

#=====================
# explosive
#=====================

def draw_explosions():

    dt = pr.get_frame_time()

    for e in explosions[:]:

        e["life"] -= dt

        progress = 1 - (e["life"] / e.get("max_life", 0.35))

        radius = max(
            1,
            int(8 + progress * e.get("max_radius", 80))
        )

        if progress < 0.15:

            pr.draw_rectangle(
                int(e["x"] - 8),
                int(e["y"] - 8),
                16,
                16,
                pr.WHITE
            )



        pr.draw_circle(
            int(e["x"]),
            int(e["y"]),
            radius,
            pr.Color(
                255,
                80,
                10,
                max(0, min(255, int(180 * (1 - progress))))
            )
        )




        core = max(
            3,
            radius // 3
        )

        pr.draw_circle(
            int(e["x"]),
            int(e["y"]),
            core,
            pr.Color(
                255,
                230,
                80,
                255
            )
        )




        for i in range(8):

            angle = i * 0.785

            px = int(
                e["x"] +
                math.cos(angle) * radius
            )

            py = int(
                e["y"] +
                math.sin(angle) * radius
            )


            pr.draw_rectangle(
                px,
                py,
                random.randint(3,6),
                random.randint(3,6),
                random.choice([
                    pr.ORANGE,
                    pr.RED,
                    pr.YELLOW
                ])
            )




        for i in range(5):

            sx = e["x"] + random.randint(
                -radius*2,
                radius*2
            )

            sy = e["y"] + random.randint(
                -radius*2,
                radius*2
            )

            pr.draw_rectangle(
                int(sx),
                int(sy),
                2,
                2,
                pr.YELLOW
            )


        if e["life"] <= 0:
            explosions.remove(e)

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

    draw_explosions()

    draw_ui()


    pr.end_mode_2d()
