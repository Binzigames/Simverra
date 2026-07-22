# MATERIAL PHYSICS
# optimized sand/water physics

from SandEngine.Libs import *
from SandEngine.DATA.GameConfig import *



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

    if world[y][x] not in (SAND, GRAVIY, SOIL):
        return




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

# ===== BOMB =====


def explode(world, x, y):
    for dy in range(-EXPLOSION_RADIUS, EXPLOSION_RADIUS + 1):
        for dx in range(-EXPLOSION_RADIUS, EXPLOSION_RADIUS + 1):

            nx = x + dx
            ny = y + dy

            if not inside(nx, ny):
                continue

            if dx * dx + dy * dy > EXPLOSION_RADIUS ** 2:
                continue

            if world[ny][nx] == BOMB and (nx != x or ny != y):
                explode(world, nx, ny)

            world[ny][nx] = AIR

            mark_dirty(nx, ny)
            add_neighbors(nx, ny)
        explosions.append({
            "x": x * PIXEL_SIZE + PIXEL_SIZE // 2,
            "y": y * PIXEL_SIZE + PIXEL_SIZE // 2,
            "radius": 1.5,
            "life": 0.4,
            "max_radius": EXPLOSION_RADIUS * PIXEL_SIZE * 2
        })

def update_bomb(world, x, y):

    if y + 1 >= MAP_H:
        explode(world, x, y)
        return

    below = world[y + 1][x]

    if below == AIR:
        move_cell(world, x, y, x, y + 1)
        return

    if below != BOMB:
        explode(world, x, y)

# ===== MAIN UPDATE =====
def update_materials(world):
    global active_cells


    count = 0

    for x,y in list(active_cells):

        active_cells.remove((x,y))


        if not inside(x,y):
            continue


        tile = world[y][x]


        if tile == SAND or tile == GRAVIY or tile == SOIL:
            update_sand(world,x,y)

        elif tile == WATER:
            update_water(world,x,y)
        elif tile == BOMB:
            update_bomb(world, x, y)


        count += 1


        if count >= MAX_MATERIAL_UPDATES:
            break


# ===== INITIALIZE MATERIAL =====

def activate_world(world):
    global active_cells, dirty_cells

    active_cells.clear()
    dirty_cells.clear()

    for y in range(MAP_H):
        for x in range(MAP_W):
            if world[y][x] in (SAND, WATER, GRAVIY, BOMB , SOIL):
                activate(x, y)