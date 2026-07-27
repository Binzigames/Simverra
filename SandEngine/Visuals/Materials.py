# ==========================================
# materials
# ==========================================

from SandEngine.Libs import *


# ==========================================
# GLOBAL STATE
# ==========================================

FRAME_TIME = 0.0


# Noise cache
_noise_cache = {}


# Material caches
_sand_cache = {}
_wall_cache = {}
_water_cache = {}
_gas_cache = {}


# ==========================================
# FRAME UPDATE
# ==========================================

def BeginFrame():
    global FRAME_TIME
    FRAME_TIME = pr.get_time()



# ==========================================
# FAST HELPERS
# ==========================================

def clamp(v):

    if v < 0:
        return 0

    if v > 255:
        return 255

    return int(v)



# ==========================================
# FAST HASH NOISE
# ==========================================

def tex_noise(x, y):

    key = (x, y)

    cached = _noise_cache.get(key)

    if cached is not None:
        return cached


    n = x * 374761393 + y * 668265263

    n = (n ^ (n >> 13)) * 1274126177

    n ^= n >> 16

    value = (n & 31) - 16


    _noise_cache[key] = value


    return value



# ==========================================
# SAND
# ==========================================

def M_Sand(color, x, y):

    key = (x, y)

    cached = _sand_cache.get(key)

    if cached:
        return cached


    n = tex_noise(x, y)

    sparkle = tex_noise(
        x + 71,
        y + 53
    )


    r = 205 + n
    g = 175 + n
    b = 110 + n // 2


    if sparkle > 13:

        r += 25
        g += 20
        b += 40


    result = pr.Color(
        clamp(r),
        clamp(g),
        clamp(b),
        255
    )


    _sand_cache[key] = result


    return result



# ==========================================
# WATER
# ==========================================

def M_Water(color, x, y, world):

    key = (x, y)


    cached = _water_cache.get(key)




    t = FRAME_TIME


    wave = math.sin(
        x * 0.3 +
        y * 0.2 +
        t * 2
    ) * 18


    glow = math.sin(
        t * 4 +
        x * 0.2
    ) * 12



    return pr.Color(
        clamp(30 + glow),
        clamp(120 + wave),
        clamp(220 + wave),
        190
    )



# ==========================================
# GAS
# ==========================================

def M_Gas():


    t = FRAME_TIME


    alpha = 70 + int(
        math.sin(t * 5) * 20
    )


    return pr.Color(
        180,
        120,
        255,
        alpha
    )



# ==========================================
# WALL
# ==========================================

def M_Wall(color, x, y):

    key = (x, y)


    cached = _wall_cache.get(key)

    if cached:
        return cached



    n = tex_noise(x, y)


    vein = tex_noise(
        x + 91,
        y + 27
    )



    r = 105 + n
    g = 105 + n
    b = 115 + n



    if vein > 12:

        r += 30
        g += 10
        b += 60



    result = pr.Color(
        clamp(r),
        clamp(g),
        clamp(b),
        255
    )


    _wall_cache[key] = result


    return result

# ==========================================
# WOOD
# ==========================================

_wood_cache = {}


def M_Wood(x, y):

    key = (x, y)


    cached = _wood_cache.get(key)

    if cached:
        return cached



    n = tex_noise(x, y)


    rings = math.sin(
        y * 0.4 +
        x * 0.05
    ) * 15



    result = pr.Color(

        clamp(
            95 +
            n +
            rings
        ),

        clamp(
            65 +
            n // 2
        ),

        clamp(
            40 +
            n // 3
        ),

        255
    )


    _wood_cache[key] = result


    return result



# ==========================================
# GRAVEL
# ==========================================

_gravel_cache = {}


def M_graviy(color, x, y):

    key = (x, y)


    cached = _gravel_cache.get(key)

    if cached:
        return cached



    n = tex_noise(x, y)



    result = pr.Color(

        100 + n,

        100 + n,

        100 + n // 2,

        255
    )


    _gravel_cache[key] = result


    return result



# ==========================================
# BOMB
# ==========================================

_bomb_cache = {}


def M_bomb(color, x, y):

    key = (x, y)


    cached = _bomb_cache.get(key)

    if cached:
        return cached



    n = tex_noise(x, y)



    if (
        (x & 3) == 1 and
        (y & 3) == 1
    ):

        result = pr.Color(
            255,
            40,
            40,
            255
        )


    else:

        result = pr.Color(

            70 + n,

            70 + n,

            80 + n,

            255
        )



    _bomb_cache[key] = result


    return result



# ==========================================
# SOIL
# ==========================================

_soil_cache = {}


def M_soil(color, x, y, world):

    key = (x, y)


    cached = _soil_cache.get(key)

    if cached:
        return cached



    n = tex_noise(x, y)



    result = pr.Color(

        110 + n,

        70 + n // 2,

        35 + n // 3,

        255
    )



    _soil_cache[key] = result


    return result



# ==========================================
# FIRE
# ==========================================

def M_fire(x, y):


    t = FRAME_TIME



    flicker = math.sin(
        t * 30 +
        x +
        y
    ) * 35



    return pr.Color(

        255,

        clamp(
            80 + flicker
        ),

        clamp(
            180 + flicker
        ),

        255
    )



