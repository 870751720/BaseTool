class Chinese(object):
	TID_COMMON_CONFIRM = "确认"
	TID_COMMON_CONFIRM2 = "确定"
	TID_COMMON_CANCEL = "取消"
	TID_COMMON_TIP = "提示"
	TID_COMMON_SETTING = "设置"
	TID_COMMON_FILE_PICK = "选择文件"
	TID_COMMON_FILE_PICK_CHECK = "路径不满足条件"
	TID_COMMON_FILE_PICK_TIP = "点击选择文件"
	TID_COMMON_FILE_NOT_EXIST = "文件不存在"
	TID_COMMON_LANGUAGE_CHANGE = "Language change"
	TID_COMMON_RELOAD = "热更新"
	TID_COMMON_SELECT_ALL = "全选"
	TID_COMMON_SEARCH_PLACEHOLDER = "输入关键字搜索..."
	TID_COMMON_CHOOSE = "选择"
	TID_COMMON_REFRESH = "刷新"
	TID_COMMON_START = "开始分析"
	TID_COMMON_LOADING = "处理中"
	TID_COMMON_COPY_SUCCESS = "复制成功"


class English(Chinese):
	TID_COMMON_CONFIRM = "Yes"
	TID_COMMON_CONFIRM2 = "OK"
	TID_COMMON_CANCEL = "No"
	TID_COMMON_TIP = "Tip"
	TID_COMMON_SETTING = "Setting"
	TID_COMMON_FILE_PICK = "File pick"
	TID_COMMON_FILE_PICK_CHECK = "Path does not meet the conditions"
	TID_COMMON_FILE_PICK_TIP = "Click to select file"
	TID_COMMON_FILE_NOT_EXIST = "File does not exist"
	TID_COMMON_LANGUAGE_CHANGE = "切换中文"
	TID_COMMON_RELOAD = "Reload"
	TID_COMMON_SELECT_ALL = "Select All"
	TID_COMMON_SEARCH_PLACEHOLDER = "Enter keywords to search..."
	TID_COMMON_CHOOSE = "Choose"
	TID_COMMON_REFRESH = "Refresh"
	TID_COMMON_START = "Start Analysis"
	TID_COMMON_LOADING = "Loading"
	TID_COMMON_COPY_SUCCESS = "Copy Success"

	def __getattribute__(self, attr: str) -> any:
		if not isInEnglish():
			return getattr(Chinese, attr)
		return super().__getattribute__(attr)


isEnglish = False


def isInEnglish() -> bool:
	global isEnglish
	return isEnglish


BASE_LH = English()
