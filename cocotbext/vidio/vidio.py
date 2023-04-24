import numpy as np
import random as rand

from .utils import mat2axis, axis2mat

def GenRGBAXIStream(resh, resv, pixelperclock, pixelquant, pattern):
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
    h ,v, q = resh, resv, pixelquant
    mat = np.zeros((h, v, 3), dtype=np.uint16)

    if pattern == "p_incr":
        for i in range(h):
            for j in range(v):
                for k in range(3):
                    mat[i, j, k] = (i * v * 3 + j * 3 + k) % (2**q)
    elif pattern == "rand":
        for i in range(h):
            for j in range(v):
                for k in range(3):
                    mat[i, j, k] = rand.randrange(1024)
    elif pattern == "h_incr":
        for i in range(v):
            for j in range(h):
                mat[i, j, :] = j
    mat = np.reshape(mat, newshape=(h*v,3))

    return mat2axis(mat, resh, pixelperclock, pixelquant)

def CompareAXIS(TestStream, TestFormat, RecvStream, RecvFormat):
    if (TestFormat == RecvFormat): 
        return np.all(axis2mat(TestStream) == axis2mat(RecvStream))