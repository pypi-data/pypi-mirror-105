# Clear Controls:
def Screen():
    return '\x1b[J'

def ScreenToEnd():
    return '\x1b[0J'

def ScreenToBeg():
    return '\x1b[1J'

def EntireScreen():
    return '\x1b[2J'

def Line():
    return '\x1b[K'

def LineToEnd():
    return '\x1b[0K'

def LineToBeg():
    return '\x1b[1K'

def EntireLine():
    return '\x1b[2K'
