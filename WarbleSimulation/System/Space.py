from enum import Enum


class SpaceFactor(Enum):
    MATTER = 'MATTER'
    TEMPERATURE = 'TEMPERATURE'
    HUMIDITY = 'HUMIDITY'
    LUMINOSITY = 'LUMINOSITY'
    AIR_MOVEMENT = 'AIR_MOVEMENT'


class Space:
    def __init__(self, name, x, y, z, space_factors, resolution=1):
        if isinstance(name, str):
            self.name = name
        else:
            raise TypeError

        if isinstance(x, int) and isinstance(y, int) and isinstance(z, int) and isinstance(resolution, int):
            self.x = x
            self.y = y
            self.z = z
            self.resolution = resolution
        else:
            raise TypeError

        self.space_factors = {}
        if isinstance(space_factors, list) and all(isinstance(sf, SpaceFactor) for sf in space_factors):
            for space_factor in space_factors:
                # TODO: should not be None
                self.space_factors[space_factor] = None
        else:
            raise TypeError

    def add_space_factor(self, space_factor):
        if isinstance(space_factor, SpaceFactor):
            # TODO: should not be None
            self.space_factors[space_factor] = None
        elif isinstance(space_factor, list) and all(isinstance(sf, SpaceFactor) for sf in space_factor):
            for sf in space_factor:
                # TODO: should not be None
                self.space_factors[sf] = None
        else:
            raise TypeError
