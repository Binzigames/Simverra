# Modding engine
from SandEngine.Libs import *
from SandEngine.DATA.GameConfig import *



mods = []
is_moded = True

# Base class for mods
class Mod:
    def __init__(self, name):
        self.name = name
        self.menu = []

    def add_button(self, text, callback):
        self.menu.append((text, callback))

    def on_load(self):
        """Called when the mod is loaded."""
        pass

    def custom_render_feature(self):
        pass

    def custom_ui(self):
        pass

    def custom_logic(self):
        pass

    def build_menu(self):
        pass



def load_mod(path):
    """Loads one mod from a python file."""

    module_name = os.path.splitext(os.path.basename(path))[0]

    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    # Search for classes derived from Mod
    for obj in module.__dict__.values():
        if isinstance(obj, type) and issubclass(obj, Mod) and obj != Mod:
            mod = obj()
            mod.on_load()
            mods.append(mod)
            print(f"[MOD] Loaded: {mod.name}")


def init_mods():
    global is_moded
    """Loads every mod from the Mods folder."""

    mods.clear()

    mods_folder = "mods"

    if not os.path.exists(mods_folder):
        os.makedirs(mods_folder)
        return

    for file in os.listdir(mods_folder):
        if file.endswith(".py"):
            try:
                load_mod(os.path.join(mods_folder, file))
                pr.set_window_title(w_title + "*moded*")
                is_moded = True
            except Exception as e:
                print(f"[MOD] Failed to load {file}: {e}")
                is_moded = False


def render_mods():
    for mod in mods:
        mod.custom_render_feature()


def ui_mods():
    for mod in mods:
        mod.custom_ui()


def logic_mods():
    for mod in mods:
        mod.custom_logic()
