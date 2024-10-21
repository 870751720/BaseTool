from qtpy.QtCore import Qt
from qtpy.QtGui import QKeyEvent
from qtpy.QtWidgets import QLineEdit

from base_tool.base_ui.base_style import NormalStyle
from base_tool.base_util.util_I18n import _L
from base_tool.base_util.util_qt import debounce


class BaseLineEdit(QLineEdit):

    def __init__(
        self,
        callback: callable = None,
        width: int = 120,
        default_text: str = None,
        place_holder: str = None,
        auto_trigger=True,
    ) -> None:
        super().__init__()
        self.setStyleSheet(NormalStyle.NORMAL_LINE_EDIT)
        self.setFixedWidth(width)
        self.setFixedHeight(22)
        if place_holder is None:
            place_holder = _L.TID_COMMON_SEARCH_PLACEHOLDER
        self.setPlaceholderText(place_holder)
        if default_text:
            self.setText(default_text)
        self.textChanged.connect(self._on_text_change)
        self._callback = callback
        self._auto_trigger = auto_trigger

    def set_callback(self, callback: callable) -> None:
        self._callback = callback

    def _on_text_change(self, text: str) -> None:
        if self._auto_trigger:
            self._on_text_change_with_debounce(text)

    @debounce(3)
    def _on_text_change_with_debounce(self, text: str) -> None:
        self._run_callback(text)

    def _run_callback(self, text: str) -> None:
        self._callback and self._callback(text)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        super().keyPressEvent(event)
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self._run_callback(self.text())
            if self._auto_trigger:
                self._on_text_change_with_debounce.cancel()
