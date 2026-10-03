from metronome import ColorMetronome
from color_output.color_output import ColorOutput

from color_util import get_two_colors

from pulse.pulse import get_pulse_from_spotify_id

from song_socket.socket import SongSocket

default_first = (255, 0, 0)
default_second = (0, 0, 0)

class App():
    def __init__(self, socket: SongSocket, color_output: ColorOutput):
        self._socket = socket
        self._metronome = ColorMetronome()
        self._color_output = color_output

    def _update_play(self, is_playing, delay):
        self._metronome.set_playing(is_playing)
        self._metronome.set_delay(delay)

    def _update_song(self, song):
        if song.get("album") is not None and song["album"].get("images"):
            first, second = get_two_colors(song["album"]["images"][0])
        else:
            first, second = default_first, default_second
        self._metronome.set_colors(first=first, second=second)
        self._metronome.set_pulse(get_pulse_from_spotify_id(song["id"]))

    def start(self):
        self._socket.add_on_play_callback(self._update_play)
        self._socket.add_on_song_played_callback(self._update_song)
        self._socket.run()
        self._metronome.run(self._color_output)


if __name__ == "__main__":  
    from color_output.window import Window
    from song_socket.spotify import SpotifyPollingSocket

    App(SpotifyPollingSocket(), Window()).start()