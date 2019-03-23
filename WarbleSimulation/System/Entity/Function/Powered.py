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

    def __eq__(self, other):
        return self.power_type == other.power_type and self.voltage == other.voltage


class PowerInput:
    identifier = 'PowerInput'

    def __init__(self, parent, power=ElectricPower(voltage=0)):
        self.parent = parent
        self.power = power
        self.power_wires = TypeList(PowerWire)

    def set_power(self, power):
        self.power = power

    def get_power(self):
        return self.power_wires[0].get_power()


class PowerOutput:
    identifier = 'PowerOutput'

    def __init__(self, parent, power=ElectricPower(voltage=0)):
        self.parent = parent
        self.power = power
        self.power_wires = TypeList(PowerWire)

    def get_power(self):
        return self.power

    def set_power(self, power):
        self.power = power
        for wire in self.power_wires:
            wire.set_power(self.power)


class Powered(BaseFunction):
    def __init__(self, entity):
        super().__init__(entity)
        self.power_inputs = TypeList(PowerInput)
        self.power_outputs = TypeList(PowerOutput)

        self.input_power_ratings = []
        self.output_power_ratings = []

    def eval(self):
        pass

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
