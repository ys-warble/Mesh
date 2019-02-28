import numpy as np

from WarbleSimulation.System.Entity import Entity


class Concrete(Entity):
    default_dimension = (1, 1, 1)

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
