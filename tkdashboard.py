#!/usr/bin/env python3
import tkinter
from tkinter import Tk, Canvas, Frame, BOTH
from utils.painter.tkpainter import TkPainter
from configuration.dashboard_config import DashboardConfig
from configuration.setup.demo_setup import DemoSetup
from utils.context.tk_context import TkContext
from functools import partial

WINDOW = (1600, 900)
FPS = 60
INTERVAL = int(1000 / FPS)


class TkFrame(Frame):
    def __init__(self, root: Tk, configuration: DashboardConfig):
        super().__init__()
        self.painter = None
        self.canvas = None
        self.configuration = configuration
        self.root = root

        self.init_ui()

    def __draw_loop_iter(self, painter, cb):
        self.canvas.delete("all")
        for drawable in self.configuration.get_drawables():
            drawable.draw(painter)

        cb()
        self.root.after(INTERVAL, partial(self.__draw_loop_iter, painter, cb))

    def start_drawing_loop(self, painter, cb):
        self.__draw_loop_iter(painter, cb)

    def init_ui(self):
        self.master.title("Dashboard")
        self.pack(fill=BOTH, expand=1)

        self.canvas = Canvas(self, highlightthickness=0)
        self.painter = TkPainter(self.canvas)

        self.canvas.pack(fill=BOTH, expand=1)
        self.canvas.configure(bg="#444257", borderwidth=0)

    def button_press(self, event: tkinter.Event):
        self.configuration.click_event(event.x, event.y)

def main():
    root = Tk(className="Dashboard", screenName="DB")

    setup = DemoSetup()
    context = TkContext(root=root)
    configuration = setup.create(context, WINDOW)

    ex = TkFrame(root, configuration)
    root.geometry(f"{WINDOW[0]}x{WINDOW[1]}+10+10")

    root.bind("<Button>", ex.button_press)

    cb = lambda: root.update()
    ex.start_drawing_loop(ex.painter, cb)
    root.mainloop()

    context.stop_all()


if __name__ == '__main__':
    main()
