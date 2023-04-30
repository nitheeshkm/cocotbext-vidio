"""Utilities"""
import numpy as np
from cocotbext.axi import AxiStreamFrame

def mat2axis(matrix, resH, pixelPerClock, pixelQuant):
    """ 
    converts matrix to axis
    - matrix: numpy array of shape mx3, where m = rows*columns 3 = color channels
    - return: cocotbext.axi.AxiStreamFrame
    """
    c = resH
    p = pixelPerClock
    v = int(matrix.shape[0]/resH)
    q = pixelQuant
    pack_range =  int(c/p)
    frame = matrix
    full_axi_frame = []
    k = 0
    for j in range(v):
        packed_list = []
        for _ in range(pack_range):
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

def axis2mat(axisFrame, resH, pixelPerClock, pixelQuant):
    """ 
    converts axis to matrix
    - axisFrame: cocotbext.axi.AxiStreamFrame
    - return: numpy array
    """
    r = len(axisFrame)
    c = resH
    p = pixelPerClock
    pack_range = int(c/p)
    q = pixelQuant
    mat = np.zeros((r, c, 3), dtype=np.int16)
    mask = (1 << q) - 1
    for i in range(r):
        for j in range(pack_range):
            d_val = int.from_bytes(axisFrame[i].tdata[j*8:8*(j+1)], byteorder='little', signed=False)
            mat[i][2*j][0] = d_val >> 0*10 & mask
            mat[i][2*j][1] = d_val >> 1*10 & mask
            mat[i][2*j][2] = d_val >> 2*10 & mask
            mat[i][2*j+1][0] = d_val >> 3*10 & mask
            mat[i][2*j+1][1] = d_val >> 4*10 & mask
            mat[i][2*j+1][2] = d_val >> 5*10 & mask
    
    return np.reshape(mat, newshape=(r*c,3))