from typing import List

from PySide6 import QtGui

from configuration.dashboard_config import DashboardConfig
from components.drawable.gauge import Gauge
from components.drawable.drawable import Drawable
from components.drawable.notificationbox import NotificationBox
from components.drawable.svg_indicator import SvgIndicator, SvgBlinker

from components.variable.demo_variables import *
from components.variable.simple_variable import SimpleVariable, SimpleRangeVariable
from components.variable.notification import NotificationList, Notification, NotificationStyles

from utils.com_supervisor.com_supervisor import ComSupervisor
from utils.com_supervisor.mapping.simple_mapper import TwoBytesHexToDecMapper
from utils.colors import Colors

class DemoDashboardConfig(DashboardConfig):
    """
    Demo dashboard configuration.
    Provides exact layout of all elements.
    """

    GAUGE_OFFX_INNER = 125
    GAUGE_OFFX_OUTER = 380
    GAUGE_OFFY_TOP = 500
    GAUGE_OFFY_BTM = 700

    BIGGAUGE_OFFX = 200
    BIGGAUGE_OFFY = 200

    SMALL_GAUGE_SIZE = 75
    SMALL_GAUGE_HINTS = 5

    def __init__(self, supervisor: ComSupervisor):	
        self.supervisor = supervisor

    def get_drawables(self, window):
        (window_width, window_height) = window

        variable_speed = SimpleRangeVariable(0, 0, 240)
        variable_dummy = SimpleRangeVariable(40, 0, 100)
        variable_motorspeed = DemoLoopingVariable(0, 0, 60)
        variable_temp = DemoLoopingVariable(50, 50, 240)

        variable_blinker = IntervalOnOffVariable(500)

        tempvariable_battery = SimpleRangeVariable(0, 0, 255)
        variable_off = SimpleVariable(0)
        variable_on = SimpleVariable(1)
        variable_onoff_2000 = IntervalOnOffVariable(2000)
        
        notification_list = NotificationList(notifications=
            [
                Notification("This is a warning", NotificationStyles.WARNING()),
                Notification("This is also a warning", NotificationStyles.WARNING()),
            ])

        self.supervisor.register('0x18', variable_speed, TwoBytesHexToDecMapper())
        self.supervisor.register('0x687', tempvariable_battery, TwoBytesHexToDecMapper())     # Battery status
        # self.supervisor.start()

        return [
            Gauge(variable_speed, window_width / 2 - self.BIGGAUGE_OFFX, window_height - self.BIGGAUGE_OFFY, 0,
                display_description="SPEED", display_unit="km/h", hint_range=13),
            Gauge(variable_motorspeed, window_width / 2 + self.BIGGAUGE_OFFX, window_height - self.BIGGAUGE_OFFY, 1,
                display_description="MOTOR SPEED", display_unit="rpm"),
            Gauge(variable_temp, window_width / 2 - self.GAUGE_OFFX_INNER, window_height - self.GAUGE_OFFY_TOP, 0,
                display_description="TEMP", size=self.SMALL_GAUGE_SIZE, hint_range=self.SMALL_GAUGE_HINTS),
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

            SvgIndicator("assets/left-arrow.svg", variable_on, 150, 150, 100, Colors.GREEN),
            SvgBlinker("assets/right-arrow.svg", variable_on, 150, 350, 100, 20, Colors.ORANGE),
            SvgBlinker("assets/right-arrow.svg", variable_onoff_2000, 150, 550, 100, 20, Colors.RED),

            NotificationBox(notification_list, window_width-270, 100, 250, 400, 50)
        ]
