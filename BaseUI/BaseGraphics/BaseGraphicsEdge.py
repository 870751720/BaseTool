from qtpy.QtCore import QPointF, Qt
from qtpy.QtGui import QColor, QPen, QPainterPath, QPainter
from qtpy.QtWidgets import QGraphicsItem, QGraphicsPathItem, QStyleOptionGraphicsItem, QWidget


class BaseGraphicsEdge(QGraphicsPathItem):
	def __init__(self) -> None:
		super().__init__()

		self.posSource = [0, 0]
		self.posDestination = [200, 100]

		self.color = QColor("#efedd6")
		self.colorSelected = QColor("#00ff00")
		self.pen = QPen(self.color)
		self.penSelected = QPen(self.colorSelected)
		self.pen.setWidthF(3.0)
		self.penSelected.setWidthF(3.0)

		self._initView()

	def _initView(self) -> None:
		self.setFlag(QGraphicsItem.ItemIsSelectable)
		self.setAcceptHoverEvents(True)

	def updateConnectedEdges(self) -> None:
		pass

	def setSource(self, x: float, y: float) -> None:
		mpos = self.pos()
		self.posSource = [x - mpos.x(), y - mpos.y()]

	def setDestination(self, x: float, y: float) -> None:
		mpos = self.pos()
		self.posDestination = [x - mpos.x(), y - mpos.y()]

	def calcPath(self) -> QPainterPath:
		s = self.posSource
		d = self.posDestination
		dist = (d[0] - s[0]) * 0.5

		cpx_s = +dist
		cpx_d = -dist
		cpy_s = 0
		cpy_d = 0

		path = QPainterPath(QPointF(self.posSource[0], self.posSource[1]))
		path.cubicTo(s[0] + cpx_s, s[1] + cpy_s, d[0] + cpx_d, d[1] + cpy_d, self.posDestination[0], self.posDestination[1])

		return path

	def paint(self, painter: QPainter, QStyleOptionGraphicsItem: QStyleOptionGraphicsItem, widget: QWidget = None) -> None:
		self.setPath(self.calcPath())
		painter.setBrush(Qt.NoBrush)
		painter.setPen(self.pen if not self.isSelected() else self.penSelected)
		painter.drawPath(self.path())
