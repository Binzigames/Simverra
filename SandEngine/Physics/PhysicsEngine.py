# MATERIAL PHYSICS
# optimized sand/water physics

from SandEngine.Libs import *
from SandEngine.DATA.GameConfig import *



def mark_dirty(x, y):
    if 0 <= x < MAP_W and 0 <= y < MAP_H:
        dirty_cells.add((x, y))


def get_dirty_cells():

    global dirty_cells

    result = dirty_cells
    dirty_cells = set()

    return result



# ===== ACTIVE PHYSICS CELLS =====

active_cells = set()
next_active = set()


def activate(x, y):
    if 0 <= x < MAP_W and 0 <= y < MAP_H:
        next_active.add((x, y))


def add_neighbors(x, y):
    activate(x, y)

    if x > 0:
        activate(x - 1, y)

    if x + 1 < MAP_W:
        activate(x + 1, y)

    if y > 0:
        activate(x, y - 1)

    if y + 1 < MAP_H:
        activate(x, y + 1)



dirty_cells = set()



# ===== HELPERS =====

def inside(x,y):

    return (
        0 <= x < MAP_W and
        0 <= y < MAP_H
    )


def move_cell(world, x1, y1, x2, y2):

    material = world[y1][x1]

    world[y2][x2] = material
    world[y1][x1] = AIR

    dirty_cells.add((x1, y1))
    dirty_cells.add((x2, y2))

    add_neighbors(x1, y1)
    add_neighbors(x2, y2)



def swap_cells(world, x1, y1, x2, y2):

    world[y1][x1], world[y2][x2] = (
        world[y2][x2],
        world[y1][x1]
    )

    dirty_cells.add((x1,y1))
    dirty_cells.add((x2,y2))

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


# ===== GASES =====

def update_gas(world, x, y):

    if not inside(x, y):
        return

    if world[y][x] != GAS:
        return


    if y - 1 >= 0:

        target = world[y-1][x]

        if target == AIR:

            move_cell(
                world,
                x, y,
                x, y-1
            )

            return


        elif target == WATER:

            world[y-1][x] = GAS
            world[y][x] = WATER

            mark_dirty(x, y)
            mark_dirty(x, y-1)

            add_neighbors(x, y)
            add_neighbors(x, y-1)

            return



    direction = (
        -1
        if random.getrandbits(1)
        else 1
    )


    for dx in (direction, -direction):

        nx = x + dx

        if inside(nx, y-1):

            target = world[y-1][nx]

            if target == AIR:

                move_cell(
                    world,
                    x, y,
                    nx, y-1
                )

                return


            elif target == WATER:

                world[y-1][nx] = GAS
                world[y][x] = WATER

                mark_dirty(x, y)
                mark_dirty(nx, y-1)

                add_neighbors(x, y)
                add_neighbors(nx, y-1)

                return



    FLOW = 4

    for dx in (direction, -direction):

        for dist in range(1, FLOW + 1):

            nx = x + dx * dist

            if not inside(nx, y):
                break


            target = world[y][nx]


            if target == AIR:

                world[y][nx] = GAS
                world[y][x] = AIR

                mark_dirty(x, y)
                mark_dirty(nx, y)

                add_neighbors(x, y)
                add_neighbors(nx, y)

                return


            elif target == WATER:

                world[y][nx] = GAS
                world[y][x] = WATER

                mark_dirty(x, y)
                mark_dirty(nx, y)

                add_neighbors(x, y)
                add_neighbors(nx, y)

                return

            else:
                break
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


# ===== FIRE =====
def update_fire(world, x, y):

    if not inside(x, y):
        return

    if world[y][x] != FIRE:
        return

    fire_life[(x, y)] = fire_life.get((x, y), 12) - 1

    if fire_life[(x, y)] <= 0:
        world[y][x] = AIR
        fire_life.pop((x, y), None)
        mark_dirty(x, y)
        return

    if y > 0 and world[y-1][x] == AIR:
        move_cell(world, x, y, x, y-1)
        fire_life[(x, y-1)] = fire_life.pop((x, y))
        return

    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):

            nx = x + dx
            ny = y + dy

            if not inside(nx, ny):
                continue

            tile = world[ny][nx]

            if tile == WATER:
                world[ny][nx] = GAS
                mark_dirty(nx, ny)
                activate(nx, ny)


            #elif tile == GAS:
                #explode(world, nx, ny)

            elif tile == BOMB:
                explode(world, nx, ny)


            elif tile == SOIL:
                if random.random() < 0.03:
                    world[ny][nx] = FIRE
                    fire_life[(nx, ny)] = random.randint(5, 10)

            elif tile == WOOD:
                if random.random() < 0.08:

                    world[ny][nx] = FIRE
                    fire_life[(nx, ny)] = random.randint(8, 15)

                    mark_dirty(nx, ny)
                    activate(nx, ny)

                    for gy in (-1, 0, 1):
                        for gx in (-1, 0, 1):

                            gas_x = nx + gx
                            gas_y = ny + gy

                            if inside(gas_x, gas_y):

                                if world[gas_y][gas_x] == AIR:

                                    if random.random() < 0.25:
                                        world[gas_y][gas_x] = GAS

                                        mark_dirty(gas_x, gas_y)
                                        activate(gas_x, gas_y)

# ===== BLACK HOLE =====

def update_black_hole(world, x, y):

    if not inside(x, y):
        return

    if world[y][x] != BLACK_HOLE:
        return

    RADIUS = 4

    for dy in range(-RADIUS, RADIUS + 1):
        for dx in range(-RADIUS, RADIUS + 1):

            nx = x + dx
            ny = y + dy

            if not inside(nx, ny):
                continue

            if nx == x and ny == y:
                continue

            tile = world[ny][nx]

            if tile in (AIR, BLACK_HOLE):
                continue


            if abs(dx) <= 1 and abs(dy) <= 1:

                world[ny][nx] = AIR

                mark_dirty(nx, ny)
                add_neighbors(nx, ny)

                continue

            sx = 0 if dx == 0 else (-1 if dx > 0 else 1)
            sy = 0 if dy == 0 else (-1 if dy > 0 else 1)

            tx = nx + sx
            ty = ny + sy

            if inside(tx, ty):

                if world[ty][tx] == AIR:

                    move_cell(
                        world,
                        nx,
                        ny,
                        tx,
                        ty
                    )
# ===== MAIN UPDATE =====
def update_materials(world):

    global active_cells, next_active


    active_cells, next_active = next_active, set()


    count = 0

    for x,y in active_cells:

        tile = world[y][x]


        if tile == SAND or tile == GRAVIY or tile == SOIL:

            update_sand(world,x,y)


        elif tile == WATER:

            update_water(world,x,y)


        elif tile == GAS:

            update_gas(world,x,y)


        elif tile == FIRE:

            update_fire(world,x,y)


        elif tile == BOMB:

            update_bomb(world,x,y)


        elif tile == BLACK_HOLE:

            update_black_hole(world,x,y)


        count += 1


        if count >= MAX_MATERIAL_UPDATES:
            break


    active_cells.clear()


# ===== INITIALIZE MATERIAL =====

def activate_world(world):

    global active_cells, next_active, dirty_cells

    active_cells.clear()
    next_active.clear()
    dirty_cells.clear()


    for y,row in enumerate(world):

        for x,tile in enumerate(row):

            if tile in (
                SAND,
                WATER,
                GRAVIY,
                BOMB,
                SOIL,
                GAS,
                FIRE,
                BLACK_HOLE
            ):
                next_active.add((x,y))