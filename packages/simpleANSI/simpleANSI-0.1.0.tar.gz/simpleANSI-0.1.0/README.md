### simpleANSI
This is a simple wrapper library for ANSI escape codes.

# Installation
`pip install simpleANSI`

# Functionality
This is the directory of the package. Functions are denoted as `function(args)`. Constants are denoted as `constant = value`. Anything with a listing under it is a module.
```
simpleANSI
|-conhostEnableANSI()
|-clear
| |-Screen()
| |-ScreenToEnd()
| |-ScreenToBeg()
| |-EntireScree()
| |-Line()
| |-LineToEnd()
| |-LineToBeg()
| `-EntireLine()
|-cursor
| |-Home()
| |-MoveTo(line, column)
| |-MoveUpBy(lines)
| |-MoveDownBy(lines)
| |-MoveRightBy(columns)
| |-MoveLeftBy(columns)
| |-MoveBegNext(lines)
| |-MoveBegPrev(lines)
| |-MoveToCol(column)
| |-SavePos()
| `-RestorePos()
`-graphics
  |-normal = 0
  |-bold = 1
  |-underline = 4
  |-blink = 5
  |-invert = 7
  |-invisible = 8
  |-fgBlack = 30
  |-fgRed = 31
  |-fgGreen = 32
  |-fgYellow = 33
  |-fgBlue = 34
  |-fgMagenta = 35
  |-fgCyan = 36
  |-fgWhite = 37
  |-fgColor = 38
  |-bgBlack = 40
  |-bgRed = 41
  |-bgGreen = 42
  |-bgYellow = 43
  |-bgBlue = 44
  |-bgMagenta = 45
  |-bgCyan = 46
  |-bgWhite = 47
  |-bgColor = 48
  |-mode8Bit = 5
  |-mode16Bit = 2
  `-setGraphicsMode(*args)
```

# Resources:
* https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797# 
* https://bluesock.org/~willkg/dev/ansi.html