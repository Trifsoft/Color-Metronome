from color_output.color_output import ColorOutput

class CombinedColorOutput(ColorOutput):
    def __init__(self, color_outputs: list[ColorOutput]):
        super().__init__()
        self._color_outputs = color_outputs

    def set_color(self, color):
        for color_output in self._color_outputs:
            color_output.set_color(color)

    def add_loop(self, ms, func):
        for color_output in self._color_outputs:
            color_output.add_loop(ms, func)

    def run(self):
        for color_output in self._color_outputs:
            color_output.run()
