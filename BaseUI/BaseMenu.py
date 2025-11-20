from functools import partial

from qtpy.QtWidgets import QMenu

from BaseTool.BaseUI.BaseStyle import NormalStyle


class BaseMenu(QMenu):
	def __init__(self) -> None:
		super().__init__()
		self.setStyleSheet(NormalStyle.NORMAL_MENU)
		self.setFixedWidth(210)

	def loadAction(self, actionConfig: list, checkData: list = None) -> None:
		# actionConfig: [] "name": str, "Callback": callable, "AllSelected": bool, "CanAction": callable
		spaces = "      "
		for one in actionConfig:
			if isinstance(one, str):
				self.addAction(one)
				self.addSeparator()
			else:
				canAction = one.get("CanAction", None)
				isAllSelected = one.get("AllSelected", False)
				if not isAllSelected:
					needData = checkData[0]
				else:
					needData = checkData[1]
				if canAction:
					if not isAllSelected:
						if not canAction(needData):
							continue
					else:
						needData = []
						for each in checkData[1]:
							if canAction(each):
								needData.append(each)
						if not needData:
							continue
				callback = one["Callback"]
				action = self.addAction(spaces + one["Name"])
				action.triggered.connect(partial(callback, needData))
