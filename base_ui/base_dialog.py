from qtpy.QtCore import Qt
from qtpy.QtWidgets import QApplication, QDialog

from base_tool.base_ui.base_frameless import BaseFramelessWindow
from base_tool.base_ui.base_layout import VBoxLayout
from base_tool.base_ui.base_style import NormalStyle
from base_tool.base_ui.base_title import BaseTitleBar


class BaseDialog(BaseFramelessWindow, QDialog):

    def __init__(self) -> None:
        self._title_height = 30
        QDialog.__init__(self)
        BaseFramelessWindow.__init__(self)
        self._init_ui()

    def _init_ui(self) -> None:
        self._set_size()
        self._set_style()
        self._set_title()
        self._design()
        self._bind_event()

    def _set_size(self) -> None:
        cursor_pos = self.cursor().pos()
        screen = QApplication.screenAt(cursor_pos)
        if screen:
            screen_rect = screen.geometry()
            width, height = self._get_size()
            if width is not None and height is not None:
                x = screen_rect.x() + (screen_rect.width() - width) // 2
                y = screen_rect.y() + (screen_rect.height() - height) // 2
                self.setGeometry(x, y, width, height)

    def _set_style(self) -> None:
        style = self._get_style()
        if style is not None:
            self.setStyleSheet(style)

    def _get_size(self) -> tuple[int, int]:
        return None, None

    def _get_style(self) -> str:
        return NormalStyle.NORMAL_DIALOG

    def _design(self) -> None:
        pass

    def _bind_event(self) -> None:
        pass

    def _title_name(self) -> str:
        return "dialog"

    def _set_title(self) -> None:
        self._title_bar = title_bar = self._get_title_bar()
        title_bar.setFixedHeight(self._title_height)

        self._main_layout = main_layout = VBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(title_bar)
        self.setLayout(main_layout)

    def _get_title_bar(self) -> BaseTitleBar:
        return BaseTitleBar(self, self._title_name())

    def set_title_name(self, title_name: str) -> None:
        self._title_bar.set_title_name(title_name)
