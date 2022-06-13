from collections.abc import Callable


class Context:
    """
    Helper functions that rely on the implementation of the context.
    """

    def run_timer(self, fn: Callable[[], None], interval: int):
        """
        Run a timer that executes a function on an interval.
        """
