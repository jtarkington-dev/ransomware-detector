import subprocess
from typing import List
import psutil
import ctypes
import hashlib
from .base import OSAbstraction

class WindowsAbstraction(OSAbstraction):
    def suspend_process(self, pid: int) -> bool:
        try:
            psutil.Process(pid).suspend()
            self.logger.info("suspend_process", pid=pid)
            return True
        except Exception as e:
            self.logger.error("suspend_process.failed", pid=pid, error=str(e))
            raise

    def kill_process(self, pid: int) -> bool:
        try:
            psutil.Process(pid).kill()
            self.logger.info("kill_process", pid=pid)
            return True
        except Exception as e:
            self.logger.error("kill_process.failed", pid=pid, error=str(e))
            raise

    def list_network_adapters(self) -> List[str]:
        output = subprocess.check_output([
            "netsh", "interface", "show", "interface"
        ], text=True)
        lines = output.splitlines()[3:]
        adapters = [l.split()[-1] for l in lines if l.strip()]
        self.logger.debug("list_network_adapters", adapters=adapters)
        return adapters

    def disable_network(self) -> bool:
        for iface in self.list_network_adapters():
            subprocess.run([
                "netsh", "interface", "set", "interface",
                iface, "admin=disable"
            ], check=True)
        self.logger.info("disable_network")
        return True

    def enable_network(self) -> bool:
        for iface in self.list_network_adapters():
            subprocess.run([
                "netsh", "interface", "set", "interface",
                iface, "admin=enable"
            ], check=True)
        self.logger.info("enable_network")
        return True

    def remount_readonly(self, paths: List[str]) -> bool:
        for p in paths:
            subprocess.run(["icacls", p, "/deny", "Everyone:(W)"], check=True)
        self.logger.info("remount_readonly", paths=paths)
        return True

    def isolate_user_account(self, username: str) -> bool:
        subprocess.run(["net", "user", username, "/active:no"], check=True)
        self.logger.info("isolate_user_account", user=username)
        return True

    def kill_user_session(self, username: str) -> bool:
        # Use taskkill to kill processes by user
        subprocess.run([
            "taskkill", "/FI", f"USERNAME eq {username}", "/F"
        ], check=True)
        self.logger.info("kill_user_session", user=username)
        return True

    def show_alert(self, title: str, message: str) -> bool:
        ctypes.windll.user32.MessageBoxW(None, message, title, 0x40)
        self.logger.info("show_alert", title=title)
        return True

    def snapshot_open_files(self, pid: int) -> List[str]:
        proc = psutil.Process(pid)
        files = [f.path for f in proc.open_files()]
        self.logger.info("snapshot_open_files", pid=pid, files=files)
        return files

    def hash_file(self, path: str) -> str:
        h = hashlib.sha256()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
        digest = h.hexdigest()
        self.logger.info("hash_file", path=path, hash=digest)
        return digest