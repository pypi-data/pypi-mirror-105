# Clear Controls:
def screen():
    return '\x1b[J'

def screenToEnd():
    return '\x1b[0J'

def screenToBeg():
    return '\x1b[1J'

def entireScreen():
    return '\x1b[2J'

def line():
    return '\x1b[K'

def lineToEnd():
    return '\x1b[0K'

def lineToBeg():
    return '\x1b[1K'

def entireLine():
    return '\x1b[2K'
