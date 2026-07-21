#manages apis <3
from SandEngine.Libs import *
from SandEngine.DATA.GameConfig import *

DISCORD_CLIENT_ID = "1528705424616984668"

RPC = Presence(DISCORD_CLIENT_ID)
def init_apis():


    RPC.connect()

    RPC.update(
        state="Creating something new...",
        details="Playing",
        large_image="Assets/icon",
        large_text=w_title
    )

def terminate_apis():
    RPC.connect()