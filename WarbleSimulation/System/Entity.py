from abc import ABC


class Entity(ABC):
    identifier = 'entity'

    def __init__(self, UUID):
        self.UUID = UUID
        self.dimension = (None, None, None)

        self.context = None
        self.preference = None
        self.action = None
        self.intent = None
