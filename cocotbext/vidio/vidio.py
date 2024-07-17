import numpy as np

from .utils import mat2axis, axis2mat
from .constants import Standard, Pattern, ColorFormat
from .csc import rgb2yuv, y444to422, y420to422

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
    rgb = np.zeros((r, c, 3), dtype=np.uint64)

    if pattern == Pattern.p_incr:
        for i in range(r):
            for j in range(c):
                for k in range(3):
                    rgb[i, j, k] = (i * r * 3 + j * 3 + k) % (2**q)
    elif pattern == Pattern.rand: # TODO: Fix bug here. The matrix returned isn't matching data on simulation (gtkwave)
        rgb = np.random.rand(r, c, 3)
        rgb = (rgb*((2**q)-1)).astype(np.uint64)
    elif pattern == Pattern.h_incr:
        for i in range(r):
            for j in range(c):
                rgb[i, j, :] = j % (2**q)
    else:
        raise ValueError("Unknown pattern")

    mask = np.ones((r*c, 3), dtype=np.uint64)
    vcount, hcount = 0, 0
    if (format == ColorFormat.YUV422):
        for i in range(r*c):
            if (i%2) :
                mask[i][1:] = [0, 0]
    elif (format == ColorFormat.YUV420):
        for i in range(r*c):
            if (i%2) :
                mask[i][1:] = [0, 0]
            if vcount%2 :
                mask[i][1:] = [0, 0]
            if hcount == resH-1:
                vcount = vcount + 1
                hcount = 0
            else:
                hcount = hcount + 1

    rgbreshape = np.reshape(rgb, newshape=(r*c,3))
    rgbreshape = rgbreshape*mask
    axis = mat2axis(rgbreshape, resH, pixelPerClock, 10, format)

    return axis, rgbreshape


def ConvertAXIStreamCS(resH, pixelPerClock, pixelQuant, inputFormat, outputFormat, axisFrame):
    """
    - returns: Color converted AXIS
    - resH: Horizontal resoltuion, >1
    - pixelperclock: Pixel per clock in AXI transaction, [2]
    - pixelquant: Quantization, 10
    - inputFormat: RGB, YUV444, YUV422, YUV420
    - outputFormat: RGB, YUV444, YUV422, YUV420
    - axisFrame: input frame to color convert
    """
    mat = axis2mat(axisFrame, resH, pixelPerClock, pixelQuant, inputFormat)
    if inputFormat == ColorFormat.RGB:
        if outputFormat == ColorFormat.YUV444:
            conv = rgb2yuv(mat, Standard.BT2020)
            return mat2axis(conv.T, resH, pixelPerClock, pixelQuant, ColorFormat.YUV444), conv.T
        else:
            raise ValueError("Unsupported Format combination")
    elif inputFormat == ColorFormat.YUV444:
        if outputFormat == ColorFormat.YUV422:
            conv = y444to422(mat)
            return mat2axis(conv.T, resH, pixelPerClock, pixelQuant, ColorFormat.YUV422), conv.T
        else:
            raise ValueError("Unsupported Format combination")
    elif inputFormat == ColorFormat.YUV420:
        if outputFormat == ColorFormat.YUV422:
            conv = y420to422(mat, resH)
            return mat2axis(conv.T, resH, pixelPerClock, pixelQuant, ColorFormat.YUV420), conv.T
    else:
        raise ValueError("Unsupported inputFormat")
