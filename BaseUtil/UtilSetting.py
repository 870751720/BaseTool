import json
import os
import pickle
import shutil
import sys

import BaseTool.BaseUtil.UtilI18n
from BaseTool.BaseUI.BaseSetting import BaseSetting
from BaseTool.BaseUtil.UtilCommon import ErrorHook, Singleton
from BaseTool.BaseUtil.UtilEnum import PackType, SettingType
from BaseTool.BaseUtil.UtilPath import getExeAndResPath
from BaseTool.BaseUtil.UtilReload import reloadPy


def onLanguageChange(isEnglish: bool) -> None:
	BaseTool.BaseUtil.UtilI18n.isEnglish = isEnglish


def onReload() -> None:
	reloadPy()


class GlobalSetting(metaclass=Singleton):
	BASE_GLOBAL_SETTING = {
		"isEnglish": {
			"name": "TID_COMMON_LANGUAGE_CHANGE",
			"default": False,
			"onChange": onLanguageChange,
			"onLoad": onLanguageChange,
			"settingType": SettingType.CHECK,
		},
	}

	BASE_LINK_FUNC = {
		"reload": {
			"name": "TID_COMMON_RELOAD",
			"clickFunc": onReload,
			"settingType": SettingType.LINK,
		},
	}

	APP_GLOBAL_SETTING = {}
	APP_LINK_FUNC = {}

	def __init__(self, toolName: str = "EasyTool") -> None:
		self._toolName = toolName
		self._initSetting()
		self._initPath()
		self._initPathPost()
		self._initPack()
		self._initConfig()
		self._initConfigPost()
		self._initCustom()

	def _initSetting(self) -> None:
		pass

	def _initPath(self) -> None:
		# exe 指的是工具目录，在代码运行的时候是指 main.py的父目录，exe运行的时候是指exe存放的文件夹
		# res 指的是调用资源目录，在代码运行的时候是指main.py的父目录，exe运行的是指_MEIPASS，即被打包进exe的资源路径
		# dataPath 指的是数据存放总目录
		self.exePath, self.resPath = getExeAndResPath()
		self.dataPath = os.path.join(os.environ["APPDATA"], self._toolName)

	def _initPathPost(self) -> None:
		if not os.path.exists(self.dataPath):
			os.mkdir(self.dataPath)

	def _initPack(self) -> None:
		packTypeFile = os.path.join(self.exePath, "packType.txt")
		if not os.path.exists(packTypeFile):
			self.packType = PackType.CODE
			return
		with open(packTypeFile, "r", encoding="utf-8") as f:
			self.packType = int(f.read())

	def _initConfig(self) -> None:
		pass

	def _initConfigPost(self) -> None:
		pass

	def loadSetting(self) -> None:
		self._settingPath = os.path.join(self.dataPath, "setting.json")
		setting = {}
		if os.path.exists(self._settingPath):
			with open(self._settingPath, "r", encoding="utf-8") as f:
				setting = json.load(f)
		totalSetting = self.BASE_GLOBAL_SETTING | self.APP_GLOBAL_SETTING
		for settingName, settingConfig in totalSetting.items():
			settingValue = setting.get(settingName, settingConfig["default"])
			setattr(self, settingName, settingValue)
			onLoad = settingConfig.get("onLoad", None)
			if onLoad is not None:
				onLoad(settingValue)

		self._loadSettingPost()

	def _loadSettingPost(self) -> None:
		errorPath = os.path.join(self.dataPath, "errors")
		if self.packType == PackType.CODE:
			if os.path.exists(errorPath):
				try:
					shutil.rmtree(errorPath)
				except:
					pass
		os.makedirs(errorPath, exist_ok=True)

		sys.excepthook = ErrorHook(display=0, logdir=errorPath, format="text", callback=self._onErrorHook)

	def _initCustom(self) -> None:
		self._customData = {}
		self._customPath = customPath = os.path.join(self.dataPath, "custom.data")
		if os.path.exists(customPath):
			try:
				with open(customPath, "rb") as f:
					self._customData = pickle.load(f)
			except:
				pass

	def getCustomKey(self, key: str, default: None = None) -> None:
		return self._customData.get(key, default)

	def setCustomKey(self, key: str, val: None) -> None:
		self._customData[key] = val
		with open(self._customPath, "wb") as f:
			pickle.dump(self._customData, f)

	def setCustomKeyByDict(self, setDict: dict) -> None:
		for key, val in setDict.items():
			self._customData[key] = val
		with open(self._customPath, "wb") as f:
			pickle.dump(self._customData, f)

	def _onErrorHook(self, info: str) -> None:
		pass

	def updateSetting(self, newSetting: dict) -> None:
		setting = {}
		totalSetting = self.BASE_GLOBAL_SETTING | self.APP_GLOBAL_SETTING

		for settingName, settingConfig in totalSetting.items():
			if settingName not in newSetting:
				setting[settingName] = getattr(self, settingName)
				continue
			newValue = newSetting[settingName]
			settingConfig = totalSetting[settingName]
			changeCheck = settingConfig.get("changeCheck", None)
			if changeCheck and not changeCheck(newValue):
				setting[settingName] = getattr(self, settingName)
				continue
			if settingName in setting and newValue == setting[settingName]:
				continue
			setting[settingName] = newValue
			setattr(self, settingName, newValue)
			onChange = settingConfig.get("onChange", None)
			if onChange is not None:
				onChange(newValue)

		with open(self._settingPath, "w", encoding="utf-8") as f:
			json.dump(setting, f, ensure_ascii=False, indent=4)

		for settingName, settingConfig in totalSetting.items():
			if settingName not in newSetting:
				continue
			afterAllChangeDone = settingConfig.get("afterAllChangeDone", None)
			afterAllChangeDone and afterAllChangeDone()

	def openSetting(self) -> None:
		baseSettingDialog = BaseSetting()
		settingConfig = {}
		totalSetting = self.APP_GLOBAL_SETTING | self.BASE_GLOBAL_SETTING | self.BASE_LINK_FUNC | self.APP_LINK_FUNC
		languageHelper = self.getToolLanguageHelper()
		for settingName, settingConfig in totalSetting.items():
			settingConfig[settingName] = settingConfig
			if settingConfig["settingType"] != SettingType.LINK:
				settingConfig["nowVal"] = getattr(self, settingName)
			settingConfig["showName"] = getattr(languageHelper, settingConfig["name"])

		baseSettingDialog.initSetting(totalSetting, self.updateSetting)
		baseSettingDialog.exec()

	def getToolLanguageHelper(self) -> None:
		from BaseTool.BaseUtil.UtilI18n import BASE_LH  # 翻译可能被项目文件重载

		return BASE_LH

	def doExit(self) -> None:
		os._exit(0)


GS = None
# GS = GlobalSetting(), 如果工具不需要独立的设置，那么就把这个打开就好
