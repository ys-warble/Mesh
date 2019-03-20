from WarbleSimulation.System.Entity.Basic.Power import PowerInput, PowerOutput
from WarbleSimulation.util.TypeList import TypeList


class PowerManagement:
    def __init__(self):
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
