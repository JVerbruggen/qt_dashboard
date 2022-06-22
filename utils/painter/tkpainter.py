from tkinter import Canvas


class TkPainter:
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


    def draw_rounded_line(self, from_x: int, from_y: int, to_x: int, to_y: int, width: int = None):
        """
        Draws a line with rounded corners.
        """
        # self.canvas.create_line(from_x, from_y, to_x, to_y, width=width)
    
    def draw_arc(self, cx: int, cy: int, rad: int, start_deg: int, length_deg: int, width: int = None):
        """
        Draws a part circle.
        """
        coords = cx-rad, cy-rad, 200, 200
        self.canvas.create_arc(coords, start=0, extent=90, width=width)
    
    def draw_box(self, x: int, y: int, w: int, h: int, color: (int,int,int,int)):
        """
        Draws a rounded box.
        """
    
    def draw_box_filled(self, x: int, y: int, w: int, h: int, color: (int,int,int,int), width: int=2):
        """
        Draws a filled rounded box.
        """

    def draw_text_at(self, x: int, y: int, w: int, h: int, color: (int,int,int,int), text: str, font_str: str="TimesMD"):
        """
        Draw text at given position and size.
        """
    
    def draw_svg(self, img, x: int, y: int, w: int, h: int, color: (int,int,int,int)):
        """
        Fill SVG image with a given color.
        Untyped because image is of unknown type.
        """

    def get_image_from(self, img_src: str):
        """
        Opens an image from source.
        """