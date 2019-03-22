from enum import Enum

from WarbleSimulation.System.Entity.Channel.PowerWire import PowerWire
from WarbleSimulation.System.Entity.Function import BaseFunction
from WarbleSimulation.util.TypeList import TypeList


class PowerType(Enum):
    ELECTRIC = 101


class Power:
    def __init__(self, power_type):
        self.power_type = power_type


class ElectricPower(Power):
    def __init__(self, voltage):
        super().__init__(PowerType.ELECTRIC)
        self.voltage = voltage


class PowerInput:
    identifier = 'PowerInput'

    def __init__(self, parent, power=ElectricPower(voltage=0)):
        self.parent = parent
        self.power = power
        self.power_wires = TypeList(PowerWire)


class PowerOutput:
    identifier = 'PowerOutput'

    def __init__(self, parent, power=ElectricPower(voltage=0)):
        self.parent = parent
        self.power = power
        self.power_wires = TypeList(PowerWire)


class Powered(BaseFunction):
    def __init__(self, entity):
        super().__init__(entity)
        self.power_inputs = TypeList(PowerInput)
        self.power_outputs = TypeList(PowerOutput)

    def get_power_input(self, index=0):
        if index < len(self.power_inputs):
            return self.power_inputs[index]
        else:
            raise IndexError

    def get_power_output(self, index=0):
        if index < len(self.power_outputs):
            return self.power_outputs[index]
        else:
            raise IndexError
