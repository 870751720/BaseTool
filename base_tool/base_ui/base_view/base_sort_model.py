from qtpy.QtCore import QModelIndex, QSortFilterProxyModel
from qtpy.QtWidgets import QTreeView


class BaseSortModel(QSortFilterProxyModel):
    def __init__(self, view: QTreeView) -> None:
        super().__init__()
        self._view = view

    def filterAcceptsRow(self, source_row: int, source_parent: QModelIndex) -> bool:
        if source_row not in self._view.cant_show_rows:
            return True
        return False
