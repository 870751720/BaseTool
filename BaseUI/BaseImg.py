from qtpy.QtCore import QSize, Qt
from qtpy.QtGui import QPixmap
from qtpy.QtWidgets import QLabel, QSizePolicy


class BaseImg(QLabel):
	def __init__(
		self, imageUrl: str = "", size: tuple[int, int] = (240, 240), scaleMode: Qt.AspectRatioMode = Qt.KeepAspectRatio
	) -> None:
		super().__init__()

		sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(0)
		self.setSizePolicy(sizePolicy)

		self.setFixedSize(QSize(*size))

		self.setAlignment(Qt.AlignCenter)

		self.setScaledContents(False)

		self._imageUrl = imageUrl
		self._size = size
		self._scaleMode = scaleMode

		if imageUrl:
			self.setImage(imageUrl)

	def setImage(self, imageUrl: str):
		"""设置图片"""
		self._imageUrl = imageUrl
		if imageUrl:
			pixmap = QPixmap(imageUrl)
			scaledPixmap = pixmap.scaled(QSize(*self._size), self._scaleMode, Qt.SmoothTransformation)
			self.setPixmap(scaledPixmap)
		else:
			self.clear()

	def changeImage(self, imageUrl: str):
		self.setImage(imageUrl)

	def getImage(self) -> str:
		return self._imageUrl
