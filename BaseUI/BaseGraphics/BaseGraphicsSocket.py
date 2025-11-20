from qtpy.QtCore import QRectF
from qtpy.QtGui import QColor, QPen, QPainter, QBrush
from qtpy.QtWidgets import QGraphicsItem, QStyleOptionGraphicsItem, QWidget


class BaseGraphicsSocket(QGraphicsItem):
	def __init__(self) -> None:
		super().__init__()

		self.radius = 6.0
		self.outlineWidth = 1.0

		self.colorOutline = QColor("#FF000000")
		self.pen = QPen(self.colorOutline)
		self.pen.setWidthF(self.outlineWidth)
		self.colorBackground = QColor("#9fa09f")
		self.brush = QBrush(self.colorBackground)

	def boundingRect(self) -> QRectF:
		return QRectF(
			-self.radius - self.outlineWidth,
			-self.radius - self.outlineWidth,
			2 * (self.radius + self.outlineWidth),
			2 * (self.radius + self.outlineWidth),
		)

	def paint(self, painter: QPainter, QStyleOptionGraphicsItem: QStyleOptionGraphicsItem, widget: QWidget = None) -> None:
		painter.setBrush(self.brush)
		painter.setPen(self.pen)
		painter.drawEllipse(int(-self.radius), int(-self.radius), int(2 * self.radius), int(2 * self.radius))
