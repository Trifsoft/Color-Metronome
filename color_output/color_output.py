from abc import ABC, abstractmethod
import heapq
import itertools
import time

class ColorOutput(ABC):

    def __init__(self):
        self._queue = []  # heap of (run_at, seq, func)
        self._counter = itertools.count()  # tie-breaker for equal timestamps
        self._running = False

    @abstractmethod
    def set_color(self, color: tuple):
        """Sets a color based on the provided RGB tuple"""

    def add_loop(self, ms: float, func):
        """Schedules func to run once, ms milliseconds from now.

        Matches Tkinter's root.after: single-shot, non-blocking, runs on
        the same thread as run(). To repeat, call add_loop again from
        inside func itself.
        """
        run_at = time.monotonic() + ms / 1000.0
        heapq.heappush(self._queue, (run_at, next(self._counter), func))

    def run(self):
        """Event loop: runs due callbacks in order, sleeping until the next is due."""
        self._running = True
        while self._running and self._queue:
            run_at, _, func = self._queue[0]
            now = time.monotonic()
            if run_at <= now:
                heapq.heappop(self._queue)
                func()
            else:
                time.sleep(min(run_at - now, 0.01))

    def stop(self):
        self._running = False