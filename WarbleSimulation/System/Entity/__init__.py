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

        self.runnable = False

    def get_shape(self):
        return None

    def run(self, mp_space_factors, mp_task_pipe):
        pass

    def handle_task(self, task):
        raise NotImplementedError
