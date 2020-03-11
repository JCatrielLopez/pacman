import multiprocessing
import threading
import time
from threading import Timer as ThreadTimer


class ClockTimer(multiprocessing.Process):
    def __init__(self, interval=10, target_function=None, name=None):
        super().__init__(name=name, group=None)
        self.paused = False
        self.pause_cond = threading.Condition(threading.RLock())
        self.interval = interval
        self.timeout = self.interval
        self.target_function = target_function
        self.last_tick = None
        self.alive = True

    def run(self):
        self.last_tick = time.perf_counter()

        while self.alive:
            with self.pause_cond:
                while self.paused:
                    self.pause_cond.wait()

                t = time.perf_counter()
                if not self.paused:
                    if int(t - self.last_tick) >= self.timeout:
                        print(f"\n{self.name} -> {time.ctime()}")
                        self.target_function()
                        self.last_tick = t
                        self.timeout = int(self.interval)

    def pause(self, update_timeout=True):
        self.paused = True

        if update_timeout:
            self.timeout = int(time.perf_counter() - self.last_tick)

        self.pause_cond.acquire()

    def resume(self):
        try:
            self.paused = False
            self.last_tick = time.perf_counter()
            self.pause_cond.notify()
            self.pause_cond.release()
        except RuntimeError:
            pass

    def set_interval(self, interval):
        self.interval = interval

    def cancel(self):
        self.alive = False


# class ClockTimer(threading.Thread):
#     def __init__(self, interval=10, target=None, name=None):
#         threading.Thread.__init__(self, name=name)
#         self.paused = False
#         self.pause_cond = threading.Condition(threading.RLock())
#         self.interval = interval
#         self.timeout = self.interval
#         self.target = target
#         self.last_tick = None
#         self.alive = True
#
#     def run(self):
#         self.last_tick = time.perf_counter()
#
#         while self.alive:
#             with self.pause_cond:
#                 while self.paused:
#                     self.pause_cond.wait()
#
#                 t = time.perf_counter()
#                 if not self.paused:
#                     if int(t - self.last_tick) >= self.timeout:
#                         print(f"\n{self.name} -> {time.ctime()}")
#                         self.target()
#                         self.last_tick = t
#                         self.timeout = int(self.interval)
#
#     def pause(self, update_timeout=True):
#         self.paused = True
#
#         if update_timeout:
#             self.timeout = int(time.perf_counter() - self.last_tick)
#
#         self.pause_cond.acquire()
#
#     def resume(self):
#         try:
#             self.paused = False
#             self.last_tick = time.perf_counter()
#             self.pause_cond.notify()
#             self.pause_cond.release()
#         except RuntimeError:
#             pass
#
#     def set_interval(self, interval):
#         self.interval = interval
#
#     def cancel(self):
#         self.alive = False


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


if __name__ == '__main__':
    def msg():
        print(f"\nHola desde {time.ctime()}")


    timer = ClockTimer(interval=10, target=msg)

    print(f"Comienza en [{time.ctime()}]. Dormimos 15 segundos.")
    timer.start()
    time.sleep(15)
    print(f"\nPausamos en [{time.ctime()}]")
    timer.pause()
    print(f"\nTimeout en {timer.timeout}s. Dormimos por 15:")
    time.sleep(15)
    print(f"\nResumimos en [{time.ctime()}]")
    timer.resume()
