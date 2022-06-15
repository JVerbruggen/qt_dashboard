from components.variable.proxy_8bit_variable import Proxy8BitVariable
from components.variable.simple_variable import SimpleVariable
from components.variable.accumulated_variable import AccumulatedVariable
from components.variable.collector.bit_collector import BitCollector
from components.variable.processor.bit_processor import BigEndianBitProcessor

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

def test_var_multiple_case1():
    mul_var = AccumulatedVariable(0, BitCollector(bit_count=2, processor=BigEndianBitProcessor()))
    configuration = { i:var for i,var in enumerate(mul_var if i == 6 or i == 7 else SimpleVariable(0) for i in range(8)) }
    proxy = Proxy8BitVariable(configuration)

    proxy.set_value(b'C0')
    values = [v.get_value() for _,v in configuration.items()]
    assert values == [0,0,0,0,0,0,3,3]

    proxy.set_value(b'80')
    values = [v.get_value() for _,v in configuration.items()]
    assert values == [0,0,0,0,0,0,2,2]
    
def test_var_multiple_case2():
    mul_var = AccumulatedVariable(0, BitCollector(bit_count=2, processor=BigEndianBitProcessor()))
    configuration = { i:var for i,var in enumerate(mul_var if i == 4 or i == 5 else SimpleVariable(0) for i in range(8)) }
    proxy = Proxy8BitVariable(configuration)

    proxy.set_value(b'20')

    values = [v.get_value() for _,v in configuration.items()]
    assert values == [0,0,0,0,2,2,0,0]