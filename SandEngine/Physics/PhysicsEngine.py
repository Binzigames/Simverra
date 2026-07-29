# MATERIAL PHYSICS
# optimized sand/water physics

from SandEngine.Libs import *
from SandEngine.DATA.GameConfig import *
from SandEngine.Visuals.Particles import *



NEIGHBORS = (
    (-1,-1),
    (0,-1),
    (1,-1),
    (-1,0),
    (1,0),
    (-1,1),
    (0,1),
    (1,1)
)
def mark_dirty(x, y):
    if 0 <= x < MAP_W and 0 <= y < MAP_H:
        dirty_cells.add((x, y))


def get_dirty_cells():

    global dirty_cells

    result = dirty_cells
    dirty_cells = set()

    return result

def set_cell(world, x, y, material):

    if not inside(x,y):
        return

    if world[y][x] == material:
        return

    world[y][x] = material

    mark_dirty(x,y)
    add_neighbors(x,y)

    if material != AIR:
        activate(x,y)


# ===== MATERIAL REACTIONS =====
def grow_tree(world, x, y):

    directions = [
        (-1,0),
        (1,0),
        (0,-1)
    ]

    random.shuffle(directions)


    for dx,dy in directions:

        nx = x + dx
        ny = y + dy


        if inside(nx,ny):

            if world[ny][nx] == AIR:

                world[ny][nx] = WOOD
                tree_growth_particles(
                    nx * PIXEL_SIZE,
                    ny * PIXEL_SIZE
                )

                mark_dirty(nx,ny)
                activate(nx,ny)

                return True


    return False

SIDE_NEIGHBORS = (
    (0, -1),
    (-1, 0),
    (1, 0),
    (0, 1),
)

def react_materials(world, x, y):

    row = world[y]
    tile = row[x]

    rand = random.randrange

    for dx, dy in SIDE_NEIGHBORS:

        nx = x + dx
        ny = y + dy

        if not (0 <= nx < MAP_W and 0 <= ny < MAP_H):
            continue

        other = world[ny][nx]

        # =========================
        # WATER + WOOD -> GROW
        # =========================
        if tile == WATER:

            if other == WOOD:

                if rand(100) < 8:

                    row[x] = WOOD

                    mark_dirty(x, y)
                    activate(x, y)

                    grow_tree(world, x, y)
                    magic_particles(
                        x * PIXEL_SIZE,
                        y * PIXEL_SIZE
                    )

                    return True

            elif other == FIRE:

                row[x] = GAS
                world[ny][nx] = GAS

                fire_life.pop((nx, ny), None)

                mark_dirty(x, y)
                mark_dirty(nx, ny)

                activate(x, y)
                activate(nx, ny)

                return True

            elif other == SOIL:

                if rand(100) < 2:

                    row[x] = SOIL

                    mark_dirty(x, y)
                    activate(x, y)

                    return True

            elif other == STONE:

                activate(nx, ny)

        # =========================
        # SAND / GRAVIY
        # =========================
        elif tile == SAND or tile == GRAVIY:

            if other == WOOD:

                if rand(100) < 1:

                    world[ny][nx] = FIRE

                    fire_life[(nx, ny)] = random.randint(8, 15)

                    mark_dirty(nx, ny)
                    activate(nx, ny)

                    return True

            elif tile == SAND and other == WATER:

                if rand(100) < 5:

                    row[x] = SOIL

                    reaction_particles(
                        x * PIXEL_SIZE,
                        y * PIXEL_SIZE,
                        pr.Color(
                            120,
                            90,
                            40,
                            180
                        )
                    )

                    mark_dirty(x, y)
                    activate(x, y)

                    return True

        # =========================
        # FIRE
        # =========================
        elif tile == FIRE:

            if other == WATER:

                row[x] = GAS
                world[ny][nx] = GAS

                fire_life.pop((x, y), None)
                fire_life.pop((nx, ny), None)

                mark_dirty(x, y)
                mark_dirty(nx, ny)

                activate(x, y)
                activate(nx, ny)

                return True

            elif other == GRAVIY:

                if rand(100) < 8:

                    row[x] = AIR

                    fire_life.pop((x, y), None)

                    mark_dirty(x, y)
                    activate(x, y)

                    return True

            elif other == WOOD:

                if rand(100) < 8:

                    world[ny][nx] = FIRE

                    fire_life[(nx, ny)] = random.randint(10, 20)

                    mark_dirty(nx, ny)
                    activate(nx, ny)

                    return True

        # =========================
        # GAS
        # =========================
        elif tile == GAS:

            if other == STONE or other == WOOD:

                if rand(100) < 15:

                    row[x] = WATER

                    mark_dirty(x, y)
                    activate(x, y)

                    return True

        # =========================
        # WOOD
        # =========================
        elif tile == WOOD:

            if other == SOIL:

                if rand(100) < 1:

                    row[x] = WATER

                    mark_dirty(x, y)
                    activate(x, y)

                    return True

    return False

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


