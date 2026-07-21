#Here is phys objects logis
#importing for you honey UwU
from SandEngine.Physics.PhysicsEngine import *
from SandEngine.DATA.GameConfig import *

#=====================
#solid material list
#=====================

SOLID_MATERIALS = (
    STONE,
    SAND,
    GRAVIY
)

#=====================
#game object class
#=====================

class GameObject:

    def __init__(self, x, y, w=16, h=16, color=pr.RED):
        self.x = x
        self.y = y

        self.w = w
        self.h = h

        self.vx = 0
        self.vy = 0

        self.mass = 1

        self.color = color

        self.alive = True

    def rect(self):
        return pr.Rectangle(
            self.x,
            self.y,
            self.w,
            self.h
        )

    def destroy(self):
        self.alive = False
        if self in objects:
            objects.remove(self)

    def rect(self):

        return pr.Rectangle(
            self.x,
            self.y,
            self.w,
            self.h
        )

#=====================
#collisions and move
#=====================

def rect_solid(world,x,y,w,h):

    left = int(x // 4)
    right = int((x+w-1)//4)

    top = int(y // 4)
    bottom = int((y+h-1)//4)


    for ty in range(top,bottom+1):

        for tx in range(left,right+1):

            if ty < 0 or tx < 0:
                return True


            if ty >= len(world):
                return True


            if tx >= len(world[0]):
                return True



            if world[ty][tx] in SOLID_MATERIALS:

                return True


    return False

def move_x(world,obj,amount):

    if amount == 0:
        return


    move = int(amount)

    if move == 0:
        return


    step = 1 if move > 0 else -1


    for _ in range(abs(move)):

        obj.x += step


        if rect_solid(
            world,
            obj.x,
            obj.y,
            obj.w,
            obj.h
        ):

            obj.x -= step
            obj.vx = 0
            break





def move_y(world,obj,amount):

    if amount == 0:
        return


    move = int(amount)

    if move == 0:
        return


    step = 1 if move > 0 else -1


    for _ in range(abs(move)):

        obj.y += step


        if rect_solid(
            world,
            obj.x,
            obj.y,
            obj.w,
            obj.h
        ):

            obj.y -= step


            if step > 0:

                while rect_solid(
                    world,
                    obj.x,
                    obj.y,
                    obj.w,
                    obj.h
                ):
                    obj.y -= 1


            obj.vy = 0
            break







def object_inside_cells(obj):

    left = int(obj.x // 4)
    right = int((obj.x + obj.w - 1) // 4)

    top = int(obj.y // 4)
    bottom = int((obj.y + obj.h - 1) // 4)

    return left,right,top,bottom


#=====================
#manipulations with objects
#=====================

def spawn_object(x,y):

    obj = GameObject(
        x,
        y,
        20,
        20,
        pr.RED
    )

    objects.append(obj)

    return obj



def clear_all_objects():
    for obj in objects:
        obj.destroy()



def draw_objects():

    for obj in objects:

        pr.draw_rectangle_rec(
            obj.rect(),
            obj.color
        )


#=====================
#push and updates
#=====================

def update_objects(world,dt):


    for obj in objects:
        obj.vy += GRAVITY * dt

        move_x(
            world,
            obj,
            obj.vx * dt
        )

        move_y(
            world,
            obj,
            obj.vy * dt
        )

        push_object_materials(
            world,
            obj,
            objects
        )



        obj.vx *= 0.8



        mark_dirty(
            int(obj.x//4),
            int(obj.y//4)
        )










def push_object_materials(world,obj,objects):


    left,right,top,bottom = object_inside_cells(obj)


    water = 0
    cells = 0

    support = False




    for y in range(top,bottom+1):

        for x in range(left,right+1):


            if not inside(x,y):
                continue



            tile = world[y][x]



            if tile == SAND:


                if inside(x,y+1):


                    below = world[y+1][x]


                    if below == AIR:

                        move_cell(
                            world,
                            x,y,
                            x,y+1
                        )


                    elif below == WATER:


                        world[y+1][x] = SAND
                        world[y][x] = WATER


                        mark_dirty(x,y)
                        mark_dirty(x,y+1)



            elif tile == WATER:


                dirs=[-1,1]
                random.shuffle(dirs)


                for dx in dirs:

                    nx=x+dx


                    if inside(nx,y):

                        if world[y][nx]==AIR:

                            move_cell(
                                world,
                                x,y,
                                nx,y
                            )

                            break



            elif tile == GRAVIY:


                if inside(x,y+1):

                    if world[y+1][x]==AIR:

                        move_cell(
                            world,
                            x,y,
                            x,y+1
                        )








    check = bottom+1


    if check < MAP_H:


        for x in range(left,right+1):

            if inside(x,check):

                if world[check][x] in SOLID_MATERIALS:

                    support=True
                    break





    for y in range(top,bottom+1):

        for x in range(left,right+1):


            if not inside(x,y):
                continue


            cells+=1


            if world[y][x]==WATER:
                water+=1



    ratio = water/max(cells,1)



    if support and obj.vy >= 0:

        obj.vy=0

        obj.y = check*4 - obj.h





    if ratio>0:


        obj.vy -= ratio*0.6

        obj.vx += random.uniform(
            -0.03,
            0.03
        )



        if ratio>0.8:

            obj.vy*=0.9







    for other in objects:


        if other is obj:
            continue



        if pr.check_collision_recs(
            obj.rect(),
            other.rect()
        ):



            dx1=(other.x+other.w)-obj.x
            dx2=(obj.x+obj.w)-other.x

            dy1=(other.y+other.h)-obj.y
            dy2=(obj.y+obj.h)-other.y



            overlap_x=min(dx1,dx2)
            overlap_y=min(dy1,dy2)



            if overlap_x < overlap_y:


                if obj.x < other.x:

                    obj.x -= overlap_x

                else:

                    obj.x += overlap_x


                obj.vx=0



            else:


                if obj.y < other.y:

                    obj.y -= overlap_y

                else:

                    obj.y += overlap_y


                obj.vy=0



