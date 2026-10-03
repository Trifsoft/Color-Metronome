from song_socket.socket import SongSocket
from spotify.spotify import getCurrentSong
import time

class SpotifyPollingSocket(SongSocket):

    def _run(self):
        currentTrackId = None
        is_playing = None
        while True:
            track = getCurrentSong()
            if(track and track["id"] != currentTrackId):
                currentTrackId = track["id"]
                is_playing = track["is_playing"]
                self.signal_on_song_played(track)
            else:
                if(track and track["is_playing"] != is_playing):
                    is_playing = track["is_playing"]
                    self.signal_on_play(is_playing, track["current_ms"])
            time.sleep(1)