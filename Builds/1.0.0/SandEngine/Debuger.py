# WELCOME TO MY SWEET CONSOLE-DEBUGER (a print functions is here!)
#importing for you honey ~
from SandEngine.Libs import *
from SandEngine.DATA.GameConfig import *

def print_message(message, Type=0):
    if Type == 0 and d_show_logs:
        print("DEBUGGER MESSAGE / ENGINE" + c.Fore.GREEN)
        print(str(message) + c.Fore.WHITE)
        print("==================================" + c.Fore.WHITE)

    elif Type == 1 and d_show_logs:
        print("DEBUGGER MESSAGE / ERROR" + c.Fore.RED)
        print(str(message) + c.Fore.WHITE)
        print("==================================" + c.Fore.WHITE)

    elif Type == 2 and d_show_logs:
        print("DEBUGGER MESSAGE / GAME" + c.Fore.YELLOW)
        print(str(message) + c.Fore.WHITE)
        print("==================================" + c.Fore.WHITE)

    else:
        if d_show_logs:
            print("Unknown debug type")
        else:
            pass


def print_init():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("==================================" + c.Fore.GREEN)
    print("SAND ENGINE LOADED / WELCOME" + c.Fore.WHITE)
    print("Nice to see you! your log is here:" )
    print("==================================" + c.Fore.GREEN)
    if not d_show_logs:
        print(c.Fore.RED +" In game logs - disabled... enable it in config" + c.Fore.WHITE )
        print("==================================")