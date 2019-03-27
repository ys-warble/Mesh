from abc import ABC

from Mesh.System.SpaceFactor import MatterType
from Mesh.util import Logger


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

        self.logger = Logger.get_logger(self.__class__.__name__)

    def get_shape(self):
        return None

    def run(self, mp_space_factors, mp_task_pipe):
        pass

    def __str__(self):
        return 'Entity(uuid=.%s)' % str(self.uuid)[-8:]
