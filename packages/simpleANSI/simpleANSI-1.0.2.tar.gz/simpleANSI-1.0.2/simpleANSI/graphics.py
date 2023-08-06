# Graphics Controls:
normal = 0
bold = 1
underline = 4
blink = 5
invert = 7
invisible = 8

fgBlack = 30
fgRed = 31
fgGreen = 32
fgYellow = 33
fgBlue = 34
fgMagenta = 35
fgCyan = 36
fgWhite = 37
fgColor = 38

bgBlack = 40
bgRed = 41
bgGreen = 42
bgYellow = 43
bgBlue = 44
bgMagenta = 45
bgCyan = 46
bgWhite = 47
bgColor = 48

mode8Bit = 5
mode16Bit = 2
    
def setGraphicsMode(*args):
    return '\x1b[{}m'.format(str(args)[1:-1].replace(', ', ';').replace(',', ''))
