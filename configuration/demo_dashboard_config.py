from components.drawable.bar_display import BarDisplay
from configuration.dashboard_config import DashboardConfig
from components.drawable.gauge import Gauge
from components.drawable.notificationbox import NotificationBox
from components.drawable.svg_indicator import SvgIndicator, SvgBlinker

from components.variable.demo_variables import *
from components.variable.simple_variable import SimpleVariable, SimpleRangeVariable
from components.variable.notification import StaticNotificationList, Notification, SimpleNotification, \
    NotificationStyles, NotificationUpdateEvent
from components.variable.proxy_variable import *
from components.variable.proxy_8bit_variable import *
from components.variable.processed_variable import ProcessedVariable
from components.variable.processor.little_endian_byte_processor import LittleEndianByteProcessor
from components.variable.factory.variable_factory import VariableFactory
from components.drawable.page_selector import PageSelectorFactory

from utils.com_supervisor.com_supervisor import ComSupervisor
from utils.com_supervisor.mapping.simple_mapper import TwoBytesHexToDecMapper, ToIntegerMapper
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

    BAR_OFFX = 500
    BAR_OFFy = 300

    def __init__(self, context: Context, supervisor: ComSupervisor, window: (int, int),
                 incoming_bytes_factory: VariableFactory, environment: {} = {}):
        self.supervisor = supervisor
        self.window = window
        self.context = context
        self.incoming_bytes_factory = incoming_bytes_factory

        self.nue = NotificationUpdateEvent()
        incoming_bytes_factory.set_update_event(self.nue)
        self.notification_variables = incoming_bytes_factory.parse_variables()
        self.notifications = incoming_bytes_factory.get_notifications()

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
            NotificationBox(
                StaticNotificationList(notifications=self.notifications, update_event=self.nue, from_priority_level=1),
                notification_paddingx, notification_paddingy,
                window_width - notification_paddingx * 2, window_height - notification_paddingy * 2,
                notification_height)
        ]

    def __page_main(self, window):
        window_width, window_height = window

        variable_speed = SimpleRangeVariable(0, 0, 240)
        variable_dummy = SimpleRangeVariable(40, 0, 100)
        variable_motorspeed = DemoLoopingVariable(self.context, 0, 0, 60)
        variable_temp = DemoLoopingVariable(self.context, 50, 50, 240)
        variable_bar = DemoLoopingVariable(self.context, 50, 50, 240)

        variable_blinker = IntervalOnOffVariable(self.context, 500)
        variable_temp_bar = DemoLoopingVariable(self.context, 0, 0, 100)

        tempvariable_battery = SimpleRangeVariable(0, 0, 255)
        variable_off = SimpleVariable(0)
        variable_on = SimpleVariable(1)
        variable_onoff_2000 = IntervalOnOffVariable(self.context, 2000)

        for iden, var in self.notification_variables.items():
            self.supervisor.register(iden, var, ByteMapper())

        self.supervisor.register("0x684", variable_speed, ToIntegerMapper(1))

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

            SvgBlinker(Icons.RIGHT_ARROW, variable_on, 150, 350, 100, 20, Colors.ORANGE),
            SvgBlinker(Icons.RIGHT_ARROW, variable_onoff_2000, 150, 550, 100, 20, Colors.RED),

            NotificationBox(StaticNotificationList(notifications=self.notifications, update_event=self.nue,
                                                   from_priority_level=100), window_width - 270, 100, 250, 400, 50),

            BarDisplay(variable_motorspeed, window_width / 2 + self.BAR_OFFX, window_height - self.BAR_OFFy, 100, 200,
                       display_description="MOTOR SPEED", display_unit="rpm")
        ]
