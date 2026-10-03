from abc import ABC, abstractmethod

import requests

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

class Pulse(ABC):

    @abstractmethod
    def evaluate(self, s: float) -> float:
        """Returns an evaluated percentage in a shown color in a given time period for an implemented pulse effect"""

class NoPulse(Pulse):

    def evaluate(self, s):
        return 0

def get_pulse_from_spotify_id(spotify_id) -> Pulse | None:
    from energy.energy import energy_from_spotify_id
    from pulse.energy_pulse import EnergyPulse
    from pulse.tempo_pulse import TempoPulse

    energy = energy_from_spotify_id(spotify_id)
    if energy is None:
        audio_data = get_audio_data(spotify_id)
        if(audio_data and audio_data["tempo"]):
            print("Tempo")
            return TempoPulse(audio_data["tempo"])
        else:
            print("NoPulse")
            return NoPulse()
    else:
        print("Energy")
        return EnergyPulse(energy)