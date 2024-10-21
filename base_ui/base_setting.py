from enum import Enum
from functools import partial

from base_tool.base_ui.base_button import BUTTON_STYLE, BaseButton
from base_tool.base_ui.base_check import BaseCheck
from base_tool.base_ui.base_dialog import BaseDialog
from base_tool.base_ui.base_filepick import BaseFilePick
from base_tool.base_ui.base_label import BaseLabel
from base_tool.base_ui.base_layout import HBoxLayout, VBoxLayout
from base_tool.base_ui.base_scroll import BaseScroll
from base_tool.base_ui.base_widget import BaseWidget
from base_tool.base_util.util_enum import SettingType
from base_tool.base_util.util_I18n import _L


class BaseSetting(BaseDialog):

    def __init__(self) -> None:
        super().__init__()
        self._setting_configs = None
        self._update_func = None
        self._setting_change = {}
        self._setting_labels = {}

    def _design(self) -> None:
        scroll_area = BaseScroll()
        content_widget = BaseWidget()
        self._content_layout = VBoxLayout(parent=content_widget)
        scroll_area.setWidget(content_widget)

        self._main_layout.addWidget(scroll_area)

        button_layout = HBoxLayout()
        self._cancel_button = BaseButton(_L.TID_COMMON_CANCEL)
        self._confirm_button = BaseButton(
            _L.TID_COMMON_CONFIRM, style=BUTTON_STYLE.MAIN
        )
        button_layout.addStretch()
        button_layout.addWidget(self._cancel_button)
        button_layout.addWidget(self._confirm_button)

        self._main_layout.addStretch()
        self._main_layout.addLayout(button_layout)
        self._main_layout.addSpacing(20)

    def init_setting(self, setting_configs: dict, update_func: callable) -> None:
        self._setting_configs = setting_configs
        self._update_func = update_func
        for setting_name, setting_config in setting_configs.items():
            layout = HBoxLayout()
            layout.setContentsMargins(0, 0, 0, 0)
            setting_type = setting_config["setting_type"]
            setting_show_name = setting_config["show_name"]
            now_val = setting_config.get("now_val", None)
            if setting_type == SettingType.CHECK:
                self._setting_labels[setting_name] = setting_name_label = BaseLabel(
                    setting_show_name
                )
                layout.addWidget(setting_name_label)
                layout.addStretch()
                setting_check = BaseCheck(
                    partial(self._on_check, setting_name), now_val
                )
                layout.addWidget(setting_check)
            elif setting_type == SettingType.LINK:
                setting_name_label = BaseLabel(
                    setting_show_name, click_func=setting_config["click_func"]
                )
                layout.addStretch()
                layout.addWidget(setting_name_label)
            elif setting_type == SettingType.FILE_PICK:
                self._setting_labels[setting_name] = setting_name_label = BaseLabel(
                    setting_show_name
                )
                layout.addWidget(setting_name_label)
                layout.addStretch()
                setting_file_pick = BaseFilePick(
                    partial(self._on_file_pick, setting_name),
                    now_val,
                    setting_config["change_check"],
                    setting_config["is_dir"],
                )
                layout.addWidget(setting_file_pick)
            else:
                continue
            self._content_layout.addLayout(layout)

    def _on_check(self, setting_name: str, state: bool) -> None:
        setting_name_label = self._setting_labels[setting_name]
        now_val = self._setting_configs[setting_name]["now_val"]
        setting_show_name = self._setting_configs[setting_name]["show_name"]
        if state != now_val:
            setting_name_label.setText("*" + setting_show_name)
            self._setting_change[setting_name] = state
        else:
            setting_name_label.setText(setting_show_name)
            self._setting_change.pop(setting_name, None)

    def _on_file_pick(self, setting_name: str, file_path: str) -> None:
        setting_name_label = self._setting_labels[setting_name]
        now_val = self._setting_configs[setting_name]["now_val"]
        setting_show_name = self._setting_configs[setting_name]["show_name"]
        if file_path != now_val:
            setting_name_label.setText("*" + setting_show_name)
            self._setting_change[setting_name] = file_path
        else:
            setting_name_label.setText(setting_show_name)
            self._setting_change.pop(setting_name, None)

    def _title_name(self) -> str:
        return _L.TID_COMMON_SETTING

    def _get_size(self) -> tuple[int, int]:
        return 480, 380

    def _bind_event(self) -> None:
        self._cancel_button.clicked.connect(self.reject)
        self._confirm_button.clicked.connect(self.accept)

    def reject(self) -> None:
        super().reject()
        self._setting_labels.clear()

    def accept(self) -> None:
        super().accept()
        self._update_func(self._setting_change)
