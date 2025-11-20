from qtpy.QtGui import QStandardItemModel


class BaseItemModel(QStandardItemModel):
	def __init__(self) -> None:
		super().__init__()
