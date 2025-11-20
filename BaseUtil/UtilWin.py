import os
import socket
import subprocess
import uuid
import psutil
import win32con
import winreg


def getMacAddress() -> str:
	mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
	return ":".join([mac[e: e + 2] for e in range(0, 11, 2)])


def getHostIp() -> str:
	hostname = socket.gethostname()
	return socket.gethostbyname(hostname)


def getAllIps() -> dict:
	return {addr.address for addrs in psutil.net_if_addrs().values() for addr in addrs if addr.family == socket.AF_INET}


def netIsUsed(ipPort: tuple) -> bool:
	"""判断端口是否占用"""
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		s.connect(ipPort)
		s.shutdown(2)
		return True
	except Exception as e:
		print("net is used, " + str(e))
		return False


def getExeExistNum(exeName):
	"""获得exe名运行数量"""
	checkCmd = 'tasklist /nh /fi "Imagename eq %s"' % exeName
	with subprocess.Popen(checkCmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as proc:
		coms = proc.communicate()
		if coms[0]:
			res = coms[0].decode("gbk")
			return res.count(exeName)
	return 0


def registerMenu(keyName: str, abspath: str, icon: str) -> bool:
	"""注册右键菜单"""
	keyNameCommand = os.path.join(keyName, "command")
	regFlags = win32con.WRITE_OWNER | win32con.KEY_WOW64_64KEY | win32con.KEY_ALL_ACCESS
	try:
		key = winreg.OpenKey(win32con.HKEY_CURRENT_USER, keyName, 0, regFlags)
	except FileNotFoundError as e:
		try:
			key = winreg.CreateKey(win32con.HKEY_CURRENT_USER, keyName)
		except:
			return False
	except:
		return False

	try:
		location, _ = winreg.QueryValueEx(key, "Icon")
		if location != icon:
			winreg.SetValueEx(key, "Icon", 0, winreg.REG_SZ, icon)
	except FileNotFoundError as e:
		try:
			winreg.SetValueEx(key, "Icon", 0, winreg.REG_SZ, icon)
		except:
			return False
	except:
		return False

	cmdCommit = abspath
	try:
		winreg.OpenKey(win32con.HKEY_CURRENT_USER, keyNameCommand, 0, regFlags)
	except FileNotFoundError as e:
		try:
			winreg.CreateKey(win32con.HKEY_CURRENT_USER, keyNameCommand)
			winreg.SetValue(key, "command", winreg.REG_SZ, cmdCommit)
		except:
			return False
	except:
		return False

	try:
		location = winreg.QueryValue(key, "command")
		if location != cmdCommit:
			winreg.SetValue(key, "command", winreg.REG_SZ, cmdCommit)
	except FileNotFoundError as e:
		try:
			winreg.SetValue(key, "command", winreg.REG_SZ, cmdCommit)
		except:
			return False
	except:
		return False

	winreg.CloseKey(key)


def unregisterMenu(keyName: str) -> bool:
	"""取消右键菜单"""
	try:
		winreg.DeleteKey(win32con.HKEY_CURRENT_USER, keyName + "\\command")
		winreg.DeleteKey(win32con.HKEY_CURRENT_USER, keyName)
	except FileNotFoundError:
		pass
	except:
		return False
	return True


def openFileInExplorer(filePath):
	"""从资源管理器打开文件"""
	filePath = os.path.normpath(filePath)
	while True:
		if os.path.exists(filePath):
			break
		dirPath = os.path.dirname(filePath)
		if dirPath == filePath:
			break
		filePath = dirPath
	if os.path.exists(filePath):
		if os.path.isdir(filePath):
			os.system(r"explorer {}".format(filePath))
		else:
			os.system(r"explorer /select, {}".format(filePath))
