""" Color Space Conversion"""

import numpy as np
from .colorconv import r2y_601, r2y_709, r2y_2020
from .constants import Standard

def rgb2yuv(rgb, standard):
    """
    returns matrix with shape (m*n, 3)
    """
    if standard == Standard.BT601:
        r2y = r2y_601()
    elif standard == Standard.BT709:
        r2y = r2y_709()
    elif standard == Standard.BT2020:
        r2y = r2y_2020()
    else:
        raise ValueError("Unknown standard '%s'; valid are '601' and '709'." % standard)
    rgb = rgb / 1023
    rgb = np.array(rgb).T
    yuv = np.array(np.dot(r2y, rgb))
    return np.clip(yuv * 1023, 0, 1023).astype(np.uint16)

def yuv2rgb():
    pass

def y444to422(y444):
    """
    returns matrix with shape (m*n, 3)
    """
    y422 = np.zeros((y444.shape[0], y444.shape[1]), dtype=np.uint16)
    y422 = y444
    for i in range(y444.shape[0]):
        if not(i%2):
            y422[i][0] = y444[i][0]
            y422[i][1] = (y444[i][1] // 2) + (y444[i+1][1] // 2)
            y422[i][2] = (y444[i][2] // 2) + (y444[i+1][2] // 2)
    return y422.T

def y420to422(y420, resH):
    """
    returns matrix with shape (m*n, 3)
    """
    y422 = np.zeros((y420.shape[0], y420.shape[1]), dtype=np.uint16)
    y422 = y420
    resV = int(len(y422) / resH)
    for i in range(resV):
        if i%2:
            for j in range(resH):
                y422[i*resH + j][0] = y420[i*resH + j][0]
                if i == resV-1 :
                    y422[i*resH + j][1] = (y420[(i-1)*resH + j][1])
                    y422[i*resH + j][2] = (y420[(i-1)*resH + j][2])
                else :
                    y422[i*resH + j][1] = (y420[(i-1)*resH + j][1] + y420[(i+1)*resH + j][1]) / 2
                    y422[i*resH + j][2] = (y420[(i-1)*resH + j][2] + y420[(i+1)*resH + j][2]) / 2
    return y422.T
