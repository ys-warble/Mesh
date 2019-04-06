import numpy as np

from Mesh.System.Entity.Concrete import Concrete
from Mesh.System.SpaceFactor import MatterType


class AirConditioner(Concrete):
    identifier = 'air_conditioner'
    default_dimension = (6, 3, 3)
    default_orientation = (0, 1, 0)

    def __init__(self, uuid, dimension_x=(1, 1, 1), selected_functions=()):
        super().__init__(uuid=uuid, dimension_x=dimension_x, matter_type=MatterType.PLASTIC,
                         selected_functions=selected_functions)

    def get_default_shape(self):
        i = self.matter_type.value
        shape = np.array([
            [[i, i, i],
             [i, i, i],
             [0, i, 0]],
            [[i, i, i],
             [i, i, i],
             [0, i, 0]],
            [[i, i, i],
             [i, i, i],
             [0, i, 0]],
            [[i, i, i],
             [i, i, i],
             [0, i, 0]],
            [[i, i, i],
             [i, i, i],
             [0, i, 0]],
            [[i, i, i],
             [i, i, i],
             [0, i, 0]],
        ])

        return shape

    def validate_functions(self, selected_functions):
        return True

    def define_functions(self, selected_functions):
        pass
