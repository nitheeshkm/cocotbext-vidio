import enum

class VideoType(enum.IntEnum):
    RGB = 0
    YUV = 1

class ChromaType(enum.IntEnum):
    YUV444 = 0
    YUV422 = 1
    YUV420 = 2

class Standard(enum.IntEnum):
    BT601 = 0
    BT709 = 1
    BT2020 = 2

class Pattern(enum.IntEnum):
    p_incr = 0
    rand = 1
    h_incr = 2


