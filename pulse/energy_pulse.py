import numpy as np
from pulse.pulse import Pulse

class EnergyPulse(Pulse):
    def __init__(self, energy, frame_rate=30):
        self._energy = energy
        
        # energy[i] sits at time (i+1)/frame_rate seconds -> convert to ms
        self._times_ms = (np.arange(1, len(energy) + 1) / frame_rate)
    def evaluate(self, s):
        """f(x_ms): interpolated, normalized (0-1) energy at time x_ms milliseconds."""
        raw = np.interp(s, self._times_ms, self._energy)
        # print(s, raw)
        return raw / 255.0