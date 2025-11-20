import cgitb
import functools
import multiprocessing
import os
import sys
import threading
import time
import traceback
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor


class Singleton(type):
	_instanceLock = threading.Lock()

	def __init__(cls, *args, **kwargs) -> None:
		super().__init__(*args, **kwargs)

	def __call__(cls, *args, **kwargs) -> None:
		if not hasattr(cls, "instance_dict"):
			Singleton.instanceDict = {}

		if str(cls) not in Singleton.instanceDict.keys():
			with Singleton._instanceLock:
				_instance = super().__call__(*args, **kwargs)
				Singleton.instanceDict[str(cls)] = _instance

		return Singleton.instanceDict[str(cls)]


class ErrorHook(cgitb.Hook):
	def __init__(
		self,
		display: int = 1,
		logdir: str = None,
		context: int = 5,
		file: str = None,
		format: str = "html",
		callback: callable = None,
	):
		super().__init__(display, logdir, context, file, format)
		self._callback = callback

	def handle(self, info: tuple = None) -> None:
		info = info or sys.exc_info()
		try:
			doc = cgitb.text(info, self.context)
		except:
			doc = "".join(traceback.format_exception(*info))
		if "KeyboardInterrupt" in str(info) or "ConnectionResetError" in str(info):
			return
		fd = os.path.join(self.logdir, str(time.time()) + ".txt")
		try:
			with open(fd, "a") as f:
				f.write(doc)
		except:
			pass
		self._callback and self._callback(doc)


def timeCost(func):
	@functools.wraps(func)
	def wrapper(*args, **kwargs):
		startTime = time.time()
		result = func(*args, **kwargs)
		endTime = time.time()
		execution_time = endTime - startTime
		print(f"Function '{func.__name__}' executed in {execution_time:.4f} seconds")
		return result

	return wrapper


def doFuncsByThreadpool(worker, argsList):
	results = []
	with ThreadPoolExecutor() as executor:
		futures = [executor.submit(worker, args) for args in argsList]
		for future in futures:
			results.append(future.result())
	return results


def doFuncsByMultiprocessing(worker, argsList, count_split=1):
	with ProcessPoolExecutor(max_workers=int(multiprocessing.cpu_count() / count_split)) as executor:
		results = list(executor.map(worker, argsList))

	return results
