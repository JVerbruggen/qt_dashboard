from configuration.demo_dashboard_config import DemoDashboardConfig
from utils.com_supervisor.simple_com_supervisor import SimpleComSupervisor
from utils.com_supervisor.readable.mock import Mock
from configuration.setup.setup import Setup
from functools import partial
from components.variable.notification import StaticNotificationList, Notification, NotificationStyles

NOTIFICATION_KEY = "notifications"

class DemoSetup(Setup):
    """
    Demo app setup.
    Works without serial connection.
    """

    def create(self, window):
        readable = Mock(interval=0.3, policy={
            # "0x18": Mock.random_first_byte,
            # "0x687": Mock.all_random_bytes,
            # "0x69": partial(Mock.take_from, ["00 00 00 00 00 00 00 00", "01 00 00 00 00 00 00 00"]),
            "0x420": partial(Mock.increment, 1),
        })

        context={
            NOTIFICATION_KEY: StaticNotificationList(notifications=
            [
                Notification("This is a warning", NotificationStyles.WARNING()),
                Notification("This is also a warning", NotificationStyles.CRUCIAL()),
            ]),
        }

        supervisor = SimpleComSupervisor(readable)
        config = DemoDashboardConfig(supervisor=supervisor, context=context, window=window)

        return config