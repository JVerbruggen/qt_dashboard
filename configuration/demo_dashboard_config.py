from typing import List

from PySide6 import QtGui

from components.drawable.bar_display import BarDisplay
from configuration.dashboard_config import DashboardConfig
from components.drawable.gauge import Gauge
from components.drawable.drawable import Drawable
from components.drawable.notificationbox import NotificationBox
from components.drawable.svg_indicator import SvgIndicator, SvgBlinker

from components.variable.demo_variables import *
from components.variable.simple_variable import SimpleVariable, SimpleRangeVariable
from components.variable.notification import StaticNotificationList, Notification, NotificationStyles
from components.variable.proxy_variable import *
from components.variable.proxy_8bit_variable import *
from components.variable.processed_variable import ProcessedVariable

from components.variable.processor.little_endian_processor import LittleEndianProcessor

from utils.com_supervisor.com_supervisor import ComSupervisor
from utils.com_supervisor.mapping.simple_mapper import TwoBytesHexToDecMapper
from utils.com_supervisor.mapping.byte_mapper import ByteMapper
from utils.colors import Colors
from utils.icons import Icons

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

    BAR_OFFX = 500
    BAR_OFFy = 300

    def __init__(self, supervisor: ComSupervisor):	
        self.supervisor = supervisor

    def get_drawables(self, window):
        (window_width, window_height) = window

        variable_speed = SimpleRangeVariable(0, 0, 240)
        variable_dummy = SimpleRangeVariable(40, 0, 100)
        variable_motorspeed = DemoLoopingVariable(0, 0, 60)
        variable_temp = DemoLoopingVariable(50, 50, 240)
        variable_bar = DemoLoopingVariable(50, 50, 240)

        variable_temp_bar = DemoLoopingVariable(0, 0, 100)

        variable_blinker = IntervalOnOffVariable(500)

        tempvariable_battery = SimpleRangeVariable(0, 0, 255)
        variable_off = SimpleVariable(0)
        variable_on = SimpleVariable(1)
        variable_onoff_2000 = IntervalOnOffVariable(2000)

        proxied_variable = ProcessedVariable(0, LittleEndianProcessor())
        proxy_variable = ProxyVariable({0: proxied_variable})
        
        notification_list = StaticNotificationList(notifications=
            [
                Notification("This is a warning", NotificationStyles.WARNING()),
                Notification("This is also a warning", NotificationStyles.CRUCIAL()),
            ])

        proxy_cont_tx_status_stat_config = {i: SimpleVariable(0) for i in range(8)}
        proxy_cont_tx_status_stat = Proxy8BitVariable(proxy_cont_tx_status_stat_config)

        proxy = ProxyVariableWithState(state_byte_index=0, states={
            b'00': ProxyVariable({
                0: None,
                1: proxy_cont_tx_status_stat,
                2: None,
                3: None,
                4: None,
                5: None,
                6: None,
                7: None,
            }),
        })

        # self.supervisor.register('0x18', variable_speed, TwoBytesHexToDecMapper())
        # self.supervisor.register('0x687', tempvariable_battery, TwoBytesHexToDecMapper())     # Battery status
        # self.supervisor.register('0x69', proxy_variable, ByteMapper())
        self.supervisor.register('0x420', proxy, ByteMapper())
        self.supervisor.start()

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

            SvgIndicator(Icons.LEFT_ARROW, proxied_variable, 150, 150, 100, Colors.GREEN),
            SvgBlinker(Icons.RIGHT_ARROW, variable_on, 150, 350, 100, 20, Colors.GREEN),
            SvgBlinker(Icons.RIGHT_ARROW, variable_onoff_2000, 150, 550, 100, 20, Colors.GREEN),

            SvgIndicator(Icons.UNKNOWN, proxy_cont_tx_status_stat_config[7], window_width - 100, 300, 50, Colors.GREEN),
            SvgIndicator(Icons.UNKNOWN, proxy_cont_tx_status_stat_config[6], window_width - 100, 350, 50, Colors.GREEN),
            SvgIndicator(Icons.UNKNOWN, proxy_cont_tx_status_stat_config[5], window_width - 100, 400, 50, Colors.GREEN),
            SvgIndicator(Icons.UNKNOWN, proxy_cont_tx_status_stat_config[4], window_width - 100, 450, 50, Colors.GREEN),
            SvgIndicator(Icons.UNKNOWN, proxy_cont_tx_status_stat_config[3], window_width - 100, 500, 50, Colors.GREEN),
            SvgIndicator(Icons.UNKNOWN, proxy_cont_tx_status_stat_config[2], window_width - 100, 550, 50, Colors.GREEN),
            SvgIndicator(Icons.UNKNOWN, proxy_cont_tx_status_stat_config[1], window_width - 100, 600, 50, Colors.GREEN),
            SvgIndicator(Icons.UNKNOWN, proxy_cont_tx_status_stat_config[0], window_width - 100, 650, 50, Colors.GREEN),

            NotificationBox(notification_list, window_width-270, 100, 250, 400, 50),

            BarDisplay(variable_motorspeed, window_width / 2 + self.BAR_OFFX, window_height - self.BAR_OFFy, 100, 200, display_description="MOTOR SPEED", display_unit="rpm")
        ]
