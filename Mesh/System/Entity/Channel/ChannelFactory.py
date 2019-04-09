from Mesh.System.Entity.Channel.PowerWire import PowerWire


class ChannelFactory:
    channel_lib = {
        PowerWire.identifier: PowerWire
    }

    def get_channel(self, channel, **kwargs):
        if channel not in ChannelFactory.channel_lib:
            raise AttributeError
        else:
            return ChannelFactory.channel_lib[channel](**kwargs)
