import enum

class ColorFormat(enum.IntEnum):
    RGB = 0
    YUV444 = 1
    YUV422 = 2
    YUV420 = 3

class Standard(enum.IntEnum):
    BT601 = 0
    BT709 = 1
    BT2020 = 2

class Pattern(enum.IntEnum):
    p_incr = 0
    rand = 1
    h_incr = 2
