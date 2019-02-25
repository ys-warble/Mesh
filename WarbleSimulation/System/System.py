import WarbleSimulation.System.Space as Space
import WarbleSimulation.System.SpaceFactor as SpaceFactor


class System:
    def __init__(self, name):
        self.name = name

        self.space = None
        self.entities = None

    def put_space(self, dimension, resolution=1, space_factor_types=None):
        """

        :param dimension: tuple: representing 3-dimensional space measures
        :param resolution: int: resolution for each space measure
        :param space_factor_types: list: ...
        :return:
        """
        if space_factor_types is None:
            space_factor_types = []

        self.space = Space(dimension, resolution, space_factor_types)

        # TODO: How if the space is re-put after putting entities?

    def init_normal_space(self):
        for space_factor in self.space.space_factors.keys():
            for space_subfactor in self.space.space_factors[space_factor].keys():
                value = 0

                if space_factor == SpaceFactor.SpaceFactor.MATTER and space_subfactor == SpaceFactor.Matter.MATTER:
                    value = SpaceFactor.MatterType.ATMOSPHERE
                elif space_factor == SpaceFactor.SpaceFactor.TEMPERATURE and space_subfactor == SpaceFactor.Temperature.TEMPERATURE:
                    value = 300
                elif space_factor == SpaceFactor.SpaceFactor.HUMIDITY and space_subfactor == SpaceFactor.Humidity.HUMIDITY:
                    value = 0
                elif space_factor == SpaceFactor.SpaceFactor.LUMINOSITY and space_subfactor in [
                    SpaceFactor.Luminosity.HUE, SpaceFactor.Luminosity.SATURATION, SpaceFactor.Luminosity.BRIGHTNESS]:
                    value = 0
                elif space_factor == SpaceFactor.SpaceFactor.AIR_MOVEMENT and space_subfactor in [
                    SpaceFactor.AirMovement.X, SpaceFactor.AirMovement.Y, SpaceFactor.AirMovement.Z]:
                    value = 0

                self.space.init_space_factor(space_factor, space_subfactor, value)

    def init_space(self):
        # This should be replaced by reading the content of input file
        self.init_normal_space()

    def put_entity(self, entity, location, direction):
        raise NotImplementedError
