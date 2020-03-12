import threading
import time
from threading import Timer as ThreadTimer


class ClockTimer(threading.Thread):
    def __init__(self, interval=10, target_function=None, name=None):
        threading.Thread.__init__(self, name=name)
        self.paused = False
        self.lock = threading.Condition(threading.Lock())
        self.interval = interval
        self.timeout = self.interval
        self.target = target_function
        self.last_tick = None
        self.alive = True

    def run(self):
        self.last_tick = time.perf_counter()

        while self.alive:
            with self.lock:
                while self.paused:
                    self.lock.wait()

                t = time.perf_counter()
                if not self.paused:
                    if int(t - self.last_tick) >= self.timeout:
                        print(f"\n{self.name} -> {time.ctime()}")
                        self.target()
                        self.last_tick = t
                        self.timeout = int(self.interval)
                time.sleep(1)

    def pause(self, update_timeout=True):
        if not self.paused:
            self.paused = True
            print(f"\n{self.name} -> pausado")

            if update_timeout:
                self.timeout = int(time.perf_counter() - self.last_tick)
                print(f" new timeout: {self.timeout}")

            self.lock.acquire()


    def remaining_time(self):
        return int(time.perf_counter() - self.last_tick)

    def set_timeout(self, timeout):
        self.timeout = timeout


    def resume(self):
        try:
            self.paused = False
            self.last_tick = time.perf_counter()
            self.lock.notify()
            self.lock.release()
        except RuntimeError as e:
            print(e)

    def set_interval(self, interval):
        self.interval = interval

    def cancel(self):
        print("Cancel: ", self.name)
        self.alive = False


    def is_alive(self):
        return self.alive


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
        print(f"\n timer1: Hola desde {time.ctime()}")

    def msg1():
        print(f"\n timer2: chau {time.ctime()}")

    timer = ClockTimer(interval=10, target_function=msg)

    # print(f"Comienza en [{time.ctime()}]. Dormimos 3 segundos.")
    # timer.start()
    # time.sleep(3)
    # print(f"\nPausamos en [{time.ctime()}]")
    # timer.pause()
    # print(f"\nTimeout en {timer.timeout}s. Dormimos por 3:")
    # time.sleep(3)
    # print(f"\nResumimos en [{time.ctime()}]")
    # timer.resume()

    print(f"Comienza en [{time.ctime()}]. Dormimos 15 segundos.")
    timer.start()
    time.sleep(15)

    timer2 = ClockTimer(interval=10, target_function=msg1)

    print(f"pausa en [{time.ctime()}]")
    timer.pause()
    timer2.start()

    time.sleep(10)
    timer2.cancel()
    timer.resume()

    time.sleep(30)

