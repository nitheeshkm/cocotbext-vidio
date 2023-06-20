# -*- coding: utf-8 -*-
#
# Produce color conversion matrices for TV scale YUV to full scale RGB
# according to the television standards ITU-R BT.601-7 (for SDTV)
# and ITU-R BT.709-5 (for HDTV).
#
# JJ 2012-03-15

import numpy as np

###########################
# config
###########################

# print output with this many decimals
np.set_printoptions(precision=15)

###########################
# functions
###########################

def shave_epsilons(A, **kwargs):
    """Shave smaller-than-epsilon components out of np.array A.

    Kwargs:
        eps = float, positive. Value of epsilon to use (default 1e-8).

    """
    if "eps" in kwargs:
        eps = kwargs["eps"]
    else:
        eps = 1e-8
    B = A.copy()
    B[ np.abs(B) < eps ] = 0.0
    return B

def r2y_601():
    """Return the RGB to YUV matrix for ITU-R BT.601-7 (standard definition television).

    Using the return value "M", the conversion is done by matrix-vector multiplication:
        yuv = np.dot(M, rgb)
    where rgb is a 3-element vector (rank-1 np.array).

    """

    # ITU-R BT.601-7, §2.5.1: RGB -> E'Y, (E'B - E'Y), (E'R - E'Y)
    # (note the order YBR, to match VLC)
    #
    # Here the color difference signals have not yet been rescaled.
    #
    r2y = np.array( [[ 0.299,  0.587,  0.114],
                     [-0.299, -0.587,  0.886],
                     [ 0.701, -0.587, -0.114]] )

    # ITU-R BT.601-7, §2.5.2: re-scale color difference signals
    # to -0.5 ... 0.5 to produce YUV
    #
    r2y[1,:] /= 1.772   # Cb
    r2y[2,:] /= 1.402   # Cr
    return r2y

def r2y_709():
    """Return the RGB to YUV matrix for ITU-R BT.709-5 (high definition television).

    Using the return value "M", the conversion is done by matrix-vector multiplication:
        yuv = np.dot(M, rgb)
    where rgb is a 3-element vector (rank-1 np.array).

    """

    # ITU-R BT.709-5, item 3.3 (p.19): RGB -> E'Y, E'CB, E'CR
    #
    r2y = np.array( [[ 0.2126,  0.7152,  0.0722],
                     [-0.2126, -0.7152,  0.9278],
                     [ 0.7874, -0.7152, -0.0722]] )
    r2y[1,:] /= 1.8556   # Cb
    r2y[2,:] /= 1.5748   # Cr
    return r2y

def r2y_2020():
    """Return the RGB to YUV matrix for ITU-R BT.2020-1 (ultra high definition television).

    Using the return value "M", the conversion is done by matrix-vector multiplication:
        yuv = np.dot(M, rgb)
    where rgb is a 3-element vector (rank-1 np.array).

    """

    # ITU-R BT.2020-1, item 3.3 (p.19): RGB -> E'Y, E'CB, E'CR
    #
    r2y = np.array( [[ 0.2627,  0.6780,  0.0593],
                     [-0.2627, -0.6780,  0.9407],
                     [ 0.7373, -0.6780, -0.0593]] )
    r2y[1,:] /= 1.8814   # Cb
    r2y[2,:] /= 1.4746   # Cr
    return r2y


def calibrate(standard, depth):
    if depth == "8bit"  or  standard == "601":
        # In ITU-R BT.709-5, see section 5, item 5.6, p. 22.
        #
        # In ITU-R BT.601-7, see Table 3, item 8, p. 9, and Table 4, item 8, p. 10.
        # These contain the same values for 4:2:2 and 4:4:4, respectively.

        tv_black_y      = 16./255.
        tv_white_y      = 235./255.

        # VLC: matrix_bt601_tv2full[] and matrix_bt709_tv2full[]
        # in modules/video_output/opengl.c
        #
        #tv_chroma_min   = 0./255.
        #tv_chroma_max   = 255./255.

        # mplayer2/VDPAU/CoreVideo (according to VLC ticket #6132)
        #
        tv_chroma_min   = 16./255.
        tv_chroma_max   = 240./255.

        tv_achromatic   = 128./255.
    elif depth == "10bit"  and (standard == "709" or standard == "2020"):
        # In ITU-R BT.709-5, see section 5, item 5.6, p. 22.

        tv_black_y    =  64./1023.
        tv_white_y    = 940./1023.

        tv_chroma_min =  64./1023.
        tv_chroma_max = 960./1023.

        tv_achromatic = 512./1023.
    else:
        raise ValueError("Unknown depth '%s'; valid are '8bit' and '10bit'." % depth)

    return (tv_black_y, tv_white_y, tv_chroma_min, tv_chroma_max, tv_achromatic)


