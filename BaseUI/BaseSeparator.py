from qtpy.QtWidgets import QLabel, QBoxLayout, QHBoxLayout

from BaseTool.BaseUI.BaseStyle import NormalStyle


class BaseSeparator(QLabel):
	def __init__(self, parentLayout: QBoxLayout) -> None:
		super().__init__()

		if isinstance(parentLayout, QHBoxLayout):
			self.setFixedWidth(2)
		else:
			self.setFixedHeight(2)

		self.setStyleSheet(NormalStyle.NORMAL_SEPARATOR)
		parentLayout.addWidget(self)
