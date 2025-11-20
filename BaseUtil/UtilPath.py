import os
import sys


def isRunningAsExe() -> bool:
	return getattr(sys, "frozen", False)


def getExeAndResPath() -> tuple[str, str]:
	# exe 指的是工具目录，在代码运行的时候是指 main.py的父目录，exe运行的时候是指exe存放的文件夹
	# res 指的是调用资源目录，在代码运行的时候是指main.py的父目录，exe运行的是指_MEIPASS，即被打包进exe的资源路径
	path = os.path.normpath(os.path.dirname(sys.argv[0]))
	if isRunningAsExe():
		return path, os.path.normpath(sys._MEIPASS)
	else:
		return path, path
