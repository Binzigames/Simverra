#imports assets like fonts or graphics or sounds
from SandEngine.Libs import *

#=====================
#FONTS
#=====================
FONT = None

def get_font():
    global FONT

    if FONT is None:
        FONT = pr.load_font("Assets/Inter.ttf")

    return FONT
#=====================
#SHADERS
#=====================
class PostProcessController:

    def __init__(self, width, height):

        self.width = width
        self.height = height


        # render buffer
        self.target = pr.load_render_texture(
            width,
            height
        )


        # post shader
        self.shader = pr.load_shader(
            "",
            "Assets/Shaders/postprocess.fs"
        )


        self.time = 0


        self.time_loc = pr.get_shader_location(
            self.shader,
            "time"
        )


        self.enabled = True



    def begin(self):

        if not self.enabled:
            return


        pr.begin_texture_mode(
            self.target
        )


        pr.clear_background(
            pr.BLACK
        )


    def end(self):

        if not self.enabled:
            return


        pr.end_texture_mode()



    def render(self):

        if not self.enabled:
            return


        self.time += pr.get_frame_time()

        pr.set_shader_value(
            self.shader,
            self.time_loc,
            pr.ffi.new("float *", self.time),
            pr.SHADER_UNIFORM_FLOAT
        )

        pr.begin_shader_mode(
            self.shader
        )


        pr.draw_texture_rec(
            self.target.texture,

            pr.Rectangle(
                0,
                0,
                self.target.texture.width,
                -self.target.texture.height
            ),

            pr.Vector2(
                0,
                0
            ),

            pr.WHITE
        )


        pr.end_shader_mode()



    def toggle(self):

        self.enabled = not self.enabled



    def unload(self):

        pr.unload_shader(
            self.shader
        )

        pr.unload_render_texture(
            self.target
        )




POST_PROCESS = None



def init_post_process(width,height):

    global POST_PROCESS

    POST_PROCESS = PostProcessController(
        width,
        height
    )



def get_post_process():

    return POST_PROCESS

#=====================
#VISUALS
#=====================
def set_icon():
    icon = pr.load_image("Assets/icon.png")
    pr.set_window_icon(icon)
    pr.unload_image(icon)
