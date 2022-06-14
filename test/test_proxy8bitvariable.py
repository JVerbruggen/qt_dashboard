from components.variable.proxy_8bit_variable import Proxy8BitVariable
from components.variable.simple_variable import SimpleVariable

def test_var_case1():
    configuration = { i:var for i,var in enumerate(SimpleVariable(0) for _ in range(8)) }
    proxy = Proxy8BitVariable(configuration)

    proxy.set_value(b'01')

    for (i,var) in configuration.items():
        val = configuration[i].get_value()
        if i == 0: assert val == 1
        else: assert val == 0

def test_var_case2():
    configuration = { i:var for i,var in enumerate(SimpleVariable(0) for _ in range(8)) }
    proxy = Proxy8BitVariable(configuration)

    proxy.set_value(b'09')

    for (i,var) in configuration.items():
        val = configuration[i].get_value()
        if i == 0: assert val == 1
        elif i == 3: assert val == 1
        else: assert val == 0