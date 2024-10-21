from qtpy.QtCore import QSize
from qtpy.QtGui import QIcon, QMouseEvent, QPixmap
from qtpy.QtWidgets import QPushButton, QSizePolicy

from base_tool.base_ui.base_style import NormalStyle


class BaseIcon(QPushButton):
    def __init__(self, icon_url: str, size: tuple[int, int] = (12, 12)) -> None:
        super().__init__()
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        self.setSizePolicy(sizePolicy)

        self.setIconSize(QSize(*size))
        self.setStyleSheet(NormalStyle.BUTTON_ICON)
        self.setIcon(QIcon(icon_url))

        self._icon_url = icon_url

    def change_icon(self, icon_url: str):
        self._icon_url = icon_url
        self.setIcon(QIcon(icon_url))

    def get_icon(self) -> str:
        return self._icon_url
