import numpy as np

from Mesh.System import SpaceFactor
from Mesh.System.Entity import Concrete
from Mesh.System.Space import Space
from Mesh.util import Logger


class System:
    def __init__(self, name):
        self.name = name

        self.space = None
        self.entities = []

        self.logger = Logger.get_logger(__name__)

    def put_space(self, dimension, resolution=1, space_factor_types=None, default_value=True):
        """

        :param dimension: tuple: representing 3-dimensional space measures
        :param resolution: int: resolution for each space measure
        :param space_factor_types: list: ...
        :return:
        """
        if space_factor_types is None:
            space_factor_types = []

        self.space = Space(dimension, resolution, space_factor_types, default_value)

        # TODO: How if the space is re-put after putting entities?

    def put_entity(self, entity, location, unit_orientation=None, reference='origin', in_resolution=False):
        # TODO check validity, entity = entity, location is tuple 3,
        # unit direction is tuple 3 and only 1 is set, rest are unset, reference is only origin

        # Check location is in space
        if self.space is None:
            raise AttributeError

        if not all(0 <= location[i] < self.space.dimension[i] * self.space.resolution for i in range(len(location))):
            return False

        res_multiplier = 1 if in_resolution is True else self.space.resolution

        # Get Entity Shape
        entity_shape = entity.get_shape()
        if entity_shape is not None and unit_orientation is not None:
            entity_shape = Concrete.transform_shape(entity_shape, type(entity).default_orientation, unit_orientation)
        elif entity_shape is None:
            entity_shape = np.full(
                tuple([int(entity.dimension[i] * res_multiplier) for i in range(len(entity.dimension))]),
                entity.matter_type.value)
        else:
            pass

        if reference == 'origin':
            x_begin = int(location[0] * res_multiplier)
            x_end = int(location[0] * res_multiplier + entity_shape.shape[0] - 1)
            y_begin = int(location[1] * res_multiplier)
            y_end = int(location[1] * res_multiplier + entity_shape.shape[1] - 1)
            z_begin = int(location[2] * res_multiplier)
            z_end = int(location[2] * res_multiplier + entity_shape.shape[2] - 1)
        else:
            return False

        # Check if fit, not exceeding boundary
        self.logger.debug('x_begin: %s; x_end: %s; y_begin: %s; y_end: %s; z_begin: %s; z_end: %s;' % (
            x_begin, x_end, y_begin, y_end, z_begin, z_end))
        if x_begin < 0 or \
                y_begin < 0 or \
                z_begin < 0 or \
                x_end > self.space.dimension[0] * self.space.resolution - 1 or \
                y_end > self.space.dimension[1] * self.space.resolution - 1 or \
                z_end > self.space.dimension[2] * self.space.resolution - 1:
            return False

        # Modify Matter
        if entity_shape is None:
            self.space.space_factors[SpaceFactor.SpaceFactor.MATTER][SpaceFactor.Matter.MATTER][x_begin:x_end + 1,
            y_begin:y_end + 1, z_begin:z_end + 1] = entity.matter_type.value
        else:
            temp = self.space.space_factors[SpaceFactor.SpaceFactor.MATTER][SpaceFactor.Matter.MATTER][
                   x_begin:x_end + 1, y_begin:y_end + 1, z_begin:z_end + 1]
            new = np.where((temp / 100).astype(int) > (entity_shape / 100).astype(int), temp, entity_shape)
            self.space.space_factors[SpaceFactor.SpaceFactor.MATTER][SpaceFactor.Matter.MATTER][x_begin:x_end + 1,
            y_begin:y_end + 1, z_begin:z_end + 1] = new

        # Change the space factor
        self.entities.append((entity, location, unit_orientation))

        return True

    def get_entity(self, index):
        if index < len(self.entities):
            return self.entities[index][0]
        else:
            raise IndexError

    def remove_entity(self, entity):
        # TODO: Implement
        raise NotImplementedError

    def destroy(self):
        for row in self.entities:
            row[0].destroy()

    def __str__(self):
        string = ''
        string += 'System'
        string += '('
        string += '\n  name=%s,' % self.name

        string += '\n  space=%s,' % str(self.space).replace('\n', '\n  ')

        string += '\n  entities=['
        entities = ['    (%s,loc=%s,ori=%s)' % (row[0], row[1], row[2]) for row in self.entities]
        string += '\n'
        string += '%s' % ',\n'.join(entities)

        string += '\n  ]'
        string += ')'

        return string

    def to_json(self):
        json = {
            "system": {
                "name": self.name
            },
            "space": {
                "dimension": self.space.dimension,
                "resolution": self.space.resolution,
                "space_factor_types": [i.value for i in self.space.space_factors.keys()]
            },
            "entities": [
                {
                    "entity": type(i[0]).identifier,
                    "uuid": str(i[0].uuid),
                    "dimension": i[0].dimension,
                    "selected_features": [j.value for j in i[0].functions.keys()],
                    "location": i[1]
                }
                for i in self.entities],
        }

        return json
