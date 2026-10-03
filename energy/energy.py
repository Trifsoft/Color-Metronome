from glob import glob
import numpy as np

energy_database = {}
songs = None

def _read_energy_file(in_path):
    """Read back an energy file written by write_energy_file()."""
    with open(in_path, "rb") as f:
        frame_rate = np.frombuffer(f.read(8), dtype=np.float64)[0]
        energy = np.frombuffer(f.read(), dtype=np.uint8)
    return energy, frame_rate

def energy_from_spotify_id(spotify_id):
    global energy_database
    if spotify_id in energy_database:
        return energy_database[spotify_id]
    else:
        global songs
        if songs is None:
            songs = glob("energy/*.energy")
        if(f"energy/{spotify_id}.energy" in songs):
            energy, _ = _read_energy_file(f"energy/{spotify_id}.energy")
            energy_database[spotify_id[:-7]] = energy
            return energy
        else:
            return None

if __name__ == "__main__":
    print(energy_from_spotify_id("asdfafsa"))
    print(energy_from_spotify_id("7EiZI6JVHllARrX9PUvAdX"))