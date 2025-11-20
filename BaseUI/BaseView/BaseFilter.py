from functools import partial

from qtpy.QtCore import QEvent, QSize
from qtpy.QtWidgets import QLabel, QMenu

from BaseTool.BaseUI.BaseButton import BaseButton
from BaseTool.BaseUI.BaseCheck import BaseCheck
from BaseTool.BaseUI.BaseLabel import BaseLabel
from BaseTool.BaseUI.BaseLayout import HBoxLayout, VBoxLayout
from BaseTool.BaseUI.BaseLineEdit import BaseLineEdit
from BaseTool.BaseUI.BaseScroll import BaseScroll
from BaseTool.BaseUI.BaseStyle import NormalStyle
from BaseTool.BaseUI.BaseWidget import BaseWidget
from BaseTool.BaseUtil.UtilI18n import BASE_LH


class BaseFilter(QMenu):
	def __init__(
		self,
		data: dict = None,
		filterFunc: callable = None,
		changeLabel: QLabel = None,
	) -> None:
		super().__init__()
		self._data = data
		self._filterFunc = filterFunc
		self._changeLabel = changeLabel
		self._checkWidgets = {}
		self._searchText = ""

		self.setStyleSheet(NormalStyle.NORMAL_FILTER)
		self.setFixedSize(QSize(180, 180))
		mainLayout = VBoxLayout(True)
		self.setLayout(mainLayout)
		opLayout = HBoxLayout(True)
		filterButton = BaseButton(BASE_LH.TID_COMMON_SELECT_ALL, size=(30, 22))
		filterButton.clicked.connect(lambda: self._onCheckAll(True))
		cancelButton = BaseButton(BASE_LH.TID_COMMON_CANCEL, size=(30, 22))
		cancelButton.clicked.connect(lambda: self._onCheckAll(False))
		searchLine = BaseLineEdit(callback=self._onSearchTextChange)
		opLayout.addWidget(filterButton)
		opLayout.addWidget(cancelButton)
		opLayout.addWidget(searchLine)
		scrollArea = BaseScroll()
		contentWidget = BaseWidget()
		self.contentLayout = VBoxLayout(True, parent=contentWidget)
		scrollArea.setWidget(contentWidget)
		mainLayout.addLayout(opLayout)
		mainLayout.addWidget(scrollArea)

		self._updateData()

	def _updateData(self) -> None:
		self.contentLayout.clear()
		self._checkWidgets.clear()
		for filterText, filterInfo in self._data.items():
			if self._searchText and self._searchText not in filterText:
				continue
			layout = HBoxLayout(True)
			layout.addSpacing(5)
			self._checkWidgets[filterText] = checkWidget = BaseCheck(
				partial(self._onCheckClick, filterText),
				defaultVal=filterInfo["isShow"],
			)
			layout.addWidget(checkWidget)
			layout.addSpacing(5)
			layout.addWidget(BaseLabel(filterText))
			self.contentLayout.addLayout(layout)

	def mousePressEvent(self, event: QEvent) -> None:
		if self.contentLayout.parentWidget().geometry().contains(event.pos()):
			event.accept()
		else:
			super().mousePressEvent(event)

	def _onCheckClick(self, filterText: str, isCheck: bool) -> None:
		self._data[filterText]["isShow"] = isCheck
		allShow = True
		for oneFilterInfo in self._data.values():
			if not oneFilterInfo["isShow"]:
				allShow = False
				break
		self._changeLabel.setVisible(not allShow)
		self._filterFunc and self._filterFunc()

	def _onCheckAll(self, isCheck: bool) -> None:
		for filterText, filterInfo in self._data.items():
			filterInfo["isShow"] = isCheck
			self._checkWidgets[filterText].setCheckedWithoutTrigger(isCheck)
		self._changeLabel.setVisible(not isCheck)
		self._filterFunc and self._filterFunc()

	def _onSearchTextChange(self, text: str) -> None:
		self._searchText = text
		self._updateData()
