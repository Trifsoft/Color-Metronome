import argparse
from math import cos, pi
import time
import tkinter as tk
import color_output

def _value(tempo: float, time_value: float) -> float:
    return cos(pi * time_value * tempo / 30) / 2 + 0.5

def _get_mixed_color(color1, color2, first_color_percentage):
    first_color_percentage = max(0.0, min(1.0, first_color_percentage))
    second_color_percentage = 1.0 - first_color_percentage

    return tuple(
        int(color1[i] * first_color_percentage + color2[i] * second_color_percentage)
        for i in range(3)
    )

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
                current_color = _get_mixed_color(self.first, self.second, _value(self.tempo, time.time() - self._delay))
                output.set_color(current_color)
            output.add_loop(16, update_color)

        update_color()
        output.run()