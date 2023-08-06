import ctypes # Used to enable VT-100 mode on windows conhost
from . import clear
from . import cursor
from . import graphics

def conhostEnableANSI():
    kernel32 = ctypes.windll.kernel32
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
    
__all__ = ['clear', 'cursor', 'graphics', 'conhostEnableANSI']
