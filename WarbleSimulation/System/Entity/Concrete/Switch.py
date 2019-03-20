import numpy as np

from WarbleSimulation.System.Entity.Concrete import Concrete
from WarbleSimulation.System.Entity.Function.Powered import PowerInput, PowerOutput
from WarbleSimulation.System.SpaceFactor import MatterType


class Switch(Concrete):
    identifier = 'switch'
    default_dimension = (1, 1, 2)
    default_orientation = (0, 1, 0)

    def __init__(self, uuid, dimension_x=(1, 1, 1)):
        super().__init__(uuid=uuid, dimension_x=dimension_x, matter_type=MatterType.PLASTIC)
        self.dimension = tuple(
            [type(self).default_dimension[i] * self.dimension_x[i] for i in range(len(type(self).default_dimension))])

        self.power_management.power_inputs.append(PowerInput(self))
        self.power_management.power_outputs.append(PowerOutput(self))

    def get_default_shape(self):
        m = self.matter_type.value
        shape = np.array([
            [[m, m]]
        ])

        return shape
