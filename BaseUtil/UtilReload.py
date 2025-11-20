# -*- encoding:utf-8 -*-
"""----------------------------------------------------------------------------
Description:
	简单理解为“旧瓶装新酒”，module、class、func指针均不变，变的只是func的实现。
	1、直接运行本文件的reload()接口，更新全部脚本文件。建议不要单个文件更新，依赖关系不好解决。
	2、默认会更新相关module里面的class和func
	3、默认不更新module里面的全局变量，如果需要请自行在文件里面定义_reload_all = True或者在本文件all_reload_modules里面定义
	4、对于Data类数据，不要直接从module import里面的Data数据，import 模块名即可，
		否则更新后会报类似错误“TypeError: descriptor 'radarType' for 'MagicFieldData' objects doesn't apply to 'MagicFieldData' object”
	5、对于class的全局数据，默认是不更新的，如果需要更新请在class中定义_reload_all = True
	6、reload过程中需要避开的逻辑请使用sys.reloading判断规避
	7、各模块在reload前后需要逻辑处理的，请注册reg_reload_operation_func
	8、See PEP 302 for details of import hooks
----------------------------------------------------------------------------"""

import imp
import importlib
import inspect
import os
import sys
import time
from gc import collect as gccollect
from gc import disable as gcdisable
from gc import enable as gcenable
from importlib import abc

# 定义不需要更新的模块
ignoreModules = []

ignoreAttrs = {
	"__module__",
	"_reload_all",
	"__dict__",
	"__weakref__",
	"__doc__",
	"__dir__",
}

allReloadModules = set()
# reload函数回调，参数是bool，True表示开始，False表示结束
reloadOperationFuncList = {}


def regReloadOperationFunc(tag, func):
	if tag not in reloadOperationFuncList:
		reloadOperationFuncList[tag] = func


def execReloadOperationFunc(start):
	for func in reloadOperationFuncList.values():
		func(start)


def _fitRules(string, rules):
	for rule in rules:
		if hasattr(rule, "search"):
			if rule.search(string) is not None:
				return True
		elif string == rule:
			return True
	return False


class finder(object):
	def setupOldModule(self, name):
		oldModule = self.getOldModule(name)
		if not oldModule:
			return

		oldModule.__dict__.pop("_reload_all", None)
		sys.modules[name] = oldModule  # for imp.load_module to reload the module

	def modifyModule(self, name, module):
		modifyModule = getattr(sys, "modifyModule", None)
		if not modifyModule:
			return module

		return modifyModule(name, module)

	def getOldModule(self, name):
		getOldModule = getattr(sys, "getOldModule", None)
		if not getOldModule:
			return

		return getOldModule(name)


class builtinFinder(finder):
	def findSpec(self, fullName, path, target=None):
		try:
			module = None
			for name in fullName.split("."):
				module = self.getModule(name, module)

			if module:
				from importlib import util

				spec = util.spec_from_loader(fullName, loader(module))
				# flynn 2017/2/15: 下面这句trick太关键了！看3.4.0的源码实现，在回调find_spec之前如果module没有在sys.modules里面，
				# 会判定is_reload为False，然后返回的这个spec就没有意义了。但是源码中看到如果module.__spec__有值，还是可以生效的。
				module.__spec__ = spec
				return spec

			return None
		except ImportError:
			oldModule = self.getOldModule(fullName)
			if oldModule:
				print("unchanged module", fullName)
				spec = importlib.util.spec_from_loader(fullName, loader(oldModule))
				oldModule.__spec__ = spec
				return spec
			else:
				raise

	def getModule(self, name, parent):
		parentName = getattr(parent, "__name__", "")
		parentPath = getattr(parent, "__path__", None)

		if parentName:
			fullName = parentName + "." + name
		else:
			fullName = name

		module = sys.modules.get(fullName)
		if module:
			return module

		return self.createModule(name, fullName, parentPath)

	def createModule(self, name, fullName, parentPath):
		self.setupOldModule(fullName)
		if parentPath:
			parentPath = list(parentPath)
		fd, path, des = imp.find_module(name, parentPath)
		module = imp.load_module(fullName, fd, path, des)

		self.modifyModule(fullName, module)
		return module


