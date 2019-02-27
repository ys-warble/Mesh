from abc import ABC

from WarbleSimulation.System.SpaceFactor import MatterType


class Entity(ABC):
    identifier = 'entity'

    def __init__(self, uuid):
        self.uuid = uuid
        self.dimension = (0, 0, 0)
        self.matter_type = MatterType.ETHER

        self.context = None
        self.preference = None
        self.action = None
        self.intent = None
