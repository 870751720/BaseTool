import os

from BaseTool.BaseUI.BaseMessagebox import execMessage
from BaseTool.BaseUI.BaseStyle import NormalStyle
from BaseTool.BaseUtil.UtilI18n import BASE_LH
from qtpy.QtCore import QSize
from qtpy.QtWidgets import QFileDialog, QPushButton


class BaseFilePick(QPushButton):
	def __init__(
		self,
		callback: callable = None,
		defaultPath: str = None,
		checkFunc: callable = None,
		isDir: bool = False,
		size: tuple[int, int] = (270, 22),
	) -> None:
		super().__init__()
		self.setFixedSize(QSize(*size))
		self.setStyleSheet(NormalStyle.NORMAL_FILE_PICK)
		self._callback = callback

		if defaultPath:
			self.setText(defaultPath)
		else:
			self.setText(BASE_LH.TID_COMMON_FILE_PICK_TIP)
		self._checkFunc = checkFunc
		self._isDir = isDir
		self.clicked.connect(self._openFileDialog)

	def _openFileDialog(self) -> None:
		options = QFileDialog.Options()
		if self._isDir:
			fileName = QFileDialog.getExistingDirectory(
				self,
				BASE_LH.TID_COMMON_FILE_PICK,
				options=options,
			)
		else:
			fileName, _ = QFileDialog.getOpenFileName(
				self,
				BASE_LH.TID_COMMON_FILE_PICK,
				options=options,
			)
		if fileName:
			fileName = os.path.normpath(fileName)
			if self._checkFunc and not self._checkFunc(fileName):
				execMessage(BASE_LH.TID_COMMON_FILE_PICK_CHECK)
				return
			self.setText(fileName)
			self.setToolTip(fileName)
			self._callback and self._callback(fileName)

	def getPickFile(self) -> str:
		pickFile = self.text()
		if pickFile == BASE_LH.TID_COMMON_FILE_PICK_TIP:
			pickFile = ""
		return pickFile

	def setCheckFunc(self, checkFunc: callable) -> None:
		self._checkFunc = checkFunc

	def setCallback(self, callback: callable) -> None:
		self._callback = callback

	def setDefaultPath(self, defaultPath: str) -> None:
		self.setText(defaultPath)
