from components.variable.watchable_variable import WatchableRangeVariable
from PySide6 import QtCore


class DemoLoopingVariable(WatchableRangeVariable):
    def __init__(self, default_value=0, lower_val=0, upper_val=100, increment=0.1, ms=10):
        self.value = default_value
        self.lower_val = lower_val
        self.upper_val = upper_val
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(ms)
        self.increment = increment

    def update(self):
        self.value = ((self.value + self.increment - self.lower_val) % (
                    self.upper_val - self.lower_val)) + self.lower_val

    def get_value(self):
        return self.value

    def get_lower_value(self):
        return self.lower_val

    def get_upper_value(self):
        return self.upper_val


class DemoStaticVariable(WatchableRangeVariable):
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
