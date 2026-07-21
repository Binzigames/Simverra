# Example Mod
from SandEngine.Libs import *
from SandEngine.DATA.GameConfig import *
from SandEngine.Additions.ModdingEngine import *


class TestMod(Mod):
    def __init__(self):
        super().__init__("Test Mod")

    def on_load(self):
        print(f"{self.name} loaded!")

    # ======================
    # Game hooks
    # ======================

    def custom_logic(self):
        pass

    def custom_ui(self):
        pass

    def custom_render_feature(self):
        pass

    # ======================
    # Menu callbacks
    # ======================

    def hello(self):
        print("Hello from Test Mod!")

    def give_sand(self):
        global Curent_material
        Curent_material = 2

    # ======================
    # Mod menu
    # ======================

    def build_menu(self):
        self.menu.clear()

        self.add_button("Hello", self.hello)
        self.add_button("Select Sand", self.give_sand)


# Required for the Modding Engine
mod = TestMod()

