import pyray as pr
from SandEngine.Physics.PhysicsEngine import *

objects = []

GRAVITY = 600



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



            if world[ty][tx] == STONE:

                return True


    return False





def move_x(world,obj,amount):

    step = 1 if amount > 0 else -1


    for i in range(abs(int(amount))):

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

    step = 1 if amount > 0 else -1


    for i in range(abs(int(amount))):

        obj.y += step


        if rect_solid(
            world,
            obj.x,
            obj.y,
            obj.w,
            obj.h
        ):

            obj.y -= step
            obj.vy = 0
            break






def update_objects(world,dt):


    for obj in objects:


        # gravity

        obj.vy += GRAVITY * dt



        # X movement

        move_x(
            world,
            obj,
            obj.vx * dt
        )



        # Y movement

        move_y(
            world,
            obj,
            obj.vy * dt
        )
        mark_dirty(obj.x *10, obj.y * 10)


        # interaction with sand/water

        push_object_materials(
            world,
            obj
        )



        obj.vx *= 0.8






def push_object_materials(world,obj):


    left = int(obj.x//4)
    right = int((obj.x+obj.w)//4)

    top = int(obj.y//4)
    bottom = int((obj.y+obj.h)//4)



    for y in range(top,bottom+1):

        for x in range(left,right+1):


            if not inside(x,y):
                continue



            tile = world[y][x]



            # sand

            if tile == SAND:


                if inside(x,y-1):

                    if world[y-1][x] == AIR:

                        world[y-1][x] = SAND
                        world[y][x] = AIR


                        mark_dirty(x,y)
                        mark_dirty(x,y-1)





            # water


            elif tile == WATER:

                world[y][x] = AIR

                mark_dirty(x,y)







def draw_objects():

    for obj in objects:

        pr.draw_rectangle_rec(
            obj.rect(),
            obj.color
        )