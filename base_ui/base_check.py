from qtpy.QtCore import QSize
from qtpy.QtWidgets import QCheckBox

from base_tool.base_ui.base_style import NormalStyle


class BaseCheck(QCheckBox):
    def __init__(
        self,
        callback: callable,
        default_val: bool = False,
        size: tuple[int, int] = (12, 12),
    ) -> None:
        super().__init__()
        self.setFixedSize(QSize(*size))
        self.setStyleSheet(NormalStyle.NORMAL_CHECK)
        self.setChecked(default_val)
        self.callback = callback
        self.stateChanged.connect(self._on_state_changed)

    def _on_state_changed(self, state: int) -> None:
        self.callback and self.callback(state == 2)

    def set_checked_without_trigger(self, checked: bool) -> None:
        self.blockSignals(True)
        self.setChecked(checked)
        self.blockSignals(False)
