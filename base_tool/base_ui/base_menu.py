from functools import partial

from qtpy.QtWidgets import QMenu

from base_tool.base_ui.base_style import NormalStyle


class BaseMenu(QMenu):
    def __init__(self) -> None:
        super().__init__()
        self.setStyleSheet(NormalStyle.NORMAL_MENU)
        self.setFixedWidth(210)

    def add_action(self, action_config: list, check_data: list = None) -> None:
        # action_config: [] "name": str, "callback": callable, "all_selected": bool, "can_action": callable
        spaces = "      "
        for one in action_config:
            if isinstance(one, str):
                self.addAction(one)
                self.addSeparator()
            else:
                can_action = one.get("can_action", None)
                is_all_selected = one.get("all_selected", False)
                if not is_all_selected:
                    need_data = check_data[0]
                else:
                    need_data = check_data[1]
                if can_action:
                    if not is_all_selected:
                        if not can_action(need_data):
                            continue
                    else:
                        need_data = []
                        for each in check_data[1]:
                            if can_action(each):
                                need_data.append(each)
                        if not need_data:
                            continue
                callback = one["callback"]
                action = self.addAction(spaces + one["name"])
                action.triggered.connect(partial(callback, need_data))
