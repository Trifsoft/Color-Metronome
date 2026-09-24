from abc import ABC, abstractmethod
import tkinter as tk

def _to_hex_color(rgb_color: tuple) -> str:
    return "#%02x%02x%02x" % rgb_color

class ColorOutput(ABC):

    @abstractmethod
    def set_color(self, color: tuple):
        """Sets a color based on the provided RGB tuple"""
    @abstractmethod
    def add_loop(self, ms: float, func):
        """Adds a callback function to the queue every ms miliseconds"""

    @abstractmethod
    def run(self):
        """Runs the client"""


class Window(ColorOutput):
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Color Metronome")
        self.root.attributes("-fullscreen", True)
    def set_color(self,color: tuple):
        self.root.configure(bg=_to_hex_color(color))
    def add_loop(self, ms, func):
        self.root.after(ms, func)
    def run(self):
        self.root.mainloop()