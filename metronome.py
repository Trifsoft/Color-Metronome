import time
import color_output.color_output as color_output
from color_util import get_mixed_color

from pulse.pulse import Pulse

class ColorMetronome():
    def __init__(self, first: tuple[int,int,int] = (0,0,0), second: tuple[int,int,int] = (0,0,0)):
        from pulse.pulse import NoPulse
        self._playing = True
        self.set_pulse(NoPulse())
        self.set_colors(first, second)
        self.set_delay()
        self.set_playing()

    def _update_ref_time(self):
        self._ref_time = time.time() - self._delay_ms / 1000.0

    def set_delay(self, delay_ms: float = 0):
        self._delay_ms = delay_ms
        self._update_ref_time()

    def is_playing(self):
        return self._playing

    def set_playing(self, playing: bool):
        self._playing = playing
        self._update_ref_time()

    def set_pulse(self, pulse: Pulse):
        self.set_function(pulse.evaluate)

    def set_function(self, function):
        self._function = function

    def set_playing(self, 
                    is_playing: bool | None = None):
        if is_playing is not None:
            self._playing = is_playing

    def set_colors(self, 
                   first: tuple | None = None, 
                   second: tuple | None = None):
        if first is not None:
            self.first = tuple(first)
        if second is not None:
            self.second = tuple(second)

    def run(self, output: color_output.ColorOutput):
        output.set_color(color=(0, 0, 0))

        def update_color():
            if(self.is_playing()):
                current_color = get_mixed_color(self.first, self.second, self._function(time.time() - self._ref_time))
                output.set_color(current_color)
            output.add_loop(16, update_color)

        update_color()
        output.run()