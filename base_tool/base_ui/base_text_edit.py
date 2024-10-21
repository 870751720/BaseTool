from base_tool.base_ui.base_style import NormalStyle
from qtpy.QtCore import Qt
from qtpy.QtWidgets import QTextEdit


class BaseTextEdit(QTextEdit):
    def __init__(
        self, is_read: bool = False, style: str = NormalStyle.NORMAL_TEXT_EDIT
    ) -> None:
        super().__init__()
        self.setStyleSheet(style)
        self.setReadOnly(is_read)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
