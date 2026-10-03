from abc import ABC, abstractmethod
from threading import Thread

class SongSocket(ABC):
    _on_play = []
    _on_song_played = []

    def add_on_play_callback(self, callback):
        self._on_play.append(callback)

    def add_on_song_played_callback(self, callback):
        self._on_song_played.append(callback)

    def signal_on_play(self, is_played: bool, delay: float):
        for callback in self._on_play:
            callback(is_played, delay)

    def signal_on_song_played(self, song):
        for callback in self._on_song_played:
            callback(song)
        self.signal_on_play(song["is_playing"], song["current_ms"])

    @abstractmethod
    def _run(self):
        """Defines a subprocess that polls song playback and handles callbacks"""

    def run(self):
        thread = Thread(target=self._run)
        thread.start()