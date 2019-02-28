import numpy as np

from WarbleSimulation.System.Entity.Concrete import Concrete
from WarbleSimulation.System.SpaceFactor import MatterType


class Table(Concrete):
    identifier = 'tables'
    default_dimension = (4, 4, 4)

    def __init__(self, uuid, dimension_x=(1, 1, 1)):
        super().__init__(uuid=uuid, dimension_x=dimension_x, matter_type=MatterType.WOOD)
        self.dimension = tuple(
            [Table.default_dimension[i] * self.dimension_x[i] for i in range(len(Table.default_dimension))])

    def get_shape(self):
        shape = np.zeros(Table.default_dimension)

        shape[:, :, Table.default_dimension[2] - 1:Table.default_dimension[2]] = self.matter_type.value
        shape[0:1, 0:1, 0:Table.default_dimension[2] - 1] = self.matter_type.value
        shape[Table.default_dimension[0] - 1:Table.default_dimension[0], 0:1,
        0:Table.default_dimension[2] - 1] = self.matter_type.value
        shape[0:1, Table.default_dimension[1] - 1:Table.default_dimension[1],
        0:Table.default_dimension[2] - 1] = self.matter_type.value
        shape[Table.default_dimension[0] - 1:Table.default_dimension[0],
        Table.default_dimension[1] - 1:Table.default_dimension[1],
        0:Table.default_dimension[2] - 1] = self.matter_type.value

        multiplier = tuple([int(self.dimension[i] / Table.default_dimension[i]) for i in range(len(self.dimension))])

        shape = np.kron(shape, np.ones(multiplier))

        return shape
