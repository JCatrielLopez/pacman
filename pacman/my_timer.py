from threading import Timer as ThreadTimer
from time import time


class MyTimer:
    timer: ThreadTimer = None
    end_time = None
    func = None
    timeout = None
    on_pause: bool = None

    def __init__(self, timeout, func):
        self.timeout = timeout
        self.func = func
        self.startTime = time()
        self.timer = ThreadTimer(timeout, func)
        self.on_pause = False

    def start(self):
        self.timer.start()

    def pause(self):
        if not self.on_pause:
            self.timer.cancel()
            self.end_time = time()
            self.on_pause = True

    def resume(self):
        if self.on_pause:
            self.timer = ThreadTimer(
                self.timeout - (self.end_time - self.startTime), self.func
            )
            self.timer.start()

    def is_on_pause(self):
        return self.on_pause

    def is_alive(self):
        return self.timer.is_alive()

    def cancel(self):
        self.timer.cancel()

    def set_timeout(self, timeout):
        self.timeout = timeout
