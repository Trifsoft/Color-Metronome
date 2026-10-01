import tinytuya
import threading
import time

if __name__ == "__main__":
    from color_output import ColorOutput
else:
    from color_output.color_output import ColorOutput

class TuyaBulb(ColorOutput):
    def __init__(self, dev_id, address, local_key, version, max_hz=15):
        super().__init__()
        self._bulb = tinytuya.BulbDevice(
            dev_id=dev_id,
            address=address,
            local_key=local_key,
            version=version,
        )
        self._bulb.set_socketPersistent(True)  # keep the connection open instead of reconnecting per call
        self._bulb.detect_bulb()
 
        self._min_interval = 1.0 / max_hz
        self._latest_color = None
        self._lock = threading.Lock()
        self._new_color_event = threading.Event()
        self._stop = threading.Event()
 
        self._worker = threading.Thread(target=self._run, daemon=True)
        self._worker.start()
 
    def set_color(self, color: tuple[int, int, int]):
        # Called from your fast audio loop. Just stashes the latest value —
        # never blocks on the network, never queues up stale colors.
        with self._lock:
            self._latest_color = color
        self._new_color_event.set()
 
    def _run(self):
        last_sent_time = 0.0
        while not self._stop.is_set():
            self._new_color_event.wait()
            self._new_color_event.clear()
 
            with self._lock:
                color = self._latest_color
 
            # Throttle to what the bulb can actually keep up with
            elapsed = time.monotonic() - last_sent_time
            if elapsed < self._min_interval:
                time.sleep(self._min_interval - elapsed)
 
            if color is None:
                continue
 
            r, g, b = color
            try:
                self._bulb.set_colour(r=r, g=g, b=b, nowait=False)
            except Exception as e:
                pass  # drop failed sends rather than blocking the loop; next color will supersede it
            last_sent_time = time.monotonic()
 
    def turn_on(self):
        self._bulb.turn_on(nowait=True)
 
    def close(self):
        self._stop.set()
        self._new_color_event.set()
        self._worker.join(timeout=1)

if __name__ == "__main__":
    from math import cos, pi
    
    def get_mixed_color(color1, color2, first_color_percentage):
        first_color_percentage = max(0.0, min(1.0, first_color_percentage))
        second_color_percentage = 1.0 - first_color_percentage

        return tuple(
            int(color1[i] * first_color_percentage + color2[i] * second_color_percentage)
            for i in range(3)
        )
    bulb = TuyaBulb("bf2508223f64b1521chzxt", "192.168.1.24", "dIIy3N_&gr/&Q-UH", "3.5", max_hz=20)

    def _value(tempo: float, time_value: float) -> float:
        return cos(pi * time_value * tempo / 30) / 2 + 0.5

    while(True):
        bulb.set_color(get_mixed_color((255,0,0), (0,255,0), _value(200, time.time())))
        time.sleep(1/60)