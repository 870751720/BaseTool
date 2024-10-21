from functools import partial

from qtpy.QtCore import QEvent, QSize
from qtpy.QtWidgets import QLabel, QMenu

from base_tool.base_ui.base_button import BaseButton
from base_tool.base_ui.base_check import BaseCheck
from base_tool.base_ui.base_label import BaseLabel
from base_tool.base_ui.base_layout import HBoxLayout, VBoxLayout
from base_tool.base_ui.base_line_edit import BaseLineEdit
from base_tool.base_ui.base_scroll import BaseScroll
from base_tool.base_ui.base_style import NormalStyle
from base_tool.base_ui.base_widget import BaseWidget
from base_tool.base_util.util_I18n import _L


class BaseFilter(QMenu):
    def __init__(
        self,
        data: dict = None,
        filter_func: callable = None,
        change_label: QLabel = None,
    ) -> None:
        super().__init__()
        self._data = data
        self._filter_func = filter_func
        self._change_label = change_label
        self._check_widgets = {}
        self._search_text = ""

        self.setStyleSheet(NormalStyle.NORMAL_FILTER)
        self.setFixedSize(QSize(180, 180))
        main_layout = VBoxLayout(True)
        self.setLayout(main_layout)
        op_layout = HBoxLayout(True)
        filter_button = BaseButton(_L.TID_COMMON_SELECT_ALL, size=(30, 22))
        filter_button.clicked.connect(lambda: self._on_check_all(True))
        cancel_button = BaseButton(_L.TID_COMMON_CANCEL, size=(30, 22))
        cancel_button.clicked.connect(lambda: self._on_check_all(False))
        search_line = BaseLineEdit(callback=self._on_search_text_change)
        op_layout.addWidget(filter_button)
        op_layout.addWidget(cancel_button)
        op_layout.addWidget(search_line)
        scroll_area = BaseScroll()
        content_widget = BaseWidget()
        self.content_layout = VBoxLayout(True, parent=content_widget)
        scroll_area.setWidget(content_widget)
        main_layout.addLayout(op_layout)
        main_layout.addWidget(scroll_area)

        self._update_data()

    def _update_data(self) -> None:
        self.content_layout.clear()
        self._check_widgets.clear()
        for filter_text, filter_info in self._data.items():
            if self._search_text and self._search_text not in filter_text:
                continue
            layout = HBoxLayout(True)
            layout.addSpacing(5)
            self._check_widgets[filter_text] = check_widget = BaseCheck(
                partial(self._on_check_click, filter_text),
                default_val=filter_info["is_show"],
            )
            layout.addWidget(check_widget)
            layout.addSpacing(5)
            layout.addWidget(BaseLabel(filter_text))
            self.content_layout.addLayout(layout)

    def mousePressEvent(self, event: QEvent) -> None:
        if self.content_layout.parentWidget().geometry().contains(event.pos()):
            event.accept()
        else:
            super().mousePressEvent(event)

    def _on_check_click(self, filter_text: str, is_check: bool) -> None:
        self._data[filter_text]["is_show"] = is_check
        all_show = True
        for one_filter_info in self._data.values():
            if not one_filter_info["is_show"]:
                all_show = False
                break
        self._change_label.setVisible(not all_show)
        self._filter_func and self._filter_func()

    def _on_check_all(self, is_check: bool) -> None:
        for filter_text, filter_info in self._data.items():
            filter_info["is_show"] = is_check
            self._check_widgets[filter_text].set_checked_without_trigger(is_check)
        self._change_label.setVisible(not is_check)
        self._filter_func and self._filter_func()

    def _on_search_text_change(self, text: str) -> None:
        self._search_text = text
        self._update_data()
