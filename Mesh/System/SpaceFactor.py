from enum import Enum

import numpy as np


# SpaceFactor
class SpaceFactor(Enum):
    MATTER = 'MATTER'
    TEMPERATURE = 'TEMPERATURE'
    HUMIDITY = 'HUMIDITY'
    LUMINOSITY = 'LUMINOSITY'
    AIR_MOVEMENT = 'AIR_MOVEMENT'


# TODO create mapping here so that the number of if-else is reduced
# SpaceSubfactor
class Matter(Enum):
    MATTER = 0


class MatterType(Enum):
    ETHER = 0

    GAS = 100
    ATMOSPHERE = 101

    LIQUID = 200
    WATER = 201

    SOLID = 300
    ORGANIC = 301
    PLASTIC = 302
    WOOD = 303
    GLASS = 304
    CONCRETE = 305
    METAL = 306
    PERFECT_SOLID = 399


class Temperature(Enum):
    TEMPERATURE = 0  # in Kelvin(K)


class Humidity(Enum):
    HUMIDITY = 0  # in percentage (%)


class Luminosity(Enum):
    HUE = 1  # range 0-360
    SATURATION = 2  # range 0-100
    BRIGHTNESS = 3  # range 0-100


class AirMovement(Enum):
    X = 1  # in m/s
    Y = 2  # in m/s
    Z = 3  # in m/s


SpaceFactorMap = {
    SpaceFactor.MATTER: {
        Matter.MATTER: {'dtype': int, 'default_value': MatterType.ATMOSPHERE.value},
    },
    SpaceFactor.TEMPERATURE: {
        Temperature.TEMPERATURE: {'dtype': int, 'default_value': 300},
    },
    SpaceFactor.LUMINOSITY: {
        Luminosity.HUE: {'dtype': int, 'default_value': 42},
        Luminosity.SATURATION: {'dtype': int, 'default_value': 99},
        Luminosity.BRIGHTNESS: {'dtype': int, 'default_value': 72},
    },
    SpaceFactor.HUMIDITY: {
        Humidity.HUMIDITY: {'dtype': int, 'default_value': 0},
    },
    SpaceFactor.AIR_MOVEMENT: {
        AirMovement.X: {'dtype': int, 'default_value': 0},
        AirMovement.Y: {'dtype': int, 'default_value': 0},
        AirMovement.Z: {'dtype': int, 'default_value': 0},
    },
}


def generate(space_factor_type, dimension, resolution, default_value=True):
    """

    :param space_factor_type: SpaceFactor Enum
    :param dimension: Tuple dimensions o
    :param resolution:
    :param default_value:
    :return:
    """

    space_matrices = {}
    for space_subfactor in SpaceFactorMap[space_factor_type]:
        space_matrices[space_subfactor] = np.full(shape=tuple([i * resolution for i in dimension]),
                                                  fill_value=(SpaceFactorMap[space_factor_type][space_subfactor][
                                                                  'default_value'] if default_value else 0),
                                                  dtype=SpaceFactorMap[space_factor_type][space_subfactor]['dtype']
                                                  )

    return space_matrices
