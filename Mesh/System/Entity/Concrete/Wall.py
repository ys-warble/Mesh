import numpy as np

from Mesh.System.Entity.Concrete import Concrete
from Mesh.System.SpaceFactor import MatterType


class Wall(Concrete):
    identifier = 'wall'
    default_dimension = (1, 1, 1)
    default_orientation = (0, 1, 0)

    def __init__(self, uuid, dimension_x=(1, 1, 1)):
        super().__init__(uuid=uuid, dimension_x=dimension_x, matter_type=MatterType.CONCRETE,
                         selected_functions=())

    def get_default_shape(self):
        i = self.matter_type.value
        shape = np.array([[[i]]])
        return shape

    def validate_functions(self, selected_functions):
        return True

    def define_functions(self, selected_functions):
        pass
