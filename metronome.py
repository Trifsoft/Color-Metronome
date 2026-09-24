from math import cos, pi
import time
import color_output.color_output as color_output
from color_util import get_mixed_color

def _value(tempo: float, time_value: float) -> float:
    return cos(pi * time_value * tempo / 30) / 2 + 0.5

class ColorMetronome():
    def __init__(self, tempo: float = 0.0, first: tuple[int,int,int] = (0,0,0), second: tuple[int,int,int] = (0,0,0)):
        self._playing = True
        self.set_values(tempo, first, second)

    def set_delay(self, delay):
        self._delay = delay

    def is_playing(self):
        return self._playing

    def set_playing(self, playing: bool):
        self._playing = playing
            
    def set_values(self, 
                   tempo: float | None = None, 
                   first: tuple | None = None, 
                   second: tuple | None = None, 
                   is_playing: bool | None = None, 
                   delay: float = 0):
        if first is not None:
            self.first = tuple(first)
        if second is not None:
            self.second = tuple(second)
        if tempo is not None:
            self.tempo = max(0.0, float(tempo))
        if is_playing is not None:
            self.set_playing(bool(is_playing))
        self.set_delay(delay)

    def run(self, output: color_output.ColorOutput):
        output.set_color(color=(0, 0, 0))

        def update_color():
            if(self.is_playing()):
                current_color = get_mixed_color(self.first, self.second, _value(self.tempo, time.time() - self._delay))
                output.set_color(current_color)
            output.add_loop(16, update_color)

        update_color()
        output.run()