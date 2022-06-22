#!/usr/bin/env python3

"""
ZetCode Tkinter tutorial

The example draws lines on the Canvas.

Author: Jan Bodnar
Website: www.zetcode.com
"""

from tkinter import Tk, Canvas, Frame, BOTH
from utils.painter.tkpainter import TkPainter
from configuration.dashboard_config import DashboardConfig
from configuration.setup.demo_setup import DemoSetup
from configuration.setup.serial_setup import SerialSetup
from configuration.setup.setup import Setup
from utils.context.qt_context import HMIQtContext
import time

WINDOW = (1600, 900)
FPS = 60
INTERVAL = 1/60

class TkFrame(Frame):
    def __init__(self, configuration: DashboardConfig):
        super().__init__()
        self.configuration = configuration

        self.initUI()


    def __draw_loop_iter(self, painter):
        for drawable in self.configuration.get_drawables():
            drawable.draw(painter)


    def start_drawing_loop(self, painter, cb):
        while True:
            self.canvas.delete("all")
            time.sleep(INTERVAL)
            self.__draw_loop_iter(painter)
            cb()

    def initUI(self):
        self.master.title("Lines")
        self.pack(fill=BOTH, expand=1)

        self.canvas = Canvas(self)
        self.painter = TkPainter(self.canvas)

        self.canvas.pack(fill=BOTH, expand=1)


def main():
    setup = DemoSetup()
    context = HMIQtContext()
    configuration = setup.create(context, WINDOW)

    root = Tk()
    ex = TkFrame(configuration)
    root.geometry(f"{WINDOW[0]}x{WINDOW[1]}+10+10")

    cb = lambda: root.update()
    ex.start_drawing_loop(ex.painter, cb)
    root.mainloop()


if __name__ == '__main__':
    main()