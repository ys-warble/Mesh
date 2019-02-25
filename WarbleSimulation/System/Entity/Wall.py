from WarbleSimulation.System import Entity


class Wall(Entity):
    identifier = 'wall'

    def __init__(self, UUID):
        super().__init__(UUID)
