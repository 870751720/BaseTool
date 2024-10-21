import ctypes
import ctypes.wintypes
from ctypes import Structure, c_int
from ctypes.wintypes import RECT

import win32con
from qtpy.QtCore import Qt


class NCCALCSIZE_PARAMS(Structure):
    _fields_ = [("rgrc", RECT * 3), ("lppos", c_int)]


class MARGINS(ctypes.Structure):
    _fields_ = [
        ("cxLeftWidth", c_int),
        ("cxRightWidth", c_int),
        ("cyTopHeight", c_int),
        ("cyBottomHeight", c_int),
    ]


def GET_Y_LPARAM(param):
    raw = param >> 16
    if raw >= 0x8000:
        return raw - 0x10000
    else:
        return raw


def GET_X_LPARAM(param):
    raw = param & 0xFFFF
    if raw >= 0x8000:
        return raw - 0x10000
    else:
        return raw


class BaseFramelessWindow(object):
    MARGIN = 4

    def __init__(self):
        self._winId = -1
        self._init()

    def _init(self):
        self._winId = int(self.winId())
        flags = int(self.windowFlags())
        flags = flags | Qt.FramelessWindowHint
        self.setWindowFlags(flags)

        style = ctypes.windll.user32.GetWindowLongW(self._winId, win32con.GWL_STYLE)
        ctypes.windll.user32.SetWindowLongW(
            int(self.winId()),
            win32con.GWL_STYLE,
            style | win32con.WS_THICKFRAME | win32con.WS_CAPTION,
        )

    def nativeEvent(self, eventType, message):
        msg = ctypes.wintypes.MSG.from_address(message.__int__())
        if msg.message == win32con.WM_NCCALCSIZE:
            np = NCCALCSIZE_PARAMS.from_address(msg.lParam)
            if ctypes.windll.user32.IsZoomed(self._winId):
                geo = self.windowHandle().screen().availableGeometry()
                r = np.rgrc[0]
                ratio = self.devicePixelRatioF()
                r.left = int(geo.left())
                r.top = int(geo.top())

                # https://doc.qt.io/qt-5/qrect.html#right
                # Note that for historical reasons this function(right) returns left() + width() - 1; use x() + width() to retrieve the true x-coordinate.
                r.right = int(geo.left() + geo.width() * ratio)
                r.bottom = int(geo.top() + geo.height() * ratio)
            if np.rgrc[0].top != 0:
                np.rgrc[0].top -= 1
            return True, 0

        elif msg.message == win32con.WM_NCHITTEST:
            ratio = self.devicePixelRatioF()
            winRect = RECT()
            ctypes.windll.user32.GetWindowRect(int(self.winId()), ctypes.byref(winRect))
            borderWidth = self.MARGIN * ratio
            resizeWidth = self.minimumWidth() != self.maximumWidth()
            resizeHeight = self.minimumHeight() != self.maximumHeight()
            x = GET_X_LPARAM(msg.lParam)
            y = GET_Y_LPARAM(msg.lParam)

            if resizeWidth and resizeHeight:
                # bottom left corner
                if (
                    winRect.left <= x < winRect.left + borderWidth
                    and winRect.bottom - borderWidth <= y < winRect.bottom
                ):
                    return True, win32con.HTBOTTOMLEFT
                # bottom right corner
                if (
                    winRect.right - borderWidth <= x < winRect.right
                    and winRect.bottom - borderWidth <= y < winRect.bottom
                ):
                    return True, win32con.HTBOTTOMRIGHT
                # top left corner
                if (
                    winRect.left <= x < winRect.left + borderWidth
                    and winRect.top <= y < winRect.top + borderWidth
                ):
                    return True, win32con.HTTOPLEFT
                # top right corner
                if (
                    winRect.right - borderWidth <= x < winRect.right
                    and winRect.top <= y < winRect.top + borderWidth
                ):
                    return True, win32con.HTTOPRIGHT

            if resizeWidth:
                # left border
                if winRect.left <= x < winRect.left + borderWidth:
                    return True, win32con.HTLEFT
                # right border
                if winRect.right - borderWidth <= x < winRect.right:
                    return True, win32con.HTRIGHT

            if resizeHeight:
                # bottom border
                if winRect.bottom - borderWidth <= y < winRect.bottom:
                    return True, win32con.HTBOTTOM
                # top border
                if winRect.top <= y < winRect.top + borderWidth:
                    return True, win32con.HTTOP

            _x, _y = (x - winRect.left) / ratio, (y - winRect.top) / ratio
            if self.is_caption_area(_x, _y):
                return True, win32con.HTCLIENT

        elif msg.message == win32con.WM_NCACTIVATE:
            return True, 1

        return super(BaseFramelessWindow, self).nativeEvent(eventType, message)

    def is_caption_area(self, x, y):
        return y < self._title_height
