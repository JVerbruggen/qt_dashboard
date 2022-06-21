class WatchableVariable:
    """
    Interface
    A variable with a single value
    """

    def get_value(self):
        raise NotImplementedError()

    def set_value(self, value):
        raise NotImplementedError()


class WatchableRangeVariable(WatchableVariable):
    """
    Interface
    A variable that has a value, upper bounds and lower bounds
    """

    def get_value(self):
        raise NotImplementedError()

    def get_lower_value(self):
        raise NotImplementedError()

    def get_upper_value(self):
        raise NotImplementedError()
