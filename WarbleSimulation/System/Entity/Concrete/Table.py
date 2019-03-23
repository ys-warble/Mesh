import numpy as np

from WarbleSimulation.System.Entity.Concrete import Concrete
from WarbleSimulation.System.SpaceFactor import MatterType


class Table(Concrete):
    identifier = 'tables'
    default_dimension = (5, 4, 4)
    default_orientation = (0, 1, 0)

    def __init__(self, uuid, dimension_x=(1, 1, 1), selected_functions=()):
        super().__init__(uuid=uuid, dimension_x=dimension_x, matter_type=MatterType.WOOD,
                         selected_functions=selected_functions)
        self.dimension = tuple(
            [Table.default_dimension[i] * self.dimension_x[i] for i in range(len(type(self).default_dimension))])

    def get_default_shape(self):
        dimension = type(self).default_dimension

        shape = np.zeros(dimension)

        shape[:, :, dimension[2] - 1:dimension[2]] = self.matter_type.value
        shape[0:1, 0:1, 0:dimension[2] - 1] = self.matter_type.value
        shape[dimension[0] - 1:dimension[0], 0:1, 0:dimension[2] - 1] = self.matter_type.value
        shape[0:1, dimension[1] - 1:dimension[1], 0:dimension[2] - 1] = self.matter_type.value
        shape[dimension[0] - 1:dimension[0], dimension[1] - 1:type(self).default_dimension[1],
        0:dimension[2] - 1] = self.matter_type.value

        return shape

    def validate_functions(self, selected_functions):
        return True

    def define_functions(self, selected_functions):
        pass
