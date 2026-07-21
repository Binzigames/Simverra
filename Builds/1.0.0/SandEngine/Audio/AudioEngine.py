# Audio engine created to play easy things in game
from SandEngine.Libs import *
from SandEngine.DATA.GameConfig import *

# =====================
# SOUNDS LIST
# =====================
MainTheme = None
ButtonSound = None
SandSound = None

# =====================
# AUDIO STATE
# =====================
AudioEnabled = True


# =====================
# INIT
# =====================
def audio_system_init():
    global MainTheme, ButtonSound, SandSound

    pr.init_audio_device()

    MainTheme = pr.load_music_stream(
        "SandEngine/Audio/Sandbox_of_no_choiseals.ogg"
    )

    ButtonSound = pr.load_sound(
        "SandEngine/Audio/Button.mp3"
    )

    SandSound = pr.load_sound(
        "SandEngine/Audio/Sand.mp3"
    )

    pr.set_music_volume(
        MainTheme,
        Music_Loudnes
    )

    pr.set_sound_volume(
        ButtonSound,
        SFX_Loudnes
    )

    pr.set_sound_volume(
        SandSound,
        SFX_Loudnes
    )

    if AudioEnabled:
        pr.play_music_stream(MainTheme)


# =====================
# UPDATE
# =====================
def audio_system_update():

    if MainTheme and AudioEnabled:

        pr.update_music_stream(MainTheme)

        if not pr.is_music_stream_playing(MainTheme):
            pr.play_music_stream(MainTheme)


# =====================
# ENABLE / DISABLE AUDIO
# =====================
def set_audio_enabled(state):

    global AudioEnabled

    AudioEnabled = state

    if MainTheme:

        if AudioEnabled:
            pr.set_music_volume(
                MainTheme,
                Music_Loudnes
            )

            pr.play_music_stream(MainTheme)

        else:
            pr.set_music_volume(
                MainTheme,
                0
            )


# =====================
# TOGGLE AUDIO
# =====================
def toggle_audio():

    global AudioEnabled

    set_audio_enabled(not AudioEnabled)


# =====================
# PLAY SOUND
# =====================
def play_sound(type):

    if not AudioEnabled:
        return

    if type == 1 and ButtonSound:
        pr.play_sound(ButtonSound)

    elif type == 2 and SandSound:
        pr.play_sound(SandSound)


# =====================
# CLEANUP
# =====================
def audio_system_close():

    global MainTheme, ButtonSound, SandSound

    if MainTheme:
        pr.stop_music_stream(MainTheme)
        pr.unload_music_stream(MainTheme)

    if ButtonSound:
        pr.unload_sound(ButtonSound)

    if SandSound:
        pr.unload_sound(SandSound)

    pr.close_audio_device()