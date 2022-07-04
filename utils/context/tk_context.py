import threading

from utils.context.context import Context
from dataclasses import dataclass, field
from tkinter import Tk
from collections.abc import Callable


@dataclass
class TkTimer:
    iden: str
    interval: int
    func: Callable[[], None]
    root: Tk
    stop_event: threading.Event = field(default_factory=lambda: threading.Event())

    def __loop(self):
        if self.stop_event.is_set():
            return
        self.func()
        self.root.after(ms=self.interval, func=self.__loop)

    def start(self):
        self.__loop()


@dataclass
class TkContext(Context):
    root: Tk
    timers: list[TkTimer] = field(default_factory=list)
    counter: int = 0

    def run_timer(self, fn, interval):
        timer = TkTimer(f"Timer {self.counter}", interval, fn, self.root)
        timer.start()
        self.timers += [timer]
        self.counter += 1

    def stop_all(self):
        print(f"Stopping all...")
        for timer in self.timers:
            timer.stop_event.set()
            print(f"Stopped {timer.iden}")
