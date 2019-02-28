import numpy as np

from WarbleSimulation.System.Entity import Entity


def transform_shape(entity_shape, from_direction, to_direction):
    # TODO check validity of entity and to_direction

    if from_direction == to_direction:
        return entity_shape
    else:
        f_s = False
        f = 0
        if 1 in from_direction:
            f = from_direction.index(1)
            f_s = False
        elif -1 in from_direction:
            f = from_direction.index(-1)
            f_s = True

        t_s = False
        t = 0
        if 1 in to_direction:
            t = to_direction.index(1)
            t_s = False
        elif -1 in to_direction:
            t = to_direction.index(-1)
            t_s = True

        if f_s is not t_s and f == t:
            rot_k = 2
            t = f + 1 if f < 2 else f - 1
            rot_dir = (f, t)
        elif f_s is not t_s:
            rot_k = 1
            rot_dir = (t, f)
        else:
            rot_k = 1
            rot_dir = (f, t)

        return np.rot90(entity_shape, rot_k, rot_dir)


class Concrete(Entity):
    default_dimension = (1, 1, 1)
    default_direction = (0, 1, 0)

    def __init__(self, uuid, dimension_x, matter_type):
        super().__init__(uuid)
        self.dimension_x = dimension_x
        self.dimension = tuple(
            [Concrete.default_dimension[i] * self.dimension_x[i] for i in range(len(Concrete.default_dimension))])
        self.matter_type = matter_type

    def get_shape(self):
        return self.multiply_shape()

    def get_default_shape(self):
        return None

    def multiply_shape(self):
        if self.get_default_shape() is None:
            return None
        else:
            multiplier = tuple(
                [int(self.dimension[i] / type(self).default_dimension[i]) for i in range(len(self.dimension))])
            return np.kron(self.get_default_shape(), np.ones(multiplier))
