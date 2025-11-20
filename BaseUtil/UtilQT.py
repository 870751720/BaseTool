import functools

import six
from qtpy.QtCore import QObject, QRect, Qt, QTimer, Signal
from qtpy.QtGui import QFont, QFontMetrics


def calculateTextSize(text: str, width: int, font: QFont) -> tuple[int, int]:
	"""计算文本在指定宽度下的尺寸"""
	metrics = QFontMetrics(font)
	rect = metrics.boundingRect(QRect(0, 0, width, 0), Qt.TextWordWrap, text)
	return rect.width(), rect.height()


class QMetaSingleton(type(QObject)):
	def __call__(cls, *args, **kwargs):
		if not cls.__dict__.get("_instance"):
			cls._instance = type(QObject).__call__(cls, *args, **kwargs)
		return cls._instance


class QSingleton(six.with_metaclass(QMetaSingleton, QObject)):
	@classmethod
	def instance(cls):
		return cls()


class _DummyQObject(QSingleton):
	callInMainThreadSignal = Signal(object, object, object)  # func, args, kwargs

	def __init__(self) -> None:
		super(_DummyQObject, self).__init__()
		self._timers = set()
		self.callInMainThreadSignal.connect(self._onRequestCallInMainThread)

	def addTimer(self, singleShot=False, startTime=0, timeoutFunc=None) -> QTimer:
		if not singleShot:
			assert startTime > 0
		timer = QTimer(self)
		timer.setSingleShot(singleShot)
		timer.timeout.connect(lambda: self._onTimeout(timer, timeoutFunc))
		timer.start(startTime)
		self._timers.add(timer)
		return timer

	def clearTimer(self, timer) -> None:
		if timer in self._timers:
			self._timers.remove(timer)
			timer.stop()
			timer.deleteLater()

	def _onTimeout(self, timer, func) -> None:
		if timer.isSingleShot():
			self.clearTimer(timer)
		if func:
			func()

	@staticmethod
	def _onRequestCallInMainThread(func, args, kwargs) -> None:
		func(*args, **kwargs)


_dummyQObject = _DummyQObject()


class debounce(object):
	"""
	immediate 为 False 时,等待 wait 秒后执行函数,如果在这期间有新的调用,则不执行
	immediate 为 True 时,立刻执行函数, wait 秒内的后续调用都不会执行
	"""

	def __init__(self, wait: float, immediate: bool = False) -> None:
		assert wait > 0
		self._wait = int(wait * 1000)
		self._immediate = immediate
		self._fn = None

		self._timeout = None
		self._result = None
		self._args = None
		self._kwargs = None

	def __call__(self, fn):
		self._fn = fn

		@functools.wraps(fn)
		def decorated(*args, **kwargs):
			self._args = args
			self._kwargs = kwargs

			if self._timeout:
				self._timeout.stop()
			if self._immediate:
				callNow = not self._timeout
				self._timeout = self._create_timer(lambda: self._later(False), self._wait)
				if callNow:
					self._result = self._fn(*self._args, **self._kwargs)
			else:
				self._timeout = self._create_timer(lambda: self._later(True), self._wait)

			return self._result

		return decorated

	def _later(self, execute):
		self._timeout = None
		if execute:
			self._result = self._fn(*self._args, **self._kwargs)

	def cancel(self):
		self._timeout.stop()
		self._timeout = None

	@staticmethod
	def _create_timer(callback, delay):
		timer = QTimer(_dummyQObject)
		timer.setSingleShot(True)
		timer.timeout.connect(callback)
		timer.start(delay)
		return timer
