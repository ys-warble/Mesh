from WarbleSimulation.System.Entity import Entity
from WarbleSimulation.System.SpaceFactor import MatterType


class Wall(Entity):
    identifier = 'wall'

    def __init__(self, uuid, dimension=(1, 1, 1)):
        super().__init__(uuid)
        self.dimension = dimension
        self.matter_type = MatterType.PERFECT_SOLID
