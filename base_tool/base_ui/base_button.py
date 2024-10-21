from base_tool.base_ui.base_style import NormalStyle
from qtpy.QtWidgets import QPushButton


class BUTTON_STYLE(object):
    DEFAULT = NormalStyle.BUTTON_DEFAULT
    MAIN = NormalStyle.BUTTON_MAIN


class BaseButton(QPushButton):
    def __init__(
        self,
        txt: str,
        style: str = BUTTON_STYLE.DEFAULT,
        size: tuple[int, int] = (80, 22),
    ) -> None:
        super().__init__()
        self.setText(txt)
        self.setFixedSize(*size)
        self.setStyleSheet(style)
