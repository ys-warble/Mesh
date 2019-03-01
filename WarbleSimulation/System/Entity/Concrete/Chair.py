import numpy as np

from WarbleSimulation.System.Entity.Concrete import Concrete
from WarbleSimulation.System.SpaceFactor import MatterType


class Chair(Concrete):
    identifier = 'chair'
    default_dimension = (3, 3, 5)
    default_orientation = (0, 1, 0)

    def __init__(self, uuid, dimension_x=(1, 1, 1)):
        super().__init__(uuid=uuid, dimension_x=dimension_x, matter_type=MatterType.WOOD)
        self.dimension = tuple(
            [type(self).default_dimension[i] * self.dimension_x[i] for i in range(len(type(self).default_dimension))])

    def get_default_shape(self):
        matter = self.matter_type.value
        shape = np.array([
            [[matter] * 5,
             [0, 0, matter, 0, 0],
             [matter, matter, matter, 0, 0]],
            [[0, 0, matter, matter, matter],
             [0, 0, matter, 0, 0],
             [0, 0, matter, 0, 0]],
            [[matter] * 5,
             [0, 0, matter, 0, 0],
             [matter, matter, matter, 0, 0]],
        ])

        return shape