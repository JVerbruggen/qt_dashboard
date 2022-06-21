from PySide6 import QtCore


def read_file(filename: str) -> QtCore.QByteArray:
    """
    DEPRECATED
    Reads a file using QT and returns the file input as a string
    """
    raise NotImplementedError()
    # f = QtCore.QFile(filename)
    # data = None

    # try:
    #     if f.open(QtCore.QFile.ReadOnly):
    #         data = f.readAll()
    # finally:
    #     f.close()

    # return data
