from utils.colors import Colors
from dataclasses import dataclass
from utils.painter.painter import Painter

BUTTON_BORDER_WIDTH = 2


@dataclass
class PageSelectorButton:
    text: str
    iden: str
    x: int
    y: int
    w: int = 100
    h: int = 100

    def draw(self, painter: Painter, selected: bool):
        if selected:
            painter.draw_box_filled(self.x, self.y, self.w, self.h, Colors.BUTTON_SELECTED, BUTTON_BORDER_WIDTH)
        else:
            painter.draw_box_filled(self.x, self.y, self.w, self.h, Colors.BUTTON_UNSELECTED, BUTTON_BORDER_WIDTH)

        painter.draw_text_at(self.x, self.y + int(self.h / 2), self.w, self.h, Colors.DEFAULT_LINE, self.text)

    def hits(self, x, y) -> bool:
        return self.x <= x <= self.x + self.w \
               and self.y <= y <= self.y + self.h


class PageSelector:
    def __init__(self, buttons):
        self.buttons = buttons
        self.selected_iden = None

    def set_selected(self, iden: str):
        self.selected_iden = iden

    def draw(self, painter: Painter):
        for button in self.buttons:
            button.draw(painter, self.selected_iden == button.iden)

    def hits(self, x, y) -> PageSelectorButton:
        for button in self.buttons:
            if button.hits(x, y):
                return button


class PageSelectorFactory:
    @staticmethod
    def from_settings(settings: dict[str, str], size=100, item_offset=10, w_offset=10, h_offset=10):
        buttons = []
        for i, (text, iden) in enumerate(settings.items()):
            buttons += [PageSelectorButton(text, iden, w_offset, i * (size + item_offset) + h_offset, w=size, h=size)]
        selector = PageSelector(buttons)
        return selector
