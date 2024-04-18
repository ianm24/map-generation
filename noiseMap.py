# Made by IcyMink Apr 2024

import math
import numpy as np
from numpy import ndarray

'''
Array used for getting randomized output; same array Perlin used
'''
PERMUTATION = [151, 160, 137, 91, 90, 15,
               131, 13, 201, 95, 96, 53, 194, 233, 7, 225, 140, 36, 103, 30,
               69, 142, 8, 99, 37, 240, 21, 10, 23, 190, 6, 148, 247, 120, 234,
               75, 0, 26, 197, 62, 94, 252, 219, 203, 117, 35, 11, 32, 57, 177,
               33, 88, 237, 149, 56, 87, 174, 20, 125, 136, 171, 168, 68, 175,
               74, 165, 71, 134, 139, 48, 27, 166, 77, 146, 158, 231, 83, 111,
               229, 122, 60, 211, 133, 230, 220, 105, 92, 41, 55, 46, 245, 40,
               244, 102, 143, 54, 65, 25, 63, 161, 1, 216, 80, 73, 209, 76,
               132, 187, 208, 89, 18, 169, 200, 196, 135, 130, 116, 188, 159,
               86, 164, 100, 109, 198, 173, 186, 3, 64, 52, 217, 226, 250, 124,
               123, 5, 202, 38, 147, 118, 126, 255, 82, 85, 212, 207, 206, 59,
               227, 47, 16, 58, 17, 182, 189, 28, 42, 223, 183, 170, 213, 119,
               248, 152, 2, 44, 154, 163, 70, 221, 153, 101, 155, 167, 43, 172,
               9, 129, 22, 39, 253, 19, 98, 108, 110, 79, 113, 224, 232, 178,
               185, 112, 104, 218, 246, 97, 228, 251, 34, 242, 193, 238, 210,
               144, 12, 191, 179, 162, 241, 81, 51, 145, 235, 249, 14, 239,
               107, 49, 192, 214, 31, 181, 199, 106, 157, 184, 84, 204, 176,
               115, 121, 50, 45, 127, 4, 150, 254, 138, 236, 205, 93, 222, 114,
               67, 29, 24, 72, 243, 141, 128, 195, 78, 66, 215, 61, 156, 180
               ]


def get_gradient_vector(x: int, y: int) -> np.ndarray[float]:
    '''
    Gets a constant gradient vector for a given position

    :param x: x-value on noise map
    :type x: int
    :param y: y-value on noise map
    :type y: int
    :return: 2D gradient vector
    :rtype: np.ndarray[float]
    '''
    hash = PERMUTATION[PERMUTATION[x]+y] & 3

    if (hash == 0):
        return np.asarray([1.0, 1.0])
    elif (hash == 1):
        return np.asarray([-1.0, 1.0])
    elif (hash == 2):
        return np.asarray([1.0, -1.0])
    else:
        return np.asarray([-1.0, -1.0])


def fade(num: float) -> float:
    '''
    The fade/ease function used by Perlin

    :param num: The number input to the function
    :type num: float
    :return: Scalar output of the fade function
    :rtype: float
    '''
    return interpolate(0, 1, num, 2)


def interpolate(a: float, b: float, w: float, method: int) -> float:
    '''
    Interpolates between a and b using weight w and selected method

    :param a: First point
    :type a: float
    :param b: Second point
    :type b: float
    :param w: Weight of interpolation
    :type w: float
    :param method: 1: Cubic interpolation (smoothstep) 2: Linear interpolation
    :type method: int
    :return: Interpolated value
    :rtype: float
    '''
    if method == 1:  # Cubic interpolation (smoothstep)
        return (b-a) * (3-w*2)*w*w + a
    elif method == 2:  # Smootherstep
        return (b-a) * ((w * (w*6 - 15) + 10) * w*w*w) + a
    else:  # Linear interpolation
        return a + w*(b-a)


def get_perlin_point(x: int, y: int, interp_method: int) -> float:
    '''
    Gives the perlin noise at a point given an interpolation method

    :param x: x-coordinate
    :type x: int
    :param y: y-coordinate
    :type y: int
    :param interp_method: 1: Cubic interpolation 2: Linear interpolation
    :type interp_method: int
    :return: Perlin noise at (x,y); range [-1,1]
    :rtype: float
    '''
    # Get offset vectors for the chosen point
    xf = x-math.floor(x)
    yf = y-math.floor(y)

    offset_vecs = np.asarray([
        [xf-1, yf-1],
        [xf, yf-1],
        [xf-1, yf],
        [xf, yf]
    ])  # type: np.ndarray[float]

    # Get gradient vectors
    xG = math.floor(x) & 255
    yG = math.floor(y) & 255
    gradient_vecs = np.asarray([
        get_gradient_vector(xG+1, yG+1),
        get_gradient_vector(xG, yG+1),
        get_gradient_vector(xG+1, yG),
        get_gradient_vector(xG, yG),
    ])  # type: np.ndarray[float]

    # Calculate the dot products
    dotp_map = np.ndarray(4)  # type: np.ndarray[float]
    for i in range(len(offset_vecs)):
        dotp_map[i] = np.dot(offset_vecs[i], gradient_vecs[i])

    # Interpolate between the dot product values
    weightX = fade(xf)
    weightY = fade(yf)
    l_interp = interpolate(
        dotp_map[3], dotp_map[1], weightY, interp_method)
    r_interp = interpolate(
        dotp_map[2], dotp_map[0], weightY, interp_method)

    return interpolate(l_interp, r_interp, weightX, interp_method)


def get_perlin_map(height: int, width: int, res: int,
                   interp_method: int) -> np.ndarray[float]:
    """
    Returns a 2D map of perlin noise.

    :param height: Height of the perlin map
    :type height: int
    :param width: Width of the perlin map
    :type width: int
    :param res: Resolution; Steps between each gradient point
    :type res: int
    :return: 2D map with values from -1 to 1 of shape [height/res, width/res]
    :rtype: np.ndarray[float]
    """

    # For each point in the map, calculate the perlin value for it
    perlin_map = np.ndarray((int(height/res),
                             int(width/res)))  # type: np.ndarray[float]
    for y in range(int(height/res)):
        for x in range(int(width/res)):
            val = get_perlin_point(x*res, y*res, interp_method)

            perlin_map[x, y] = val

    return perlin_map
