from utils.context.context import Context
from PySide6 import QtCore

class HMIQtContext(Context):
    def run_timer(self, fn, interval):
        timer = QtCore.QTimer()
        timer.timeout.connect(fn)
        timer.start(interval)
