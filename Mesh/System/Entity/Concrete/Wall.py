from Mesh.System.Entity.Concrete import Concrete
from Mesh.System.SpaceFactor import MatterType


class Wall(Concrete):
    identifier = 'wall'
    default_dimension = (1, 1, 1)
    default_orientation = (0, 1, 0)

    def __init__(self, uuid, dimension_x=(1, 1, 1), selected_functions=()):
        super().__init__(uuid=uuid, dimension_x=dimension_x, matter_type=MatterType.CONCRETE,
                         selected_functions=selected_functions)
        self.dimension = tuple(
            [type(self).default_dimension[i] * self.dimension_x[i] for i in range(len(type(self).default_dimension))])

    def get_default_shape(self):
        return None

    def validate_functions(self, selected_functions):
        return True

    def define_functions(self, selected_functions):
        pass