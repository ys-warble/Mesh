from WarbleSimulation.System import Entity


class Light(Entity):
    identifier = 'light'

    def __init__(self, UUID):
        super().__init__(UUID)
