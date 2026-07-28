from SandEngine.Libs import *


particles = []


PARTICLE_LIMIT = 5000



def add_particle(x,y,vx,vy,color,life,size):

    if len(particles) >= PARTICLE_LIMIT:
        return


    particles.append({

        "x":x,

        "y":y,

        "vx":vx,

        "vy":vy,

        "color":color,

        "life":life,

        "max":life,

        "size":size,

        "drag":random.uniform(
            0.94,
            0.99
        )

    })



def burst(x,y,color,count=10,power=2):

    for i in range(count):

        angle = random.random()*math.pi*2

        speed = random.uniform(
            0.3,
            power
        )


        add_particle(

            x,

            y,

            math.cos(angle)*speed,

            math.sin(angle)*speed,

            color,

            random.randint(
                25,
                80
            ),

            random.randint(
                1,
                3
            )

        )



def sand_dust(x,y):

    burst(

        x,

        y,

        pr.Color(
            220,
            180,
            90,
            230
        ),

        8,

        1.5

    )



def water_splash(x,y):

    burst(

        x,

        y,

        pr.Color(
            40,
            170,
            255,
            240
        ),

        10,

        2

    )



def fire_particles(x,y):

    burst(

        x,

        y,

        pr.Color(
            255,
            80,
            10,
            255
        ),

        12,

        2.5

    )



def magic_particles(x,y):

    burst(

        x,

        y,

        pr.Color(
            180,
            70,
            255,
            255
        ),

        15,

        3

    )



def tree_growth_particles(x,y):

    burst(

        x,

        y,

        pr.Color(
            70,
            255,
            90,
            240
        ),

        18,

        2

    )



def gas_particles(x,y):

    burst(

        x,

        y,

        pr.Color(
            220,
            130,
            255,
            220
        ),

        10,

        1.5

    )



def reaction_particles(x,y,color):

    burst(

        x,

        y,

        color,

        12,

        2

    )



def explosion_particles(x,y):

    burst(

        x,

        y,

        pr.Color(
            255,
            120,
            20,
            255
        ),

        50,

        5

    )


    burst(

        x,

        y,

        pr.Color(
            100,
            100,
            100,
            180
        ),

        30,

        2

    )



def draw_pixel_particle(p):


    life = (
        p["life"] /
        p["max"]
    )


    alpha = int(
        255 *
        life
    )


    c = p["color"]


    size = p["size"]


    x = int(
        p["x"]
    )

    y = int(
        p["y"]
    )



    glow = pr.Color(

        min(
            c.r + 80,
            255
        ),

        min(
            c.g + 80,
            255
        ),

        min(
            c.b + 80,
            255
        ),

        alpha // 3

    )


    pr.draw_rectangle(

        x-size,

        y-size,

        size*3,

        size*3,

        glow

    )


    pr.draw_rectangle(

        x,

        y,

        size,

        size,

        pr.Color(

            c.r,

            c.g,

            c.b,

            alpha

        )

    )
ambient_particles = []


AMBIENT_LIMIT = 500



def add_ambient(x,y,vx,vy,color,life,size):

    if len(ambient_particles) >= AMBIENT_LIMIT:
        return


    ambient_particles.append({

        "x":x,

        "y":y,

        "vx":vx,

        "vy":vy,

        "color":color,

        "life":life,

        "max":life,

        "size":size

    })



def spawn_dust_fall(width,height):

    if random.random() < 0.35:


        add_ambient(

            random.randint(
                0,
                width
            ),

            -5,

            random.uniform(
                -0.15,
                0.15
            ),

            random.uniform(
                0.2,
                0.8
            ),

            pr.Color(

                170,
                150,
                110,
                80

            ),

            random.randint(
                100,
                250
            ),

            random.randint(
                1,
                2
            )

        )



def spawn_fog(width,height):

    if random.random() < 0.15:


        add_ambient(

            random.randint(
                0,
                width
            ),

            random.randint(
                0,
                height
            ),

            random.uniform(
                -0.3,
                0.3
            ),

            random.uniform(
                -0.05,
                0.05
            ),

            pr.Color(

                80,
                70,
                150,
                25

            ),

            random.randint(
                200,
                400
            ),

            random.randint(
                8,
                20
            )

        )



def update_ambient_particles(width,height):

    global ambient_particles


    alive=[]


    for p in ambient_particles:


        p["x"] += p["vx"]

        p["y"] += p["vy"]


        p["life"] -= 1



        if p["life"] > 0:


            alpha=int(

                p["color"].a *

                (
                    p["life"] /
                    p["max"]
                )

            )


            pr.draw_rectangle(

                int(p["x"]),

                int(p["y"]),

                p["size"],

                p["size"],

                pr.Color(

                    p["color"].r,

                    p["color"].g,

                    p["color"].b,

                    alpha

                )

            )


            alive.append(p)


    ambient_particles = alive


def update_particles():

    global particles


    alive=[]


    for p in particles:


        p["x"] += p["vx"]

        p["y"] += p["vy"]


        p["vy"] += 0.02


        p["vx"] *= p["drag"]


        p["life"] -= 1



        if p["life"] > 0:

            draw_pixel_particle(p)

            alive.append(p)



    particles = alive


    width = pr.get_screen_width()
    height = pr.get_screen_height()


    spawn_dust_fall(
        width,
        height
    )


    spawn_fog(
        width,
        height
    )


    update_ambient_particles(
        width,
        height
    )