from BaseTool.BaseUI.BaseStyle import NormalStyle
from qtpy.QtWidgets import QComboBox


class BaseComboBox(QComboBox):
	def __init__(
		self,
		style: str = NormalStyle.NORMAL_COMBOBOX,
		size: tuple[int, int] = (180, 22),
	) -> None:
		super().__init__()
		self.setFixedSize(*size)
		self.setStyleSheet(style)
