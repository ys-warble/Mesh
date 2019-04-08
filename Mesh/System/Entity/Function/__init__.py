from enum import Enum


class Function(Enum):
    POWERED = 'POWERED'
    TASKED = 'TASKED'

    COMPUTE = 'COMPUTE'

    SENSE = 'SENSE'
    ACTUATE = 'ACTUATE'


class BaseFunction:
    def __init__(self, entity):
        self.entity = entity

    def eval(self):
        raise NotImplementedError

    def init(self):
        raise NotImplementedError

    def terminate(self):
        raise NotImplementedError


class FunctionSetError(Exception):
    pass


class FunctionUnsupportedError(Exception):
    pass
