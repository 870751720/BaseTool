from qtpy.QtCore import QModelIndex, Qt
from qtpy.QtWidgets import QStyledItemDelegate, QStyleOptionViewItem, QTreeView, QWidget

from base_tool.base_ui.base_view.base_view_widget import BaseViewWidget


class BaseItemDelegate(QStyledItemDelegate):
    def __init__(self, view: QTreeView) -> None:
        super().__init__()
        self._view = view
        self.widgets = {}

    def paint(self, _, option: QStyleOptionViewItem, index: QModelIndex) -> None:
        header_config = self._view.header_config
        column, row = index.column(), self._view.get_real_index_row(index)
        config = header_config[column]

        key = (row, column)
        widget = self.widgets.get(key, None)
        if widget is None:
            self.widgets[key] = widget = BaseViewWidget(
                index.data(Qt.UserRole),
                config,
                self._check_func,
                row,
                row in self._view.checked_rows_state,
            )
            widget.setGeometry(option.rect)
            self._view.setIndexWidget(index, widget)

    def destroyEditor(self, editor: QWidget, index: QModelIndex) -> None:
        super().destroyEditor(editor, index)
        column, row = index.column(), self._view.get_real_index_row(index)
        key = (row, column)
        self.widgets.pop(key, None)

    def _check_func(self, row: int, is_checked: bool) -> None:
        check_column = 0
        more_check = None
        for index, one_config in enumerate(self._view.header_config):
            if one_config.get("can_check", False):
                more_check = one_config.get("more_check", None)
                check_column = index
                break
        need_row = {row}
        need_row.update(self._view.selected_rows_state)
        if more_check:
            need_row = more_check(need_row, is_checked)
        for each_row in need_row:
            if is_checked:
                self._view.checked_rows_state.add(each_row)
            else:
                self._view.checked_rows_state.discard(each_row)
            self._view.on_checked_changed()
            widget = self.widgets.get((each_row, check_column), None)
            if widget:
                widget.check_widget.set_checked_without_trigger(is_checked)
