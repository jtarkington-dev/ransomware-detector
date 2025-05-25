from abc import ABC, abstractmethod
from typing import List
import logging

class OSAbstraction(ABC):
    def __init__(self, logger: logging.Logger):
        """Initialize with a logger instance."""
        self.logger = logger

    # ===== Process control =====
    @abstractmethod
    def suspend_process(self, pid: int) -> bool:
        """Suspend the given process ID."""

    @abstractmethod
    def kill_process(self, pid: int) -> bool:
        """Force-kill the given process ID."""

    # ===== Network control =====
    @abstractmethod
    def list_network_adapters(self) -> List[str]:
        """Return a list of network interface names."""

    @abstractmethod
    def disable_network(self) -> bool:
        """Disable all network interfaces."""

    @abstractmethod
    def enable_network(self) -> bool:
        """Re-enable all network interfaces."""

    # ===== Filesystem lockdown =====
    @abstractmethod
    def remount_readonly(self, paths: List[str]) -> bool:
        """
        Remount each path as read-only (Linux) or adjust ACL to deny write (Windows).
        """

    # ===== User isolation =====
    @abstractmethod
    def isolate_user_account(self, username: str) -> bool:
        """Lock or disable the given user account."""

    @abstractmethod
    def kill_user_session(self, username: str) -> bool:
        """Terminate all processes for the given user."""

    # ===== Alerts =====
    @abstractmethod
    def show_alert(self, title: str, message: str) -> bool:
        """Display a popup/console alert to the user."""

    # ===== Forensic utilities =====
    @abstractmethod
    def snapshot_open_files(self, pid: int) -> List[str]:
        """Copy or list open files for PID before further action."""

    @abstractmethod
    def hash_file(self, path: str) -> str:
        """Compute and return the SHA256 hash of the given file."""