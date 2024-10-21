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
ignore_modules = []

ignore_attrs = {
    "__module__",
    "_reload_all",
    "__dict__",
    "__weakref__",
    "__doc__",
    "__dir__",
}

all_reload_modules = set()
# reload函数回调，参数是bool，True表示开始，False表示结束
reload_operation_func_list = {}


def reg_reload_operation_func(tag, func):
    if tag not in reload_operation_func_list:
        reload_operation_func_list[tag] = func


def exec_reload_operation_func(start):
    for func in reload_operation_func_list.values():
        func(start)


def _fit_rules(string, rules):
    for rule in rules:
        if hasattr(rule, "search"):
            if rule.search(string) is not None:
                return True
        elif string == rule:
            return True
    return False


class finder(object):
    def setup_old_module(self, name):
        old_module = self.get_old_module(name)
        if not old_module:
            return

        old_module.__dict__.pop("_reload_all", None)
        sys.modules[name] = old_module  # for imp.load_module to reload the module

    def modify_module(self, name, module):
        modify_module = getattr(sys, "modify_module", None)
        if not modify_module:
            return module

        return modify_module(name, module)

    def get_old_module(self, name):
        get_old_module = getattr(sys, "get_old_module", None)
        if not get_old_module:
            return

        return get_old_module(name)


class builtin_finder(finder):
    def find_spec(self, full_name, path, target=None):
        try:
            module = None
            for name in full_name.split("."):
                module = self.get_module(name, module)

            if module:
                from importlib import util

                spec = util.spec_from_loader(full_name, loader(module))
                # flynn 2017/2/15: 下面这句trick太关键了！看3.4.0的源码实现，在回调find_spec之前如果module没有在sys.modules里面，
                # 会判定is_reload为False，然后返回的这个spec就没有意义了。但是源码中看到如果module.__spec__有值，还是可以生效的。
                module.__spec__ = spec
                return spec

            return None
        except ImportError:
            old_module = self.get_old_module(full_name)
            if old_module:
                print("unchanged module", full_name)
                spec = importlib.util.spec_from_loader(full_name, loader(old_module))
                old_module.__spec__ = spec
                return spec
            else:
                raise

    def get_module(self, name, parent):
        parent_name = getattr(parent, "__name__", "")
        parent_path = getattr(parent, "__path__", None)

        if parent_name:
            full_name = parent_name + "." + name
        else:
            full_name = name

        module = sys.modules.get(full_name)
        if module:
            return module

        return self.create_module(name, full_name, parent_path)

    def create_module(self, name, full_name, parent_path):
        self.setup_old_module(full_name)
        if parent_path:
            parent_path = list(parent_path)
        fd, path, des = imp.find_module(name, parent_path)
        module = imp.load_module(full_name, fd, path, des)

        self.modify_module(full_name, module)
        return module


class loader(abc.Loader):
    def __init__(self, module):
        self.module = module

    def load_module(self, fullname):
        return self.module


_old_modules = {}
_module_infos = {}
sys._last_reload_time = time.time()  # 进程启动的时候记录当前时间，避免第一次全量更新


def reload_py(names=None):
    import sys

    last_reload_time = getattr(sys, "_last_reload_time", 0)
    if not last_reload_time:
        sys._last_reload_time = 0

    old_sys_meta_path = sys.meta_path
    sys.meta_path = [builtin_finder()]

    exec_reload_operation_func(True)
    print("********** start reload script ***************")

    gcdisable()

    global _old_modules
    global _module_infos

    _old_modules = dict(sys.modules)
    store_module_infos()

    sys.get_old_module = get_old_module
    sys.modify_module = modify_module
    sys.reloading = True

    modules = get_reload_modified_modules(names, last_reload_time)

    for name in modules:  # pop the module to be reloaded
        if name in sys.modules:
            sys.modules.pop(name)

    for name in modules:
        if name == __name__:
            continue
        try:
            importlib.import_module(name)
        except Exception as e:
            print(
                "********** reload script failed in module %s %s ***************\n%s"
                % (name, type(e), e)
            )
            sys.modules.update(_old_modules)
            raise

    import sys

    sys.get_old_module = None
    sys.modify_module = None
    sys.reloading = False

    _old_modules = None
    _module_infos = {}

    gcenable()
    gccollect()
    print("********** reload script successed ***************")

    sys.meta_path = old_sys_meta_path
    exec_reload_operation_func(False)


def get_reload_modules(names):
    result = []
    names = names or _old_modules.keys()

    for name in names:

        module = sys.modules[name]

        if is_ignored_module(module):
            continue

        if not _fit_rules(name, ignore_modules):
            module = _old_modules.get(name)
            if inspect.ismodule(module) and getattr(module, "__file__", None):
                result.append(name)

    return result


def is_ignored_module(module):
    module_file = getattr(module, "__file__", None)
    if not module_file:
        return True
    module_file = os.path.normpath(module_file)
    sys_paths = tuple(sys.path[:])
    return not module_file.endswith(".py") or not module_file.startswith(sys_paths)


