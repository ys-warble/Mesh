import numpy as np

from WarbleSimulation.System import SpaceFactor
from WarbleSimulation.System.Space import Space
from WarbleSimulation.util import Logger


class System:
    def __init__(self, name):
        self.name = name

        self.space = None
        self.entities = []

        self.logger = Logger.get_logger(__name__)

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

    def put_entity(self, entity, location, unit_direction=None, reference='origin', in_resolution=False):
        self.logger.debug('Entity dimension = %s => %s' % (
        entity.dimension, tuple([i * self.space.resolution for i in entity.dimension])))
        self.logger.debug('Put Location = %s => %s' % (location, tuple([i * self.space.resolution for i in location])))
        self.logger.debug('Space = %s => %s' % (
        self.space.dimension, tuple([i * self.space.resolution for i in self.space.dimension])))
        # TODO check validity

        # TODO: Check location is in space
        if not all(0 <= location[i] < self.space.dimension[i] * self.space.resolution for i in range(len(location))):
            return False

        res_multiplier = 1 if in_resolution is True else self.space.resolution

        if reference == 'origin':
            x_begin = int(location[0] * res_multiplier)
            x_end = int(location[0] * res_multiplier + entity.dimension[0] * res_multiplier - 1)
            y_begin = int(location[1] * res_multiplier)
            y_end = int(location[1] * res_multiplier + entity.dimension[1] * res_multiplier - 1)
            z_begin = int(location[2] * res_multiplier)
            z_end = int(location[2] * res_multiplier + entity.dimension[2] * res_multiplier - 1)

        elif reference == 'center':
            x_center = int((entity.dimension[0] * self.space.resolution - 1) / 2)
            y_center = int((entity.dimension[1] * self.space.resolution - 1) / 2)
            z_center = int((entity.dimension[2] * self.space.resolution - 1) / 2)

            x_begin = (location[0] * self.space.resolution - int((entity.dimension[0] * self.space.resolution + 1) / 2))
            x_end = (location[0] * self.space.resolution + int((entity.dimension[0] * self.space.resolution + 1) / 2))
            y_begin = (location[1] * self.space.resolution - int((entity.dimension[1] * self.space.resolution + 1) / 2))
            y_end = (location[1] * self.space.resolution + int((entity.dimension[1] * self.space.resolution + 1) / 2))
            z_begin = (location[2] * self.space.resolution - int((entity.dimension[2] * self.space.resolution + 1) / 2))
            z_end = (location[2] * self.space.resolution + int((entity.dimension[2] * self.space.resolution + 1) / 2))

        else:
            return False

        # Check if fit, not exceeding boundary
        if x_begin < 0 or \
                y_begin < 0 or \
                z_begin < 0 or \
                x_end > self.space.dimension[0] * self.space.resolution - 1 or \
                y_end > self.space.dimension[1] * self.space.resolution - 1 or \
                z_end > self.space.dimension[2] * self.space.resolution - 1:
            return False

        # Modify Matter
        entity_shape = entity.get_shape()
        if entity_shape is None:
            self.logger.debug('entity_shape doesn\'t exist')
            self.space.space_factors[SpaceFactor.SpaceFactor.MATTER][SpaceFactor.Matter.MATTER][x_begin:x_end + 1,
            y_begin:y_end + 1, z_begin:z_end + 1] = entity.matter_type.value
        else:
            self.logger.debug('entity_shape exists')
            temp = self.space.space_factors[SpaceFactor.SpaceFactor.MATTER][SpaceFactor.Matter.MATTER][
                   x_begin:x_end + 1, y_begin:y_end + 1, z_begin:z_end + 1]
            new = np.where((temp / 100).astype(int) > (entity_shape / 100).astype(int), temp, entity_shape)
            self.space.space_factors[SpaceFactor.SpaceFactor.MATTER][SpaceFactor.Matter.MATTER][x_begin:x_end + 1,
            y_begin:y_end + 1, z_begin:z_end + 1] = new

        # Change the space factor
        self.entities.append((entity, location, unit_direction))

        return True

    def remove_entity(self):
        pass
