import json
import os
import shutil
import sys

import base_tool.base_util.util_I18n
from base_tool.base_ui.base_setting import BaseSetting
from base_tool.base_util.util_common import ErrorHook, Singleton
from base_tool.base_util.util_enum import PackType, SettingType
from base_tool.base_util.util_path import get_exe_and_res_path
from base_tool.base_util.util_reload import reload_py


def on_language_change(is_english: bool) -> None:
    base_tool.base_util.util_I18n.is_english = is_english


def on_reload() -> None:
    reload_py()


class GlobalSetting(metaclass=Singleton):
    BASE_GLOBAL_SETTING = {
        "is_english": {
            "name": "TID_COMMON_LANGUAGE_CHANGE",
            "default": False,
            "on_change": on_language_change,
            "on_load": on_language_change,
            "setting_type": SettingType.CHECK,
        },
    }

    BASE_LINK_FUNC = {
        "reload": {
            "name": "TID_COMMON_RELOAD",
            "click_func": on_reload,
            "setting_type": SettingType.LINK,
        },
    }

    APP_GLOBAL_SETTING = {}
    APP_LINK_FUNC = {}

    def __init__(self, tool_name: str = "EasyTool") -> None:
        self._tool_name = tool_name
        self.main_window = None
        self._init_path()
        self._init_pack()
        self._load_global_setting()

    # region 初始化
    def _init_path(self) -> None:
        # exe 指的是工具目录，在代码运行的时候是指 main.py的父目录，exe运行的时候是指exe存放的文件夹
        # res 指的是调用资源目录，在代码运行的时候是指main.py的父目录，exe运行的是指_MEIPASS，即被打包进exe的资源路径
        # data_path 指的是数据存放总目录
        self.exe_path, self.res_path = get_exe_and_res_path()
        self.data_path = data_path = os.path.join(
            os.environ["APPDATA"], self._tool_name
        )
        if not os.path.exists(data_path):
            os.mkdir(data_path)

        self._global_setting_path = os.path.join(self.data_path, "global_setting.txt")

    def _init_pack(self) -> None:
        pack_type_file = os.path.join(self.exe_path, "pack_type.txt")
        if not os.path.exists(pack_type_file):
            self.pack_type = PackType.CODE
            return
        with open(pack_type_file, "r", encoding="utf-8") as f:
            self.pack_type = int(f.read())

    def _load_global_setting(self) -> None:
        global_setting = {}
        global_setting_path = self._global_setting_path
        if os.path.exists(global_setting_path):
            with open(global_setting_path, "r", encoding="utf-8") as f:
                global_setting = json.load(f)
        total_setting = self.BASE_GLOBAL_SETTING | self.APP_GLOBAL_SETTING
        for setting_name, setting_config in total_setting.items():
            setting_value = global_setting.get(setting_name, setting_config["default"])
            setattr(self, setting_name, setting_value)
            on_load = setting_config.get("on_load", None)
            if on_load is not None:
                on_load(setting_value)

        self._load_global_setting_post()

    def _load_global_setting_post(self) -> None:
        _error_path = self._get_error_path()
        if self.pack_type == PackType.CODE:
            if os.path.exists(_error_path):
                try:
                    shutil.rmtree(_error_path)
                except:
                    pass
        os.makedirs(_error_path, exist_ok=True)

        sys.excepthook = ErrorHook(display=0, logdir=_error_path, format="text")

    def _get_error_path(self):
        return os.path.join(self.data_path, "error")

    def update_global_setting(self, new_setting: dict) -> None:
        global_setting = {}
        total_setting = self.BASE_GLOBAL_SETTING | self.APP_GLOBAL_SETTING

        for setting_name, setting_config in total_setting.items():
            if setting_name not in new_setting:
                global_setting[setting_name] = getattr(self, setting_name)
                continue
            new_value = new_setting[setting_name]
            setting_config = total_setting[setting_name]
            change_check = setting_config.get("change_check", None)
            if change_check and not change_check(new_value):
                global_setting[setting_name] = getattr(self, setting_name)
                continue
            global_setting[setting_name] = new_value
            setattr(self, setting_name, new_value)
            on_change = setting_config.get("on_change", None)
            if on_change is not None:
                on_change(new_value)

        with open(self._global_setting_path, "w", encoding="utf-8") as f:
            json.dump(global_setting, f, ensure_ascii=False, indent=4)

        for setting_name, setting_config in total_setting.items():
            if setting_name not in new_setting:
                continue
            after_all_change_done = setting_config.get("after_all_change_done", None)
            after_all_change_done and after_all_change_done()

    def open_setting(self) -> None:
        from base_tool.base_util.util_I18n import _L  # 翻译可能被项目文件重载

        base_setting_dialog = BaseSetting()
        setting_config = {}
        total_setting = (
            self.APP_GLOBAL_SETTING
            | self.BASE_GLOBAL_SETTING
            | self.BASE_LINK_FUNC
            | self.APP_LINK_FUNC
        )
        for setting_name, setting_config in total_setting.items():
            setting_config[setting_name] = setting_config
            if setting_config["setting_type"] != SettingType.LINK:
                setting_config["now_val"] = getattr(self, setting_name)
            setting_config["show_name"] = getattr(_L, setting_config["name"])

        base_setting_dialog.init_setting(total_setting, self.update_global_setting)
        base_setting_dialog.exec()

    def get_log_path(self) -> str:
        return self.data_path

    def get_log_who(self) -> str:
        return self._tool_name

    # endregion

    # region 启动
    def do_exit(self) -> None:
        os._exit(0)

    # endregion


GS = None
# GS = GlobalSetting(), 如果工具不需要独立的设置，那么就把这个打开就好
