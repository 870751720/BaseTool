from base_tool.base_ui.base_button import BUTTON_STYLE, BaseButton
from base_tool.base_ui.base_dialog import BaseDialog
from base_tool.base_ui.base_layout import HBoxLayout, VBoxLayout
from base_tool.base_ui.base_text_edit import BaseTextEdit
from base_tool.base_util.util_I18n import _L
from base_tool.base_util.util_qt import calculate_text_size
from qtpy.QtWidgets import QDialog


class BaseMessageBox(BaseDialog):

    @property
    def _max_msg_width(self) -> int:
        return 1000

    @property
    def _max_msg_height(self) -> int:
        return 650

    def _design(self) -> None:
        vbox_layout = VBoxLayout()
        self._msg_text_edit = msg_text_edit = BaseTextEdit()
        msg_text_edit.setMaximumHeight(self._max_msg_height)
        msg_text_edit.setReadOnly(True)
        vbox_layout.addWidget(msg_text_edit)

        hbox_layout = HBoxLayout()

        self._cancel_button = BaseButton(_L.TID_COMMON_CANCEL)
        self._confirm_button = BaseButton(_L.TID_COMMON_CONFIRM, BUTTON_STYLE.MAIN)
        hbox_layout.addStretch()
        hbox_layout.addWidget(self._cancel_button)
        hbox_layout.addWidget(self._confirm_button)
        vbox_layout.addLayout(hbox_layout)
        self._main_layout.addLayout(vbox_layout)

    def _bind_event(self) -> None:
        self._cancel_button.clicked.connect(self.reject)
        self._confirm_button.clicked.connect(self.accept)

    def _title_name(self) -> str:
        return _L.TID_COMMON_TIP

    def set_message_info(self, msg: str, show_cancel: bool) -> None:
        msg_text_edit = self._msg_text_edit
        width, height = calculate_text_size(
            msg, self._max_msg_width, msg_text_edit.font()
        )
        msg_text_edit.setText(msg)
        if height > self._max_msg_height:
            height = self._max_msg_height
        if width > self._max_msg_width:
            width = self._max_msg_width

        msg_text_edit.setFixedWidth(width + 10)
        if width + 40 < 220:
            width = 180
        self.resize(width + 40, height + 125)
        self._cancel_button.setVisible(show_cancel)


msg_box_instance = None


def show_message(msg: str, show_cancel: bool = False) -> None:
    global msg_box_instance
    if msg_box_instance is None:
        msg_box_instance = BaseMessageBox()
    msg_box_instance.set_message_info(msg, show_cancel)
    msg_box_instance.show()
    msg_box_instance.raise_()
    msg_box_instance.activateWindow()


def hide_message() -> None:
    msg_box_instance and msg_box_instance.hide()


def message(msg: str, show_cancel: bool = False) -> bool:
    msg_box = BaseMessageBox()
    msg_box.set_message_info(msg, show_cancel)
    res = msg_box.exec_()
    return res == QDialog.Accepted
