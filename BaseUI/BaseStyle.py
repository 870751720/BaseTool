class ImgRes(object):
	CLOSE = ":/BaseRes/close.png"
	MAX = ":/BaseRes/max.png"
	MIN = ":/BaseRes/min.png"
	SETTING = ":/BaseRes/setting.png"

	ADD = ":/BaseRes/add.png"
	DELETE = ":/BaseRes/delete.png"

	ERROR = ":/BaseRes/error.png"
	MINX_PASS = ":/BaseRes/mixpass.png"
	PASS = ":/BaseRes/pass.png"
	WARNING = ":/BaseRes/warning.png"
	INFO = ":/BaseRes/info.png"

	FILTER = ":/BaseRes/filter.png"
	SORT = ":/BaseRes/sort.png"
	SORT_DOWN = ":/BaseRes/sortDown.png"
	SORT_UP = ":/BaseRes/sortUp.png"
	LINK = ":/BaseRes/link.png"

	FOLD = ":/BaseRes/fold.png"
	UNFOLD = ":/BaseRes/unfold.png"

	RETRY = ":/BaseRes/retry.png"
	CHANGE = ":/BaseRes/change.png"
	HOME = ":/BaseRes/home.png"


class NormalStyle(object):
	WHITE_LABEL = "QLabel{color:rgb(235,235,235);border:none;background-color:transparent;}"
	RED_LABEL = "QLabel{color:rgb(199,84,80);border:none;background-color:transparent;}"
	GREEN_LABEL = "QLabel{color:rgb(102,187,106);border:none;background-color:transparent;}"

	STRONG_WHITE_LABEL = "QLabel{color:rgb(235,235,235);font-weight: bold;font-size: 24px;border:none;}"
	STRONG_BLUE_LABEL = "QLabel{color:rgb(235,235,235);font-weight: bold;font-size: 24px;border:none;background-color:rgb(149,149,149);border-radius:4px}"
	GRAY_LABEL = "QLabel{color:rgb(128,128,128);border:none;background-color:transparent;}"
	HOVER_LABEL = (
		"QLabel{text-decoration: underline;} QLabel:hover{color:rgb(64,169,255);} QLabel:pressed{color:rgb(9,109,217);}"
	)
	TITLE_LABEL = "QLabel{color:rgb(235,235,235);border:none;background-color:rgb(83,83,83);}"
	TAG_BLUE_LABEL = (
		"QLabel{color: #ffffff;background-color:rgb(0,120,215);border-radius:4px;padding-left:4px;padding-right:4px;}"
	)
	TAG_RED_LABEL = "QLabel{color: #ffffff;background-color:#e74c3c;border-radius:4px;padding-left:4px;padding-right:4px;}"

	BUTTON_DEFAULT = (
		"QPushButton{border:none;background-color:rgb(83,83,83);color:rgb(203,203,203);border-radius:4px} "
		"QPushButton:hover{background-color:rgb(68,70,84);} "
		"QPushButton:pressed{background-color:rgb(52,52,65);} "
	)

	BUTTON_DISABLE = "QPushButton {background-color: gray;color: lightgray;border: 1px solid darkgray;border-radius: 2px;}"

	BUTTON_MAIN = (
		"QPushButton{border:none;background-color:rgb(0,120,215);color:rgb(203,203,203);border-radius:4px} "
		"QPushButton:hover{background-color:rgb(64,169,255)} "
		"QPushButton:pressed{background-color:rgb(9,109,217)} "
	)

	BUTTON_BLACK = (
		"QPushButton{color: white;border-radius: 2px;border: 1px groove gray; border-style:outset}"
		"QPushButton:hover{background-color:white; color: black;}"
		"QPushButton:pressed{background-color:rgb(85, 170, 255); border-style: inset; }"
		"QPushButton:checked{background-color:white; color: black;}"
	)

	BUTTON_ICON = (
		"QPushButton{border:none;} " "QPushButton:hover{padding-bottom: 3px;} " "QPushButton:pressed{padding-top: 4px;}"
	)
	SELECT_BUTTON_ICON = (
		"QPushButton{border:none;background-color:rgb(24,144,255);} "
		"QPushButton:hover{padding-bottom: 3px;} "
		"QPushButton:pressed{padding-top: 4px;}"
	)

	NORMAL_DIALOG = "QDialog {background-color: rgb(36,36,34);border: 1px solid rgb(15,15,15);}"

	NORMAL_LINE_EDIT = "QLineEdit{border-radius:3px;color: rgb(235,235,235);background-color:black;}"

	RED_LINE_EDIT = "QLineEdit{border-radius:3px;color: rgb(235,235,235);background-color:red;}"

	NORMAL_TEXT_EDIT = "QTextEdit{border-radius:3px;color: rgb(235,235,235);background-color:rgb(36,36,34);}"

	GRAY_TEXT_EDIT = "QTextEdit{border-radius:3px;color: rgb(235,235,235);background-color:rgb(71,71,71);}"

	NORMAL_TITLE = "background-color: rgb(25,25,25);"

	NORMAL_WINDOW = "QMainWindow{background-color: rgb(36,36,34);} QMainWindow::titleBar {background-color: #4CAF50;color: red;padding: 5px;}"

	NORMAL_AREA = "QScrollArea {background-color: rgb(36,36,34);border:none;}"

	NORMAL_WIDGET = "QWidget {background-color: rgb(36,36,34);}"

	NORMAL_CHECK = (
		"QCheckBox::indicator:unchecked{image:url(:/BaseRes/unchecked.png);}"
		"QCheckBox::indicator:checked{image:url(:/BaseRes/checked.png);}"
		"QCheckBox{color: white;}"
	)
	DISABLE_CHECK = (
		"QCheckBox::indicator:unchecked{image:url(:/BaseRes/unchecked.png);}"
		"QCheckBox::indicator:checked{image:url(:/BaseRes/checkedDisable.png);}"
		"QCheckBox{color: white;}"
	)
	LINK_CHECK = (
		"QCheckBox::indicator:unchecked{image:url(:/BaseRes/uncheckedLink.png);}"
		"QCheckBox::indicator:checked{image:url(:/BaseRes/checkedLink.png);}"
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
		"QTreeView::branch:has-siblings:!adjoins-item{border-image:url(:/BaseRes/vline.png) 0}"
		"QTreeView::branch:!has-siblings:adjoins-item{border-image:url(:/BaseRes/branchEnd.png) 0}"
		"QTreeView::branch:has-siblings:adjoins-item{border-image:url(:/BaseRes/branchMore.png) 0}"
		"QTreeView::branch:closed:has-children{border-image:none;image: url(:/BaseRes/treeClose.png);width:25px}"
		"QTreeView::branch:open:has-children{border-image:none;image: url(:/BaseRes/treeOpen.png);width:25px}"
	)

	NORMAL_MENU = (
		"QMenu{color:#E8E8E8;background-color:rgb(77,77,77);margin:0px;}"
		"QMenu::item{padding:5px 0px 3px 3px;}"
		"QMenu::indicator{width:13px;height:13px;}"
		"QMenu::item:selected{color:#E8E8E8; border:0px solid #575757; background:#1E90FF;}"
		"QMenu::separator{height:1px; background:rgb(71,71,71); margin-bottom:0px;}"
	)

	NORMAL_FILTER = "QMenu{background-color:rgb(40,40,40);border: 1px solid rgb(15,15,15);}"

	NORMAL_SEPARATOR = "QLabel{border:1px solid black;}"

	NORMAL_COMBOBOX = (
		"QComboBox {background:rgb(36,36,34);color:rgb(205,205,205);border:1px groove gray;padding:5px} "
		"QComboBox::drop-down{border:none;}"
		"QComboBox::down-arrow{image:url(:/BaseRes/comboBoxDown.png);width:15px;height:13px}"
		"QComboBox QAbstractItemView {background:gray;color:rgb(235,235,235)}"
		"QComboBox QAbstractItemView::item {background-color:white;color:rgb(43,43,43);padding:0px}"
	)

	NORMAL_TAB = """QTabWidget {background-color: rgb(36,36,34);} QTabWidget::pane {padding: 0px;} QWidget {background-color: rgb(36,36,34);}"""
