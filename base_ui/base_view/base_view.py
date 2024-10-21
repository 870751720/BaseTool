from qtpy.QtCore import QEvent, QItemSelection, QModelIndex, QPoint, Qt
from qtpy.QtGui import QColor
from qtpy.QtWidgets import QAbstractItemView, QTreeView

from base_tool.base_ui.base_menu import BaseMenu
from base_tool.base_ui.base_style import NormalStyle
from base_tool.base_ui.base_view.base_head import BaseHeadView
from base_tool.base_ui.base_view.base_item import BaseItem
from base_tool.base_ui.base_view.base_item_delegate import BaseItemDelegate
from base_tool.base_ui.base_view.base_item_model import BaseItemModel
from base_tool.base_ui.base_view.base_sort_model import BaseSortModel
from base_tool.base_util.util_enum import RowStateColor


class BaseView(QTreeView):
    ROW_STATE_COLOR = {
        (RowStateColor.NORMAL, True): (14, 74, 86, 205),
        (RowStateColor.NORMAL, False): (0, 0, 0, 0),
        (RowStateColor.ERROR, True): (156, 51, 55, 205),
        (RowStateColor.ERROR, False): (156, 51, 55, 150),
        (RowStateColor.WARNING, True): (110, 72, 29, 205),
        (RowStateColor.WARNING, False): (110, 72, 29, 150),
        (RowStateColor.CANT_USE, True): (71, 71, 71, 150),
        (RowStateColor.CANT_USE, False): (71, 71, 71, 150),
    }

    def __init__(self) -> None:
        super().__init__()
        self.setStyleSheet(NormalStyle.NORMAL_VIEW)
        self.setAnimated(True)
        self.setDragEnabled(False)
        self.setSortingEnabled(True)
        self.setRootIsDecorated(False)  # 根节点不需要装饰
        self.setUniformRowHeights(True)
        self.setDropIndicatorShown(False)
        self.setAlternatingRowColors(True)
        self.setContextMenuPolicy(Qt.CustomContextMenu)  # 设置自定义上下文菜单
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 不能编辑
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.customContextMenuRequested.connect(self._on_menu_event)

        self._item_model = BaseItemModel()
        self.sort_model = sort_model = BaseSortModel(self)
        sort_model.setSourceModel(self._item_model)

        self._item_deletegate = BaseItemDelegate(self)
        self.setItemDelegate(self._item_deletegate)
        self.setModel(sort_model)
        self.selectionModel().selectionChanged.connect(self._on_selection_changed)

        self.setHeader(BaseHeadView())

        self._action_config = []
        self.header_config = []
        self.header_filter_info = {}

        self._filter_text = ""
        self.cant_show_rows = set()

        self._checked_changed_callback = None

        self._show_can_use_info()

    def drawRow(self, painter, option, index):
        super(BaseView, self).drawRow(painter, option, index)
        is_selected = self.get_real_index_row(index) in self.selected_rows_state
        row_state = index.data(Qt.BackgroundRole)
        color = self.ROW_STATE_COLOR.get((row_state, is_selected), None)
        if color is not None:
            painter.fillRect(option.rect, QColor.fromRgb(*color))

    def viewportEvent(self, event: QEvent) -> bool:
        if event.type() == QEvent.Resize and not self.header().underMouse():
            self._adjust_column_widths()
        return super().viewportEvent(event)

    def _on_selection_changed(
        self, selected: QItemSelection, deselected: QItemSelection
    ) -> None:
        for index in selected.indexes():
            self.selected_rows_state.add(self.get_real_index_row(index))
        for index in deselected.indexes():
            self.selected_rows_state.discard(self.get_real_index_row(index))

    def get_real_index_row(self, index: QModelIndex) -> int:
        return index.model().mapToSource(index).row()

    def _adjust_column_widths(self) -> None:
        width = self.viewport().width()
        width_data = [one["width"] for one in self.header_config]
        fixed_col_widths = {}
        proportions = []
        for index, one in enumerate(width_data):
            if one > 1:
                fixed_col_widths[index] = one
            else:
                proportions.append(one)
        remaining_width = width - sum(fixed_col_widths.values())

        for col, width in fixed_col_widths.items():
            self.setColumnWidth(col, width)

        start_col = 0
        for proportion in proportions:
            while True:
                if start_col in fixed_col_widths:
                    start_col += 1
                else:
                    break
            col_width = int(remaining_width * proportion)
            self.setColumnWidth(start_col, col_width)
            start_col += 1

    def _on_menu_event(self, pos: QPoint) -> None:
        if not self._action_config:
            return
        index = self.currentIndex()
        if not index.isValid():
            return
        menu = BaseMenu()
        row = self.get_real_index_row(index)
        menu.add_action(
            self._action_config,
            [self.data[row], [self.data[one] for one in self.selected_rows_state]],
        )

        menu.exec_(self.mapToGlobal(pos))

    def on_trigger_filter(self) -> None:
        """触发过滤"""
        cant_show_rows = set()
        for index_info in self.header_filter_info.values():
            for filter_info in index_info.values():
                if not filter_info["is_show"]:
                    cant_show_rows.update(filter_info["rows"])
        if self._filter_text:
            for row, row_dict in enumerate(self.data):
                if row in cant_show_rows:
                    continue
                for one in row_dict.values():
                    is_show = False
                    if type(one) is str:
                        if self._filter_text in one:
                            is_show = True
                            break
                    if not is_show:
                        cant_show_rows.add(row)
        self.cant_show_rows = cant_show_rows
        self.sort_model.invalidateRowsFilter()

    # region 外部调用
    def _show_can_use_info(self):
        """开发可能经常用到的对象放到这里展示"""
        self.selected_rows_state = set()
        self.checked_rows_state = set()
        self.data = []

    def set_view_config(self, header_config: list, action_config: list = None) -> None:
        """
        header_config: 这是标题头的配置,每一个config是一个dict
        {
            "text_key": 对应data数据的文本键,会去取对应键的值进行文本展示
            "icon_key": 对应data数据的icon键,会去取对应键的值进行icon展示
            "row_decorate": 需要传入一个方法,这个方法会接受一行的data数据进行icon和文本的返回
            "name": 标题头的显示
            "width": 每列的占比,如果是小于1 就是百分占比,大于1就是固定数值
            "can_filter": 是否可以过滤显示
            "filter_decorate": 需要传入一个方法,这个方法会接受一行的data数据进行进行过滤文本的返回
            "can_sort": 是否可以排序
            "can_check": 会显示出一个可以勾选的框,可以在view的checked_rows_state取到所有勾选的行
            "more_check": 传入一个方法,接受当前需要改变勾选的行,和当前勾选的状态,返回一个总共需要改变勾选的行
            "center_align": 如果需要数据居中,填入这个就好
        }
        action_config: 这是右键菜单的action配置,每一个config是一个dict或者str, 直接传字符串的话就是分组标题
        {
            "name": action名
            "callback": 回调方法,接受一个参数,如果是单选的回调, 那么得到的是当前行数据,如果是多选, 那么得到的是选中的行数据的列表
            "all_selected": 决定是否多选
            "can_action": 如果是单选,会传入当前的行数据判断是否可以显示这个action, 如果是多选,那么只要有至少一行数据可以显示那么就显示
            在callback传入的列表是满足显示条件的数据
        }
        """
        self.header_config = header_config
        self._action_config = action_config
        self._item_model.setHorizontalHeaderLabels(
            [config["name"] for config in header_config]
        )

        header = self.header()
        header.setModel(self._item_model)
        header.setFixedHeight(22)

    def on_search_trigger_filter(self, text: str) -> None:
        """如果view有搜索组件, 请绑定这个函数"""
        self._filter_text = text
        self.on_trigger_filter()

    def set_data(self, data: list, clear_checked: bool = True) -> None:
        """
        设置数据,每一行数据必须是一个dict, 每个列的键在header已经定义了, 所以这里的数据需要有这个对应的键值的键
        如果一行有 错误,警告,禁用的状态, 那么数据里面需要设置一个 back_state 的键,对应RowStateColor的枚举
        """
        self.clear_data(clear_checked)
        old_header_filter_info = self.header_filter_info
        self.header_filter_info = {}

        self.data = data
        for row, row_dict in enumerate(data):
            items = []
            for index, one_header in enumerate(self.header_config):
                item = BaseItem(
                    row_dict, row_dict.get(one_header.get("text_key", ""), "")
                )
                items.append(item)
                can_filter = one_header.get("can_filter", False)
                if can_filter:
                    filter_text = one_header["filter_decorate"](row_dict)
                    self.header_filter_info.setdefault(index, {}).setdefault(
                        filter_text, {"is_show": True, "rows": set()}
                    )["rows"].add(row)
            self._item_model.appendRow(items)

        for index, one_header in enumerate(self.header_config):
            if one_header.get("can_filter", False):
                for filter_text, filter_info in self.header_filter_info.get(
                    index, {}
                ).items():
                    if filter_text in old_header_filter_info.get(index, {}):
                        filter_info["is_show"] = old_header_filter_info[index][
                            filter_text
                        ]["is_show"]
        old_header_filter_info.clear()

    def clear_data(self, clear_checked: bool = True) -> None:
        """清理当前所有数据"""
        self.data.clear()
        if clear_checked:
            self.checked_rows_state.clear()
        self.selected_rows_state.clear()
        self._item_deletegate.widgets.clear()
        self._item_model.removeRows(0, self._item_model.rowCount())

    def set_checked_changed_callback(self, callback: callable) -> None:
        """设置勾选状态改变的回调"""
        self._checked_changed_callback = callback

    def on_checked_changed(self) -> None:
        """当勾选状态改变时触发"""
        self._checked_changed_callback and self._checked_changed_callback()

    # endregion
