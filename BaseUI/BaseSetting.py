from functools import partial

from BaseTool.BaseUI.BaseButton import BaseButton
from BaseTool.BaseUI.BaseCheck import BaseCheck
from BaseTool.BaseUI.BaseDialog import BaseDialog
from BaseTool.BaseUI.BaseFilepick import BaseFilePick
from BaseTool.BaseUI.BaseLabel import BaseLabel
from BaseTool.BaseUI.BaseLayout import HBoxLayout, VBoxLayout
from BaseTool.BaseUI.BaseScroll import BaseScroll
from BaseTool.BaseUI.BaseStyle import NormalStyle
from BaseTool.BaseUI.BaseWidget import BaseWidget
from BaseTool.BaseUtil.UtilEnum import SettingType
from BaseTool.BaseUtil.UtilI18n import BASE_LH


class BaseSetting(BaseDialog):
	def __init__(self) -> None:
		super().__init__()
		self._settingConfigs = None
		self._updateFunc = None
		self._settingChange = {}
		self._settingLabels = {}

	def _design(self) -> None:
		scrollArea = BaseScroll()
		contentWidget = BaseWidget()
		self._contentLayout = VBoxLayout(parent=contentWidget)
		scrollArea.setWidget(contentWidget)

		self._mainLayout.addWidget(scrollArea)

		buttonLayout = HBoxLayout()
		self._cancelButton = BaseButton(BASE_LH.TID_COMMON_CANCEL)
		self._confirmButton = BaseButton(BASE_LH.TID_COMMON_CONFIRM, style=NormalStyle.BUTTON_MAIN)
		buttonLayout.addStretch()
		buttonLayout.addWidget(self._cancelButton)
		buttonLayout.addWidget(self._confirmButton)

		self._mainLayout.addStretch()
		self._mainLayout.addLayout(buttonLayout)
		self._mainLayout.addSpacing(20)

	def initSetting(self, settingConfigs: dict, updateFunc: callable) -> None:
		self._settingConfigs = settingConfigs
		self._updateFunc = updateFunc
		for settingName, settingConfig in settingConfigs.items():
			layout = HBoxLayout()
			layout.setContentsMargins(0, 0, 0, 0)
			settingType = settingConfig["settingType"]
			settingShowName = settingConfig["showName"]
			nowVal = settingConfig.get("nowVal", None)
			if settingType == SettingType.CHECK:
				self._settingLabels[settingName] = settingNameLabel = BaseLabel(settingShowName)
				layout.addWidget(settingNameLabel)
				layout.addStretch()
				settingCheck = BaseCheck(partial(self._onCheck, settingName), nowVal)
				layout.addWidget(settingCheck)
			elif settingType == SettingType.LINK:
				settingNameLabel = BaseLabel(settingShowName, clickFunc=settingConfig["clickFunc"])
				layout.addStretch()
				layout.addWidget(settingNameLabel)
			elif settingType == SettingType.FILE_PICK:
				self._settingLabels[settingName] = settingNameLabel = BaseLabel(settingShowName)
				layout.addWidget(settingNameLabel)
				layout.addStretch()
				settingFilePick = BaseFilePick(
					partial(self._onFilePick, settingName),
					nowVal,
					settingConfig["changeCheck"],
					settingConfig["isDir"],
				)
				layout.addWidget(settingFilePick)
			else:
				continue
			self._contentLayout.addLayout(layout)

	def _onCheck(self, settingName: str, state: bool) -> None:
		settingNameLabel = self._settingLabels[settingName]
		nowVal = self._settingConfigs[settingName]["nowVal"]
		settingShowName = self._settingConfigs[settingName]["showName"]
		if state != nowVal:
			settingNameLabel.setText("*" + settingShowName)
			self._settingChange[settingName] = state
		else:
			settingNameLabel.setText(settingShowName)
			self._settingChange.pop(settingName, None)

	def _onFilePick(self, settingName: str, filePath: str) -> None:
		settingNameLabel = self._settingLabels[settingName]
		nowVal = self._settingConfigs[settingName]["nowVal"]
		settingShowName = self._settingConfigs[settingName]["showName"]
		if filePath != nowVal:
			settingNameLabel.setText("*" + settingShowName)
			self._settingChange[settingName] = filePath
		else:
			settingNameLabel.setText(settingShowName)
			self._settingChange.pop(settingName, None)

	def _titleName(self) -> str:
		return BASE_LH.TID_COMMON_SETTING

	def _getSize(self) -> tuple[int, int]:
		return 480, 400

	def _bindEvent(self) -> None:
		self._cancelButton.clicked.connect(self.reject)
		self._confirmButton.clicked.connect(self.accept)

	def reject(self) -> None:
		super().reject()
		self._settingLabels.clear()

	def accept(self) -> None:
		super().accept()
		self._updateFunc(self._settingChange)
