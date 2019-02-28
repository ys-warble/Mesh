from WarbleSimulation.System.Entity.Concrete import Concrete
from WarbleSimulation.System.SpaceFactor import MatterType


class Wall(Concrete):
    identifier = 'wall'
    default_dimension = (1, 1, 1)

    def __init__(self, uuid, dimension_x=(1, 1, 1)):
        super().__init__(uuid=uuid, dimension_x=dimension_x, matter_type=MatterType.CONCRETE)
        self.dimension = tuple(
            [Wall.default_dimension[i] * self.dimension_x[i] for i in range(len(Wall.default_dimension))])
