from components.variable.watchable_variable import WatchableRangeVariable, WatchableVariable
from collections.abc import Callable
from dataclasses import dataclass, field


class SimpleRangeVariable(WatchableRangeVariable):
    """
    A simple implementation of the WatchableRangeVariable 
    """

    def __init__(self, default_value=0, lower_val=0, upper_val=100):
        self.value = default_value
        self.lower_val = lower_val
        self.upper_val = upper_val

    def get_value(self):
        return self.value

    def set_value(self, value):
        self.value = value

    def get_lower_value(self):
        return self.lower_val

    def get_upper_value(self):
        return self.upper_val


class SimpleVariable(WatchableVariable):
    """
    A simple implementation of the WatchableVariable 
    """

    def __init__(self, default_value=0, callback: Callable[[], []] = None):
        self.value = default_value
        self.callback = callback

    def get_value(self):
        return self.value

    def set_value(self, value):
        self.value = value
        if self.callback is not None: self.callback()


@dataclass
class WrappedVariable(WatchableVariable):
    """
    A variable that sets all its children.
    Does not support get_value().
    """

    children: list[WatchableVariable] = field(default_factory=list)

    def set_value(self, value):
        [c.set_value(value) for c in self.children]


@dataclass
class MapperVariable(WatchableVariable):
    """
    A variable that maps its underlying child to different values.
    """

    child: WatchableVariable
    offset_from: float
    step: float

    def set_value(self, value):
        self.child.set_value(value)

    def get_value(self):
        val = self.child.get_value() * self.step + self.offset_from
        return val
