import numpy as np

from WarbleSimulation.System.Entity.Concrete import Concrete
from WarbleSimulation.System.SpaceFactor import MatterType


class Human(Concrete):
    identifier = 'human'
    default_dimension = (4, 2, 8)
    default_orientation = (0, 1, 0)

    def __init__(self, uuid, dimension_x=(1, 1, 1)):
        super().__init__(uuid=uuid, dimension_x=dimension_x, matter_type=MatterType.ORGANIC)
        self.dimension = tuple(
            [type(self).default_dimension[i] * self.dimension_x[i] for i in range(len(type(self).default_dimension))])

    def get_default_shape(self):
        i = self.matter_type.value
        shape = np.array([
            [[0, 0, 0, i, i, i, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0]],
            [[i, i, i, i, i, i, i, i],
             [i, 0, 0, 0, 0, 0, 0, 0]],
            [[i, i, i, i, i, i, i, i],
             [i, 0, 0, 0, 0, 0, 0, 0]],
            [[0, 0, 0, i, i, i, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0]],
        ])

        return shape

    def define_functions(self):
        pass