def get_reload_modified_modules(names, last_reload_time):
    result = set()
    names = names or _old_modules.keys()

    for name in names:
        modifytime = 0
        module = _old_modules.get(name)
        if (
            is_ignored_module(module)
            or _fit_rules(name, ignore_modules)
            or name.endswith(".img_qss_rc")
            or name.startswith("bt.")
        ):
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

        if last_reload_time < modifytime:
            result.add(name)
            if modifytime > sys._last_reload_time:
                sys._last_reload_time = modifytime

    return result


def store_module_infos():
    for name, module in _old_modules.items():
        if module:
            _module_infos[name] = dict(module.__dict__)


def get_old_module(name):
    return _old_modules.get(name)


def modify_module(name, module):
    old_infos = _module_infos.get(name)
    if not old_infos:
        return module

    print("reload module", name)
    update_module(
        old_infos,
        module,
        getattr(module, "_reload_all", False) or _fit_rules(name, all_reload_modules),
    )

    return module


def update_module(old_attrs, module, reload_all):
    for name, attr in inspect.getmembers(module):
        if isinstance(attr, type) and attr is not type:
            old_class = old_attrs.get(name)
            if old_class:
                update_type(
                    old_class, attr, reload_all or getattr(attr, "_reload_all", False)
                )
                setattr(module, name, old_class)
        elif inspect.isfunction(attr):
            old_fun = old_attrs.get(name)
            if not old_fun:
                old_attrs[name] = attr
            elif inspect.isfunction(old_fun):
                if not update_fun(old_fun, attr):
                    old_attrs[name] = attr
                else:
                    setattr(module, name, old_fun)

    not reload_all and module.__dict__.update(old_attrs)


def update_fun(old_fun, new_fun, update_cell_depth=2):
    if not inspect.isfunction(old_fun):
        return False
    old_cell_num = 0
    if old_fun.__closure__:
        old_cell_num = len(old_fun.__closure__)
    new_cell_num = 0
    if new_fun.__closure__:
        new_cell_num = len(new_fun.__closure__)

    if old_cell_num != new_cell_num:
        return False

    setattr(old_fun, "__code__", new_fun.__code__)
    setattr(old_fun, "__doc__", new_fun.__doc__)
    setattr(old_fun, "__dict__", new_fun.__dict__)

    if new_fun.__defaults__:
        new_defaults = tuple([update_object(obj) for obj in new_fun.__defaults__])
        setattr(old_fun, "__defaults__", new_defaults)
    else:
        setattr(old_fun, "__defaults__", new_fun.__defaults__)

    if not (update_cell_depth and old_cell_num):
        return True

    for index, cell in enumerate(old_fun.__closure__):
        if inspect.isfunction(cell.cell_contents):
            update_fun(
                cell.cell_contents,
                new_fun.__closure__[index].cell_contents,
                update_cell_depth - 1,
            )

    return True


def update_object(obj):
    new_class = getattr(obj, "__class__", None)
    if not new_class:
        return obj
    if not (getattr(new_class, "__flags__", 0) & 0x200):  # Py_TPFLAGS_HEAPTYPE
        return obj

    old_infos = _module_infos.get(new_class.__module__)
    if not old_infos:
        return obj

    old_class = old_infos.get(new_class.__name__)
    if old_class:
        obj.__class__ = old_class

    return obj


def update_type(old_class, new_class, reload_all):  # noqa
    if not (getattr(new_class, "__flags__", 0) & 0x200):  # Py_TPFLAGS_HEAPTYPE
        return

    attrNames = list(old_class.__dict__.keys())
    for name in attrNames:  # delete function
        if name in new_class.__dict__:
            continue

        if not inspect.isfunction(old_class.__dict__[name]):
            continue

        type.__delattr__(old_class, name)

    for name, attr in new_class.__dict__.items():
        if name in ignore_attrs:
            continue

        if name not in old_class.__dict__:  # new attribute
            setattr(old_class, name, attr)
            continue

        old_attr = old_class.__dict__[name]
        new_attr = attr

        if inspect.isfunction(old_attr) and inspect.isfunction(new_attr):
            if not update_fun(old_attr, new_attr):
                setattr(old_class, name, new_attr)
        elif isinstance(new_attr, staticmethod) or isinstance(new_attr, classmethod):
            if (
                hasattr(old_attr, "__func__")
                and hasattr(new_attr, "__func__")
                and not update_fun(old_attr.__func__, new_attr.__func__)
            ):
                old_attr.__func__ = new_attr.__func__
        elif isinstance(new_attr, property):
            setattr(old_class, name, new_attr)
        elif inspect.isclass(new_attr) and attr.__name__ is old_attr.__name__:
            if (
                new_attr.__name__ == new_class.__name__
                and new_attr.__module__ == new_class.__module__
            ):
                # 属性是当前类对象，会出现递归
                continue
            if attr.__name__ in ["c_long", "c_long_be"]:
                continue
            update_type(
                old_attr, attr, reload_all or getattr(attr, "_reload_all", False)
            )
        elif inspect.ismemberdescriptor(old_attr):
            pass
        elif inspect.isgetsetdescriptor(new_attr) or inspect.ismemberdescriptor(
            new_attr
        ):
            pass
        elif reload_all:
            setattr(old_class, name, attr)
