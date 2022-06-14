from dataclasses import dataclass, field
import json
from components.variable.watchable_variable import WatchableVariable
from components.variable.factory.variable_factory import VariableFactory
from components.variable.proxy_variable import *
from components.variable.proxy_8bit_variable import *
from components.variable.simple_variable import SimpleVariable, SimpleRangeVariable

@dataclass
class JsonVariableFactory(VariableFactory):
    notification_config: str = "data/notifications.json"
    byte_config: str = "data/input-byte-config.json"
    variable_pool: dict[str, "WatchableVariable"] = field(default_factory=dict)

    def parse_variables(self):
        json_notification_config = self.__get_json_contents(self.notification_config)
        json_byte_config = self.__get_json_contents(self.byte_config)
        variable = self.__parse_json_root(json_byte_config, json_notification_config)
        
        return variable

    def get_notifications(self):
        pass

    def __get_json_contents(self, filename):
        with open(filename, 'r') as f:
            return json.load(f)

    def __parse_json_root(self, json_byte_config, json_notification_config) -> "WatchableVariable":
        iden = json_byte_config["iden"]
        spec = json_byte_config["spec"]
        child = self.__parse_json_child(spec, json_notification_config)
        return child

    def __parse_json_child(self, json_node, json_notification_config):
        child_type = json_node["type"]
        if child_type == "switch-by-state-byte": return self.__parse_json_switchbystatebyte(json_node, json_notification_config)
        elif child_type == "byte-proxy": return self.__parse_json_byteproxy(json_node, json_notification_config)
        elif child_type == "bit-proxy": return self.__parse_json_bitproxy(json_node, json_notification_config)

    def __parse_json_switchbystatebyte(self, json_node, json_notification_config):
        raw_switch_byte_index = json_node["switch-byte-index"]
        raw_states = json_node["states"]
        states = { int(byte_value, 16): self.__parse_json_child(state, json_notification_config) \
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

        if s_type == "simple" or s_type == "multiple": return self.__variable_parse_simple(spec)

        raise ValueError(f"Notification type {s_type} not supported")

    def __variable_parse_simple(self, json_node) -> "WatchableVariable":
        return SimpleVariable()
