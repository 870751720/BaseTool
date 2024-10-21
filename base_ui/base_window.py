from qtpy.QtCore import Qt
from qtpy.QtWidgets import QApplication, QMainWindow, QWidget

from base_tool.base_ui.base_frameless import BaseFramelessWindow
from base_tool.base_ui.base_layout import VBoxLayout
from base_tool.base_ui.base_style import NormalStyle
from base_tool.base_ui.base_title import BaseTitleBar


class BaseWindow(BaseFramelessWindow, QMainWindow):

    def __init__(self) -> None:
        self._title_height = 40
        QMainWindow.__init__(self)
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
        self.setWindowTitle(self._title_name())

    def _get_size(self) -> tuple[int, int]:
        return None, None

    def _get_style(self) -> str:
        return NormalStyle.NORMAL_WINDOW

    def _design(self) -> None:
        pass

    def _bind_event(self) -> None:
        pass

    def _title_name(self) -> str:
        return "window"

    def _set_title(self) -> None:
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self._main_layout = main_layout = VBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)

        self._title_bar = self._get_title_bar()
        self._title_bar.setFixedHeight(self._title_height)
        main_layout.addWidget(self._title_bar)

        central_widget.setLayout(self._main_layout)

    def _get_title_bar(self) -> BaseTitleBar:
        return BaseTitleBar(self, self._title_name(), setting_func=None)
