from PySide6 import QtCore

def read_file(filename: str) -> QtCore.QByteArray:
    f = QtCore.QFile(filename)
    data = None

    try:
        if f.open(QtCore.QFile.ReadOnly):
            data = f.readAll()
    finally:
        f.close()
    
    return data