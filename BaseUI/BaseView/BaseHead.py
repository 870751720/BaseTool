from qtpy.QtCore import Qt, QEvent, QObject, QRect
from qtpy.QtGui import QColor, QCursor, QPainter
from qtpy.QtWidgets import QHeaderView, QWidget

from BaseTool.BaseUI.BaseIcon import BaseIcon
from BaseTool.BaseUI.BaseLabel import BaseLabel
from BaseTool.BaseUI.BaseLayout import HBoxLayout
from BaseTool.BaseUI.BaseStyle import ImgRes
from BaseTool.BaseUI.BaseView.BaseFilter import BaseFilter


class BaseHeadView(QHeaderView):
	def __init__(self) -> None:
		super().__init__(Qt.Horizontal)
		self.setSectionsMovable(True)
		self.setSectionsClickable(True)
		self.setStretchLastSection(True)
		self.widgets = {}

	def leaveEvent(self, event: QEvent) -> None:
		self.setCursor(QCursor(Qt.ArrowCursor))
		super().leaveEvent(event)

	def mouseMoveEvent(self, event: QEvent) -> None:
		self.setCursor(QCursor(Qt.SplitHCursor))
		super().mouseMoveEvent(event)

	def eventFilter(self, obj: QObject, event: QEvent) -> bool:
		if event.type() == QEvent.MouseMove:
			self.setCursor(QCursor(Qt.ArrowCursor))
		return super().eventFilter(obj, event)

	def paintSection(self, painter: QPainter, rect: QRect, logicalIndex: int) -> None:
		painter.save()
		super().paintSection(painter, rect, logicalIndex)
		painter.restore()
		rightRect = rect.adjusted(rect.width() - 2, 0, 0, 0)
		painter.fillRect(rightRect, QColor(15, 15, 15))
		if logicalIndex in self.widgets:
			contentWidget = self.widgets[logicalIndex]
		else:
			config = self.parentWidget().headerConfig[logicalIndex]
			self.widgets[logicalIndex] = contentWidget = QWidget(self)
			contentWidget.setMouseTracking(True)
			contentWidget.installEventFilter(self)
			contentWidget.setStyleSheet("background-color:rgb(71,71,71);")
			layout = HBoxLayout(True)
			layout.addSpacing(5)
			label = BaseLabel(self.model().headerData(logicalIndex, Qt.Horizontal))
			layout.addWidget(label)
			canSort = config.get("CanSort", False)
			if canSort:
				contentWidget.sortButton = sortButton = BaseIcon(ImgRes.SORT)
				sortButton.clicked.connect(lambda: self._onSectionClicked(logicalIndex))
				layout.addWidget(sortButton)
			canFilter = config.get("CanFilter", False)
			if canFilter:
				contentWidget.changeLabel = changeLabel = BaseLabel("*")
				changeLabel.setVisible(False)
				filterButton = BaseIcon(ImgRes.FILTER, (22, 22))
				filterButton.clicked.connect(lambda: self._onFilterClick(logicalIndex))
				layout.addStretch()
				layout.addWidget(changeLabel)
				layout.addWidget(filterButton)
				layout.addSpacing(5)
			else:
				layout.addStretch()
			contentWidget.setLayout(layout)

		adjustedRect = rect.adjusted(0, 0, -2, 0)
		contentWidget.setGeometry(adjustedRect)
		contentWidget.show()

	def _onSectionClicked(self, logicalIndex: int) -> None:
		sortButton = self.widgets[logicalIndex].sortButton
		nextIcon = ImgRes.SORT_UP
		if sortButton.getIcon() == ImgRes.SORT_UP:
			nextIcon = ImgRes.SORT_DOWN
			self.parentWidget().sortByColumn(logicalIndex, Qt.DescendingOrder)
		else:
			self.parentWidget().sortByColumn(logicalIndex, Qt.AscendingOrder)
		sortButton.changeIcon(nextIcon)

	def _onFilterClick(self, logicalIndex: int) -> None:
		changeLabel = self.widgets[logicalIndex].changeLabel
		parentWidget = self.parentWidget()
		filterInfo = parentWidget.headerFilterInfo.get(logicalIndex, None)
		if filterInfo is None:
			return
		pos = self.mapToGlobal(self.widgets[logicalIndex].geometry().bottomRight())
		pos.setX(pos.x() - 22)
		menu = BaseFilter(filterInfo, parentWidget.onTriggerFilter, changeLabel)
		menu.exec_(pos)
