from utils.drawing import *
from dataclasses import dataclass

@dataclass
class PageSelectorButton:
    text: str
    iden: str
    x: int
    y: int
    w: int = 100
    h: int = 100

    def draw(self, painter):
        painter.setPen(default_line_pen())
        draw_box(painter, self.x, self.y, self.w, self.h)
        draw_text_at(painter, self.x+self.w/4, self.y+self.w/4, self.w/2, self.h/2, self.text)
    
    def hits(self, x, y) -> bool:
        return x >= self.x \
            and y >= self.y \
            and x <= self.x+self.w \
            and y <= self.y+self.h

class PageSelector:
    def __init__(self, buttons):
        self.buttons = buttons

    def draw(self, painter):
        for button in self.buttons:
            button.draw(painter)

    def hits(self, x, y) -> PageSelectorButton:
        for button in self.buttons:
            if button.hits(x, y): return button
        return None


class PageSelectorFactory:
    def from_settings(settings: dict[str, str], size=100, item_offset=10, w_offset=10, h_offset=10):
        buttons = []
        for i, (text, iden) in enumerate(settings.items()):
            buttons += [PageSelectorButton(text, iden, w_offset, i*(size+item_offset)+h_offset, w=size, h=size)]
        selector = PageSelector(buttons)
        return selector