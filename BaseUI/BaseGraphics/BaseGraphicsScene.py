import math

from qtpy.QtCore import QLine, QRectF
from qtpy.QtGui import QColor, QPen, QFont, QPainter
from qtpy.QtWidgets import QGraphicsScene


class BaseGraphicsScene(QGraphicsScene):
	def __init__(self) -> None:
		super().__init__()

		self.setItemIndexMethod(QGraphicsScene.NoIndex)
		self.gridSize = 20
		self.gridSquares = 5
		self.textureItem = None

		self.colorBackground = QColor("#393939")
		self.colorLight = QColor("#2f2f2f")
		self.colorDark = QColor("#292929")
		self.colorState = QColor("#ccc")

		self.penLight = QPen(self.colorLight)
		self.penLight.setWidth(1)
		self.penDark = QPen(self.colorDark)
		self.penDark.setWidth(2)

		self.penState = QPen(self.colorState)
		self.fontState = QFont("Ubuntu", 16)

		self.setBackgroundBrush(self.colorBackground)

	def setGrScene(self, width: float, height: float) -> None:
		self.setSceneRect(-width // 2, -height // 2, width, height)

	def drawBackground(self, painter: QPainter, rect: QRectF) -> None:
		super().drawBackground(painter, rect)

		left = int(math.floor(rect.left()))
		right = int(math.ceil(rect.right()))
		top = int(math.floor(rect.top()))
		bottom = int(math.ceil(rect.bottom()))

		firstLeft = left - (left % self.gridSize)
		firstTop = top - (top % self.gridSize)

		linesLight, linesDark = [], []
		for x in range(firstLeft, right, self.gridSize):
			if x % (self.gridSize * self.gridSquares) != 0:
				linesLight.append(QLine(x, top, x, bottom))
			else:
				linesDark.append(QLine(x, top, x, bottom))

		for y in range(firstTop, bottom, self.gridSize):
			if y % (self.gridSize * self.gridSquares) != 0:
				linesLight.append(QLine(left, y, right, y))
			else:
				linesDark.append(QLine(left, y, right, y))

		painter.setPen(self.penLight)
		painter.drawLines(linesLight)

		painter.setPen(self.penDark)
		painter.drawLines(linesDark)
