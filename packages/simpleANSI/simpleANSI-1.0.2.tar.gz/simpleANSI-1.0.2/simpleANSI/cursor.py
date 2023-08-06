# Cursor Controls:
def home():
    return '\x1b[H'

def moveTo(column, line):
    return '\x1b[{};{}H'.format(line,column)

def moveUpBy(lines):
    return '\x1b[{}A'.format(lines)

def moveDownBy(lines):
    return '\x1b[{}B'.format(lines)

def moveRightBy(columns):
    return '\x1b[{}C'.format(columns)

def moveLeftBy(columns):
    return '\x1b[{}D'.format(columns)

def moveBegNext(lines):
    return '\x1b[{}E'.format(lines)

def moveBegPrev(lines):
    return '\x1b[{}F'.format(lines)

def moveToCol(column):
    return '\x1b[{}G'.format(column)

def savePos():
    return '\x1b[s'

def restorePos():
    return '\x1b[u'
