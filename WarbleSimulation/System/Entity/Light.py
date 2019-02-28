from WarbleSimulation.System import Entity


class Light(Entity):
    identifier = 'light'

    def __init__(self, uuid):
        super().__init__(uuid)
        self.dimension = (1, 1, 1)
