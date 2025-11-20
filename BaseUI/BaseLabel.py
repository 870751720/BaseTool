from qtpy.QtCore import Qt
from qtpy.QtGui import QMouseEvent
from qtpy.QtWidgets import QLabel

from BaseTool.BaseUI.BaseStyle import NormalStyle


class BaseLabel(QLabel):
	def __init__(
		self,
		text: str = "",
		style: str = NormalStyle.WHITE_LABEL,
		tooltip: str = None,
		clickFunc: callable = None,
	):
		super().__init__()
		self.setText(text)

		if tooltip is not None:
			self.setToolTip(tooltip)
		if clickFunc:
			self.setCursor(Qt.PointingHandCursor)
			self.setStyleSheet("%s %s" % (style, NormalStyle.HOVER_LABEL))
		else:
			self.setStyleSheet(style)
		self.clickFunc = clickFunc

	def mousePressEvent(self, event: QMouseEvent) -> None:
		self.clickFunc and self.clickFunc()
		super().mousePressEvent(event)
