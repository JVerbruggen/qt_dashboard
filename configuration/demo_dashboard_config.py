from typing import List

from configuration.dashboard_config import DashboardConfig
from components.drawable.gauge import Gauge
from components.drawable.drawable import Drawable
from components.drawable.notificationbox import NotificationBox
from components.drawable.svg_indicator import SvgIndicator, SvgBlinker

from components.variable.demo_variables import *
from components.variable.simple_variable import SimpleVariable, SimpleRangeVariable
from components.variable.notification import StaticNotificationList, Notification, NotificationStyles, NotificationUpdateEvent
from components.variable.proxy_variable import *
from components.variable.proxy_8bit_variable import *
from components.variable.processed_variable import ProcessedVariable
from components.variable.processor.little_endian_processor import LittleEndianProcessor
from components.variable.factory.variable_factory import VariableFactory
from components.drawable.page_selector import PageSelectorFactory

from utils.com_supervisor.com_supervisor import ComSupervisor
from utils.com_supervisor.mapping.simple_mapper import TwoBytesHexToDecMapper
from utils.com_supervisor.mapping.byte_mapper import ByteMapper
from utils.colors import Colors
from utils.context.context import Context
from utils.icons import Icons

class DemoDashboardConfig(DashboardConfig):
    """
    Demo dashboard configuration.
    Provides exact layout of all elements.
    """

    NOTIFICATION_KEY = "notifications"

    PAGE_IDEN_MAIN = "main"
    PAGE_IDEN_MSG = "messages"

    GAUGE_OFFX_INNER = 125
    GAUGE_OFFX_OUTER = 380
    GAUGE_OFFY_TOP = 500
    GAUGE_OFFY_BTM = 700

    BIGGAUGE_OFFX = 200
    BIGGAUGE_OFFY = 200

    SMALL_GAUGE_SIZE = 75
    SMALL_GAUGE_HINTS = 5

    def __init__(self, context: Context, supervisor: ComSupervisor, window: (int, int), notification_variable_factory: VariableFactory, environment: {} = {}):	
        self.supervisor = supervisor
        self.window = window
        self.context = context

        # notification_configuration = {
        #     "0000": ("This is a warning", NotificationStyles.WARNING()),
        #     "0001": ("This is also a warning", NotificationStyles.CRUCIAL()),
        # }
        # self.notification_visibility_variables = {
        #     iden: SimpleVariable(1) for iden, _ in notification_configuration.items()
        # }

        nue = NotificationUpdateEvent()
        # notifications = {iden: Notification(n_msg, n_style, nue, self.notification_visibility_variables[iden]) for iden, (n_msg, n_style) in notification_configuration.items()}
        # notifications = notification_variable_factory.get_variable()
        notifications = {}
        self.environment = {
            self.NOTIFICATION_KEY: StaticNotificationList(notifications=notifications, update_event=nue)
        }

        self.pages = {
            self.PAGE_IDEN_MAIN: self.__page_main(window),
            self.PAGE_IDEN_MSG: self.__page_notifications(window),
        }

        self.page_selector = PageSelectorFactory.from_settings({
            "Main": self.PAGE_IDEN_MAIN,
            "Messages": self.PAGE_IDEN_MSG,
        })
        self.__select_page(self.PAGE_IDEN_MAIN)

    def get_drawables(self):
        return self.pages[self.selected_page_iden] + [self.page_selector]

    def click_event(self, x, y):
        hit_button = self.page_selector.hits(x, y)
        if hit_button is None: return
        self.__select_page(hit_button.iden)

    def __select_page(self, iden: str):
        if iden not in self.pages: return

        self.selected_page_iden = iden
        self.selected_page = self.pages[self.selected_page_iden]
        self.page_selector.set_selected(iden)

    def __page_notifications(self, window):
        window_width, window_height = window
        notification_paddingx = 270
        notification_paddingy = 100
        notification_height = 70

        return [
            NotificationBox(self.environment["notifications"], notification_paddingx, notification_paddingy, 
                window_width - notification_paddingx*2, window_height-notification_paddingy*2, notification_height)
        ]

    def __page_main(self, window):
        window_width, window_height = window

        variable_speed = SimpleRangeVariable(0, 0, 240)
        variable_dummy = SimpleRangeVariable(40, 0, 100)
        variable_motorspeed = DemoLoopingVariable(self.context, 0, 0, 60)
        variable_temp = DemoLoopingVariable(self.context, 50, 50, 240)

        variable_blinker = IntervalOnOffVariable(self.context, 500)

        tempvariable_battery = SimpleRangeVariable(0, 0, 255)
        variable_off = SimpleVariable(0)
        variable_on = SimpleVariable(1)
        variable_onoff_2000 = IntervalOnOffVariable(self.context, 2000)

        proxied_variable = ProcessedVariable(0, LittleEndianProcessor())
        proxy_variable = ProxyVariable({0: proxied_variable})


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

            SvgIndicator(Icons.LEFT_ARROW, proxied_variable, 150, 150, 100, Colors.GREEN),
            SvgBlinker(Icons.RIGHT_ARROW, variable_on, 150, 350, 100, 20, Colors.ORANGE),
            SvgBlinker(Icons.RIGHT_ARROW, variable_onoff_2000, 150, 550, 100, 20, Colors.RED),

            SvgIndicator(Icons.UNKNOWN, proxy_cont_tx_status_stat_config[7], window_width - 100, 300, 50, Colors.GREEN),
            SvgIndicator(Icons.UNKNOWN, proxy_cont_tx_status_stat_config[6], window_width - 100, 350, 50, Colors.GREEN),
            SvgIndicator(Icons.UNKNOWN, proxy_cont_tx_status_stat_config[5], window_width - 100, 400, 50, Colors.GREEN),
            SvgIndicator(Icons.UNKNOWN, proxy_cont_tx_status_stat_config[4], window_width - 100, 450, 50, Colors.GREEN),
            SvgIndicator(Icons.UNKNOWN, proxy_cont_tx_status_stat_config[3], window_width - 100, 500, 50, Colors.GREEN),
            SvgIndicator(Icons.UNKNOWN, proxy_cont_tx_status_stat_config[2], window_width - 100, 550, 50, Colors.GREEN),
            SvgIndicator(Icons.UNKNOWN, proxy_cont_tx_status_stat_config[1], window_width - 100, 600, 50, Colors.GREEN),
            SvgIndicator(Icons.UNKNOWN, proxy_cont_tx_status_stat_config[0], window_width - 100, 650, 50, Colors.GREEN),

            NotificationBox(self.environment[self.NOTIFICATION_KEY], window_width-270, 100, 250, 400, 50)
        ]
