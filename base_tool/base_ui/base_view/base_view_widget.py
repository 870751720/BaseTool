from qtpy.QtWidgets import QWidget

from base_tool.base_ui.base_check import BaseCheck
from base_tool.base_ui.base_icon import BaseIcon
from base_tool.base_ui.base_label import BaseLabel
from base_tool.base_ui.base_layout import HBoxLayout
from base_tool.base_ui.base_style import NormalStyle


class BaseViewWidget(QWidget):

    def __init__(
        self,
        data: dict,
        config: dict,
        check_func: callable,
        row: int,
        is_checked: bool = False,
    ) -> None:
        super().__init__()

        main_layout = HBoxLayout(True)
        main_layout.addSpacing(5)
        content_widget = QWidget()
        content_widget.setStyleSheet("border-right:1px solid rgb(15,15,15);")
        inner_layout = HBoxLayout(True)

        is_center_align = config.get("center_align", False)
        if is_center_align:
            inner_layout.addStretch()
        can_check = config.get("can_check", False)
        if can_check:
            self.check_widget = BaseCheck(
                lambda state: check_func(row, state), is_checked
            )
            inner_layout.addWidget(self.check_widget)
            inner_layout.addSpacing(5)
        row_decorate = config.get("row_decorate", None)
        if row_decorate:
            icon_url, text = row_decorate(data)
        else:
            icon_url, text = data.get(config.get("icon_key", None), None), data.get(
                config.get("text_key", None), None
            )

        if icon_url:
            icon = BaseIcon(icon_url, (20, 20))
            inner_layout.addWidget(icon)
        if text:
            title_label = BaseLabel(str(text))
            inner_layout.addWidget(title_label)

        inner_layout.addStretch()
        content_widget.setLayout(inner_layout)
        main_layout.addWidget(content_widget)
        self.setLayout(main_layout)
