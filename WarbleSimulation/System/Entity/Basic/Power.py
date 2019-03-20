from enum import Enum

from WarbleSimulation.System.Entity.Channel.PowerWire import PowerWire
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

    def __init__(self, parent):
        self.parent = parent
        self.power = ElectricPower(voltage=0)
        self.power_wires = TypeList(PowerWire)


class PowerOutput:
    identifier = 'PowerOutput'

    def __init__(self, parent):
        self.parent = parent
        self.power = ElectricPower(voltage=0)
        self.power_wires = TypeList(PowerWire)
