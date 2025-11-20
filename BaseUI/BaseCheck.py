from qtpy.QtCore import QSize
from qtpy.QtWidgets import QCheckBox

from BaseTool.BaseUI.BaseStyle import NormalStyle


class BaseCheck(QCheckBox):
	def __init__(
		self,
		callback: callable = None,
		defaultVal: bool = False,
		size: tuple[int, int] = (12, 12),
		hoverFunc: callable = None,
	) -> None:
		super().__init__()
		self.setFixedSize(QSize(*size))
		self.setStyleSheet(NormalStyle.NORMAL_CHECK)
		self.setChecked(defaultVal)
		self.callback = callback
		self.hoverFunc = hoverFunc
		self.isHover = False
		self.stateChanged.connect(self._onStateChanged)

	def _onStateChanged(self, state: int) -> None:
		self.callback and self.callback(self.isChecked())

	def enterEvent(self, event):
		super().enterEvent(event)
		self.isHover = True
		self._onHoverFuncTrigger()

	def leaveEvent(self, event):
		super().leaveEvent(event)
		self.isHover = False
		self._onHoverFuncTrigger()

	def _onHoverFuncTrigger(self):
		self.hoverFunc and self.hoverFunc(self)

	def setCheckedWithoutTrigger(self, checked: bool) -> None:
		self.blockSignals(True)
		self.setChecked(checked)
		self.blockSignals(False)
