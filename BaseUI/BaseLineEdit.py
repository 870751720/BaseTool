from qtpy.QtCore import Qt
from qtpy.QtGui import QKeyEvent
from qtpy.QtWidgets import QLineEdit

from BaseTool.BaseUI.BaseStyle import NormalStyle
from BaseTool.BaseUtil.UtilI18n import BASE_LH
from BaseTool.BaseUtil.UtilQT import debounce


class BaseLineEdit(QLineEdit):
	def __init__(
		self,
		callback: callable = None,
		width: int = 120,
		defaultText: str = None,
		placeHolder: str = None,
		autoTrigger=False,
	) -> None:
		super().__init__()
		self.setStyleSheet(NormalStyle.NORMAL_LINE_EDIT)
		self.setFixedWidth(width)
		self.setFixedHeight(22)
		if placeHolder is None:
			placeHolder = BASE_LH.TID_COMMON_SEARCH_PLACEHOLDER
		self.setPlaceholderText(placeHolder)
		if defaultText:
			self.setText(defaultText)
		self.textChanged.connect(self._onTextChange)
		self._callback = callback
		self._autoTrigger = autoTrigger

	def setCallback(self, callback: callable) -> None:
		self._callback = callback

	def _onTextChange(self, text: str) -> None:
		if not text:
			self._runCallback(text)
		elif self._autoTrigger:
			self._onTextChangeWithDebounce(text)

	@debounce(3)
	def _onTextChangeWithDebounce(self, text: str) -> None:
		self._runCallback(text)

	def _runCallback(self, text: str) -> None:
		self._callback and self._callback(text)

	def keyPressEvent(self, event: QKeyEvent) -> None:
		super().keyPressEvent(event)
		if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
			self._runCallback(self.text())
			if self._autoTrigger:
				self._onTextChangeWithDebounce.cancel()
