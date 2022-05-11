import math


def point_at_angle(cx: int, cy: int, angle: float, length: int) -> (int, int):
    return math.cos(angle) * length + cx, -math.sin(angle) * length + cy
