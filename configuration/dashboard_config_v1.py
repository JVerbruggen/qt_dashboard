from components.drawable.bar_display import BarDisplay
from configuration.dashboard_config import DashboardConfig
from components.drawable.gauge import Gauge
from components.drawable.notificationbox import NotificationBox
from components.drawable.svg_indicator import SvgIndicator, SvgBlinker

from components.variable.demo_variables import *
from components.variable.simple_variable import SimpleVariable, SimpleRangeVariable
from components.variable.proxy_variable import *
from components.variable.proxy_8bit_variable import *
from components.variable.processed_variable import ProcessedVariable
from components.variable.processor.little_endian_processor import LittleEndianProcessor
from components.drawable.page_selector import PageSelectorFactory

from utils.com_supervisor.com_supervisor import ComSupervisor
from utils.com_supervisor.mapping.byte_mapper import ByteMapper
from utils.colors import Colors
from utils.context.context import Context
from utils.icons import Icons


class DashboardConfigV1(DashboardConfig):
    """
    Demo dashboard configuration.
    Provides exact layout of all elements.
    """

    PAGE_IDEN_MAIN = "main"
    PAGE_IDEN_MSG = "messages"

    GAUGE_OFFX_INNER = 125
    GAUGE_OFFX_OUTER = 380
    GAUGE_OFFY_TOP = 400
    GAUGE_OFFY_BTM = 600

    BIGGAUGE_OFFX = 350
    BIGGAUGE_OFFY = 300

    SMALL_GAUGE_SIZE = 75
    SMALL_GAUGE_HINTS = 5

    BAR_OFFX = 130
    BAR_OFFY = 370

    def __init__(self, context: Context, supervisor: ComSupervisor, window: (int, int), environment: {} = {}):
        self.supervisor = supervisor
        self.environment = environment
        self.window = window
        self.context = context

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
                            window_width - notification_paddingx * 2, window_height - notification_paddingy * 2,
                            notification_height)
        ]

    def __page_main(self, window):
        window_width, window_height = window

        variable_speed = SimpleRangeVariable(0, 0, 240)
        variable_dummy = SimpleRangeVariable(40, 0, 100)
        variable_motorspeed = DemoLoopingVariable(self.context, 0, 0, 60)
        variable_temp = DemoLoopingVariable(self.context, 50, 50, 240)

        tempvariable_battery = SimpleRangeVariable(0, 0, 255)
        left_blinker = SimpleVariable(1)
        right_blinker = SimpleVariable(1)

        proxied_variable = ProcessedVariable(0, LittleEndianProcessor())
        proxy_variable = ProxyVariable({0: proxied_variable})

        # notification_list = StaticNotificationList(notifications=
        #     [
        #         Notification("This is a warning", NotificationStyles.WARNING()),
        #         Notification("This is also a warning", NotificationStyles.CRUCIAL()),
        #     ])

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
            SvgBlinker(Icons.LEFT_ARROW, left_blinker, 400, 100, 100, 20, Colors.GREEN),
            SvgBlinker(Icons.RIGHT_ARROW, right_blinker, 1200, 100, 100, 20, Colors.GREEN),

            Gauge(variable_speed, window_width / 2 - self.BIGGAUGE_OFFX, window_height - self.BIGGAUGE_OFFY, 0,
                  display_description="SPEED", display_unit="km/h", hint_range=13),
            Gauge(variable_motorspeed, window_width / 2 + self.BIGGAUGE_OFFX, window_height - self.BIGGAUGE_OFFY, 1,
                  display_description="MOTOR SPEED", display_unit="rpm"),

            # Gauge(variable_temp, window_width / 2 - self.GAUGE_OFFX_INNER, window_height - self.GAUGE_OFFY_TOP, 0,
            #       display_description="TEMP", size=self.SMALL_GAUGE_SIZE, hint_range=self.SMALL_GAUGE_HINTS),
            # Gauge(variable_dummy, window_width / 2 - self.GAUGE_OFFX_OUTER, window_height - self.GAUGE_OFFY_TOP, 0,
            #       display_description="dummy", size=self.SMALL_GAUGE_SIZE, hint_range=self.SMALL_GAUGE_HINTS),

            SvgIndicator(Icons.UNKNOWN, proxy_cont_tx_status_stat_config[7], window_width - 100, 300, 50, Colors.GREEN),
            SvgIndicator(Icons.UNKNOWN, proxy_cont_tx_status_stat_config[6], window_width - 100, 350, 50, Colors.GREEN),
            SvgIndicator(Icons.UNKNOWN, proxy_cont_tx_status_stat_config[5], window_width - 100, 400, 50, Colors.GREEN),
            SvgIndicator(Icons.UNKNOWN, proxy_cont_tx_status_stat_config[4], window_width - 100, 450, 50, Colors.GREEN),
            SvgIndicator(Icons.UNKNOWN, proxy_cont_tx_status_stat_config[3], window_width - 100, 500, 50, Colors.GREEN),
            SvgIndicator(Icons.UNKNOWN, proxy_cont_tx_status_stat_config[2], window_width - 100, 550, 50, Colors.GREEN),
            SvgIndicator(Icons.UNKNOWN, proxy_cont_tx_status_stat_config[1], window_width - 100, 600, 50, Colors.GREEN),
            SvgIndicator(Icons.UNKNOWN, proxy_cont_tx_status_stat_config[0], window_width - 100, 650, 50, Colors.GREEN),

            NotificationBox(self.environment["notifications"], window_width - 270, 100, 250, 400, 50),

            BarDisplay(variable_motorspeed, window_width / 2 - self.BAR_OFFX, window_height - self.BAR_OFFY, 100, 200,
                       display_description="MOTOR SPEED", display_unit="rpm"),

            BarDisplay(variable_temp, window_width / 2 - self.BAR_OFFX + 180, window_height - self.BAR_OFFY, 100, 200,
                       display_description="TEMP", display_unit="°C")
        ]