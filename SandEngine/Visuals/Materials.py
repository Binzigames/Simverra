from SandEngine.Libs import *


def tex_noise(x, y):
    n = x * 374761393 + y * 668265263
    n = (n ^ (n >> 13)) * 1274126177
    n ^= n >> 16
    return (n & 31) - 16


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
# GASES
# =========================
def M_Gas():

    return pr.Color(
        150,
        150,
        150,
        80
    )
# =========================
# WALL
# =========================
def M_Wall(color, x, y):
    n = tex_noise(x, y)

    base = clamp(120 + n)

    return pr.Color(base, base, base, 255)
# =========================
# WOOD
# =========================
def M_Wood( x, y):
    n = tex_noise(x, y)

    r = clamp(110 + n)
    g = clamp(70 + n // 2)
    b = clamp(35 + n // 3)

    if tex_noise(x * 3, y * 3) > 20:
        r -= 25
        g -= 15
        b -= 10

    return pr.Color(r, g, b, 255)



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
# BOMB
# =========================
def M_bomb(color, x, y):
    nois = tex_noise(x, y)

    if (x % 4 == 1 and y % 4 == 1):
        return pr.Color(
            255,
            40,
            40,
            255
        )


    return pr.Color(
        70 + nois,
        70 + nois,
        80 + nois,
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

# =========================
# GRASS + DIRT
# =========================
def M_soil(color, x, y , world):

    nois = tex_noise(x, y)

    return pr.Color(
        110 + nois,
        70 + nois // 2,
        35 + nois // 3,
        255
    )
# =========================
# FIRE
# =========================
def M_fire( x, y):

    flicker = int(
        math.sin(pr.get_time() * 18 + x * 0.7 + y * 0.5) * 25
    )

    nois = tex_noise(x, y)

    r = min(255, 240 + flicker)
    g = max(80, 170 + nois // 3 + flicker)
    b = max(0, 30 + nois // 8)

    return pr.Color(r, g, b, 255)

# =========================
# BlackHole
# =========================
def M_hole(x, y):

    t = pr.get_time()


    u = x / 16.0
    v = y / 16.0



    space = (math.sin(u * 0.8) + math.cos(v * 0.7)) * 0.5

    bg_r = int(5 + 10 * space)
    bg_g = int(8 + 15 * space)
    bg_b = int(25 + 50 * space)



    holes = [
        (0.25, 0.30, 0.10),
        (0.70, 0.25, 0.07),
        (0.45, 0.75, 0.13),
        (0.85, 0.70, 0.08),
        (0.15, 0.80, 0.06),
    ]

    total_glow = 0
    total_dark = 0

    for hx, hy, size in holes:

        dx = u - hx
        dy = v - hy

        d = math.sqrt(dx*dx + dy*dy)

        angle = math.atan2(dy, dx)

        noise = tex_noise(x + int(hx*100), y + int(hy*100)) / 255.0



        ring = math.sin(
            angle * 12 -
            t * 6 +
            noise * 8
        )


        glow = math.exp(
            -((d - size*2.2) * 30)**2
        )

        glow *= 0.6 + ring * 0.4



        hole = 1.0 - min(
            1.0,
            d / size
        )

        hole = hole ** 4


        total_glow += glow
        total_dark += hole




    star_noise = tex_noise(x*3, y*3)

    if star_noise > 245:
        bg_r += 80
        bg_g += 80
        bg_b += 120




    r = bg_r + int(total_glow * 180)
    g = bg_g + int(total_glow * 70)
    b = bg_b + int(total_glow * 230)


    dark = int(total_dark * 255)

    r -= dark
    g -= dark
    b -= dark



    flick = int(
        (math.sin(t*20 + x*y) + 1) * 4
    )

    r += flick
    g += flick//2
    b += flick


    return pr.Color(
        int(max(0,min(255,r))),
        int(max(0,min(255,g))),
        int(max(0,min(255,b))),
        255
    )