def move_cell(world,x1,y1,x2,y2):

    material = world[y1][x1]

    world[y2][x2] = material
    world[y1][x1] = AIR


    mark_dirty(x1,y1)
    mark_dirty(x2,y2)


    add_neighbors(x1,y1)
    add_neighbors(x2,y2)


    activate(x2,y2)



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

    react_materials(world, x, y)




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


    react_materials(world,x,y)


    if world[y][x] != WATER:
        return



    # вниз

    if inside(x,y+1):

        target = world[y+1][x]


        if target == AIR:

            move_cell(
                world,
                x,y,
                x,y+1
            )

            return


        # вода важча за газ

        if target == GAS:

            swap_cells(
                world,
                x,y,
                x,y+1
            )

            return



    direction = -1 if random.getrandbits(1) else 1


    # діагональ

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



    # горизонтальна течія

    flow=random.randint(1,3)


    for dx in (direction,-direction):

        for i in range(1,flow+1):

            nx=x+dx*i


            if not inside(nx,y):
                break


            if world[y][nx] == AIR:

                move_cell(
                    world,
                    x,y,
                    nx,y
                )

                return

            else:
                break

# ===== GAS =====

def update_gas(world, x, y):

    if not inside(x, y):
        return


    if world[y][x] != GAS:
        return

    react_materials(world, x, y)


    if world[y][x] != GAS:
        return



    if y - 1 >= 0:

        target = world[y-1][x]


        if target == AIR:

            move_cell(
                world,
                x,y,
                x,y-1
            )

            return


        elif target == WATER:

            world[y-1][x] = GAS
            world[y][x] = WATER


            mark_dirty(x,y)
            mark_dirty(x,y-1)


            add_neighbors(x,y)
            add_neighbors(x,y-1)

            return



    direction = -1 if random.getrandbits(1) else 1


    for dx in (direction,-direction):

        nx = x + dx


        if inside(nx,y-1):

            target = world[y-1][nx]


            if target == AIR:

                move_cell(
                    world,
                    x,y,
                    nx,y-1
                )

                return


            elif target == WATER:

                world[y-1][nx] = GAS
                world[y][x] = WATER


                mark_dirty(x,y)
                mark_dirty(nx,y-1)


                add_neighbors(x,y)
                add_neighbors(nx,y-1)

                return



    FLOW = 4


    for dx in (direction,-direction):

        for dist in range(1,FLOW+1):

            nx = x + dx*dist


            if not inside(nx,y):
                break


            target = world[y][nx]


            if target == AIR:

                world[y][nx] = GAS
                world[y][x] = AIR


                mark_dirty(x,y)
                mark_dirty(nx,y)


                add_neighbors(x,y)
                add_neighbors(nx,y)

                return


            elif target == WATER:

                world[y][nx] = GAS
                world[y][x] = WATER


                mark_dirty(x,y)
                mark_dirty(nx,y)


                add_neighbors(x,y)
                add_neighbors(nx,y)

                return


            else:
                break
# ===== BOMB =====


def explode(world,x,y):


    explosions.append({

        "x":x*PIXEL_SIZE+
        PIXEL_SIZE//2,

        "y":y*PIXEL_SIZE+
        PIXEL_SIZE//2,

        "radius":1.5,

        "life":0.4,

        "max_radius":
        EXPLOSION_RADIUS*PIXEL_SIZE*2

    })
    explosion_particles(

        x * PIXEL_SIZE,
        y * PIXEL_SIZE

    )


    for dy in range(
        -EXPLOSION_RADIUS,
        EXPLOSION_RADIUS+1
    ):

        for dx in range(
            -EXPLOSION_RADIUS,
            EXPLOSION_RADIUS+1
        ):


            nx=x+dx
            ny=y+dy


            if not inside(nx,ny):
                continue


            distance = (
                dx*dx+
                dy*dy
            )


            if distance > EXPLOSION_RADIUS**2:
                continue



            if world[ny][nx]==BOMB:

                if (nx,ny)!=(x,y):

                    explode(
                        world,
                        nx,
                        ny
                    )


            set_cell(
                world,
                nx,
                ny,
                AIR
            )

def update_bomb(world, x, y):
    react_materials(world, x, y)
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

    react_materials(world, x, y)

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
    react_materials(world, x, y)
# ===== MAIN UPDATE =====
UPDATE_FUNCS = {
    SAND: update_sand,
    GRAVIY: update_sand,
    SOIL: update_sand,
    WATER: update_water,
    GAS: update_gas,
    FIRE: update_fire,
    BOMB: update_bomb,
    BLACK_HOLE: update_black_hole,
}
def update_materials(world):

    global active_cells, next_active

    active_cells, next_active = next_active, active_cells
    next_active.clear()

    updates = 0

    for x, y in active_cells:

        func = UPDATE_FUNCS.get(world[y][x])

        if func is not None:
            func(world, x, y)

            updates += 1
            if updates >= MAX_MATERIAL_UPDATES:
                break


# ===== INITIALIZE MATERIAL =====
ACTIVE_TILES = {
    SAND,
    WATER,
    GRAVIY,
    BOMB,
    SOIL,
    GAS,
    FIRE,
    BLACK_HOLE,
    WOOD,
}

def activate_world(world):

    global active_cells, next_active, dirty_cells

    active_cells.clear()
    next_active.clear()
    dirty_cells.clear()

    add = next_active.add

    for y, row in enumerate(world):
        for x, tile in enumerate(row):
            if tile in ACTIVE_TILES:
                add((x, y))