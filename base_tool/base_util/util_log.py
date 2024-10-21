import os
from datetime import datetime

from base_tool.global_setting import GS


def log(log: str, who: str = None) -> None:
    if not log or log == "\n":
        return
    log = str(log)
    time_log = datetime.now().strftime("%m-%d %H:%M:%S ") + log + "\n"
    if who is None:
        who = GS.get_log_who()
    log_path = os.path.join(GS.get_log_path(), "log_" + who + ".txt")
    with open(log_path, "a") as f:
        f.write(time_log)
