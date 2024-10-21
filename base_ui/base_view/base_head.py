from qtpy.QtCore import Qt
from qtpy.QtWidgets import QHeaderView, QWidget

from base_tool.base_ui.base_icon import BaseIcon
from base_tool.base_ui.base_label import BaseLabel
from base_tool.base_ui.base_layout import HBoxLayout
from base_tool.base_ui.base_style import ImgRes
from base_tool.base_ui.base_view.base_filter import BaseFilter


class BaseHeadView(QHeaderView):
    def __init__(self) -> None:
        super().__init__(Qt.Horizontal)
        self.setSectionsMovable(False)
        self.setSectionsClickable(True)
        self.setStretchLastSection(True)
        self.widgets = {}

    def paintSection(self, painter, rect, logicalIndex) -> None:
        painter.save()
        super().paintSection(painter, rect, logicalIndex)
        painter.restore()
        if logicalIndex in self.widgets:
            content_widget = self.widgets[logicalIndex]
        else:
            config = self.parentWidget().header_config[logicalIndex]
            self.widgets[logicalIndex] = content_widget = QWidget(self)
            content_widget.setStyleSheet(
                "background-color:rgb(71,71,71);border-right:1px solid rgb(15,15,15);"
            )
            layout = HBoxLayout(True)
            layout.addSpacing(5)
            label = BaseLabel(self.model().headerData(logicalIndex, Qt.Horizontal))
            layout.addWidget(label)
            can_sort = config.get("can_sort", False)
            if can_sort:
                content_widget.sort_button = sort_button = BaseIcon(ImgRes.SORT)
                sort_button.clicked.connect(
                    lambda: self._on_section_clicked(logicalIndex)
                )
                layout.addWidget(sort_button)
            can_filter = config.get("can_filter", False)
            if can_filter:
                content_widget.change_label = change_label = BaseLabel("*")
                change_label.setVisible(False)
                filter_button = BaseIcon(ImgRes.FILTER, (22, 22))
                filter_button.clicked.connect(
                    lambda: self._on_filter_click(logicalIndex)
                )
                layout.addStretch()
                layout.addWidget(change_label)
                layout.addWidget(filter_button)
                layout.addSpacing(5)
            else:
                layout.addStretch()
            content_widget.setLayout(layout)

        content_widget.setGeometry(rect)
        content_widget.show()

    def _on_section_clicked(self, logicalIndex) -> None:
        sort_button = self.widgets[logicalIndex].sort_button
        next_icon = ImgRes.SORT_UP
        if sort_button.get_icon() == ImgRes.SORT_UP:
            next_icon = ImgRes.SORT_DOWN
            self.parentWidget().sortByColumn(logicalIndex, Qt.DescendingOrder)
        else:
            self.parentWidget().sortByColumn(logicalIndex, Qt.AscendingOrder)
        sort_button.change_icon(next_icon)

    def _on_filter_click(self, logicalIndex) -> None:
        change_label = self.widgets[logicalIndex].change_label
        parentWidget = self.parentWidget()
        pos = self.mapToGlobal(self.widgets[logicalIndex].geometry().bottomRight())
        pos.setX(pos.x() - 22)
        menu = BaseFilter(
            parentWidget.header_filter_info[logicalIndex],
            parentWidget.on_trigger_filter,
            change_label,
        )
        menu.exec_(pos)
