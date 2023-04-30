import numpy as np

from .utils import mat2axis, axis2mat
from .constants import VideoType, Standard, Pattern
from .csc import rgb2yuv

def GenRGBAXIStream(resH, resV, pixelPerClock, pixelQuant, pattern):
    """ 
    - returns: AXIS transaction for one frame
    - resh: Horizontal resoltuion, >1
    - resv: Vertixal resolution, >1
    - pixelperclock: Pixel per clock in AXI transaction, [2]
    - pixelquant: Quantization, 10
    - pattern: 
        - p_incr = counter increment on every pixel
        - rand = random
        - h_incr = horizontal pixel increment
    """
    c ,r, q = resH, resV, pixelQuant
    mat = np.zeros((r, c, 3), dtype=np.uint16)

    if pattern == Pattern.p_incr:
        for i in range(r):
            for j in range(c):
                for k in range(3):
                    mat[i, j, k] = 512 + (i * r * 3 + j * 3 + k) % (2**q)
    elif pattern == Pattern.rand:
        mat = np.random.rand(r, c, 3)
        mat = (mat*1023).astype(np.uint16)
    elif pattern == Pattern.h_incr:
        for i in range(r):
            for j in range(c):
                mat[i, j, :] = j
    else:
        raise ValueError("Unknown pattern")

    mat = np.reshape(mat, newshape=(r*c,3))

    return mat2axis(mat, resH, pixelPerClock, pixelQuant)
    
def ConvertAXIStreamCS(resH, pixelPerClock, pixelQuant, outputVideoType, axisFrame):
    """ 
    - returns: Color converted AXIS 
    - resh: Horizontal resoltuion, >1
    - pixelperclock: Pixel per clock in AXI transaction, [2]
    - pixelquant: Quantization, 10
    - outputVideoType: VideoType
    - axisFrame: input frame to color convert
    """
    mat = axis2mat(axisFrame, resH, pixelPerClock, pixelQuant)
    if outputVideoType == VideoType.YUV:
        conv = rgb2yuv(mat, Standard.BT2020)
        return mat2axis(conv.T, resH, pixelPerClock, pixelQuant)
    else:
        raise ValueError("Unknown outputVideoType")
