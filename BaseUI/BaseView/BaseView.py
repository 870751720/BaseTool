from qtpy.QtCore import QEvent, QItemSelection, QModelIndex, QPoint, Qt
from qtpy.QtGui import QColor
from qtpy.QtWidgets import QAbstractItemView, QTreeView

from BaseTool.BaseUI.BaseMenu import BaseMenu
from BaseTool.BaseUI.BaseStyle import NormalStyle
from BaseTool.BaseUI.BaseView.BaseHead import BaseHeadView
from BaseTool.BaseUI.BaseView.BaseItem import BaseItem
from BaseTool.BaseUI.BaseView.BaseItemDelegate import BaseItemDelegate
from BaseTool.BaseUI.BaseView.BaseItemModel import BaseItemModel
from BaseTool.BaseUI.BaseView.BaseSortModel import BaseSortModel
from BaseTool.BaseUtil.UtilEnum import RowStateColor


class BaseView(QTreeView):
	ROW_STATE_COLOR = {
		(RowStateColor.NORMAL, True): (14, 74, 86, 205),
		(RowStateColor.NORMAL, False): (0, 0, 0, 0),
		(RowStateColor.ERROR, True): (156, 51, 55, 205),
		(RowStateColor.ERROR, False): (156, 51, 55, 150),
		(RowStateColor.WARNING, True): (110, 72, 29, 205),
		(RowStateColor.WARNING, False): (110, 72, 29, 150),
		(RowStateColor.GREEN, True): (34, 139, 34, 205),
		(RowStateColor.GREEN, False): (34, 139, 34, 150),
	}

	def __init__(self) -> None:
		super().__init__()
		self.setStyleSheet(NormalStyle.NORMAL_VIEW)
		self.setAnimated(True)
		self.setDragEnabled(False)
		self.setSortingEnabled(True)
		self.setRootIsDecorated(True)
		self.setUniformRowHeights(True)
		self.setDropIndicatorShown(False)
		self.setAlternatingRowColors(True)
		self.setContextMenuPolicy(Qt.CustomContextMenu)  # 设置自定义上下文菜单
		self.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 不能编辑
		self.setSelectionBehavior(QAbstractItemView.SelectRows)
		self.setSelectionMode(QAbstractItemView.ExtendedSelection)
		self.customContextMenuRequested.connect(self._onMenuEvent)
		self.expanded.connect(self._onNodeExpandChanged)
		self.collapsed.connect(self._onNodeExpandChanged)

		self.itemModel = BaseItemModel()
		self.sortModel = sortModel = BaseSortModel(self)
		sortModel.setSourceModel(self.itemModel)

		self._itemDeletegate = BaseItemDelegate(self)
		self.setItemDelegate(self._itemDeletegate)
		self.setModel(sortModel)
		self.selectionModel().selectionChanged.connect(self._onSelectionChanged)

		self.setHeader(BaseHeadView())

		self.bottomVal = ""  # 符合对应值的排序会一直在最下面
		self._actionConfig = []
		self.headerConfig = []
		self.headerFilterInfo = {}

		self._filterTextSet = set()
		self.cantShowRows = set()

		self.afterCheckDoneFunc = None

		self._showCanUseInfo()

	def drawRow(self, painter, option, index):
		super().drawRow(painter, option, index)
		isSelected = self.getRealIndexRow(index) in self.selectedRowsState
		rowState = index.data(Qt.BackgroundRole)
		color = self.ROW_STATE_COLOR.get((rowState, isSelected), None)
		if color is not None:
			painter.fillRect(option.rect, QColor.fromRgb(*color))

	def viewportEvent(self, event: QEvent) -> bool:
		if event.type() == QEvent.Resize and not self.header().underMouse():
			self._adjustColumnWidths()
		return super().viewportEvent(event)

	def _onSelectionChanged(self, selected: QItemSelection, deselected: QItemSelection) -> None:
		for index in selected.indexes():
			self.selectedRowsState.add(self.getRealIndexRow(index))
		for index in deselected.indexes():
			self.selectedRowsState.discard(self.getRealIndexRow(index))

	def getRealIndexRow(self, index: QModelIndex) -> int:
		sourceIndex = self.sortModel.mapToSource(index)
		item = self.itemModel.itemFromIndex(sourceIndex)
		return item.dataIndex

	def _adjustColumnWidths(self) -> None:
		width = self.viewport().width()
		widthData = [one["Width"] for one in self.headerConfig]
		fixedColWidths = {}
		proportions = []
		for index, one in enumerate(widthData):
			if one > 1:
				fixedColWidths[index] = one
			else:
				proportions.append(one)
		remainingWidth = width - sum(fixedColWidths.values())

		for col, width in fixedColWidths.items():
			self.setColumnWidth(col, width)

		startCol = 0
		for proportion in proportions:
			while True:
				if startCol in fixedColWidths:
					startCol += 1
				else:
					break
			colWidth = int(remainingWidth * proportion)
			self.setColumnWidth(startCol, colWidth)
			startCol += 1

	def _onMenuEvent(self, pos: QPoint) -> None:
		if not self._actionConfig:
			return
		index = self.currentIndex()
		if not index.isValid():
			return
		menu = BaseMenu()
		row = self.getRealIndexRow(index)
		menu.loadAction(
			self._actionConfig,
			[self.data[row], [self.data[one] for one in self.selectedRowsState]],
		)

		menu.exec_(self.mapToGlobal(pos))

	def _onNodeExpandChanged(self, index: QModelIndex) -> None:
		sourceIndex = self.sortModel.mapToSource(index)
		dataRow = self.itemModel.itemFromIndex(sourceIndex).dataIndex

		for column in range(len(self.headerConfig)):
			key = (dataRow, column)
			if key in self._itemDeletegate.widgets:
				widget = self._itemDeletegate.widgets[key]
				widget.refreshData(index)

	def onTriggerFilter(self) -> None:
		"""触发过滤"""
		cantShowRows = set()
		for indexInfo in self.headerFilterInfo.values():
			for filterInfo in indexInfo.values():
				if not filterInfo["isShow"]:
					cantShowRows.update(filterInfo["rows"])
		if self._filterTextSet:
			for row, rowDict in enumerate(self.data):
				if row in cantShowRows:
					continue
				isShow = False
				for key, one in rowDict.items():
					if "Tip" in key:
						continue
					if type(one) is str:
						for filterText in self._filterTextSet:
							if filterText in one.lower():
								isShow = True
								break
						if isShow:
							break
				if not isShow:
					cantShowRows.add(row)
		for row, rowDict in enumerate(self.data):
			if rowDict.get("CantShow", False):
				cantShowRows.add(row)

		self._itemDeletegate.widgets.clear()

		self.cantShowRows = cantShowRows
		self.sortModel.invalidateRowsFilter()

	# region 外部调用
	def _showCanUseInfo(self):
		"""开发可能经常用到的对象放到这里展示"""
		self.selectedRowsState = set()
		self.checkedRowsState = set()
		self.data = []

	def setViewConfig(self, headerConfig: list, actionConfig: list = None) -> None:
		"""
		headerConfig: 这是标题头的配置,每一个config是一个dict
		{
			"TextKey": 对应data数据的文本键,会去取对应键的值进行文本展示
			"Tip": 对应data显示的tip
			"IconKey": 对应data数据的icon键,会去取对应键的值进行icon展示
			"RowDecorate": 需要传入一个方法,这个方法会接受一行的data数据进行icon和文本的返回
			"EditKey": 表示此处会有一个输入框, 会取值对这个输入框进行设置
			"EditCallback: 输入框变化执行的函数
			"Name": 标题头的显示
			"Width": 每列的占比,如果是小于1 就是百分占比,大于1就是固定数值
			"CanFilter": 是否可以过滤显示
			"FilterDecorate": 需要传入一个方法,这个方法会接受一行的data数据进行进行过滤文本的返回
			"IconSize": 自定义图标大小
			"CanSort": 是否可以排序
			"CanCheck": 会显示出一个可以勾选的框,可以在view的checked_rows_state取到所有勾选的行
			"CustomCheck": 自定义勾选的函数
			"MoreCheck": 传入一个方法,接受当前需要改变勾选的行,和当前勾选的状态,返回一个总共需要改变勾选的行
			"CenterAlign": 如果需要数据居中,填入这个就好
			"ForceLabel": 就算文本为空,也会创建label,主要是动态改label的需求
			"ClickFunc": 点击执行的函数
		}
		actionConfig: 这是右键菜单的action配置,每一个config是一个dict或者str, 直接传字符串的话就是分组标题
		{
			"Name": action名
			"Callback": 回调方法,接受一个参数,如果是单选的回调, 那么得到的是当前行数据,如果是多选, 那么得到的是选中的行数据的列表
			"AllSelected": 决定是否多选
			"CanAction": 如果是单选,会传入当前的行数据判断是否可以显示这个action, 如果是多选,那么只要有至少一行数据可以显示那么就显示
			在callback传入的列表是满足显示条件的数据
		}
		"""
		self.headerConfig = headerConfig
		self._actionConfig = actionConfig
		self.itemModel.setHorizontalHeaderLabels([config["Name"] for config in headerConfig])

		header = self.header()
		header.setModel(self.itemModel)
		header.setFixedHeight(22)

	def onSearchTriggerFilter(self, text: str) -> None:
		"""如果view有搜索组件, 请绑定这个函数"""
		self._filterTextSet = {one.lower() for one in text.split(",") if one}
		self.onTriggerFilter()

	def setData(self, data: list, clearChecked: bool = True, showTree=False) -> None:
		"""
		设置数据,每一行数据必须是一个dict, 每个列的键在header已经定义了, 所以这里的数据需要有这个对应的键值的键
		{
			"Parent": int -> [可选] 树数据的父节点的index
			"RowState": RowStateColor -> [可选] 节点底色, 分 普通,错误,警告
			"CanCheck": bool -> [可选] 如果节点不行被勾选框那么设置False
			"CantShow": bool -> [可选] 如果节点不想显示,那么设置True
		}
		"""
		self.scheduleDelayedItemsLayout()
		self.setRootIsDecorated(showTree)
		self.clearData(clearChecked)
		oldHeaderFilterInfo = self.headerFilterInfo
		self.headerFilterInfo = {}

		self.data = data
		allRowItems = []

		for row, rowDict in enumerate(data):
			items = []
			for index, oneHeader in enumerate(self.headerConfig):
				text = rowDict.get(oneHeader.get("TextKey", ""), "")
				item = BaseItem(rowDict, text, row)
				items.append(item)

				CanFilter = oneHeader.get("CanFilter", False)
				if CanFilter:
					if "FilterDecorate" in oneHeader:
						filterText = oneHeader["FilterDecorate"](rowDict)
					else:
						filterText = text
					if filterText:
						self.headerFilterInfo.setdefault(index, {}).setdefault(filterText, {"isShow": True, "rows": set()})["rows"].add(
							row
						)
			allRowItems.append(items)

		rootItems = []
		for row, rowDict in enumerate(data):
			if rowDict.get("Parent", None) is None or not showTree:
				rootItems.append((row, allRowItems[row]))

		for _, items in rootItems:
			self.itemModel.appendRow(items)

		for row, rowDict in enumerate(data):
			if rowDict.get("Parent", None) is not None and showTree:
				Parent = rowDict["Parent"]
				if 0 <= Parent < len(allRowItems):
					allRowItems[Parent][0].appendRow(allRowItems[row])

		for index, oneHeader in enumerate(self.headerConfig):
			if oneHeader.get("CanFilter", False):
				for filterText, filterInfo in self.headerFilterInfo.get(index, {}).items():
					if filterText in oldHeaderFilterInfo.get(index, {}):
						filterInfo["isShow"] = oldHeaderFilterInfo[index][filterText]["isShow"]
		oldHeaderFilterInfo.clear()
		self.executeDelayedItemsLayout()

	def addData(self, data: list) -> None:
		if self.rootIsDecorated():
			return

		if not data:
			return

		self.scheduleDelayedItemsLayout()

		startRow = len(self.data)

		self.data.extend(data)

		for rowOffset, rowDict in enumerate(data):
			currentRow = startRow + rowOffset
			items = []

			for index, oneHeader in enumerate(self.headerConfig):
				text = rowDict.get(oneHeader.get("TextKey", ""), "")
				item = BaseItem(rowDict, text, currentRow)
				items.append(item)

				CanFilter = oneHeader.get("CanFilter", False)
				if CanFilter:
					if "FilterDecorate" in oneHeader:
						filterText = oneHeader["FilterDecorate"](rowDict)
					else:
						filterText = text
					if filterText:
						self.headerFilterInfo.setdefault(index, {}).setdefault(filterText, {"isShow": True, "rows": set()})["rows"].add(
							currentRow
						)

			self.itemModel.appendRow(items)

		self.executeDelayedItemsLayout()

	def clearData(self, clearChecked: bool = True) -> None:
		"""清理当前所有数据"""
		self.data = []
		if clearChecked:
			self.checkedRowsState.clear()
		self.selectedRowsState.clear()
		self._itemDeletegate.widgets.clear()
		self._itemDeletegate.notCheckableRows.clear()
		self.itemModel.removeRows(0, self.itemModel.rowCount())

	def checkAll(self, isChecked: bool) -> None:
		self.checkedRowsState.clear()
		if isChecked:
			for row, data in enumerate(self.data):
				if data.get("CanCheck", True):
					self.checkedRowsState.add(row)
		self._itemDeletegate.checkAll(isChecked)

	def checkRows(self, isChecked: bool, rows: list) -> None:
		for row in rows:
			if isChecked:
				self.checkedRowsState.add(row)
			else:
				self.checkedRowsState.discard(row)
		self._itemDeletegate.checkRows(isChecked, rows)

	def setCheckAbleRows(self, checkable: bool, rows: list) -> None:
		self._itemDeletegate.setCheckAbleRows(checkable, rows)

	def getDataRowByIndex(self, index: QModelIndex) -> int:
		sourceIndex = self.sortModel.mapToSource(index)
		return self.itemModel.itemFromIndex(sourceIndex).dataIndex

	def getWidgetByRowAndHeadIndex(self, row: int, headIndex: int) -> int:
		return self._itemDeletegate.getWidgetByRowAndHeadIndex(row, headIndex)

	def deleteRow(self, row: int) -> bool:
		if self.rootIsDecorated():
			return False

		if row < 0 or row >= len(self.data):
			return False

		self.data.pop(row)

		for itemRow in range(row, len(self.data)):
			for col in range(len(self.headerConfig)):
				sourceItem = self.itemModel.item(itemRow, col)
				if sourceItem:
					sourceItem.dataIndex = itemRow

		self.itemModel.removeRow(row)

		self.selectedRowsState.discard(row)
		self.checkedRowsState.discard(row)

		newSelectedRows = set()
		newCheckedRows = set()

		for selectedRow in self.selectedRowsState:
			if selectedRow < row:
				newSelectedRows.add(selectedRow)
			elif selectedRow > row:
				newSelectedRows.add(selectedRow - 1)

		for checkedRow in self.checkedRowsState:
			if checkedRow < row:
				newCheckedRows.add(checkedRow)
			elif checkedRow > row:
				newCheckedRows.add(checkedRow - 1)

		self.selectedRowsState = newSelectedRows
		self.checkedRowsState = newCheckedRows

		keysToRemove = []
		for key in list(self._itemDeletegate.widgets.keys()):
			widgetRow, _ = key
			if widgetRow == row:
				keysToRemove.append(key)
			elif widgetRow > row:
				oldWidget = self._itemDeletegate.widgets.pop(key)
				newKey = (widgetRow - 1, key[1])
				self._itemDeletegate.widgets[newKey] = oldWidget

		for key in keysToRemove:
			self._itemDeletegate.widgets.pop(key, None)

		return True

	def afterCheckDone(self, rows: list, isChecked: bool):
		self.afterCheckDoneFunc and self.afterCheckDoneFunc(rows, isChecked)

	def refreshRowView(self, row: int):
		for column in range(len(self.headerConfig)):
			key = (row, column)
			if key in self._itemDeletegate.widgets:
				widget = self._itemDeletegate.widgets[key]
				widget.refreshData(None)

	# endregion
