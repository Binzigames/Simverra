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
    # піна
    if y > 0 and world[y - 1][x] != 3:
        return pr.Color(180, 240, 255, 255)

    wave = math.sin(x * 0.35 + y * 0.15) * 12
    n = tex_noise(x, y) * 0.3

    return pr.Color(
        clamp(25 + wave + n),
        clamp(110 + wave + n),
        clamp(200 + wave),
        255
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

