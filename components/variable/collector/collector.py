class Collector:
    """
    Collects values with a certain strategy.
    Returns the value when collection is done.
    """
    
    def add_to_buffer(self, value) -> int:
        raise NotImplementedError()

    def get_value(self) -> int:
        raise NotImplementedError()