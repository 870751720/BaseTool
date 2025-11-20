from qtpy.QtCore import Qt
from qtpy.QtGui import QStandardItem

from BaseTool.BaseUtil.UtilEnum import RowStateColor


class BaseItem(QStandardItem):
	def __init__(self, rowDict: dict, display: any, dataIndex: int) -> None:
		super().__init__()
		self.dataIndex = dataIndex
		self.rowDict = rowDict
		self.setData(self, Qt.UserRole)
		self.setData(display, Qt.DisplayRole)
		self.setData(rowDict.get("RowState", RowStateColor.NORMAL), Qt.BackgroundRole)
