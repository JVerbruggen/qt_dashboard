from components.variable.notification import Notification, NotificationUpdateEvent
from components.variable.watchable_variable import WatchableVariable

class VariableFactory:
    def parse_variables(self) -> dict[str, WatchableVariable]:
        raise NotImplementedError()
    
    def get_notifications(self) -> list[Notification]:
        raise NotImplementedError()

    def set_update_event(self, nue: NotificationUpdateEvent):
        raise NotImplementedError()