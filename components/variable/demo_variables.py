from components.variable.watchable_variable import WatchableRangeVariable, WatchableVariable
from utils.context.context import Context


class DemoLoopingVariable(WatchableRangeVariable):
    """
    A range variable that increments on update.
    Used for demonstration purposes.
    """

    def __init__(self, context: Context, default_value=0, lower_val=0, upper_val=100, increment=0.1, ms=10):
        self.value = default_value
        self.lower_val = lower_val
        self.upper_val = upper_val
        self.increment = increment
        context.run_timer(self.update, ms)

    def update(self):
        self.value = ((self.value + self.increment - self.lower_val) % (
                self.upper_val - self.lower_val)) + self.lower_val

    def get_value(self):
        return self.value
    
    def set_value(self, value):
        self.value = value

    def get_lower_value(self):
        return self.lower_val

    def get_upper_value(self):
        return self.upper_val


class DemoStaticVariable(WatchableRangeVariable):
    """
    A range variable that doesn't change unless value is set.
    Used for demonstration purposes.
    """

    def __init__(self, default_value=0, lower_val=0, upper_val=100):
        self.value = default_value
        self.lower_val = lower_val
        self.upper_val = upper_val

    def set_value(self, value):
        self.value = value

    def get_value(self):
        return self.value

    def get_lower_value(self):
        return self.lower_val

    def get_upper_value(self):
        return self.upper_val


class IntervalOnOffVariable(WatchableVariable):
    """
    A variable that changes between on and off on update.
    Used for demonstration purposes.
    """

    def __init__(self, context: Context, interval: int):
        self.interval = interval
        self.value = 1
        context.run_timer(self.update, interval)

    def get_value(self):
        return self.value
    
    def set_value(self, value):
        self.value = value

    def update(self):
        self.value = 1 if self.value == 0 else 0
