
import time
import logging
from typing import List, Callable
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from .base_monitor import Monitor
from .event import Event
from dataclasses import field

class WatchdogMonitor(Monitor):
    def __init__(self, paths: List[str]):
        self._observer = Observer()
        self._paths = paths
        self._handler = _InternalHandler(self._dispatch)
        self._callbacks: List[Callable[[Event], None]] = []
        self.logger = logging.getLogger(__name__)

    def on_event(self, cb: Callable[[Event], None]) -> None:
        self._callbacks.append(cb)

    def _dispatch(self, fs_event):
        try:
            evt = Event(
                path=fs_event.src_path,
                event_type=fs_event.event_type
            )
            self.logger.debug("Filesystem event received", extra={
                "path": fs_event.src_path,
                "type": fs_event.event_type
            })
            for cb in self._callbacks:
                cb(evt)
        except Exception as e:
            self.logger.error("Error dispatching event", exc_info=e)

    def start(self):
        if not self._observer.is_alive():
            for p in self._paths:
                self._observer.schedule(self._handler, p, recursive=True)
            self._observer.start()

    def stop(self):
        if self._observer.is_alive():
            self._observer.stop()
            self._observer.join()

class _InternalHandler(FileSystemEventHandler):
    def __init__(self, dispatch: Callable):
        self._dispatch = dispatch

    def on_any_event(self, event):
        self._dispatch(event)
