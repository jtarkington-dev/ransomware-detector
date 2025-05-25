import os
import signal
import subprocess
from typing import List
from .base import OSAbstraction
import hashlib

class LinuxAbstraction(OSAbstraction):
    def suspend_process(self, pid: int) -> bool:
        try:
            os.kill(pid, signal.SIGSTOP)
            self.logger.info("suspend_process", pid=pid)
            return True
        except Exception as e:
            self.logger.error("suspend_process.failed", pid=pid, error=str(e))
            raise

    def kill_process(self, pid: int) -> bool:
        try:
            os.kill(pid, signal.SIGKILL)
            self.logger.info("kill_process", pid=pid)
            return True
        except Exception as e:
            self.logger.error("kill_process.failed", pid=pid, error=str(e))
            raise

    def list_network_adapters(self) -> List[str]:
        output = subprocess.check_output(["ip", "-o", "link"], text=True)
        adapters = [line.split(":")[1].strip() for line in output.splitlines()]
        self.logger.debug("list_network_adapters", adapters=adapters)
        return adapters

    def disable_network(self) -> bool:
        try:
            subprocess.run(["nmcli", "radio", "all", "off"], check=True)
        except subprocess.CalledProcessError:
            for iface in self.list_network_adapters():
                subprocess.run(["ip", "link", "set", iface, "down"], check=False)
        self.logger.info("disable_network")
        return True

    def enable_network(self) -> bool:
        try:
            subprocess.run(["nmcli", "radio", "all", "on"], check=True)
        except subprocess.CalledProcessError:
            for iface in self.list_network_adapters():
                subprocess.run(["ip", "link", "set", iface, "up"], check=False)
        self.logger.info("enable_network")
        return True

    def remount_readonly(self, paths: List[str]) -> bool:
        for p in paths:
            subprocess.run(["mount", "-o", "remount,ro", p], check=True)
        self.logger.info("remount_readonly", paths=paths)
        return True

    def isolate_user_account(self, username: str) -> bool:
        subprocess.run(["usermod", "--lock", username], check=True)
        self.logger.info("isolate_user_account", user=username)
        return True

    def kill_user_session(self, username: str) -> bool:
        subprocess.run(["taskkill", "/FI", f"USERNAME eq {username}", "/F"], check=True)
        self.logger.info("kill_user_session", user=username)
        return True

    def show_alert(self, title: str, message: str) -> bool:
        print(f"[ALERT] {title}: {message}")
        self.logger.info("show_alert", title=title)
        return True

    def snapshot_open_files(self, pid: int) -> List[str]:
        files = subprocess.check_output(["lsof", "-p", str(pid)], text=True).splitlines()
        self.logger.info("snapshot_open_files", pid=pid, files=files)
        return files

    def hash_file(self, path: str) -> str:
        h = hashlib.sha256()
        with open(path, "rb") as f:
            while chunk := f.read(8192):
                h.update(chunk)
        digest = h.hexdigest()
        self.logger.info("hash_file", path=path, hash=digest)
        return digest