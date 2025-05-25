from abc import ABC, abstractmethod
from monitors.event import Event
from typing import Callable

class Detector(ABC):
    """
    Consume file‐system Events and invoke a callback when
    a detection threshold is crossed.
    """

    @abstractmethod
    def on_event(self, event: Event) -> None:
        """Feed a new Event into the detector."""

    @abstractmethod
    def on_alert(self, callback: Callable[[Event, str], None]) -> None:
        """
        Register a callback to invoke when ransomware is detected.
        Callback will be passed the triggering Event and a short reason.
        """
