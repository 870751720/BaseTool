from qtpy.QtCore import Qt
from qtpy.QtGui import QStandardItem

from base_tool.base_util.util_enum import RowStateColor


class BaseItem(QStandardItem):
    def __init__(self, row_dict: dict, display: any) -> None:
        super().__init__()
        self.setData(row_dict, Qt.UserRole)
        self.setData(display, Qt.DisplayRole)
        self.setData(
            row_dict.get("back_state", RowStateColor.NORMAL), Qt.BackgroundRole
        )