class loader(abc.Loader):
	def __init__(self, module):
		self.module = module

	def load_module(self, fullname):
		return self.module


_oldModules = {}
_moduleInfos = {}
sys._lastReloadTime = time.time()  # 进程启动的时候记录当前时间，避免第一次全量更新


def reloadPy(names=None):
	import sys

	lastReloadTime = getattr(sys, "_lastReloadTime", 0)
	if not lastReloadTime:
		sys._lastReloadTime = 0

	oldSysMetaPath = sys.meta_path
	sys.meta_path = [builtinFinder()]

	execReloadOperationFunc(True)
	print("********** start reload script ***************")

	gcdisable()

	global _oldModules
	global _moduleInfos

	_oldModules = dict(sys.modules)
	storeModuleInfos()

	sys.getOldModule = getOldModule
	sys.modifyModule = modifyModule
	sys.reloading = True

	modules = getReloadModifiedModules(names, lastReloadTime)

	for name in modules:  # pop the module to be reloaded
		if name in sys.modules:
			sys.modules.pop(name)

	for name in modules:
		if name == __name__:
			continue
		try:
			importlib.import_module(name)
		except Exception as e:
			print("********** reload script failed in module %s %s ***************\n%s" % (name, type(e), e))
			sys.modules.update(_oldModules)
			raise

	import sys

	sys.getOldModule = None
	sys.modifyModule = None
	sys.reloading = False

	_oldModules = None
	_moduleInfos = {}

	gcenable()
	gccollect()
	print("********** reload script successed ***************")

	sys.meta_path = oldSysMetaPath
	execReloadOperationFunc(False)


def getReloadModules(names):
	result = []
	names = names or _oldModules.keys()

	for name in names:
		module = sys.modules[name]

		if isIgnoredModule(module):
			continue

		if not _fitRules(name, ignoreModules):
			module = _oldModules.get(name)
			if inspect.ismodule(module) and getattr(module, "__file__", None):
				result.append(name)

	return result


def isIgnoredModule(module):
	moduleFile = getattr(module, "__file__", None)
	if not moduleFile:
		return True
	moduleFile = os.path.normpath(moduleFile)
	sysPaths = tuple(sys.path[:])
	return not moduleFile.endswith(".py") or not moduleFile.startswith(sysPaths)


def getReloadModifiedModules(names, lastReloadTime):
	result = set()
	names = names or _oldModules.keys()

	for name in names:
		modifytime = 0
		module = _oldModules.get(name)
		if isIgnoredModule(module) or _fitRules(name, ignoreModules) or name.endswith(".img_qss_rc"):
			continue
		filename, extension = os.path.splitext(module.__file__)
		try:
			if os.path.exists(filename + ".py"):
				filename += ".py"
			elif os.path.exists(filename + ".pyc"):
				filename += ".pyc"
			elif os.path.exists(filename + ".pyo"):
				filename += ".pyo"
			elif not os.path.exists(module.__file__):
				continue

			modifytime = os.stat(filename).st_mtime
			pyfile = os.path.splitext(module.__file__)[0] + ".py"
			if os.path.exists(pyfile):
				modifytime = max(modifytime, os.stat(pyfile).st_mtime)
		except OSError as e:
			sys.stderr.write("Failed To Check Module %s Because %s\n" % (name, str(e)))

		if lastReloadTime < modifytime:
			result.add(name)
			if modifytime > sys._lastReloadTime:
				sys._lastReloadTime = modifytime

	return result


def storeModuleInfos():
	for name, module in _oldModules.items():
		if module:
			_moduleInfos[name] = dict(module.__dict__)


def getOldModule(name):
	return _oldModules.get(name)


def modifyModule(name, module):
	oldInfos = _moduleInfos.get(name)
	if not oldInfos:
		return module

	print("reload module", name)
	updateModule(
		oldInfos,
		module,
		getattr(module, "_reload_all", False) or _fitRules(name, allReloadModules),
	)

	return module


