import numpy as np

from WarbleSimulation.System.Entity.Basic.Power import PowerOutput
from WarbleSimulation.System.Entity.Concrete import Concrete
from WarbleSimulation.System.SpaceFactor import MatterType


class PowerSupply(Concrete):
    identifier = 'PowerSource'
    default_dimension = (1, 1, 1)
    default_orientation = (0, 1, 0)

    def __init__(self, uuid, dimension_x=(1, 1, 1)):
        super().__init__(uuid=uuid, dimension_x=dimension_x, matter_type=MatterType.METAL)
        self.dimension = tuple(
            [type(self).default_dimension[i] * self.dimension_x[i] for i in range(len(type(self).default_dimension))])

        self.runnable = True
        self.task_active = False

        self.power_management.power_outputs.append(PowerOutput(self))

    def get_default_shape(self):
        matter = self.matter_type.value
        shape = np.array([[[matter]]])

        return shape
