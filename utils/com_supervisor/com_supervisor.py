from utils.com_supervisor.mapping.mapper import Mapper
from components.variable.watchable_variable import WatchableVariable

class ComSupervisor():
    """
    Interface
    Supervises external communication to the dashboard variables
    """

    def register(self, identifier: str, variable: WatchableVariable, mapper: Mapper):
        raise NotImplementedError()

    def start(self):
        raise NotImplementedError()