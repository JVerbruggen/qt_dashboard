class Readable:
    def read(self):
        raise NotImplementedError()

    def __enter__(self):
        raise NotImplementedError()

    def __exit__(self):
        raise NotImplementedError()