from qtpy.QtCore import Qt
from qtpy.QtGui import QKeyEvent
from qtpy.QtWidgets import QApplication, QDialog

from BaseTool.BaseUI.BaseFrameless import BaseFramelessWindow
from BaseTool.BaseUI.BaseLayout import VBoxLayout
from BaseTool.BaseUI.BaseStyle import NormalStyle
from BaseTool.BaseUI.BaseTitle import BaseTitleBar


class BaseDialog(BaseFramelessWindow, QDialog):
	def __init__(self) -> None:
		self._titleHeight = 30
		QDialog.__init__(self)
		BaseFramelessWindow.__init__(self)
		self._initData()
		self._initUI()

	def _initData(self) -> None:
		pass

	def _initUI(self) -> None:
		self._setSize()
		self._setStyle()
		self._setTitle()
		self._design()
		self._bindEvent()

	def _setSize(self) -> None:
		screen = QApplication.screenAt(self.cursor().pos())
		if screen:
			screenRect = screen.geometry()
			width, height = self._getSize()
			if width is not None and height is not None:
				x = screenRect.x() + (screenRect.width() - width) // 2
				y = screenRect.y() + (screenRect.height() - height) // 2
				self.setGeometry(x, y, width, height)

	def _setStyle(self) -> None:
		style = self._getStyle()
		if style is not None:
			self.setStyleSheet(style)

	def _getSize(self) -> tuple[int, int]:
		return None, None

	def _getStyle(self) -> str:
		return NormalStyle.NORMAL_DIALOG

	def _design(self) -> None:
		pass

	def _bindEvent(self) -> None:
		pass

	def _titleName(self) -> str:
		return "dialog"

	def _setTitle(self) -> None:
		self._titleBar = titleBar = self._getTitleBar()
		titleBar.setFixedHeight(self._titleHeight)

		self._mainLayout = mainLayout = VBoxLayout(isEmpty=True)
		mainLayout.addWidget(titleBar)
		self.setLayout(mainLayout)

	def _getTitleBar(self) -> BaseTitleBar:
		return BaseTitleBar(self, self._titleName())

	def setTitleName(self, titleName: str) -> None:
		self._titleBar.setTitleName(titleName)

	def keyPressEvent(self, event: QKeyEvent) -> None:
		if event.key() in (Qt.Key_Enter, Qt.Key_Return):
			event.accept()
			return
		super().keyPressEvent(event)
