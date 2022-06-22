from utils.context.context import Context
from dataclasses import dataclass, field
from tkinter import Tk
from collections.abc import Callable

@dataclass
class TkTimer():
    interval: int
    func: Callable[[], None]
    root: Tk

    def __loop(self):
        self.func()
        self.root.after(ms=self.interval, func=self.__loop)

    def start(self):
        self.__loop()

@dataclass
class TkContext(Context):
    root: Tk
    timers: list[TkTimer] = field(default_factory=list)

    def run_timer(self, fn, interval):
        timer = TkTimer(interval, fn, self.root)
        timer.start()
        self.timers += [timer]