from components.variable.notification import Notification
from components.variable.watchable_variable import WatchableVariable

class VariableFactory:
    def parse_variables(self) -> WatchableVariable:
        raise NotImplementedError()
    
    def get_notifications(self) -> list[Notification]:
        raise NotImplementedError()