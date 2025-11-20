from qtpy.QtCore import Qt
from qtpy.QtWidgets import QHBoxLayout, QVBoxLayout


class HBoxLayout(QHBoxLayout):
	def __init__(self, isEmpty=False, parent=None) -> None:
		super().__init__(parent)
		if isEmpty:
			self.setContentsMargins(0, 0, 0, 0)
			self.setSpacing(0)
		else:
			self.setContentsMargins(20, 0, 20, 0)
			self.setSpacing(10)

	def clear(self):
		while self.count():
			child = self.takeAt(0)
			if child.widget() is not None:
				child.widget().deleteLater()
			elif child.layout() is not None:
				child.layout().clear()


class VBoxLayout(QVBoxLayout):
	def __init__(self, isEmpty=False, parent=None) -> None:
		super().__init__(parent)
		self.setAlignment(Qt.AlignTop)
		if isEmpty:
			self.setContentsMargins(0, 0, 0, 0)
			self.setSpacing(0)
		else:
			self.setContentsMargins(20, 20, 20, 20)
			self.setSpacing(10)

	def clear(self):
		while self.count():
			child = self.takeAt(0)
			if child.widget() is not None:
				child.widget().deleteLater()
			elif child.layout() is not None:
				child.layout().clear()
