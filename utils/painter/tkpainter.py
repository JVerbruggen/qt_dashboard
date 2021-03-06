from tkinter import *

from utils.colors import Colors
from utils.painter.painter import Painter


def from_rgb(rgba):
    """translates a rgb tuple of int to a tkinter friendly color code
    """
    return "#%02x%02x%02x" % rgba[0:3]


class TkPainter(Painter):
    """
    TK Painter
    """
    DEFAULT_LINE_WIDTH = 2
    DEFAULT_ROUNDED_WIDTH = 7
    DEFAULT_FONT = "TimesMD"
    FONT_SM = "TimesSM"
    FONT_SM_BOLD = "TimesSMBold"

    def __init__(self, canvas: Canvas):
        self.canvas = canvas

    def draw_rounded_line(self, from_x: int, from_y: int, to_x: int, to_y: int, color: (int, int, int, int),
                          width: int = None):
        """
        Draws a line with rounded corners.
        """
        self.canvas.create_line(from_x, from_y, to_x, to_y, width=width, capstyle='round', fill=from_rgb(color))

    def draw_arc(self, cx: int, cy: int, rad: int, start_deg: int, length_deg: int, color: (int, int, int, int),
                 width: int = None):
        """
        Draws a part circle.
        """
        coords = cx - rad, cy - rad, cx + rad, cy + rad
        self.canvas.create_arc(coords, start=start_deg, extent=length_deg, width=width, style='arc',
                               outline=from_rgb(color))

    def draw_box(self, x: int, y: int, w: int, h: int, color: (int, int, int, int)):
        """
        Draws a rounded box.
        """

        x1 = x
        y1 = y
        x2 = x + w
        y2 = y + h
        radius = 5
        points = [x1 + radius, y1,
                  x1 + radius, y1,
                  x2 - radius, y1,
                  x2 - radius, y1,
                  x2, y1,
                  x2, y1 + radius,
                  x2, y1 + radius,
                  x2, y2 - radius,
                  x2, y2 - radius,
                  x2, y2,
                  x2 - radius, y2,
                  x2 - radius, y2,
                  x1 + radius, y2,
                  x1 + radius, y2,
                  x1, y2,
                  x1, y2 - radius,
                  x1, y2 - radius,
                  x1, y1 + radius,
                  x1, y1 + radius,
                  x1, y1]

        self.canvas.create_polygon(points, smooth=True, fill=from_rgb(Colors.BACKGROUND), outline=from_rgb(color))

    def draw_box_filled(self, x: int, y: int, w: int, h: int, color: (int, int, int, int), width: int = 2):
        """
        Draws a filled rounded box.
        """
        self.draw_box(x, y, w, h, color)

    def draw_text_at(self, x: int, y: int, w: int, h: int, color: (int, int, int, int),
                     text: str, font_str: str = "TimesMD"):
        """
        Draw text at given position and size.
        """
        self.canvas.create_text(x + w / 2, y + h / 2, text=text, font="Arial 14 bold", width=w, anchor='center',
                                fill=from_rgb(color))

    def draw_svg(self, img, x: int, y: int, w: int, h: int, color: (int, int, int, int)):
        """
        Fill SVG image with a given color.
        Untyped because image is of unknown type.
        """

    def get_image_from(self, img_src: str):
        """
        Opens an image from source.
        """
