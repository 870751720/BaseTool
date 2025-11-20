from qtpy.QtCore import QModelIndex, Qt
from qtpy.QtWidgets import QStyledItemDelegate, QStyleOptionViewItem, QTreeView, QWidget

from BaseTool.BaseUI.BaseCheck import BaseCheck
from BaseTool.BaseUI.BaseStyle import NormalStyle
from BaseTool.BaseUI.BaseView.BaseViewWidget import BaseViewWidget


class BaseItemDelegate(QStyledItemDelegate):
	def __init__(self, view: QTreeView) -> None:
		self._view = view
		self.widgets = {}
		self.notCheckableRows = []
		super().__init__()

	def paint(self, _, option: QStyleOptionViewItem, index: QModelIndex) -> None:
		headerConfig = self._view.headerConfig
		column = index.column()
		config = headerConfig[column]

		itemData = index.data(Qt.UserRole).rowDict
		if itemData is None:
			return

		sourceIndex = self._view.sortModel.mapToSource(index)
		item = self._view.itemModel.itemFromIndex(sourceIndex)
		if not hasattr(item, "dataIndex"):
			return

		dataRow = item.dataIndex
		key = (dataRow, column)

		widget = self.widgets.get(key, None)

		if len(self.widgets) > 1000:
			self._cleanupOldWidgets()

		if widget is None:
			self.widgets[key] = widget = BaseViewWidget(
				index,
				itemData,
				config,
				self._checkFunc,
				self._hoverFunc,
				dataRow,
				dataRow in self._view.checkedRowsState,
				dataRow not in self.notCheckableRows,
			)
			widget.setGeometry(option.rect)
			self._view.setIndexWidget(index, widget)

	def _cleanupOldWidgets(self):
		if len(self.widgets) > 500:
			keysToRemove = list(self.widgets.keys())[:-500]
			for key in keysToRemove:
				self.widgets.pop(key, None)

	def destroyEditor(self, editor: QWidget, index: QModelIndex) -> None:
		super().destroyEditor(editor, index)
		try:  # 会偶先报错，先容错看看
			sourceIndex = self._view.sortModel.mapToSource(index)
			item = self._view.itemModel.itemFromIndex(sourceIndex)
			if hasattr(item, "dataIndex"):
				key = (item.dataIndex, index.column())
				self.widgets.pop(key, None)
		except:
			return

	def _getCheckColumn(self):
		checkColumn = 0
		for index, oneConfig in enumerate(self._view.headerConfig):
			if oneConfig.get("CanCheck", False):
				checkColumn = index
				break
		return checkColumn

	def _checkFunc(self, row: int, isChecked: bool) -> None:
		checkColumn = self._getCheckColumn()
		moreCheck = None
		for oneConfig in self._view.headerConfig:
			if oneConfig.get("CanCheck", False):
				moreCheck = oneConfig.get("MoreCheck", None)
				break
		needRow = {row}
		needRow.update(self._view.selectedRowsState)
		needShowLink = set()
		if moreCheck:
			needRow, needShowLink = moreCheck(needRow, isChecked)
		for eachRow in needRow:
			if isChecked:
				self._view.checkedRowsState.add(eachRow)
			else:
				self._view.checkedRowsState.discard(eachRow)
			widget = self.widgets.get((eachRow, checkColumn), None)
			if widget:
				checkWidget = widget.checkWidget
				if checkWidget:
					checkWidget.setCheckedWithoutTrigger(isChecked)
					icon = widget.icon
					if icon:
						icon.setVisible(eachRow in needShowLink)
					checkWidget.setStyleSheet(NormalStyle.LINK_CHECK if eachRow in needShowLink else NormalStyle.NORMAL_CHECK)
		self._view.afterCheckDone(needRow, isChecked)

	def _hoverFunc(self, row: int, hoverFunc: callable, checkBox: BaseCheck) -> None:
		if hoverFunc is None:
			return
		if checkBox.isChecked():
			return
		checkColumn = self._getCheckColumn()
		needRow = hoverFunc(row)
		isHover = checkBox.isHover
		for eachRow in needRow:
			widget = self.widgets.get((eachRow, checkColumn), None)
			if widget:
				checkWidget = widget.checkWidget
				if not checkWidget or checkWidget.isChecked():
					continue
				widget.checkWidget.setStyleSheet(NormalStyle.LINK_CHECK if isHover else NormalStyle.NORMAL_CHECK)
				widget.icon.setVisible(isHover)

	def checkAll(self, isCheck: bool) -> None:
		for widget in self.widgets.values():
			checkWidget = widget.checkWidget
			if checkWidget:
				checkWidget.setCheckedWithoutTrigger(isCheck)

	def checkRows(self, isCheck: bool, rows: list) -> None:
		checkColumn = self._getCheckColumn()
		for row in rows:
			widget = self.widgets.get((row, checkColumn), None)
			if widget:
				checkWidget = widget.checkWidget
				if checkWidget:
					checkWidget.setCheckedWithoutTrigger(isCheck)

	def setCheckAbleRows(self, checkable: bool, rows: list) -> None:
		checkColumn = self._getCheckColumn()
		if not checkable:
			self.notCheckableRows = rows
		for row in rows:
			widget = self.widgets.get((row, checkColumn), None)
			if widget:
				checkWidget = widget.checkWidget
				if checkWidget:
					checkWidget.setStyleSheet(NormalStyle.NORMAL_CHECK if checkable else NormalStyle.DISABLE_CHECK)
					checkWidget.setDisabled(not checkable)

	def getWidgetByRowAndHeadIndex(self, row: int, headIndex: int) -> int:
		return self.widgets.get((row, headIndex), None)
