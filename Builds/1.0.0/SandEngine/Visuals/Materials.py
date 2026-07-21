from SandEngine.Libs import *

def tex_noise(x, y):
    random.seed((x * 92837111) ^ (y * 689287499))
    return random.randint(-18, 18)


def clamp(v):
    return max(0, min(255, int(v)))


# =========================
# SAND
# =========================
def M_Sand(color, x, y):
    n = tex_noise(x, y)

    return pr.Color(
        clamp(210 + n),
        clamp(175 + n),
        clamp(100 + n // 2),
        255
    )


# =========================
# WATER
# =========================
def M_Water(color, x, y, world):

    wave = math.sin(x * 0.35 + y * 0.15) * 12
    n = tex_noise(x, y) * 0.3

    return pr.Color(
        clamp(25 + wave + n),
        clamp(110 + wave + n),
        clamp(200 + wave),
        199
    )


# =========================
# WALL
# =========================
def M_Wall(color, x, y):
    n = tex_noise(x, y)

    base = clamp(120 + n)

    return pr.Color(base, base, base, 255)

# =========================
# GRAVIY
# =========================
def M_graviy(color, x, y):
    nois = tex_noise(x, y)

    return pr.Color(
        100 + nois,
        100 + nois,
        100 + nois // 2,
        255
    )
# =========================
# BACKGROUND
# =========================
def M_Background():
    pr.clear_background(pr.Color(35, 35, 40, 255))
    #gradient
    width = pr.get_screen_width()
    height = pr.get_screen_height()

    top = pr.Color(45, 45, 50, 255)
    bottom = pr.Color(25, 25, 30, 255)

    for y in range(height):
        t = y / height

        r = int(top.r * (1 - t) + bottom.r * t)
        g = int(top.g * (1 - t) + bottom.g * t)
        b = int(top.b * (1 - t) + bottom.b * t)

        pr.draw_line(
            0,
            y,
            width,
            y,
            pr.Color(r, g, b, 255)
        )
    #grid
    grid_color = pr.Color(55, 55, 60, 80)

    for x in range(0, pr.get_screen_width(), 50):
        pr.draw_line(x, 0, x, pr.get_screen_height(), grid_color)

    for y in range(0, pr.get_screen_height(), 50):
        pr.draw_line(0, y, pr.get_screen_width(), y, grid_color)