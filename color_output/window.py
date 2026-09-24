from color_output.color_output import ColorOutput
from color_util import to_hex_color
import tkinter as tk

class Window(ColorOutput):
    def __init__(self):
        super().__init__()
        self.root = tk.Tk()
        self.root.title("Color Metronome")
        self.root.attributes("-fullscreen", True)

    def set_color(self, color: tuple):
        self.root.configure(bg=to_hex_color(color))

    def add_loop(self, ms, func):
        self.root.after(ms, func)

    def run(self):
        self.root.mainloop()