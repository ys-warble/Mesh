from enum import Enum


class Function(Enum):
    POWERED = 'POWERED'

    COMPUTE = 'COMPUTE'

    SENSE = 'SENSE'
    ACTUATE = 'ACTUATE'


class BaseFunction:
    def __init__(self):
        pass