def updateModule(oldAttrs, module, reloadAll):
	for name, attr in inspect.getmembers(module):
		if isinstance(attr, type) and attr is not type:
			oldClass = oldAttrs.get(name)
			if oldClass:
				updateType(oldClass, attr, reloadAll or getattr(attr, "_reload_all", False))
				setattr(module, name, oldClass)
		elif inspect.isfunction(attr):
			oldFun = oldAttrs.get(name)
			if not oldFun:
				oldAttrs[name] = attr
			elif inspect.isfunction(oldFun):
				if not updateFunc(oldFun, attr):
					oldAttrs[name] = attr
				else:
					setattr(module, name, oldFun)

	not reloadAll and module.__dict__.update(oldAttrs)


def updateFunc(oldFunc, newFunc, updateCellDepth=2):
	if not inspect.isfunction(oldFunc):
		return False
	oldCellNum = 0
	if oldFunc.__closure__:
		oldCellNum = len(oldFunc.__closure__)
	newCellNum = 0
	if newFunc.__closure__:
		newCellNum = len(newFunc.__closure__)

	if oldCellNum != newCellNum:
		return False

	setattr(oldFunc, "__code__", newFunc.__code__)
	setattr(oldFunc, "__doc__", newFunc.__doc__)
	setattr(oldFunc, "__dict__", newFunc.__dict__)

	if newFunc.__defaults__:
		newDefaults = tuple([updateObject(obj) for obj in newFunc.__defaults__])
		setattr(oldFunc, "__defaults__", newDefaults)
	else:
		setattr(oldFunc, "__defaults__", newFunc.__defaults__)

	if not (updateCellDepth and oldCellNum):
		return True

	for index, cell in enumerate(oldFunc.__closure__):
		if inspect.isfunction(cell.cell_contents):
			updateFunc(
				cell.cell_contents,
				newFunc.__closure__[index].cell_contents,
				updateCellDepth - 1,
			)

	return True


def updateObject(obj):
	newClass = getattr(obj, "__class__", None)
	if not newClass:
		return obj
	if not (getattr(newClass, "__flags__", 0) & 0x200):  # Py_TPFLAGS_HEAPTYPE
		return obj

	oldInfos = _moduleInfos.get(newClass.__module__)
	if not oldInfos:
		return obj

	oldClass = oldInfos.get(newClass.__name__)
	if oldClass:
		obj.__class__ = oldClass

	return obj


def updateType(oldClass, newClass, reloadAll):  # noqa
	if not (getattr(newClass, "__flags__", 0) & 0x200):  # Py_TPFLAGS_HEAPTYPE
		return

	attrNames = list(oldClass.__dict__.keys())
	for name in attrNames:  # delete function
		if name in newClass.__dict__:
			continue

		if not inspect.isfunction(oldClass.__dict__[name]):
			continue

		type.__delattr__(oldClass, name)

	for name, attr in newClass.__dict__.items():
		if name in ignoreAttrs:
			continue

		if name not in oldClass.__dict__:  # new attribute
			setattr(oldClass, name, attr)
			continue

		oldAttr = oldClass.__dict__[name]
		newAttr = attr

		if inspect.isfunction(oldAttr) and inspect.isfunction(newAttr):
			if not updateFunc(oldAttr, newAttr):
				setattr(oldClass, name, newAttr)
		elif isinstance(newAttr, staticmethod) or isinstance(newAttr, classmethod):
			if (
				hasattr(oldAttr, "__func__") and hasattr(newAttr, "__func__") and not updateFunc(oldAttr.__func__, newAttr.__func__)
			):
				oldAttr.__func__ = newAttr.__func__
		elif isinstance(newAttr, property):
			setattr(oldClass, name, newAttr)
		elif inspect.isclass(newAttr) and attr.__name__ is oldAttr.__name__:
			if newAttr.__name__ == newClass.__name__ and newAttr.__module__ == newClass.__module__:
				# 属性是当前类对象，会出现递归
				continue
			if attr.__name__ in ["c_long", "c_long_be"]:
				continue
			updateType(oldAttr, attr, reloadAll or getattr(attr, "_reload_all", False))
		elif inspect.ismemberdescriptor(oldAttr):
			pass
		elif inspect.isgetsetdescriptor(newAttr) or inspect.ismemberdescriptor(newAttr):
			pass
		elif reloadAll:
			setattr(oldClass, name, attr)
