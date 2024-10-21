import os

from base_tool.base_ui.base_messagebox import message
from base_tool.base_ui.base_style import NormalStyle
from base_tool.base_util.util_I18n import _L
from qtpy.QtCore import QSize
from qtpy.QtWidgets import QFileDialog, QPushButton


class BaseFilePick(QPushButton):
    def __init__(
        self,
        callback: callable = None,
        default_path: str = None,
        check_func: callable = None,
        is_dir: bool = False,
        size: tuple[int, int] = (270, 22),
    ) -> None:
        super().__init__()
        self.setFixedSize(QSize(*size))
        self.setStyleSheet(NormalStyle.NORMAL_FILE_PICK)
        self._callback = callback

        if default_path:
            self.setText(default_path)
        else:
            self.setText(_L.TID_COMMON_FILE_PICK_TIP)
        self._check_func = check_func
        self._is_dir = is_dir
        self.clicked.connect(self._open_file_dialog)

    def _open_file_dialog(self) -> None:
        options = QFileDialog.Options()
        if self._is_dir:
            file_name = QFileDialog.getExistingDirectory(
                self,
                _L.TID_COMMON_FILE_PICK,
                options=options,
            )
        else:
            file_name, _ = QFileDialog.getOpenFileName(
                self,
                _L.TID_COMMON_FILE_PICK,
                options=options,
            )
        if file_name:
            file_name = os.path.normpath(file_name)
            if self._check_func and not self._check_func(file_name):
                message(_L.TID_COMMON_FILE_PICK_CHECK)
                return
            self.setText(file_name)
            self.setToolTip(file_name)
            self._callback and self._callback(file_name)

    def get_pick_file(self) -> str:
        pick_file = self.text()
        if pick_file == _L.TID_COMMON_FILE_PICK_TIP:
            pick_file = ""
        return pick_file

    def set_check_func(self, check_func: callable) -> None:
        self._check_func = check_func

    def set_callback(self, callback: callable) -> None:
        self._callback = callback

    def set_default_path(self, default_path: str) -> None:
        self.setText(default_path)
