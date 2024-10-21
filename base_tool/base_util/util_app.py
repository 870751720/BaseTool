import multiprocessing
import os
import sys

os.environ["QT_API"] = "pyside6"
os.environ["QT_FONT_DPI"] = "96"

from qtpy.QtCore import QTranslator
from qtpy.QtGui import QIcon, QPixmap
from qtpy.QtWidgets import QApplication

translator = QTranslator()
# 修复与有道不兼容的问题
if sys.platform == "win32":
    from ctypes import wintypes

    import win32con
    from qtpy.QtCore import QAbstractNativeEventFilter

    class AppNativeEventFilter(QAbstractNativeEventFilter):
        def nativeEventFilter(self, _, message):
            msg = wintypes.MSG.from_address(message.__int__())
            if msg.message == win32con.WM_GETOBJECT:
                return True, msg.message
            return False, msg.message

    appFilter = AppNativeEventFilter()

# 防止多开
multiprocessing.freeze_support()


def get_application(app_icon: str = None) -> QApplication:
    app = QApplication([])
    app.installNativeEventFilter(appFilter)
    if app_icon:
        icon = QIcon()
        icon.addPixmap(QPixmap(app_icon), QIcon.Normal, QIcon.Off)
        app.setWindowIcon(icon)
    return app
