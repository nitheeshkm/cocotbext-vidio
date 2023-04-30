""" Test pattern generator"""

import numpy as np
import random as rand
from cocotbext.axi import (AxiStreamFrame)

def generate_frame(resh, resv, pixelperclock, pixelquant, pattern):
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
    m ,n, p, q = resh, resv, pixelperclock, pixelquant

    # Create a 10-bit RGB frame with dimensions resHxresV
    frame = np.zeros((m, n, 3), dtype=np.uint16)

    match pattern:
        case "p_incr":
            for i in range(m):
                for j in range(n):
                    for k in range(3):
                        frame[i, j, k] = (i * n * 3 + j * 3 + k) % (2**q)
        case "rand":
            for i in range(m):
                for j in range(n):
                    for k in range(3):
                        frame[i, j, k] = rand.randrange(1024)
        case "h_incr":
            for i in range(n):
                for j in range(m):
                    frame[i, j, :] = j

    frame = np.reshape(frame, newshape=(m*n,3))
    pack_range = int(m/p)
    full_axi_frame = []
    k = 0
    for j in range(n):
        packed_list = []
        for i in range(pack_range):
            packed_value = (frame[k+1, 2] << q*5) | (frame[k+1, 1] << q*4) | (frame[k+1, 0] << q*3) | (frame[k, 2] << q*2) | (frame[k, 1] << q) | frame[k, 0]
            packed_list.append(packed_value.tobytes())
            k = k + p
        bytearray_ = bytearray()
        for byte_array in packed_list:
            bytearray_.extend(byte_array)

        single_axi_frame = AxiStreamFrame(
                tdata=bytearray_,
                tuser=[1]*8 + [0] * (len(bytearray_)-8) if j == 0 else [0]*len(bytearray_)
            )
        full_axi_frame.append(single_axi_frame)
    return full_axi_frame