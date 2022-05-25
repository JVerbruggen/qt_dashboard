from typing import List

from PySide6 import QtGui

from components.drawable.gauge import Gauge
from components.drawable.drawable import Drawable
from components.variable.demo_variables import *
from components.variable.simple_variable import SimpleVariable
from components.drawable.blinker import SvgIndicator
from utils.comreader.com_reader import ComReader


class DemoGaugeConfig:
    GAUGE_OFFX_INNER = 125
    GAUGE_OFFX_OUTER = 380
    GAUGE_OFFY_TOP = 500
    GAUGE_OFFY_BTM = 700

    BIGGAUGE_OFFX = 200
    BIGGAUGE_OFFY = 200

    SMALL_GAUGE_SIZE = 75
    SMALL_GAUGE_HINTS = 5

    def __init__(self, comreader: ComReader):	
        self.comreader = comreader

    def get_drawables(self, window: (int, int)) -> List[Drawable]:
        (window_width, window_height) = window

        #   variable_speed = DemoLoopingVariable(0, 0, 240, 0.25)
        variable_speed = DemoStaticVariable(0, 0, 240)
        variable_dummy = DemoStaticVariable(40, 0, 100)
        variable_motorspeed = DemoLoopingVariable(0, 0, 60)
        variable_temp = DemoLoopingVariable(50, 50, 240)

        #   variable_can_speed = CanbusVariable(0, 0, 100)

        variable_blinker = IntervalOnOffVariable(500)

        self.comreader.register('0x18', variable_speed)
        self.comreader.start()

        return [
            Gauge(variable_speed, window_width / 2 - self.BIGGAUGE_OFFX, window_height - self.BIGGAUGE_OFFY, 0,
                display_description="SPEED", display_unit="km/h", hint_range=13),
            Gauge(variable_motorspeed, window_width / 2 + self.BIGGAUGE_OFFX, window_height - self.BIGGAUGE_OFFY, 1,
                display_description="MOTOR SPEED", display_unit="rpm"),
            Gauge(variable_temp, window_width / 2 - self.GAUGE_OFFX_INNER, window_height - self.GAUGE_OFFY_TOP, 0,
                display_description="TEMP", size=self.SMALL_GAUGE_SIZE, hint_range=self.SMALL_GAUGE_HINTS),

            # dummy's

            Gauge(variable_dummy, window_width / 2 - self.GAUGE_OFFX_OUTER, window_height - self.GAUGE_OFFY_TOP, 0,
                display_description="dummy", size=self.SMALL_GAUGE_SIZE, hint_range=self.SMALL_GAUGE_HINTS),
            Gauge(variable_dummy, window_width / 2 - self.GAUGE_OFFX_INNER, window_height - self.GAUGE_OFFY_BTM, 0,
                display_description="dummy", size=self.SMALL_GAUGE_SIZE, hint_range=self.SMALL_GAUGE_HINTS),
            Gauge(variable_dummy, window_width / 2 - self.GAUGE_OFFX_OUTER, window_height - self.GAUGE_OFFY_BTM, 0,
                display_description="dummy", size=self.SMALL_GAUGE_SIZE, hint_range=self.SMALL_GAUGE_HINTS),
            Gauge(variable_dummy, window_width / 2 + self.GAUGE_OFFX_OUTER, window_height - self.GAUGE_OFFY_TOP, 0,
                display_description="dummy", size=self.SMALL_GAUGE_SIZE, hint_range=self.SMALL_GAUGE_HINTS),
            Gauge(variable_dummy, window_width / 2 + self.GAUGE_OFFX_OUTER, window_height - self.GAUGE_OFFY_BTM, 0,
                display_description="dummy", size=self.SMALL_GAUGE_SIZE, hint_range=self.SMALL_GAUGE_HINTS),
            Gauge(variable_dummy, window_width / 2 + self.GAUGE_OFFX_INNER, window_height - self.GAUGE_OFFY_TOP, 0,
                display_description="dummy", size=self.SMALL_GAUGE_SIZE, hint_range=self.SMALL_GAUGE_HINTS),
            Gauge(variable_dummy, window_width / 2 + self.GAUGE_OFFX_INNER, window_height - self.GAUGE_OFFY_BTM, 0,
                display_description="dummy", size=self.SMALL_GAUGE_SIZE, hint_range=self.SMALL_GAUGE_HINTS),

            SvgIndicator("assets/left-arrow.svg", variable_blinker, QtGui.QColor.fromRgb(41, 110, 1), 150, 150, 100),
            SvgIndicator("assets/right-arrow.svg", variable_blinker, QtGui.QColor.fromRgb(41, 110, 1), 150, 350, 100),
        ]
