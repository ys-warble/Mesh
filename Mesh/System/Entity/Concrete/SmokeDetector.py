import numpy as np

from Mesh.System.Entity.Concrete import Concrete
from Mesh.System.SpaceFactor import MatterType


class SmokeDetector(Concrete):
    identifier = 'smoke_detector'
    default_dimension = (2, 2, 1)
    default_orientation = (0, 0, -1)

    def __init__(self, uuid, dimension_x=(1, 1, 1), selected_functions=()):
        super().__init__(uuid=uuid, dimension_x=dimension_x, matter_type=MatterType.PLASTIC,
                         selected_functions=selected_functions)
        self.dimension = tuple(
            [type(self).default_dimension[i] * self.dimension_x[i] for i in range(len(type(self).default_dimension))])

    def get_default_shape(self):
        i = self.matter_type.value
        shape = np.array([
            [[i],
             [i]],
            [[i],
             [i]],
        ])

        return shape

    def validate_functions(self, selected_functions):
        return True

    def define_functions(self, selected_functions):
        pass
