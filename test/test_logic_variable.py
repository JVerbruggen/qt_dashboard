from components.variable.logic_variables import *
from components.variable.simple_variable import *

def test_or_variable():
    a = SimpleVariable(0)
    b = SimpleVariable(0)
    o = OrVariable([a,b])

    assert o.get_value() == 0
    a.set_value(1)
    assert o.get_value() == 1
    a.set_value(0)
    b.set_value(1)
    assert o.get_value() == 1
    a.set_value(1)
    assert o.get_value() == 1
    a.set_value(0)
    b.set_value(0)
    assert o.get_value() == 0
