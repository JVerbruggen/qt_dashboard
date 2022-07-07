# from utils.context.context import Context
# from PySide6 import QtCore
# from dataclasses import dataclass, field


# @dataclass
# class HMIQtContext(Context):
#     timers: list[QtCore.QTimer] = field(default_factory=list)

#     def run_timer(self, fn, interval):
#         timer = QtCore.QTimer()
#         timer.timeout.connect(fn)
#         timer.start(interval)

#         self.timers += [timer]