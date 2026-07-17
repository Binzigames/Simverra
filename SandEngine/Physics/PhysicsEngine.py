# MATERIAL PHYSICS
# optimized sand/water physics

from SandEngine.Libs import *


# ===== MATERIAL IDS =====

AIR = 0
SAND = 2
WATER = 3
STONE = 4
GRAVIY = 5


# ===== MAP SIZE =====

MAP_W = 256
MAP_H = 256



# ===== DIRTY PIXELS =====

dirty_cells = set()


def mark_dirty(x, y):

    if inside(x, y):
        dirty_cells.add((x, y))



def get_dirty_cells():

    global dirty_cells

    result = dirty_cells.copy()
    dirty_cells.clear()

    return result



# ===== ACTIVE PHYSICS CELLS =====

active_cells = set()


def activate(x, y):

    if inside(x, y):

        if y < MAP_H:

            active_cells.add((x, y))



def add_neighbors(x, y):

    activate(x, y)
    activate(x, y-1)
    activate(x, y+1)
    activate(x-1, y)
    activate(x+1, y)



# ===== HELPERS =====

def inside(x,y):

    return (
        0 <= x < MAP_W and
        0 <= y < MAP_H
    )



def move_cell(world,x1,y1,x2,y2):

    world[y2][x2] = world[y1][x1]
    world[y1][x1] = AIR


    mark_dirty(x1,y1)
    mark_dirty(x2,y2)


    add_neighbors(x1,y1)
    add_neighbors(x2,y2)



# ===== SAND =====

def update_sand(world,x,y):

    if not inside(x,y):
        return


    if world[y][x] != SAND and world[y][x] != GRAVIY:
        return



    # вниз

    if y + 1 < MAP_H:

        if world[y+1][x] == AIR:

            move_cell(
                world,
                x,y,
                x,y+1
            )

            return



    direction = (
        -1
        if random.getrandbits(1)
        else 1
    )


    for dx in (direction,-direction):

        nx=x+dx


        if inside(nx,y+1):

            target = world[y+1][nx]


            if target == AIR or target == WATER:

                old = world[y+1][nx]

                world[y+1][nx] = world[y][x]
                world[y][x] = old


                mark_dirty(x,y)
                mark_dirty(nx,y+1)


                add_neighbors(x,y)
                add_neighbors(nx,y+1)

                return




# ===== WATER =====

def update_water(world,x,y):

    if not inside(x,y):
        return


    if world[y][x] != WATER:
        return





    if y+1 < MAP_H:


        if world[y+1][x] == AIR:

            move_cell(
                world,
                x,y,
                x,y+1
            )

            return



    direction = (
        -1
        if random.getrandbits(1)
        else 1
    )





    for dx in (direction,-direction):

        nx=x+dx


        if inside(nx,y+1):

            if world[y+1][nx] == AIR:


                move_cell(
                    world,
                    x,y,
                    nx,y+1
                )

                return



    FLOW = 3


    for dx in (direction,-direction):

        for dist in range(1,FLOW+1):

            nx=x+dx*dist


            if not inside(nx,y):
                break


            if world[y][nx] != AIR:
                break



            world[y][nx]=WATER
            world[y][x]=AIR


            mark_dirty(x,y)
            mark_dirty(nx,y)


            add_neighbors(x,y)
            add_neighbors(nx,y)


            return

# ===== OBJECT INTERACTION =====

OBJECT_PUSH_POWER = 2


def object_inside_cells(obj):

    left = int(obj.x / 4)
    right = int((obj.x + obj.w) / 4)

    top = int(obj.y / 4)
    bottom = int((obj.y + obj.h) / 4)

    return left, right, top, bottom



def push_object_materials(world, obj):

    left, right, top, bottom = object_inside_cells(obj)

    water = 0
    cells = 0
    support = False

    for y in range(bottom, top - 1, -1):
        for x in range(left, right + 1):

            if not inside(x, y):
                continue

            tile = world[y][x]

            if tile == SAND:

                if inside(x, y + 1):

                    if world[y + 1][x] == AIR:
                        move_cell(world, x, y, x, y + 1)

                    elif world[y + 1][x] == WATER:
                        world[y + 1][x] = SAND
                        world[y][x] = WATER
                        mark_dirty(x, y)
                        mark_dirty(x, y + 1)

            elif tile == WATER:

                dirs = [-1, 1]
                random.shuffle(dirs)

                for dx in dirs:

                    nx = x + dx

                    if inside(nx, y) and world[y][nx] == AIR:
                        move_cell(world, x, y, nx, y)
                        break

            elif tile == GRAVIY:

                if inside(x, y + 1):

                    if world[y + 1][x] == AIR:
                        move_cell(world, x, y, x, y + 1)


    check = bottom + 1

    if check < MAP_H:

        for x in range(left, right + 1):

            if inside(x, check):

                if world[check][x] in (SAND, STONE, GRAVIY):
                    support = True
                    break


    for y in range(top, bottom + 1):
        for x in range(left, right + 1):

            if not inside(x, y):
                continue

            cells += 1

            if world[y][x] == WATER:
                water += 1

    ratio = water / max(cells, 1)



    if support and obj.vy >= 0:

        obj.vy = 0

        obj.y = check * 4 - obj.h


    if ratio > 0:

        obj.vy -= ratio * 0.6

        obj.vx += random.uniform(-0.03, 0.03)

        if ratio > 0.8:
            obj.vy *= 0.9

# ===== MAIN UPDATE =====
MAX_MATERIAL_UPDATES = 3000
def update_materials(world):
    global active_cells


    count = 0

    for x,y in list(active_cells):

        active_cells.remove((x,y))


        if not inside(x,y):
            continue


        tile = world[y][x]


        if tile == SAND or tile == GRAVIY:

            update_sand(world,x,y)


        elif tile == WATER:

            update_water(world,x,y)


        count += 1


        if count >= MAX_MATERIAL_UPDATES:
            break


# ===== INITIALIZE MATERIAL =====

def activate_world(world):

    for y in range(MAP_H):

        for x in range(MAP_W):

            if world[y][x] in (
                SAND,
                WATER,
                GRAVIY
            ):
                activate(x,y)