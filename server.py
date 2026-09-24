import time
from threading import Thread

import requests

from metronome import ColorMetronome
from color_output import Window
from color_util import get_two_colors
from spotify.spotify import getCurrentSong

default_first = (255, 0, 0)
default_second = (0, 0, 0)

metronome = ColorMetronome()
window = None

def get_audio_data(spotify_id: str):
    """Returns audio data from ReccoBeats."""
    if not spotify_id:
        return None

    url = f"https://api.reccobeats.com/v1/audio-features?ids={spotify_id}"
    response = requests.get(url, timeout=10)
    try:
        response.raise_for_status()
        return response.json()["content"][0]
    except requests.RequestException as exc:
        print(f"Error fetching audio data for {spotify_id}: {exc}")
        return None
    except:
        return None


def start_metronome():
    global window
    if window is not None:
        metronome.run(window)


def update_songs():
    currentTrackId = None
    is_playing = None
    while True:
        track = getCurrentSong()
        if(track and track["id"] != currentTrackId):
            currentTrackId = track["id"]
            is_playing = track["is_playing"]
            audio_data = get_audio_data(track["id"])
            if(audio_data and audio_data["tempo"]):
                if track.get("album") is not None and track["album"].get("images"):
                    first, second = get_two_colors(track["album"]["images"][0])
                else:
                    first, second = default_first, default_second
                print(f"first: {first}, second: {second}, tempo: {audio_data["tempo"]}")
                metronome.set_values(
                    first=first, 
                    second=second,
                    tempo=audio_data["tempo"], 
                    is_playing=is_playing,
                    delay = track["current_ms"]
                )
            else:
                print(f"No data: {track["name"]}")
                metronome.set_values(0, (0,0,0), (0,0,0), track["is_playing"])
            time.sleep(1)
        else:
            if(track and track["is_playing"] != is_playing):
                is_playing = track["is_playing"]
                print(f"Setting playback to {is_playing}")
                metronome.set_playing(is_playing)
                metronome.set_delay(track["current_ms"])
            time.sleep(1)


if __name__ == "__main__":
    window = Window()
    spotify_thread = Thread(target=update_songs, daemon=True)
    spotify_thread.start()
    start_metronome()