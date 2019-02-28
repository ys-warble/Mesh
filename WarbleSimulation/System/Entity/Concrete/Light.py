import numpy as np

from WarbleSimulation.System.Entity.Concrete import Concrete
from WarbleSimulation.System.SpaceFactor import MatterType


class Light(Concrete):
    identifier = 'light'
    default_dimension = (3, 3, 3)

    def __init__(self, uuid, dimension_x=(1, 1, 1)):
        super().__init__(uuid=uuid, dimension_x=dimension_x, matter_type=MatterType.GLASS)
        self.dimension = tuple(
            [Light.default_dimension[i] * self.dimension_x[i] for i in range(len(Light.default_dimension))])

    def get_default_shape(self):
        matter = self.matter_type.value
        shape = np.array([
            [[0, 0, 0],
             [0, matter, 0],
             [0, 0, 0]],
            [[0, matter, 0],
             [matter, matter, matter],
             [0, matter, 0]],
            [[0, 0, 0],
             [0, matter, 0],
             [0, 0, 0]],
        ])

        return shape
