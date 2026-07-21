# LOGIC ENGINE COUNTS MATH ETC
#importing for you honey ~
from SandEngine.Additions.ModdingEngine import is_moded
from SandEngine.Libs import *
from SandEngine.DATA.TMP import *
from SandEngine.Visuals.VisualEngine import *
from SandEngine.Physics.objects import *
from SandEngine.Debuger import *
from SandEngine.DATA.GameConfig import *
from SandEngine.Audio.AudioEngine import *


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
                    play_sound(2)
                else:
                    if not get_mouse_hovery():
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
def open_wiki():
    webbrowser.open(
        "https://github.com/Binzigames/Simverra/wiki"
    )
#=====================
#Groops tabs
#=====================
opened_group = None

material_groups = {
    "Physics": [
        ("Sand", select_sand),
        ("Water", select_water),
    ],

    "Not Physical": [
        ("Wall", select_wall),
    ],

    "Special": [
        ("Gravity", select_gravity),
    ],
    "Mods": [

    ]
}

def refresh_material_groups(mods):
    material_groups["Mods"] = [
        item
        for mod in mods
        for item in (
            [(f"[{mod.name}]", None)] +
            (mod.build_menu() or mod.menu)
        )
    ]
def handle_ui_buttons():

    global opened_group

    sw = pr.get_screen_width()
    sh = pr.get_screen_height()

    margin = 20
    gap = 8



    # ==========================
    # GROUP PANEL
    # ==========================

    clear_w = 120

    group_panel = pr.Rectangle(
        margin,
        sh - 60,
        sw - margin * 2 - clear_w - 15,
        40
    )


    panel_ui(group_panel)


    groups = list(material_groups.keys())


    group_w = (
        group_panel.width - 20 - gap * (len(groups)-1)
    ) / len(groups)


    x = group_panel.x + 10


    for group in groups:


        def choose(g=group):

            global opened_group

            if opened_group == g:
                opened_group = None
            else:
                opened_group = g


        Button(
            pr.Rectangle(
                x,
                group_panel.y + 4,
                group_w,
                32
            ),
            group,
            choose
        )


        x += group_w + gap



    # ==========================
    # CLEAR PANEL
    # ==========================
    clear_w = 80
    panel_h = 220
    margin = 20

    clear_panel = pr.Rectangle(
        sw - clear_w - margin,
        sh - panel_h - margin,
        clear_w,
        panel_h
    )

    panel_ui(clear_panel)

    Button(
        pr.Rectangle(
            clear_panel.x + 10,
            clear_panel.y + 10,
            clear_w - 20,
            32
        ),
        "CLEAR",
        reset_map
    )

    Button(
        pr.Rectangle(
            clear_panel.x + 10,
            clear_panel.y + 50,
            clear_w - 20,
            32
        ),
        "WIKI",
        open_wiki
    )

    Button(
        pr.Rectangle(
            clear_panel.x + 10,
            clear_panel.y + 90,
            clear_w - 20,
            32
        ),
        "SAVE",
        save_world_as
    )

    Button(
        pr.Rectangle(
            clear_panel.x + 10,
            clear_panel.y + 130,
            clear_w - 20,
            32
        ),
        "LOAD",
        load_world_from_file
    )

    Button(
        pr.Rectangle(
            clear_panel.x + 10,
            clear_panel.y + 170,
            clear_w - 20,
            32
        ),
        "AUDIO",
        toggle_audio
    )


    # ==========================
    # MATERIAL PANEL
    # ==========================


    if opened_group is not None:


        materials = material_groups[opened_group]


        material_w = 115
        material_h = 34


        panel_w = (
            len(materials) *
            (material_w + gap)
            + 20
        )


        material_panel = pr.Rectangle(

            margin,

            sh - 128,

            max(250, panel_w),

            58
        )


        panel_ui(
            material_panel
        )


        x = material_panel.x + 10


        for name, action in materials:


            Button(

                pr.Rectangle(

                    x,

                    material_panel.y + 20,

                    material_w,

                    material_h
                ),

                name,

                action
            )


            x += material_w + gap