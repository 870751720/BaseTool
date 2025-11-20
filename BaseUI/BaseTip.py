from BaseTool.BaseUI.BaseDialog import BaseDialog
from BaseTool.BaseUI.BaseLayout import VBoxLayout
from BaseTool.BaseUI.BaseTextEdit import BaseTextEdit
from BaseTool.BaseUtil.UtilQT import calculateTextSize
from BaseTool.BaseUtil.UtilI18n import BASE_LH
from qtpy.QtCore import QTimer, Qt
from qtpy.QtWidgets import QApplication


class BaseTip(BaseDialog):
	_instance = None

	@classmethod
	def getInstance(cls):
		if cls._instance is None:
			cls._instance = cls()
		return cls._instance

	@property
	def _maxTipWidth(self) -> int:
		return 600

	@property
	def _maxTipHeight(self) -> int:
		return 400

	def _setTitle(self) -> None:
		super()._setTitle()
		self._titleBar.setVisible(False)

	def _design(self) -> None:
		self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
		vboxLayout = VBoxLayout()
		self._tipTextEdit = tipTextEdit = BaseTextEdit()
		tipTextEdit.setMaximumHeight(self._maxTipHeight)
		tipTextEdit.setReadOnly(True)

		tipTextEdit.setStyleSheet("border: none; background: transparent; color: white;")
		vboxLayout.addWidget(tipTextEdit)

		self._mainLayout.addLayout(vboxLayout)

		self._autoCloseTimer = QTimer()
		self._autoCloseTimer.setSingleShot(True)
		self._autoCloseTimer.timeout.connect(self.accept)

		self._loadingTimer = QTimer()
		self._loadingTimer.timeout.connect(self._updateLoadingText)
		self._loadingDots = 0
		self._loadingBaseText = ""

	def setTipInfo(self, msg: str, autoCloseSeconds: float = 0) -> None:
		self._updateMsgAndSize(msg)
		if autoCloseSeconds <= 0:
			autoCloseSeconds = 1
		if autoCloseSeconds > 0:
			self._autoCloseTimer.start(int(autoCloseSeconds * 1000))

	def setLoadingInfo(self, msg: str) -> None:
		self._loadingBaseText = msg
		self._loadingDots = 0

		self._updateMsgAndSize(msg)
		self._updateLoadingText()
		self._loadingTimer.start(500)

	def _updateMsgAndSize(self, msg: str) -> None:
		tipTextEdit = self._tipTextEdit
		width, height = calculateTextSize(msg, self._maxTipWidth, tipTextEdit.font())
		tipTextEdit.setText(msg)

		if height > self._maxTipHeight:
			height = self._maxTipHeight
		if width > self._maxTipWidth:
			width = self._maxTipWidth

		tipTextEdit.setFixedWidth(width + 30)
		if width + 40 < 200:
			width = 160
		self.resize(width + 40, height + 10)

	def _updateLoadingText(self) -> None:
		dots = "." * self._loadingDots
		self._tipTextEdit.setText(self._loadingBaseText + dots)
		self._loadingDots = (self._loadingDots + 1) % 4


def showTip(msg: str, autoCloseSeconds: float = 0.5) -> None:
	tipInstance = BaseTip.getInstance()
	tipInstance.setModal(False)
	tipInstance.setTipInfo(msg, autoCloseSeconds)
	tipInstance.show()
	tipInstance.raise_()
	tipInstance.activateWindow()


def showLoading(msg: str = BASE_LH.TID_COMMON_LOADING) -> None:
	loadingInstance = BaseTip.getInstance()
	loadingInstance.setModal(True)
	loadingInstance.setLoadingInfo(msg)
	loadingInstance.show()
	loadingInstance.raise_()
	loadingInstance.activateWindow()
	QApplication.processEvents()


def hideLoading() -> None:
	loadingInstance = BaseTip.getInstance()
	loadingInstance and loadingInstance.accept()
