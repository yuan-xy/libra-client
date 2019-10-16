import sys
import os

_force_color = None

def set_force_color(force_color):
    global _force_color
    _force_color = force_color

def support_color():
    if _force_color is not None:
        return _force_color
    if not sys.stdout.isatty():
        return False
    if os.name == 'posix':
        return True
    if os.name == 'nt':
        try:
            #os.system('') #enable VT100 Escape Sequence for WINDOWS 10 Ver. 1607
            import ctypes
            kernel32 = ctypes.windll.kernel32
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
            return True
        except Exception:
            return False
    return False


def print_color(str, color, **kargs):
    if support_color():
        print(color + str + bcolors.ENDC, **kargs)
    else:
        print(str, **kargs)

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
