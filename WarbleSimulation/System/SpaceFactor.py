from enum import Enum

import numpy as np


class SpaceFactor(Enum):
    MATTER = 'MATTER'
    TEMPERATURE = 'TEMPERATURE'
    HUMIDITY = 'HUMIDITY'
    LUMINOSITY = 'LUMINOSITY'
    AIR_MOVEMENT = 'AIR_MOVEMENT'


class Matter(Enum):
    MATTER = 0


class MatterType(Enum):
    ETHER = 0
    ATMOSPHERE = 1
    WATER = 2
    WOOD = 3
    CONCRETE = 4
    SOLID = 5


class Temperature(Enum):
    TEMPERATURE = 0  # in Kelvin(K)


class Humidity(Enum):
    HUMIDITY = 0  # in percentage (%)


class Luminosity(Enum):
    HUE = 1  # range 0-255
    SATURATION = 2  # range 0-255
    BRIGHTNESS = 3  # range 0-255


class AirMovement(Enum):
    X = 1  # in m/s
    Y = 2  # in m/s
    Z = 3  # in m/s


def generate(space_factor_type, dimension, resolution):
    '''

    :param space_factor_type: SpaceFactor Enum
    :param dimension: Tuple dimensions o
    :param resolution:
    :return:
    '''

    space_subfactors = []
    dtypes = []
    if space_factor_type == SpaceFactor.MATTER:
        space_subfactors = Matter
        dtypes = [MatterType]

    elif space_factor_type == SpaceFactor.TEMPERATURE:
        space_subfactors = Temperature
        dtypes = [int]

    elif space_factor_type == SpaceFactor.HUMIDITY:
        space_subfactors = Humidity
        dtypes = [int]

    elif space_factor_type == SpaceFactor.LUMINOSITY:
        space_subfactors = Luminosity
        dtypes = [int, int, int]

    elif space_factor_type == SpaceFactor.AIR_MOVEMENT:
        space_subfactors = AirMovement
        dtypes = [int, int, int]
    else:
        raise Exception('Unknown SpaceFactor Type')

    space_matrices = {}
    for i, space_subfactor in enumerate(space_subfactors):
        if i < len(dtypes) and dtypes[i] is not None:
            space_matrices[space_subfactor] = np.zeros(tuple([i * resolution for i in dimension]), dtypes[i])
        else:
            space_matrices[space_subfactor] = np.zeros(tuple([i * resolution for i in dimension]))

    return space_matrices
