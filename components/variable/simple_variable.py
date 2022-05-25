from components.variable.watchable_variable import WatchableRangeVariable

class SimpleVariable(WatchableRangeVariable):
    def __init__(self, default_value=0, lower_val=0, upper_val=100):
        self.value = default_value
        self.lower_val = lower_val
        self.upper_val = upper_val

    def get_value(self):
        return self.value

    def get_lower_value(self):
        return self.lower_val

    def get_upper_value(self):
        return self.upper_val
