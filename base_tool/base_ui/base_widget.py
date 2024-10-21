from base_tool.base_ui.base_style import NormalStyle
from qtpy.QtWidgets import QWidget


class BaseWidget(QWidget):

    def __init__(self) -> None:
        super().__init__()
        self._init_ui()

    def _init_ui(self) -> None:
        self._set_size()
        self._set_style()
        self._design()
        self._bind_event()

    def _set_size(self) -> None:
        width, height = self._get_size()
        if width is not None:
            self.resize(width, height)

    def _set_style(self) -> None:
        style = self._get_style()
        if style is not None:
            self.setStyleSheet(style)

    def _get_size(self) -> tuple[int, int]:
        return None, None

    def _get_style(self) -> str:
        return NormalStyle.NORMAL_WIDGET

    def _design(self) -> None:
        pass

    def _bind_event(self) -> None:
        pass
