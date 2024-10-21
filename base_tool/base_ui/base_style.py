class ImgRes(object):
    CLOSE = ":/base_res/close.png"
    MAX = ":/base_res/max.png"
    MIN = ":/base_res/min.png"
    SETTING = ":/base_res/setting.png"

    ADD = ":/base_res/add.png"
    DELETE = ":/base_res/delete.png"

    ERROR = ":/base_res/error.png"
    MINX_PASS = ":/base_res/mixpass.png"
    PASS = ":/base_res/pass.png"
    WARNING = ":/base_res/warning.png"
    INFO = ":/base_res/info.png"

    FILTER = ":/base_res/filter.png"
    SORT = ":/base_res/sort.png"
    SORT_DOWN = ":/base_res/sort_down.png"
    SORT_UP = ":/base_res/sort_up.png"
    LINK = ":/base_res/link.png"

    FOLD = ":/base_res/fold.png"
    UNFOLD = ":/base_res/unfold.png"

    RETRY = ":/base_res/retry.png"
    CHANGE = ":/base_res/change.png"
    HOME = ":/base_res/home.png"


class NormalStyle(object):

    WHITE_LABEL = "QLabel{color:rgb(235,235,235);border:none;}"
    STRONG_WHITE_LABEL = (
        "QLabel{color:rgb(235,235,235);font-weight: bold;font-size: 24px;border:none;}"
    )

    BUTTON_DEFAULT = (
        "QPushButton{border:none;background-color:rgb(83,83,83);color:rgb(203,203,203);border-radius:4px} "
        "QPushButton:hover{background-color:rgb(68,70,84);} "
        "QPushButton:pressed{background-color:rgb(52,52,65);} "
    )

    BUTTON_MAIN = (
        "QPushButton{border:none;background-color:rgb(24,144,255);color:rgb(203,203,203);border-radius:4px} "
        "QPushButton:hover{background-color:rgb(64,169,255)} "
        "QPushButton:pressed{background-color:rgb(9,109,217)} "
    )

    BUTTON_ICON = (
        "QPushButton{border:none;} "
        "QPushButton:hover{padding-bottom: 3px;} "
        "QPushButton:pressed{padding-top: 4px;}"
    )

    NORMAL_DIALOG = (
        "QDialog {background-color: rgb(36,36,34);border: 1px solid rgb(57,57,56);}"
    )

    NORMAL_LINE_EDIT = (
        "QLineEdit{border-radius:3px;color: rgb(235,235,235);background-color:black;}"
    )

    NORMAL_TEXT_EDIT = "QTextEdit{border-radius:3px;color: rgb(235,235,235);background-color:rgb(36,36,34);}"

    NORMAL_TITLE = "background-color: rgb(25,25,25);"

    NORMAL_WINDOW = "QMainWindow{background-color: rgb(36,36,34);} QMainWindow::titleBar {background-color: #4CAF50;color: red;padding: 5px;}"

    NORMAL_AREA = "QScrollArea {background-color: rgb(36,36,34);border:none;}"

    NORMAL_WIDGET = "QWidget {background-color: rgb(36,36,34);}"

    NORMAL_CHECK = (
        "QCheckBox::indicator:unchecked{image:url(:/base_res/unchecked.png);}"
        "QCheckBox::indicator:checked{image:url(:/base_res/checked.png);}"
        "QCheckBox{color: white;}"
    )

    NORMAL_FILE_PICK = (
        "QPushButton{border:1px solid rgb(235,235,235);background-color:rgb(36,36,34);color:rgb(235,235,235);border-radius:4px} "
        "QPushButton:hover{background-color:rgb(255,255,255);color:rgb(0,0,0);} "
        "QPushButton:pressed{background-color:rgb(85,170,255);} "
    )

    NORMAL_VIEW = (
        "QTreeView{background-color:rgb(36,36,34);border:none;show-decoration-selected:1;outline:none}"
        "QScrollBar::add-line:vertical {width: 0px;height: 0px;}"
        "QScrollBar::sub-line:vertical {width: 0px;height: 0px;}"
        "QTreeView::item:alternate{border:none;background-color:rgb(36,36,34);}"
        "QTreeView::item:!alternate{border:none;background-color:rgb(40,40,40);}"
        "QTreeView::item:hover{background-color:rgb(14,74,85);}"
        "QTreeView::item:selected{background-color:rgb(14,74,86);} "
        "QTreeView::item:selected:!active{background-color:rgb(87,87,87);}"
        "QTreeView::branch{background-color:rgb(36,36,34);}"
        "QTreeView::branch:!alternate{background-color:rgb(40,40,40);}"
        "QTreeView::branch:hover{background-color:rgb(14,74,87);}"
        "QTreeView::branch:selected{background-color:rgb(14,74,88);}"
        "QTreeView::branch:selected:!active{background-color:rgb(87,87,87);}"
        "QTreeView::branch:has-siblings:!adjoins-item{border-image:url(:/base_res/vline.png) 0}"
        "QTreeView::branch:!has-siblings:adjoins-item{border-image:url(:/base_res/branch_end.png) 0}"
        "QTreeView::branch:has-siblings:adjoins-item{border-image:url(:/base_res/branch_more.png) 0}"
        "QTreeView::branch:closed:has-children{border-image:none;image: url(:/base_res/tree_close.png);width:25px}"
        "QTreeView::branch:open:has-children{border-image:none;image: url(:/base_res/tree_open.png);width:25px}"
    )

    NORMAL_MENU = (
        "QMenu{color:#E8E8E8;background-color:rgb(77,77,77);margin:0px;}"
        "QMenu::item{padding:5px 0px 3px 3px;}"
        "QMenu::indicator{width:13px;height:13px;}"
        "QMenu::item:selected{color:#E8E8E8; border:0px solid #575757; background:#1E90FF;}"
        "QMenu::separator{height:1px; background:rgb(71,71,71); margin-bottom:0px;}"
    )

    NORMAL_FILTER = (
        "QMenu{background-color:rgb(40,40,40);border: 1px solid rgb(15,15,15);}"
    )
