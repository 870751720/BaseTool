from BaseTool.BaseUI.BaseIcon import BaseIcon
from BaseTool.BaseUI.BaseLabel import BaseLabel
from BaseTool.BaseUI.BaseLayout import HBoxLayout
from BaseTool.BaseUI.BaseStyle import ImgRes, NormalStyle
from BaseTool.BaseUI.BaseWidget import BaseWidget
from qtpy.QtCore import Qt
from qtpy.QtGui import QMouseEvent
from qtpy.QtWidgets import QWidget


class BaseTitleBar(BaseWidget):
	def __init__(
		self,
		parent: QWidget,
		title: str,
		icon: str = None,
		subTitle: str = None,
		showMin: bool = False,
		showSetting: bool = False,
		settingFunc: callable = None,
	) -> None:
		self._parent = parent
		self._startPos = None
		self._title = title
		self._icon = icon
		self._subTitle = subTitle
		self._showMin = showMin
		self._showSetting = showSetting
		self._settingFunc = settingFunc
		super().__init__()

	def _design(self) -> None:
		mainLayout = HBoxLayout(isEmpty=True)
		contentWidget = QWidget()
		innerLayout = HBoxLayout()
		innerLayout.setContentsMargins(10, 8, 0, 10)
		innerLayout.setSpacing(10)
		if self._icon:
			icon = BaseIcon(self._icon, (30, 30))
			innerLayout.addWidget(icon)
		self._titleLabel = BaseLabel(self._title)
		innerLayout.addWidget(self._titleLabel)
		if self._subTitle:
			subTitle = BaseLabel(self._subTitle, NormalStyle.STRONG_WHITE_LABEL)
			innerLayout.addWidget(subTitle)
		self.ssubTitle = BaseLabel()
		innerLayout.addWidget(self.ssubTitle)
		innerLayout.addStretch()

		if self._showSetting:
			self._btnSetting = BaseIcon(ImgRes.SETTING, (30, 40))
			innerLayout.addWidget(self._btnSetting)
		else:
			self._btnSetting = None
		if self._showMin:
			self._btnMin = BaseIcon(ImgRes.MIN, (30, 40))
			innerLayout.addWidget(self._btnMin)
		else:
			self._btnMin = None

		self._btnClose = BaseIcon(ImgRes.CLOSE, (30, 40))
		innerLayout.addWidget(self._btnClose)
		contentWidget.setLayout(innerLayout)
		mainLayout.addWidget(contentWidget)
		self.setLayout(mainLayout)

	def _bindEvent(self) -> None:
		self._btnClose.clicked.connect(self._parent.close)
		if self._btnMin:
			self._btnMin.clicked.connect(self._onMinsizeWindow)
		if self._settingFunc:
			self._btnSetting.clicked.connect(self._settingFunc)

	def _onMinsizeWindow(self) -> None:
		if self._parent.isMinimized():
			self._parent.showNormal()
		else:
			self._parent.showMinimized()

	def _getStyle(self) -> str:
		return NormalStyle.NORMAL_TITLE

	def mousePressEvent(self, event: QMouseEvent) -> None:
		if event.button() == Qt.LeftButton:
			self._startPos = event.pos()

	def mouseReleaseEvent(self, event: QMouseEvent) -> None:
		self._startPos = None

	def mouseMoveEvent(self, event: QMouseEvent) -> None:
		if event.buttons() == Qt.LeftButton and self._startPos:
			self._parent.move(self._parent.pos() + event.pos() - self._startPos)

	def setTitleName(self, titleName: str) -> None:
		self._titleLabel.setText(titleName)
