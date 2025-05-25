import time
from collections import deque
from typing import Deque, Callable
from .base_detector import Detector
from monitors.event import Event
from utils.config import config
import logging

class ChangeRateDetector(Detector):
    def __init__(self, window: float = 60.0):
        """
        window: how many seconds to look back
        """
        self.window = window
        self.events: Deque[float] = deque()
        self.alert_callbacks = []
        self.logger = logging.getLogger(__name__)

    def on_event(self, event: Event) -> None:
        now = event.timestamp
        self.events.append(now)
        # purge old
        while self.events and now - self.events[0] > self.window:
            self.events.popleft()

        rate = len(self.events) * (60.0 / self.window)
        self.logger.debug("ChangeRate", count=len(self.events), rate=rate)

        if rate >= config.FILE_CHANGE_RATE:
            reason = f"High change rate: {rate:.1f} events/min"
            self.logger.warning("Ransomware suspected", reason=reason)
            for cb in self.alert_callbacks:
                cb(event, reason)

    def on_alert(self, callback: Callable[[Event, str], None]) -> None:
        self.alert_callbacks.append(callback)
