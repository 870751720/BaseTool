from BaseTool.BaseUI.BaseStyle import NormalStyle
from qtpy.QtWidgets import QPushButton


class BaseButton(QPushButton):
	def __init__(
		self,
		txt: str = "",
		style: str = NormalStyle.BUTTON_DEFAULT,
		size: tuple[int, int] = (80, 22),
	) -> None:
		super().__init__()
		self.setText(txt)
		self.setFixedSize(*size)
		self.setStyleSheet(style)