# ==========================================
# BLACK HOLE CACHE
# ==========================================

_hole_cache = {}


def _create_hole_pixel(x, y):


    u = x / 18
    v = y / 18


    dx = u - 0.5
    dy = v - 0.5


    dist2 = (
        dx * dx +
        dy * dy
    )

    angle = math.atan2(
        dy,
        dx
    )



    dist = dist2 ** 0.5



    warp = math.sin(
        angle * 10 +
        dist * 30
    ) * 0.08


    dist += warp



    hole = max(
        0,
        1 - dist / 0.18
    )


    hole = hole ** 5



    ring = math.exp(
        -(
            (dist - 0.26)
            * 28
        ) ** 2
    )



    swirl = (
        math.sin(
            angle * 14 +
            dist * 80
        )
        + 1
    ) * 0.5



    ring *= (
        0.5 +
        swirl
    )



    aura = math.exp(
        -(
            (dist - 0.36)
            * 10
        ) ** 2
    )



    r = 8
    g = 5
    b = 20



    r += int(
        ring * 255
    )

    g += int(
        ring * 80
    )

    b += int(
        ring * 255
    )



    r += int(
        aura * 60
    )

    g += int(
        aura * 20
    )

    b += int(
        aura * 140
    )



    dark = int(
        hole * 255
    )



    r -= dark
    g -= dark
    b -= dark



    return pr.Color(
        clamp(r),
        clamp(g),
        clamp(b),
        255
    )



# ==========================================
# BLACK HOLE
# ==========================================

def M_hole(x, y):

    key = (x, y)


    cached = _hole_cache.get(key)


    if cached:

        return cached



    result = _create_hole_pixel(
        x,
        y
    )



    _hole_cache[key] = result


    return result

# ==========================================
# BACKGROUND OPTIMIZED
# ==========================================


_stars = []
_stars_ready = False


def _generate_stars():

    global _stars_ready


    if _stars_ready:
        return


    width = pr.get_screen_width()
    height = pr.get_screen_height()



    for x in range(0, width, 6):

        for y in range(0, height, 6):

            if tex_noise(
                x * 4,
                y * 4
            ) > 14:


                size = 1

                brightness = (
                    tex_noise(
                        x,
                        y
                    ) + 16
                ) * 4


                _stars.append(
                    (
                        x,
                        y,
                        size,
                        brightness
                    )
                )


    _stars_ready = True



def M_Background():

    _generate_stars()



    width = pr.get_screen_width()
    height = pr.get_screen_height()


    t = FRAME_TIME



    # ==================================
    # GRADIENT
    # ==================================

    top_r = 20
    top_g = 15
    top_b = 45


    bottom_r = 4
    bottom_g = 5
    bottom_b = 18



    for y in range(height):

        k = y / height


        color = pr.Color(

            int(
                top_r *
                (1-k)
                +
                bottom_r *
                k
            ),

            int(
                top_g *
                (1-k)
                +
                bottom_g *
                k
            ),

            int(
                top_b *
                (1-k)
                +
                bottom_b *
                k
            ),

            255
        )


        pr.draw_line(
            0,
            y,
            width,
            y,
            color
        )



    # ==================================
    # MAGIC FOG
    # ==================================

    for y in range(
        0,
        height,
        6
    ):


        wave = math.sin(
            y * 0.018 +
            t * 0.4
        ) * 20



        alpha = 7 + int(
            (
                math.sin(
                    y * 0.05 +
                    t
                )
                + 1
            )
            * 3
        )



        pr.draw_rectangle(

            int(wave),

            y,

            width,

            6,

            pr.Color(
                60,
                35,
                110,
                alpha
            )
        )



    # ==================================
    # NEBULA
    # ==================================

    for x in range(
        0,
        width,
        40
    ):

        for y in range(
            0,
            height,
            40
        ):


            n = tex_noise(
                x // 8,
                y // 8
            )



            if n > 8:


                pulse = int(

                    (
                        math.sin(
                            t +
                            x * 0.01 +
                            y * 0.02
                        )
                        + 1
                    )
                    * 5

                )



                pr.draw_circle(

                    x,

                    y,

                    12 + n,

                    pr.Color(

                        70 + pulse,

                        40 + pulse,

                        120 + pulse,

                        10

                    )
                )



    # ==================================
    # STARS
    # ==================================

    for star in _stars:


        x, y, size, bright = star



        flicker = int(

            (
                math.sin(
                    t * 5 +
                    x * 0.1 +
                    y * 0.2
                )
                + 1
            )
            * 20

        )



        c = clamp(
            bright +
            flicker
        )


        pr.draw_pixel(

            x,

            y,

            pr.Color(

                c,

                c,

                255,

                200

            )
        )



    # ==================================
    # MAGIC RUNES
    # ==================================

    rune = pr.Color(
        130,
        70,
        255,
        20
    )


    for x in range(
        100,
        width,
        320
    ):


        r = 60 + int(
            math.sin(
                t + x
            ) * 5
        )


        pr.draw_circle_lines(
            x,
            120,
            r,
            rune
        )


        pr.draw_circle_lines(
            x,
            120,
            r - 8,
            rune
        )


        pr.draw_circle_lines(
            x,
            120,
            r + 8,
            rune
        )



# ==========================================
# END
# ==========================================