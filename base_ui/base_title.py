from base_tool.base_ui.base_icon import BaseIcon
from base_tool.base_ui.base_label import BaseLabel
from base_tool.base_ui.base_layout import HBoxLayout
from base_tool.base_ui.base_style import ImgRes, NormalStyle
from base_tool.base_ui.base_widget import BaseWidget
from qtpy.QtCore import Qt
from qtpy.QtGui import QMouseEvent
from qtpy.QtWidgets import QWidget


class BaseTitleBar(BaseWidget):
    def __init__(
        self,
        parent: QWidget,
        title: str,
        icon: str = None,
        sub_title: str = None,
        show_min: bool = False,
        show_setting: bool = False,
        setting_func: callable = None,
    ) -> None:
        self._parent = parent
        self._start_pos = None
        self._title = title
        self._icon = icon
        self._sub_title = sub_title
        self._show_min = show_min
        self._show_setting = show_setting
        self._setting_func = setting_func
        super().__init__()

    def _design(self) -> None:
        main_layout = HBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        content_widget = QWidget()
        inner_layout = HBoxLayout()
        if self._icon:
            icon = BaseIcon(self._icon, (30, 30))
            inner_layout.addWidget(icon)
        self._title_label = BaseLabel(self._title)
        inner_layout.addWidget(self._title_label)
        if self._sub_title:
            sub_title = BaseLabel(self._sub_title, NormalStyle.STRONG_WHITE_LABEL)
            inner_layout.addWidget(sub_title)

        inner_layout.addStretch()

        if self._show_setting:
            self._btn_setting = BaseIcon(ImgRes.SETTING, (30, 40))
            inner_layout.addWidget(self._btn_setting)
        else:
            self._btn_setting = None
        if self._show_min:
            self._btn_min = BaseIcon(ImgRes.MIN, (30, 40))
            inner_layout.addWidget(self._btn_min)
        else:
            self._btn_min = None

        self._btn_close = BaseIcon(ImgRes.CLOSE, (30, 40))
        inner_layout.addWidget(self._btn_close)
        content_widget.setLayout(inner_layout)
        main_layout.addWidget(content_widget)
        self.setLayout(main_layout)

    def _bind_event(self) -> None:
        self._btn_close.clicked.connect(self._parent.close)
        if self._btn_min:
            self._btn_min.clicked.connect(self._on_minsize_window)
        if self._setting_func:
            self._btn_setting.clicked.connect(self._setting_func)

    def _on_minsize_window(self) -> None:
        if self._parent.isMinimized():
            self._parent.showNormal()
        else:
            self._parent.showMinimized()

    def _get_style(self) -> str:
        return NormalStyle.NORMAL_TITLE

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            self._start_pos = event.pos()

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        self._start_pos = None

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if event.buttons() == Qt.LeftButton and self._start_pos:
            self._parent.move(self._parent.pos() + event.pos() - self._start_pos)

    def set_title_name(self, title_name: str) -> None:
        self._title_label.setText(title_name)
