from pulse.pulse import Pulse

from math import cos,pi

class TempoPulse(Pulse):

    def __init__(self, tempo):
        self._tempo = tempo

    def evaluate(self, ms):
        return cos(pi * ms * max(0.0, float(self._tempo)) / 30) / 2 + 0.5