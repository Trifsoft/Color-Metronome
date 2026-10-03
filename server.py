import time
from threading import Thread

from metronome import ColorMetronome
from color_output.window import Window
from color_output.tuya import TuyaBulb
from color_output.combined import CombinedColorOutput
from color_util import get_two_colors
from spotify.spotify import getCurrentSong

from pulse.pulse import get_pulse_from_spotify_id

from song_socket.spotify import SpotifyPollingSocket

default_first = (255, 0, 0)
default_second = (0, 0, 0)

metronome = ColorMetronome()
window = Window()


def start_metronome():
    global window
    if window is not None:
        print("Running metronome")
        metronome.run(window)
        print("Finished")


def update_songs():
    currentTrackId = None
    is_playing = None
    while True:
        track = getCurrentSong()
        if(track and track["id"] != currentTrackId):
            currentTrackId = track["id"]
            is_playing = track["is_playing"]
            if track.get("album") is not None and track["album"].get("images"):
                first, second = get_two_colors(track["album"]["images"][0])
            else:
                first, second = default_first, default_second
            metronome.set_playing(is_playing)
            metronome.set_colors(first=first, second=second)
            metronome.set_delay(track["current_ms"])
            metronome.set_pulse(get_pulse_from_spotify_id(currentTrackId))
            time.sleep(1)
        else:
            if(track and track["is_playing"] != is_playing):
                is_playing = track["is_playing"]
                metronome.set_playing(is_playing)
                metronome.set_delay(track["current_ms"])
            time.sleep(1)

def update_play(is_playing, delay):
    metronome.set_playing(is_playing)
    metronome.set_delay(delay)

def update_song(song):
    if song.get("album") is not None and song["album"].get("images"):
        first, second = get_two_colors(song["album"]["images"][0])
    else:
        first, second = default_first, default_second
    metronome.set_colors(first=first, second=second)
    metronome.set_pulse(get_pulse_from_spotify_id(song["id"]))

if __name__ == "__main__":
    # spotify_thread = Thread(target=update_songs, daemon=True)
    # spotify_thread.start()
    spotify_socket = SpotifyPollingSocket()
    spotify_socket.add_on_play_callback(update_play)
    spotify_socket.add_on_song_played_callback(update_song)
    spotify_socket.run()
    start_metronome()