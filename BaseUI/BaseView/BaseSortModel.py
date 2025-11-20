from qtpy.QtCore import QModelIndex, QSortFilterProxyModel, Qt
from qtpy.QtWidgets import QTreeView


class BaseSortModel(QSortFilterProxyModel):
	def __init__(self, view: QTreeView) -> None:
		super().__init__()
		self._view = view
		self.setSortRole(Qt.DisplayRole)
		self.setDynamicSortFilter(True)

	def filterAcceptsRow(self, source_row: int, sourceParent: QModelIndex) -> bool:
		if sourceParent.isValid():
			parentItem = self.sourceModel().itemFromIndex(sourceParent)
			item = parentItem.child(source_row, 0)
		else:
			item = self.sourceModel().item(source_row, 0)
		if item.dataIndex not in self._view.cantShowRows:
			return True
		return self._hasAcceptedChildren(item)

	def _hasAcceptedChildren(self, item) -> bool:
		for row in range(item.rowCount()):
			childItem = item.child(row, 0)
			if childItem.dataIndex not in self._view.cantShowRows:
				return True
			if self._hasAcceptedChildren(childItem):
				return True
		return False

	def lessThan(self, left: QModelIndex, right: QModelIndex) -> bool:
		if left.parent() != right.parent():
			return False
		leftData = self.sourceModel().data(left, Qt.DisplayRole)
		rightData = self.sourceModel().data(right, Qt.DisplayRole)
		sortOrder = self.sortOrder()
		isLeftEmpty = False if leftData and leftData != self._view.bottomVal else True
		isRightEmpty = False if rightData and rightData != self._view.bottomVal else True
		if sortOrder == Qt.AscendingOrder:
			if isLeftEmpty and not isRightEmpty:
				return False
			if not isLeftEmpty and isRightEmpty:
				return True
		else:
			if isLeftEmpty and not isRightEmpty:
				return True
			if not isLeftEmpty and isRightEmpty:
				return False
		return super().lessThan(left, right)
