from WarbleSimulation.System.Entity import Entity


class Basic(Entity):
    def __init__(self, uuid, dimension):
        super().__init__(uuid)
        self.dimension = dimension