def compute_conversion_matrix(standard, depth):
    """Produce color conversion matrix for TV scale YUV to full scale RGB.

    This is done according to the television standards ITU-R BT.601-7 (for SDTV)
    and ITU-R BT.709-5 (for HDTV).

    The matrix A is returned in a scale-and-shift form, which is used like this:
        fullscale_rgb = np.dot( A[:,:-1], tv_yuv ) + A[:,-1]
    where fullscale_rgb and tv_yuv are 3-element vectors (rank-1 np.array).

    This is a matrix-vector product using the 3x3 part of A, and then a vector shift
    using the last column of A.

    """
    # Get the RGB -> YUV (full scale) conversion matrix.
    #
    if standard == "601":
        r2y = r2y_601()
    elif standard == "709":
        r2y = r2y_709()
    elif standard == "2020":
        r2y = r2y_2020()
    else:
        raise ValueError("Unknown standard '%s'; valid are '601' and '709'." % standard)

    # Form the inverse conversion YUV (full scale) -> RGB by taking the matrix inverse.
    #
    # Remember that the ranges of the YUV components are:
    #
    # Y in [0,1], U in [-0.5,0.5], V in [-0.5,0.5].
    #
    y2r = shave_epsilons( np.linalg.inv(r2y) )

#    # A few examples.
#    #
#    def convert(matrix, color, name):
#        color_in  = np.array(color)
#        color_out = shave_epsilons( np.dot( matrix, color_in ) )
#        print "%s: original first, then converted:" % name
#        print color_in
#        print color_out
#
#    print "RGB -> YUV (full scale) examples:"
#    convert( r2y, (1.,1.,1.), "White" )
#    convert( r2y, (.5,.5,.5), "50% gray" )
#    convert( r2y, (1.,0.,0.), "Red" )
#    convert( r2y, (0.,1.,0.), "Green" )
#    convert( r2y, (0.,0.,1.), "Blue" )

    # We would like to convert "TV scale" YUV, i.e. YUV with
    # limited range luma (16..235), to full-scale RGB.
    #
    # Let us define (Y',U',V') such that we get the mappings
    #
    # Y = 0      =>  Y' = tv_black_y
    # Y = 1      =>  Y' = tv_white_y
    # U = -0.5   =>  U' = tv_chroma_min
    # U = +0.5   =>  U' = tv_chroma_max
    # V = -0.5   =>  V' = tv_chroma_min
    # V = +0.5   =>  V' = tv_chroma_max
    #
    # Let us also define
    #
    # tv_y_range      = tv_white_y    - tv_black_y
    # tv_chroma_range = tv_chroma_max - tv_chroma_min
    # tv_achromatic   = (achromatic chroma value from the relevant standard)
    #
    # Hence, we must have
    #
    # Y' = tv_black_y    + (tv_y_range)     /(full_y_range)      * Y
    # U' = tv_achromatic + (tv_chroma_range)/(full_chroma_range) * U
    # V' = tv_achromatic + (tv_chroma_range)/(full_chroma_range) * V
    #
    # All the full ranges are simply 1. Hence, the inverse transform is
    #
    # Y = (Y' - tv_black_y)     / tv_y_range
    # U = (U' - tv_achromatic)  / tv_chroma_range
    # V = (V' - tv_achromatic)  / tv_chroma_range
    #
    # In effect, (Y',U',V') are the raw video signal,
    # for which often an unsigned integer format is used.
    #
    # The ranges of the new variables are:
    #
    # Y' in [tv_black_y, tv_white_y],  U',V' in [tv_chroma_min,tv_chroma_max].
    #
    # We need to introduce a scaling and a shift to all components.
    #
    # Let us begin with the scaling. First we need to define the ranges.
    #
    tv_black_y, tv_white_y,         \
    tv_chroma_min, tv_chroma_max,   \
    tv_achromatic = calibrate(standard, depth)

    tv_y_range      = tv_white_y    - tv_black_y
    tv_chroma_range = tv_chroma_max - tv_chroma_min
    ytv2r = y2r.copy()
    ytv2r[:,0] /= tv_y_range
    ytv2r[:,1] /= tv_chroma_range
    ytv2r[:,2] /= tv_chroma_range

    # So far, we have
    #
    # result[j] = Y' * y2r[j,0]
    #           + U' * y2r[j,1]
    #           + V' * y2r[j,2].
    #
    # which takes care of the rescaling, but does not shift.
    #
    # We would like to have
    #
    # rgb[j] = (Y' - tv_black_y)    * ytv2r[j,0]
    #        + (U' - tv_achromatic) * ytv2r[j,1]
    #        + (V' - tv_achromatic) * ytv2r[j,2].
    #
    # Let us group all constant terms into a shift vector.
    # The conversion becomes
    #
    # rgb[j] = Y' * ytv2r[j,0]
    #        + U' * ytv2r[j,1]
    #        + V' * ytv2r[j,2]
    #        + shift[j]
    #
    # where
    #
    # shift[j] = - tv_black_y    * ytv2r[j,0]
    #            - tv_achromatic * ytv2r[j,1]
    #            - tv_achromatic * ytv2r[j,2].
    #
    # Finally, define the augmented conversion matrix, where the first three columns
    # are ytv2r, and the last column is the shift.
    #
    ytv2r_with_shift = np.empty( [3,4] )
    ytv2r_with_shift[:,:-1] = ytv2r   # scaling part (all except last column)

    # shift part (last column)
    ytv2r_with_shift[:,-1] = - tv_black_y*ytv2r_with_shift[:,0]      \
                             - tv_achromatic*ytv2r_with_shift[:,1]   \
                             - tv_achromatic*ytv2r_with_shift[:,2]

    return ytv2r_with_shift


