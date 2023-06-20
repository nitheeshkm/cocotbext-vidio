import numpy as np

from .utils import mat2axis, axis2mat, csy444toy422
from .constants import Standard, Pattern, ColorFormat
from .csc import rgb2yuv

def GenAXIStream(resH, resV, pixelPerClock, pixelQuant, pattern, format):
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
    - format: RGB, YUV444, YUV422, YUV420
    """
    c ,r, q = resH, resV, pixelQuant
    rgb = np.zeros((r, c, 3), dtype=np.uint16)

    if pattern == Pattern.p_incr:
        for i in range(r):
            for j in range(c):
                for k in range(3):
                    rgb[i, j, k] = (i * r * 3 + j * 3 + k) % (2**q)
    elif pattern == Pattern.rand:
        rgb = np.random.rand(r, c, 3)
        rgb = (rgb*((2**q)-1)).astype(np.uint16)
    elif pattern == Pattern.h_incr:
        for i in range(r):
            for j in range(c):
                rgb[i, j, :] = j % (2**q)
    else:
        raise ValueError("Unknown pattern")
    
    rgbreshape = np.reshape(rgb, newshape=(r*c,3))
    axis = mat2axis(rgbreshape, resH, pixelPerClock, pixelQuant, format)

    return axis

    
def ConvertAXIStreamCS(resH, pixelPerClock, pixelQuant, outputFormat, axisFrame):
    """ 
    - returns: Color converted AXIS 
    - resh: Horizontal resoltuion, >1
    - pixelperclock: Pixel per clock in AXI transaction, [2]
    - pixelquant: Quantization, 10
    - outputFormat: RGB, YUV444, YUV422, YUV420
    - axisFrame: input frame to color convert
    """
    mat = axis2mat(axisFrame, resH, pixelPerClock, pixelQuant)
    if outputFormat == ColorFormat.YUV444:
        conv = rgb2yuv(mat, Standard.BT2020)
        return mat2axis(conv.T, resH, pixelPerClock, pixelQuant, outputFormat)
    else:
        raise ValueError("Unknown outputFormat")
