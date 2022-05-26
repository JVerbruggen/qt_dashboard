class ComSupervisor():
    """
    Interface
    Supervises external communication to the dashboard variables
    """

    def register(self, identifier, variable):
        raise NotImplementedError()

    def start(self):
        raise NotImplementedError()