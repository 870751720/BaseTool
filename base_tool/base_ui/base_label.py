from qtpy.QtCore import Qt
from qtpy.QtGui import QMouseEvent
from qtpy.QtWidgets import QLabel, QWidget

from base_tool.base_ui.base_style import NormalStyle


class BaseLabel(QLabel):
    def __init__(
        self,
        txt: str = "",
        style: str = NormalStyle.WHITE_LABEL,
        tooltip: str = None,
        click_func: callable = None,
    ):
        super().__init__()
        self.setText(txt)

        if tooltip is not None:
            self.setToolTip(tooltip)
        if click_func:
            self.setCursor(Qt.PointingHandCursor)
            self.setStyleSheet(
                style
                + " QLabel{text-decoration: underline;} QLabel:hover{color:rgb(64,169,255);} QLabel:pressed{color:rgb(9,109,217);}"
            )
        else:
            self.setStyleSheet(style)
        self._click_func = click_func

    def mousePressEvent(self, event: QMouseEvent) -> None:
        self._click_func and self._click_func()
        super().mousePressEvent(event)
