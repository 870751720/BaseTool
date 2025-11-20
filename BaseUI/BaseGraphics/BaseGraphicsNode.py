from qtpy.QtCore import Qt, QRectF
from qtpy.QtGui import QColor, QPen, QFont, QPainterPath, QBrush, QPixmap, QCursor, QMouseEvent, QPainter
from qtpy.QtWidgets import QGraphicsItem, QGraphicsTextItem, QLabel, QStyleOptionGraphicsItem, QWidget

from BaseTool.BaseUI.BaseGraphics.BaseGraphicsEdge import BaseGraphicsEdge
from BaseTool.BaseUI.BaseGraphics.BaseGraphicsSocket import BaseGraphicsSocket
from BaseTool.BaseUI.BaseMenu import BaseMenu


class BaseGraphicsNode(QGraphicsItem):
	width = 160
	height = 140
	outline = 4
	nameHeight = 22

	def __init__(self) -> None:
		super().__init__()

		self.hovered = False
		self.content = None
		self.titleItem = None
		self.nameItem = None

		self.insocket = None
		self.outsocket = None
		self.inlines = []
		self.outlines = []

		self._initView()

	def _initView(self) -> None:
		self.setFlag(QGraphicsItem.ItemIsSelectable)
		self.setFlag(QGraphicsItem.ItemIsMovable)
		self.setAcceptHoverEvents(True)

		self.nameItem = nameItem = QGraphicsTextItem(self)
		nameItem.setDefaultTextColor(Qt.white)
		nameItem.setFont(QFont("Ubuntu", 9))
		nameItem.setPos(4, 0)
		nameItem.setTextWidth(self.width - 2 * 4)

	def contextMenuEvent(self, event: QMouseEvent) -> None:
		super().contextMenuEvent(event)

		menu = BaseMenu()
		menu.exec_(self.mapToGlobal(QCursor.pos()))

	def mouseMoveEvent(self, event: QMouseEvent) -> None:
		super().mouseMoveEvent(event)

		for node in self.scene().items():
			if node.isSelected():
				node.updateConnectedEdges()

	def boundingRect(self) -> QRectF:
		return QRectF(0, 0, self.width, self.height).normalized()

	def paint(self, painter: QPainter, QStyleOptionGraphicsItem: QStyleOptionGraphicsItem, widget: QWidget = None) -> None:
		pathTitle = QPainterPath()
		pathTitle.setFillRule(Qt.WindingFill)
		pathTitle.addRoundedRect(0, 0, self.width, self.nameHeight, self.outline, self.outline)
		pathTitle.addRect(0, self.nameHeight - self.outline, self.outline, self.outline)
		pathTitle.addRect(self.width - self.outline, self.nameHeight - self.outline, self.outline, self.outline)
		painter.setPen(Qt.NoPen)
		painter.setBrush(QBrush(QColor("#FF313131")))
		painter.drawPath(pathTitle.simplified())

		pathContent = QPainterPath()
		pathContent.setFillRule(Qt.WindingFill)
		pathContent.addRoundedRect(0, self.nameHeight, self.width, self.height - self.nameHeight, self.outline, self.outline)
		pathContent.addRect(0, self.nameHeight, self.outline, self.outline)
		pathContent.addRect(self.width - self.outline, self.nameHeight, self.outline, self.outline)
		painter.setPen(Qt.NoPen)
		painter.setBrush(QBrush(QColor("#E3212121")))
		painter.drawPath(pathContent.simplified())

		pathOutline = QPainterPath()
		pathOutline.addRoundedRect(0, 0, self.width, self.height, self.outline, self.outline)
		painter.setBrush(Qt.NoBrush)
		if self.hovered:
			painter.setPen(QPen(QColor("#FF37A6FF")))
			painter.drawPath(pathOutline.simplified())
		else:
			painter.setPen(QPen(QColor("#7F000000")) if not self.isSelected() else QPen(QColor("#FFFFA637")))
			painter.drawPath(pathOutline.simplified())

	def addInLine(self, inline: BaseGraphicsEdge) -> None:
		if self.insocket is None:
			self.insocket = BaseGraphicsSocket()
			gpos = self.pos()
			self.insocket.setPos(gpos.x(), gpos.y() + self.height / 2)
			self.scene().addItem(self.insocket)

		if inline not in self.inlines:
			self.inlines.append(inline)

		mpos = self.insocket.pos()
		inline.setDestination(mpos.x(), mpos.y())

	def addOutLine(self, outline: BaseGraphicsEdge) -> None:
		if self.outsocket is None:
			self.outsocket = BaseGraphicsSocket()
			gpos = self.pos()
			self.outsocket.setPos(gpos.x() + self.width, gpos.y() + self.height / 2)
			self.scene().addItem(self.outsocket)

		if outline not in self.outlines:
			self.outlines.append(outline)

		mpos = self.outsocket.pos()
		outline.setSource(mpos.x(), mpos.y())

	def updateConnectedEdges(self):
		gpos = self.pos()
		if self.insocket is not None:
			self.insocket.setPos(gpos.x(), gpos.y() + self.height / 2)
			mpos = self.insocket.pos()
			for line in self.inlines:
				line.setDestination(mpos.x(), mpos.y())
				line.update()

		if self.outsocket is not None:
			self.outsocket.setPos(gpos.x() + self.width, gpos.y() + self.height / 2)
			mpos = self.outsocket.pos()
			for line in self.outlines:
				line.setSource(mpos.x(), mpos.y())
				line.update()

	def setItemInfo(self, item):
		self.nameItem.setPlainText(item["Name"])

		if self.content is None:
			self.content = QLabel()
			self.content.setGeometry(30, self.nameHeight + 8, self.width - 60, self.width - 60)
			self.content.setAlignment(Qt.AlignCenter)
			content = self.scene().addWidget(self.content)
			content.setParentItem(self)
		objPixmap = QPixmap(item.get("Icon", None))
		self.content.setPixmap(objPixmap.scaled(self.content.width(), self.content.height()))

		if self.titleItem is None:
			self.titleItem = QLabel()
			content = self.scene().addWidget(self.titleItem)
			content.setParentItem(self)

		title = item["Title"]
		self.titleItem.setText(title)
		self.titleItem.setGeometry(0, -26, len(title) * 6 + 5, 20)
