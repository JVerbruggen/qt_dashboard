class Mapper:
    """
    Interface for rawvalue-to-variable mapping strategies
    """

    def map(self, value):
        raise NotImplementedError()