from BaseTool.BaseUI.BaseStyle import NormalStyle
from qtpy.QtWidgets import QWidget


class BaseWidget(QWidget):
	def __init__(self) -> None:
		super().__init__()
		self._initData()
		self._initUI()

	def _initData(self) -> None:
		pass

	def _initUI(self) -> None:
		self._setSize()
		self._setStyle()
		self._design()
		self._bindEvent()

	def _setSize(self) -> None:
		width, height = self._getSize()
		if width is not None:
			self.resize(width, height)

	def _setStyle(self) -> None:
		style = self._getStyle()
		if style is not None:
			self.setStyleSheet(style)

	def _getSize(self) -> tuple[int, int]:
		return None, None

	def _getStyle(self) -> str:
		return NormalStyle.NORMAL_WIDGET

	def _design(self) -> None:
		pass

	def _bindEvent(self) -> None:
		pass