###########################
# main script
###########################

# print("=" * 120)
# print("Conversion matrices from TV scale YUV to full scale RGB.")
# print( )
# print("First three columns = scalings, last column = shift.")
# print( )
# print("Matrix usage: do a matrix-vector product and a shift")
# print("    (R,G,B) = A[:,:-1] * (Y,U,V)  +  A[:,-1].")
# print("using RAW INPUT in TV ranges.")
# print( )
# print("Written explicitly:")
# print("    R = A[0,0]*Y + A[0,1]*U + A[0,2]*V  +  A[0,3]")
# print("    G = A[1,0]*Y + A[1,1]*U + A[1,2]*V  +  A[1,3]")
# print("    B = A[2,0]*Y + A[2,1]*U + A[2,2]*V  +  A[2,3]")
# print( )
# print("where Y is in [tv_black_y, tv_white_y],")
# print("      U is in [tv_min_chroma, tv_max_chroma], and")
# print("      V is in [tv_min_chroma, tv_max_chroma].")
# print( )
# print("This will convert and expand the ranges to full scale,")
# print("assuming the same bit depth in RGB and YUV.")

# # Television standards.
# # 601 is for SDTV, 709 is for HDTV.
# for standard in ["601", "709", "2020"]:
#     # Bit depth of signal.
#     # 709 defines some things differently depending on this.
#     for depth in ["8bit", "10bit"]:
#         A = compute_conversion_matrix(standard, depth)

#         print( )
#         print( "=" * 120)
#         print( "Standard: %s,  signal depth: %s" % (standard, depth))
#         print( "=" * 120)
#         print( )
#         print( A)


## Usage example.
##
#standard = "601"
#depth    = "8bit"
#
#A = compute_conversion_matrix(standard, depth)
#
#tv_black_y, tv_white_y,         \
#tv_chroma_min, tv_chroma_max,   \
#tv_achromatic = calibrate(standard, depth)
#
#white_yuv_tv        = np.array( (tv_white_y, tv_achromatic, tv_achromatic) )
#white_rgb_fullscale = np.dot( A[:,:-1], white_yuv_tv ) + A[:,-1]
#print white_rgb_fullscale

