from WarbleSimulation.System.Entity.Channel import Channel


class PowerWire(Channel):
    def __init__(self, power_output, power_input):
        from WarbleSimulation.System.Entity.Function.Powered import PowerInput, PowerOutput

        super().__init__()

        if (not isinstance(power_input, PowerInput) or power_input is None) or \
                (not isinstance(power_output, PowerOutput) or power_output is None):
            raise TypeError()

        self.power_input = power_input
        self.power_output = power_output

        self.power_input.power_wires.append(self)
        self.power_output.power_wires.append(self)
