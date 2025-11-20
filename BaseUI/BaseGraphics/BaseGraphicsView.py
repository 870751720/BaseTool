import time

from qtpy.QtCore import Signal, Qt, QEvent
from qtpy.QtGui import QPainter, QMouseEvent
from qtpy.QtWidgets import QGraphicsView, QGraphicsItem

from BaseTool.BaseUI.BaseGraphics.BaseGraphicsScene import BaseGraphicsScene


class BaseGraphicsView(QGraphicsView):
	itemDoubleClicked = Signal(QGraphicsItem)

	def __init__(self) -> None:
		super().__init__()

		self.zoomInFactor = 1.25
		self.zoomClamp = True
		self.zoom = 10
		self.zoomStep = 1
		self.zoomRange = [0, 5]
		self.lastClickItem = None
		self.lastPressItem = None
		self.lastClickTime = time.time()

		self._initView()

	def _initView(self) -> None:
		scene = BaseGraphicsScene()
		scene.setGrScene(40000, 40000)

		self.setScene(scene)
		self.setStyleSheet("padding:0px;border:0px")
		self.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing | QPainter.SmoothPixmapTransform)

		self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)

		self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

		self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
		self.setDragMode(QGraphicsView.RubberBandDrag)

	def mousePressEvent(self, event: QMouseEvent) -> None:
		if event.button() == Qt.MiddleButton:
			self.middleMouseButtonPress(event)
		elif event.button() == Qt.LeftButton:
			self.leftMouseButtonPress(event)
		elif event.button() == Qt.RightButton:
			self.rightMouseButtonPress(event)
		else:
			super().mousePressEvent(event)

	def mouseReleaseEvent(self, event: QMouseEvent) -> None:
		if event.button() == Qt.MiddleButton:
			self.middleMouseButtonRelease(event)
		elif event.button() == Qt.LeftButton:
			self.leftMouseButtonRelease(event)
		elif event.button() == Qt.RightButton:
			self.rightMouseButtonRelease(event)
		else:
			super().mouseReleaseEvent(event)

	def rightMouseButtonPress(self, event: QMouseEvent) -> None:
		releaseEvent = QMouseEvent(
			QEvent.MouseButtonRelease, event.position(), event.scenePosition(), Qt.LeftButton, Qt.NoButton, event.modifiers()
		)
		super().mouseReleaseEvent(releaseEvent)
		self.setDragMode(QGraphicsView.ScrollHandDrag)
		fakeEvent = QMouseEvent(
			QEvent.MouseButtonPress,
			event.position(),
			event.scenePosition(),
			Qt.LeftButton,
			event.buttons() | Qt.LeftButton,
			event.modifiers(),
		)
		super().mousePressEvent(fakeEvent)

	def rightMouseButtonRelease(self, event: QMouseEvent) -> None:
		fakeEvent = QMouseEvent(
			QEvent.MouseButtonRelease,
			event.position(),
			event.scenePosition(),
			Qt.LeftButton,
			event.buttons() & ~Qt.LeftButton,
			event.modifiers(),
		)
		super().mouseReleaseEvent(fakeEvent)
		self.setDragMode(QGraphicsView.RubberBandDrag)

	def middleMouseButtonPress(self, event: QMouseEvent) -> None:
		super().mousePressEvent(event)

	def middleMouseButtonRelease(self, event: QMouseEvent) -> None:
		super().mouseReleaseEvent(event)

	def leftMouseButtonPress(self, event: QMouseEvent) -> None:
		self.lastPressItem = self.getItemAtClick(event)
		super().mousePressEvent(event)

	def leftMouseButtonRelease(self, event: QMouseEvent) -> None:
		item = self.getItemAtClick(event)
		if item is not None and item == self.lastPressItem:
			if item == self.lastClickItem and time.time() - self.lastClickTime < 0.5:
				self.itemDoubleClicked.emit(item)
			else:
				self.lastClickItem = item
				self.lastClickTime = time.time()

		super().mouseReleaseEvent(event)

	def getItemAtClick(self, event: QMouseEvent) -> QGraphicsItem:
		pos = event.pos()
		obj = self.itemAt(pos)
		return obj

	def wheelEvent(self, event: QMouseEvent):
		zoomOutFactor = 1 / self.zoomInFactor

		if event.angleDelta().y() > 0:
			zoomFactor = self.zoomInFactor
			self.zoom += self.zoomStep
		else:
			zoomFactor = zoomOutFactor
			self.zoom -= self.zoomStep

		clamped = False
		if self.zoom < self.zoomRange[0]:
			self.zoom, clamped = self.zoomRange[0], True
		if self.zoom > self.zoomRange[1]:
			self.zoom, clamped = self.zoomRange[1], True

		if not clamped or self.zoomClamp is False:
			self.scale(zoomFactor, zoomFactor)
