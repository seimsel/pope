from numpy import linspace
from channels.demo import DemoChannel
from channels.moving_average import MovingAverageChannel
from scope import Scope

class DemoScope(Scope):
    def __init__(self, address):
        super().__init__(address)

        self.sample_frequency = 10e3
        self.sample_depth = 1000

        self.add_channel(DemoChannel('Demo1', amplitude=1, function='square', frequency=100))
        self.add_channel(DemoChannel('Demo2', amplitude=1, function='sine', frequency=100))
        self.add_channel(MovingAverageChannel('MovingAverage1', source=self.channels[1], n=16))

        for channel in self.channels:
            channel.active = True

