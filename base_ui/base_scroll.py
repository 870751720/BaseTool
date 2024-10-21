from base_tool.base_ui.base_style import NormalStyle
from qtpy.QtCore import Qt
from qtpy.QtWidgets import QScrollArea


class BaseScroll(QScrollArea):
    def __init__(self, style: str = NormalStyle.NORMAL_AREA) -> None:
        super().__init__()
        self.setStyleSheet(style)
        self.setWidgetResizable(True)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
