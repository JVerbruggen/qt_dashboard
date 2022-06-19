from dataclasses import dataclass, field
import json
from collections.abc import Callable
from components.variable.watchable_variable import WatchableVariable
from components.variable.factory.variable_factory import VariableFactory
from components.variable.logic_variables import TwosComplementMapper
from components.variable.proxy_variable import *
from components.variable.proxy_8bit_variable import *
from components.variable.simple_variable import SimpleVariable, SimpleRangeVariable, MapperVariable
from components.variable.accumulated_variable import AccumulatedVariable
from components.variable.collector.bit_collector import BitCollector
from components.variable.processor.bit_processor import BigEndianBitProcessor
from components.variable.notification import Notification, SimpleNotification, NotificationStyles, \
    NotificationUpdateEvent, MultipleNotification, NumberFormatNotification

@dataclass
class JsonVariableFactory(VariableFactory):
    notification_config: str = "data/notifications.json"
    byte_config: str = "data/input-byte-config.json"
    variable_pool: dict[str, "WatchableVariable"] = field(default_factory=dict)
    notifications: dict[str, "Notification"] = field(default_factory=dict)
    nue: NotificationUpdateEvent = None

    def parse_variables(self) -> dict[str, "WatchableVariable"]:
        json_notification_config = self.__get_json_contents(self.notification_config)
        json_byte_config = self.__get_json_contents(self.byte_config)
        variables = self.__parse_json_root(json_byte_config, json_notification_config)
        
        return variables

    def get_notifications(self) -> list["Notification"]:
        return self.notifications

    def set_update_event(self, nue: NotificationUpdateEvent):
        self.nue = nue

    def __get_json_contents(self, filename):
        with open(filename, 'r') as f:
            return json.load(f)

    def __parse_json_root(self, json_byte_config, json_notification_config) -> dict[str, "WatchableVariable"]:
        config = json_byte_config["config"]
        rootdict = {}

        for iden, spec in config.items():
            rootdict[iden] = self.__parse_json_child(spec, json_notification_config)
        
        return rootdict

    def __parse_json_child(self, json_node, json_notification_config):
        child_type = json_node["type"]
        if child_type == "switch-by-state-byte": return self.__parse_json_switchbystatebyte(json_node, json_notification_config)
        elif child_type == "byte-proxy": return self.__parse_json_byteproxy(json_node, json_notification_config)
        elif child_type == "bit-proxy": return self.__parse_json_bitproxy(json_node, json_notification_config)

    def __parse_json_switchbystatebyte(self, json_node, json_notification_config):
        raw_switch_byte_index = json_node["switch-byte-index"]
        raw_states = json_node["states"]
        states = { byte_value.encode(): self.__parse_json_child(state, json_notification_config) \
            for byte_value,state in raw_states.items()}

        return ProxyVariableWithState(int(raw_switch_byte_index), states)
    
    def __parse_json_byteproxy(self, json_node, json_notification_config):
        raw_bytes = json_node["bytes"]
        configuration = { int(i): self.__parse_json_child(var, json_notification_config) \
            for i, var in raw_bytes.items()}            

        return ProxyVariable(configuration)

    def __parse_json_bitproxy(self, json_node, json_notification_config):
        raw_bits = json_node["bits"]
        configuration = {}
        for i, iden in raw_bits.items():
            var = self.__get_variable(iden, json_notification_config)
            configuration[int(i)] = var
            self.variable_pool[iden] = var

        return Proxy8BitVariable(configuration)

    def __get_variable(self, iden: str, json_notification_config) -> "WatchableVariable":
        notifications = json_notification_config["notifications"]
        if iden not in notifications: raise ValueError(f"Notification {iden} not found in notifications.json")
        spec = notifications[iden]
        s_type = spec["type"]
        
        if s_type == "simple":
            var = self.__variable_parse_simple(spec)
            self.notifications[iden] = self.__parse_notification_simple(spec, var)
            return var
        elif s_type == "multiple":
            var = self.__variable_parse_accumulate_bits(spec, iden)
            self.notifications[iden] = self.__parse_notification_multiple(spec, var)
            return var
        elif s_type == "number-unsign":
            var = self.__variable_parse_number_unsigned(spec, iden)
            self.notifications[iden] = self.__parse_notification_numberformat(spec, var)
            return var
        elif s_type == "number-sign-twos":
            var = self.__variable_parse_number_signed_twos(spec, iden)
            self.notifications[iden] = self.__parse_notification_numberformat(spec, var)
            return var

        raise ValueError(f"Notification type {s_type} not supported")

    def __variable_parse_simple(self, json_node) -> "WatchableVariable":
        return SimpleVariable(callback=self.nue.set)

    def __variable_parse_accumulate_bits(self, json_node, iden, size: int=2) -> "WatchableVariable":
        return self.__get_var_from_pool(iden, lambda : 
            AccumulatedVariable(BitCollector(BigEndianBitProcessor(), size), callback=self.nue.set)
        )
    
    def __variable_parse_number_unsigned(self, json_node, iden) -> "WatchableVariable":
        bits = json_node["bits"]
        offset = 0 if "offset" not in json_node else json_node["offset"]
        step = 1 if "step" not in json_node else json_node["step"]

        return self.__get_var_from_pool(iden, lambda : 
            MapperVariable(
                AccumulatedVariable(BitCollector(BigEndianBitProcessor(), bits), callback=self.nue.set), 
                offset, 
                step
            )
        )

    def __variable_parse_number_signed_twos(self, json_node, iden) -> "WatchableVariable":
        bits = json_node["bits"]
        offset = 0 if "offset" not in json_node else json_node["offset"]
        step = 1 if "step" not in json_node else json_node["step"]

        return self.__get_var_from_pool(iden, lambda : 
            MapperVariable(
                TwosComplementMapper(
                    AccumulatedVariable(BitCollector(BigEndianBitProcessor(), bits), callback=self.nue.set), 
                    from_number=2**(bits-1), add=-(2**bits)
                ), 
                offset,
                step
            )
        )

    def __parse_notification_simple(self, json_node, variable: "WatchableVariable") -> "Notification":
        return SimpleNotification(json_node["title"], json_node["message"], NotificationStyles.from_iden(json_node["style"]), 
            self.nue, variable, int(json_node["priority"]))

    def __parse_notification_multiple(self, json_node, variable: "WatchableVariable") -> "Notification":
        return MultipleNotification(json_node["title"], json_node["messages"], NotificationStyles.from_iden(json_node["style"]), 
            self.nue, variable, int(json_node["priority"]))
    
    def __parse_notification_numberformat(self, json_node, variable: "WatchableVariable") -> "Notification":
        step = 1 if "step" not in json_node else json_node["step"]
        step_spl = str(step).split(".")
        decimals = 0
        if len(step_spl) > 1: 
            print(step_spl)
            decimals = step_spl[1]
        
        return NumberFormatNotification(json_node["title"], json_node["message"], NotificationStyles.from_iden(json_node["style"]),
            self.nue, variable, int(json_node["priority"]), decimals=decimals)

    def __get_var_from_pool(self, iden: str, else_new: Callable[[], "WatchableVariable"]) -> "WatchableVariable":
        if iden not in self.variable_pool:
            var = else_new()
            self.variable_pool[iden] = var
            return var
        return self.variable_pool[iden]

