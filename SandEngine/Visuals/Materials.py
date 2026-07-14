# VISUAL ENGINE/MATERIALS GIVES SOME MATERIALS
#importing for you honey ~
from SandEngine.Libs import *

IsnoiseGenerated = False
NoiseTMP = 0
def noise():
    global IsnoiseGenerated , NoiseTMP
    if not IsnoiseGenerated:
        noise = random.randint(-18, 18)
        NoiseTMP = noise
        IsnoiseGenerated = True
    else:
        noise = NoiseTMP
    return noise

def M_sand(color, x, y):
    nois = noise()

    return pr.Color(
        210 + nois,
        175 + nois,
        100 + nois // 2,
        255
    )


def M_Water(color, x, y, world):
    if y > 0 and world[y-1][x] != 3:
        return pr.Color(180, 240, 255, 255)

    wave = math.sin(x * 0.4 + y * 0.2) * 15

    noise = random.randint(0, 8)

    return pr.Color(
        int(20 + wave + noise),
        int(110 + wave + noise),
        int(200 + wave),
        255
    )


def M_Wall(color, x, y):
    nois = noise()

    base = 120 + nois

    return pr.Color(
        base,
        base,
        base,
        255
    )