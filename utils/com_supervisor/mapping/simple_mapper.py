from utils.com_supervisor.mapping.mapper import Mapper

class TwoBytesHexToDecMapper(Mapper):
    def map(self, value):
        return int(value.split()[0], 16)