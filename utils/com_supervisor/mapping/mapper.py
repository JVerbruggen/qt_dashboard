from components.variable.watchable_variable import WatchableVariable


class Mapper:
    """
    Interface for rawvalue-to-variable mapping strategies
    """

    def map_to(self, value: bytes, variable: WatchableVariable):
        raise NotImplementedError()
