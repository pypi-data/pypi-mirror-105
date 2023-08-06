# Cursor Controls:
def Home():
    return '\x1b[H'

def MoveTo(line, column):
    return '\x1b[{};{}H'.format(line,column)

def MoveUpBy(lines):
    return '\x1b[{}A'.format(lines)

def MoveDownBy(lines):
    return '\x1b[{}B'.format(lines)

def MoveRightBy(columns):
    return '\x1b[{}C'.format(columns)

def MoveLeftBy(columns):
    return '\x1b[{}D'.format(columns)

def MoveBegNext(lines):
    return '\x1b[{}E'.format(lines)

def MoveBegPrev(lines):
    return '\x1b[{}F'.format(lines)

def MoveToCol(column):
    return '\x1b[{}G'.format(column)

def SavePos():
    return '\x1b[s'

def RestorePos():
    return '\x1b[u'
