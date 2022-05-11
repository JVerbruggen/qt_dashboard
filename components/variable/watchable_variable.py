class WatchableVariable:
    def get_value(self):
        raise NotImplementedError()


class WatchableRangeVariable(WatchableVariable):
    def get_value(self):
        pass

    def get_lower_value(self):
        raise NotImplementedError()

    def get_upper_value(self):
        raise NotImplementedError()