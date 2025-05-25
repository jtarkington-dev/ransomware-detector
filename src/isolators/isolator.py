import platform
import logging
from typing import List
from src.utils.config import config
from src.os_abstraction.linux import LinuxAbstraction
from src.os_abstraction.windows import WindowsAbstraction

class Isolator:
    """
    High-level interface to perform isolation actions by delegating
    to the appropriate OS-specific implementation.
    """
    def __init__(self, logger: logging.Logger = None):
        self.logger = logger or logging.getLogger(__name__)
        os_name = config.OS_OVERRIDE or platform.system().lower()
        if os_name.startswith("linux"):
            self.impl = LinuxAbstraction(self.logger)
        elif os_name.startswith("win") or os_name.startswith("windows"):
            self.impl = WindowsAbstraction(self.logger)
        else:
            raise RuntimeError(f"Unsupported OS: {os_name}")

    def suspend_process(self, pid: int) -> bool:
        return self.impl.suspend_process(pid)

    def kill_process(self, pid: int) -> bool:
        return self.impl.kill_process(pid)

    def disable_network(self) -> bool:
        return self.impl.disable_network()

    def enable_network(self) -> bool:
        return self.impl.enable_network()

    def remount_readonly(self, paths: List[str]) -> bool:
        return self.impl.remount_readonly(paths)

    def isolate_user_account(self, username: str) -> bool:
        return self.impl.isolate_user_account(username)

    def kill_user_session(self, username: str) -> bool:
        return self.impl.kill_user_session(username)

    def show_alert(self, title: str, message: str) -> bool:
        return self.impl.show_alert(title, message)

    def snapshot_open_files(self, pid: int) -> List[str]:
        return self.impl.snapshot_open_files(pid)

    def hash_file(self, path: str) -> str:
        return self.impl.hash_file(path)