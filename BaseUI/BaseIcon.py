from qtpy.QtCore import QSize
from qtpy.QtGui import QIcon
from qtpy.QtWidgets import QPushButton, QSizePolicy

from BaseTool.BaseUI.BaseStyle import NormalStyle


class BaseIcon(QPushButton):
	def __init__(self, iconUrl: str = "", size: tuple[int, int] = (12, 12), style=NormalStyle.BUTTON_ICON) -> None:
		super().__init__()
		sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		self.setSizePolicy(sizePolicy)

		self.setIconSize(QSize(*size))
		self.setStyleSheet(style)
		if iconUrl:
			self.setIcon(QIcon(iconUrl))

		self._iconUrl = iconUrl

	def changeIcon(self, iconUrl: str):
		self._iconUrl = iconUrl
		self.setIcon(QIcon(iconUrl))

	def getIcon(self) -> str:
		return self._iconUrl
