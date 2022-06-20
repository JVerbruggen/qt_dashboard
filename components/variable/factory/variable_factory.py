from components.variable.notification import Notification, NotificationUpdateEvent
from components.variable.watchable_variable import WatchableVariable

class VariableFactory:
    """
    Create variables for display of notifications.
    """

    def parse_variables(self) -> dict[str, WatchableVariable]:
        raise NotImplementedError()
    
    def get_notifications(self) -> list[Notification]:
        raise NotImplementedError()

    def set_update_event(self, nue: NotificationUpdateEvent):
        raise NotImplementedError()
    
    def get_variable(self, identifier: str) -> WatchableVariable:
        raise NotImplementedError()