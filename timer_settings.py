import time
class Timer_settings(object):
    TIMER_STOP = -1

    def __init__(self, duration):
        self._start_time = self.TIMER_STOP
        self._duration = duration

    # Starts the timer
    def start_timer(self):
        if self._start_time == self.TIMER_STOP:
            self._start_time = time.time()

    # Stops the timer
    def stop_timer(self):
        if self._start_time != self.TIMER_STOP:
            self._start_time = self.TIMER_STOP

    # Determines whether the timer is runnning
    def running_timer(self):
        return self._start_time != self.TIMER_STOP

    # Determines whether the timer timed out
    def timeout_timer(self):
        if not self.running_timer():
            return False
        else:
            return time.time() - self._start_time >= self._duration