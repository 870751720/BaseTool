from qtpy.QtCore import QModelIndex
from qtpy.QtWidgets import QWidget

from BaseTool.BaseUI.BaseCheck import BaseCheck
from BaseTool.BaseUI.BaseIcon import BaseIcon
from BaseTool.BaseUI.BaseLabel import BaseLabel
from BaseTool.BaseUI.BaseLayout import HBoxLayout
from BaseTool.BaseUI.BaseLineEdit import BaseLineEdit
from BaseTool.BaseUI.BaseStyle import ImgRes, NormalStyle


class BaseViewWidget(QWidget):
	def __init__(
		self,
		index: QModelIndex,
		data: dict,
		config: dict,
		checkFunc: callable,
		hoverFunc: callable,
		row: int,
		isChecked: bool = False,
		checkable: bool = True,
	) -> None:
		super().__init__()
		self.data = data
		self.config = config
		mainLayout = HBoxLayout(True)
		mainLayout.addSpacing(5)
		contentWidget = QWidget()
		contentWidget.setStyleSheet("border-right:1px solid rgb(15,15,15);background-color:transparent;")
		innerLayout = HBoxLayout(True)

		isCenterAlign = config.get("CenterAlign", False)
		if isCenterAlign:
			innerLayout.addStretch()
		canCheck = config.get("CanCheck", False)
		self.configHoverFunc = configHoverFunc = config.get("HoverFunc", None)
		self.checkWidget = None
		self.icon = None
		if canCheck and data.get("CanCheck", True):
			checkFunc = config.get("CustomCheck", checkFunc)
			self.checkWidget = checkWidget = BaseCheck(
				lambda state: checkFunc(row, state), isChecked, hoverFunc=lambda checkBox: hoverFunc(row, configHoverFunc, checkBox)
			)
			innerLayout.addWidget(self.checkWidget)
			innerLayout.addSpacing(5)
			if not checkable:
				checkWidget.setStyleSheet(NormalStyle.DISABLE_CHECK)
				checkWidget.setDisabled(True)
		RowDecorate = config.get("RowDecorate", None)
		ClickFunc = config.get("ClickFunc", None)
		if RowDecorate:
			iconUrl, text = RowDecorate(data, index)
		else:
			iconUrl, text = data.get(config.get("IconKey", ""), None), data.get(config.get("TextKey", ""), None)
		if configHoverFunc:
			iconUrl = ImgRes.LINK
		if iconUrl:
			self.icon = icon = BaseIcon(iconUrl, config.get("IconSize", (20, 20)))
			innerLayout.addWidget(icon)
			if configHoverFunc:
				self.icon.setVisible(False)
			if ClickFunc:
				icon.clicked.connect(lambda: ClickFunc(data))
		if text or config.get("ForceLabel", False):
			text = str(text) if text else ""
			tip = data.get(config.get("Tip", ""), text)
			self.titleLabel = titleLabel = BaseLabel(text, style=NormalStyle.GRAY_LABEL, tooltip=tip)
			if ClickFunc:
				titleLabel.clickFunc = lambda: ClickFunc(data)
			innerLayout.addWidget(titleLabel)
		editKey = config.get("EditKey", None)
		if editKey:
			self.lineEdit = lineEdit = BaseLineEdit(width=230, placeHolder="", defaultText=data.get(editKey, ""))
			editCallback = config.get("EditCallback", None)
			if editCallback:
				lineEdit.setCallback(lambda text: editCallback(data, text))
			innerLayout.addWidget(lineEdit)

		innerLayout.addStretch()
		contentWidget.setLayout(innerLayout)
		mainLayout.addWidget(contentWidget)
		self.setLayout(mainLayout)

	def refreshData(self, index):
		data = self.data
		config = self.config
		RowDecorate = config.get("RowDecorate", None)
		if RowDecorate:
			iconUrl, text = RowDecorate(data, index)
		else:
			iconUrl, text = data.get(config.get("IconKey", ""), None), data.get(config.get("TextKey", ""), None)

		if self.icon:
			self.icon.setVisible(True if iconUrl else False)
		if not self.configHoverFunc and iconUrl:
			self.icon.changeIcon(iconUrl)
		if text:
			self.titleLabel.setText(text)
