from configuration.demo_dashboard_config import DemoDashboardConfig
from utils.com_supervisor.simple_com_supervisor import SimpleComSupervisor
from utils.com_supervisor.readable.mock import Mock
from configuration.setup.setup import Setup
from functools import partial
from components.variable.notification import StaticNotificationList, Notification, NotificationStyles, NotificationUpdateEvent
from utils.context.context import Context
from components.variable.simple_variable import SimpleVariable
from components.variable.factory.json_variable_factory import JsonVariableFactory

class DemoSetup(Setup):
    """
    Demo app setup.
    Works without serial connection.
    """

    def create(self, context: Context, window: (int, int)):
        readable = Mock(interval=0.3, policy={
            # "0x18": Mock.random_first_byte,
            # "0x687": Mock.all_random_bytes,
            # "0x69": partial(Mock.take_from, ["00 00 00 00 00 00 00 00", "01 00 00 00 00 00 00 00"]),
            # "0x684": partial(Mock.increment, 1, ["01" if i==0 else "00" for i in range(8)]),
            # "0x684": partial(Mock.increment_multiple, [1,2], ["01" if i==0 else "00" for i in range(8)]),
            "0x684": partial(Mock.increment, 3, ["03" if i==0 else "00" for i in range(8)]),
        })

        environment={}

        supervisor = SimpleComSupervisor(readable)
        notification_variable_factory = JsonVariableFactory()
        config = DemoDashboardConfig(
            context=context, 
            supervisor=supervisor, 
            window=window, 
            incoming_bytes_factory=notification_variable_factory,
            environment=environment)

        return config
