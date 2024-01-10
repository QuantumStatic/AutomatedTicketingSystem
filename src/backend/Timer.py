"""Class to handle timers."""
from __future__ import annotations
import time
import math

from threading import Thread

class Timer:
    _timers: dict[int, Timer] = {}

    def __init__(self, seconds: int, precision:float = 0.25):
        self._seconds = seconds
        self._seconds_left: float = seconds
        self._completed:bool = False
        self._running:bool = False
        self._sig_pause:bool = False
        self._precision:float = precision
        # self._timer_thread = Thread(target= (), args=[self._seconds_left])

        self._id:int = self._generate_id()

    def _generate_id(self) -> int:
        """Generate unique id"""
        for x in range(len(Timer._timers)):
            if x not in Timer._timers:
                Timer._timers[x] = self
                return x
        
        return len(Timer._timers)

    @property
    def get_id(self) -> int:
        """Non-overidable access to ID"""
        return self._id

    @classmethod
    def get_timer(cls, timer_id: int) -> Timer:
        """Get timer by ID"""
        return cls._timers[timer_id]

    def reset(self):
        """Reset timer"""
        self._completed = False
        self._running = False
        self._sig_pause = True
        try:
            self._timer_thread.join()
        except (RuntimeError, AttributeError):
            pass
        self._sig_pause = False
        self._seconds_left = self._seconds

    def start(self):
        """Start timer"""
        
        def start_timer(seconds):
            # print("started timer")
            self._running = True
            
            multiplier: int = int(1/self._precision)
            for x in range(math.ceil(seconds)*multiplier):
                time.sleep(self._precision)
                if self._sig_pause:
                    self._sig_pause = False
                    self._seconds_left -= (x/multiplier)
                    break
            else:
                self._completed = True
            
            self._running = False
        
        if not self._running and not self._completed:
            self._timer_thread = Thread(target=start_timer, args=[self._seconds_left])
            self._timer_thread.start()
    
    @property
    def completed(self) -> bool:
        """Check if timer is completed"""
        return self._completed

    @property
    def running(self) -> bool:
        """Check if timer is running"""
        return self._running

    def pause(self):
        """Pause timer"""
        self._sig_pause = True

    def resume(self):
        """Resume timer"""
        self.start()

    @property
    def paused(self) -> bool:
        """Check if timer is paused"""
        return not self._running and not self._completed

    def restart(self):
        """Restart timer"""
        self.reset()
        self.start()

    @classmethod
    def remove_completed_timers(cls):
        """Remove completed timers"""
        for timer in cls._timers.copy():
            if timer.completed:
                del cls._timers[timer]
