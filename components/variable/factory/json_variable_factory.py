from dataclasses import dataclass
import json
from components.variable.watchable_variable import WatchableVariable
from components.variable.factory.variable_factory import VariableFactory

@dataclass
class JsonVariableFactory(VariableFactory):
    notification_config: str = "/data/notifications.json"
    byte_config: str = "/data/input-byte-config.json"

    def get_variable(self):
        json_notification_config = self.__get_json_contents(self.notification_config)
        json_byte_config = self.__get_json_contents(self.byte_config)
        variable = self.__parse_json_root(json_byte_config, json_notification_config)
        
        return variable

    def __get_json_contents(self, filename):
        with open(filename, 'r') as f:
            return json.load(f)

    def __parse_json_root(self, json_byte_config, json_notification_config) -> "WatchableVariable":
        iden = json_byte_config["iden"]
        spec = json_byte_config["spec"]
        child = self.__parse_json_child(json_byte_config, json_notification_config)
        return child

    def __parse_json_child(self, json_byte_node, json_notification_config):
        child_type = json_byte_node["type"]
        if child_type == "switch-by-state-byte": return self.__parse_json_switchbystatebyte(json_byte_node, json_notification_config)
        elif child_type == "byte-proxy": return None
        elif child_type == "bit-proxy": return None

    def __parse_json_switchbystatebyte(self, json_byte_node, json_notification_config):
        switch_byte_index = json_byte_node["switch-byte-index"]
        states = json_byte_node["states"]



        for (byte_value, state) in states.items():
            child = self.__parse_json_child(state, json_notification_config)
            