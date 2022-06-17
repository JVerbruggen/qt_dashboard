from components.variable.watchable_variable import WatchableVariable
from dataclasses import dataclass, field

@dataclass
class OrVariable(WatchableVariable):
    """
    Variable that returns 1 if one or more of the child variables is 1.
    Does not support set_value()
    """
    children: list[WatchableVariable] = field(default_factory=list)

    def get_value(self):
        for child in self.children:
            if child.get_value() == 1: return 1
        return 0