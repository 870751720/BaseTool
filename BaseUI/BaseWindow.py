from qtpy.QtWidgets import QApplication, QMainWindow, QWidget

from BaseTool.BaseUI.BaseFrameless import BaseFramelessWindow
from BaseTool.BaseUI.BaseLayout import VBoxLayout
from BaseTool.BaseUI.BaseStyle import NormalStyle
from BaseTool.BaseUI.BaseTitle import BaseTitleBar


class BaseWindow(BaseFramelessWindow, QMainWindow):
	def __init__(self) -> None:
		self._titleHeight = 40
		QMainWindow.__init__(self)
		BaseFramelessWindow.__init__(self)
		self._initData()
		self._initUI()
		self._postInitData()

	def _initData(self) -> None:
		pass

	def _postInitData(self) -> None:
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
		self.setWindowTitle(self._titleName())

	def _getSize(self) -> tuple[int, int]:
		return None, None

	def _getStyle(self) -> str:
		return NormalStyle.NORMAL_WINDOW

	def _design(self) -> None:
		pass

	def _bindEvent(self) -> None:
		pass

	def _titleName(self) -> str:
		return "window"

	def _setTitle(self) -> None:
		centralWidget = QWidget()
		self.setCentralWidget(centralWidget)

		self._mainLayout = mainLayout = VBoxLayout()
		mainLayout.setContentsMargins(0, 0, 0, 0)

		self._titleBar = self._getTitleBar()
		self._titleBar.setFixedHeight(self._titleHeight)
		mainLayout.addWidget(self._titleBar)

		centralWidget.setLayout(self._mainLayout)

	def _getTitleBar(self) -> BaseTitleBar:
		return BaseTitleBar(self, self._titleName(), settingFunc=None)
