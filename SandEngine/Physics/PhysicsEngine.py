# MATERIAL PHYSICS
# handles sand, water and other tile behaviors

from random import randint


# ===== MATERIAL IDS =====

AIR = 0
SAND = 2
WATER = 3
STONE = 4
GRAVIY = 5

# ===== MAP SIZE =====

MAP_W = 256
MAP_H = 256



# ===== HELPERS =====

def inside(x, y):
    return 0 <= x < MAP_W and 0 <= y < MAP_H



def swap(world, x1, y1, x2, y2):

    world[y1][x1], world[y2][x2] = (
        world[y2][x2],
        world[y1][x1]
    )



# ===== SAND =====

def update_sand(world, x, y):

    # falling down
    if world[y + 1][x] == AIR:
        swap(world, x, y, x, y + 1)
        return


    # diagonal movement
    direction = -1 if randint(0, 1) else 1


    for dx in (direction, -direction):

        nx = x + dx

        if inside(nx, y + 1):

            target = world[y + 1][nx]

            if target == AIR or target == WATER:

                swap(world, x, y, nx, y + 1)
                return



# ===== WATER =====

def update_water(world, x, y):

    # вниз
    if inside(x, y + 1) and world[y + 1][x] == AIR:
        swap(world, x, y, x, y + 1)
        return

    direction = -1 if randint(0, 1) else 1

    # діагональ вниз
    for dx in (direction, -direction):

        nx = x + dx

        if inside(nx, y + 1) and world[y + 1][nx] == AIR:
            swap(world, x, y, nx, y + 1)
            return

    # шукати шлях убік
    MAX_FLOW = 2

    for dx in (direction, -direction):

        for dist in range(1, MAX_FLOW + 1):

            nx = x + dx * dist

            if not inside(nx, y):
                break

            # стіна
            if world[y][nx] != AIR:
                break

            # знайшли місце, де можна впасти
            if inside(nx, y + 1) and world[y + 1][nx] == AIR:
                swap(world, x, y, nx, y)
                return

        # якщо просто є вільне місце поруч
        nx = x + dx

        if inside(nx, y) and world[y][nx] == AIR:
            swap(world, x, y, nx, y)
            return


# ===== MAIN UPDATE =====

def update_materials(world):

    # bottom to top update
    # prevents double movement

    for y in range(MAP_H - 2, -1, -1):

        # randomize horizontal order
        start = randint(0, MAP_W - 1)


        for i in range(MAP_W):

            x = (start + i) % MAP_W

            tile = world[y][x]


            if tile == SAND:

                update_sand(world, x, y)


            elif tile == WATER:

                update_water(world, x, y)

            elif tile == GRAVIY:
                update_sand(world, x, y)
