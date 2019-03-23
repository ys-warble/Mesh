from WarbleSimulation.System.Entity.Channel import Channel
from WarbleSimulation.System.Entity.Function import Function


class PowerWire(Channel):
    def __init__(self, _from, _to):
        from WarbleSimulation.System.Entity.Function.Powered import Powered, PowerInput, PowerOutput
        from WarbleSimulation.System.Entity.Concrete import Concrete

        super().__init__()

        from_power_output = None
        if isinstance(_from, PowerOutput):
            from_power_output = _from
        elif isinstance(_from, Powered):
            from_power_output = _from.get_power_output()
        elif isinstance(_from, Concrete) and _from.has_function(Function.POWERED):
            from_power_output = _from.get_function(Function.POWERED).get_power_output()
        else:
            pass

        to_power_input = None
        if isinstance(_to, PowerInput):
            to_power_input = _to
        elif isinstance(_to, Powered):
            to_power_input = _to.get_power_input()
        elif isinstance(_to, Concrete) and _to.has_function(Function.POWERED):
            to_power_input = _to.get_function(Function.POWERED).get_power_input()
        else:
            pass

        if isinstance(from_power_output, PowerOutput) and isinstance(to_power_input, PowerInput):
            self.power_output = from_power_output
            self.power_input = to_power_input

            self.power_output.power_wires.append(self)
            self.power_input.power_wires.append(self)
        else:
            raise TypeError

    def set_power(self, power):
        self.power_input.set_power(power)

    def get_power(self):
        return self.power_output.get_power()
