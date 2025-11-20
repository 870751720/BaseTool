from qtpy.QtCore import Qt

from BaseTool.BaseUI.BaseButton import BaseButton
from BaseTool.BaseUI.BaseDialog import BaseDialog
from BaseTool.BaseUI.BaseLayout import HBoxLayout, VBoxLayout
from BaseTool.BaseUI.BaseStyle import NormalStyle
from BaseTool.BaseUI.BaseTextEdit import BaseTextEdit
from BaseTool.BaseUtil.UtilI18n import BASE_LH
from BaseTool.BaseUtil.UtilQT import calculateTextSize
from qtpy.QtWidgets import QDialog


class BaseMessageBox(BaseDialog):
	_instance = None

	@classmethod
	def getInstance(cls):
		if cls._instance is None:
			cls._instance = cls()
		return cls._instance

	@property
	def _maxMsgWidth(self) -> int:
		return 1000

	@property
	def _maxMsgHeight(self) -> int:
		return 650

	def _design(self) -> None:
		self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint | Qt.Tool)
		vboxLayout = VBoxLayout()
		self._msgTextEdit = msgTextEdit = BaseTextEdit()
		msgTextEdit.setMaximumHeight(self._maxMsgHeight)
		msgTextEdit.setReadOnly(True)
		vboxLayout.addWidget(msgTextEdit)

		hboxLayout = HBoxLayout()

		self._cancelButton = BaseButton(BASE_LH.TID_COMMON_CANCEL)
		self._confirmButton = BaseButton(BASE_LH.TID_COMMON_CONFIRM, NormalStyle.BUTTON_MAIN)
		hboxLayout.addStretch()
		hboxLayout.addWidget(self._cancelButton)
		hboxLayout.addWidget(self._confirmButton)
		vboxLayout.addLayout(hboxLayout)
		self._mainLayout.addLayout(vboxLayout)

	def _bindEvent(self) -> None:
		self._cancelButton.clicked.connect(self.reject)
		self._confirmButton.clicked.connect(self.accept)

	def _titleName(self) -> str:
		return BASE_LH.TID_COMMON_TIP

	def setMessageInfo(self, msg: str, showCancel: bool) -> None:
		msgTextEdit = self._msgTextEdit
		width, height = calculateTextSize(msg, self._maxMsgWidth, msgTextEdit.font())
		msgTextEdit.setText(msg)
		if height > self._maxMsgHeight:
			height = self._maxMsgHeight
		if width > self._maxMsgWidth:
			width = self._maxMsgWidth

		msgTextEdit.setFixedWidth(width + 10)
		if width + 40 < 220:
			width = 180
		self.resize(width + 40, height + 125)
		self._cancelButton.setVisible(showCancel)


def showMessage(msg: str, showCancel: bool = False) -> None:
	msgBoxInstance = BaseMessageBox.getInstance()
	msgBoxInstance.setMessageInfo(msg, showCancel)
	if not msgBoxInstance.isVisible():
		msgBoxInstance.exec()


def execMessage(msg: str, showCancel: bool = False) -> bool:
	msgBox = BaseMessageBox()
	msgBox.setMessageInfo(msg, showCancel)
	res = msgBox.exec()
	return res == QDialog.Accepted
