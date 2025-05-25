from abc import ABC, abstractmethod
from typing import Callable
from .event import Event

class Monitor(ABC):
    """
    Watch for file‐system events and invoke a callback
    for each event seen.
    """

    @abstractmethod
    def start(self) -> None:
        """Begin watching in the background."""

    @abstractmethod
    def stop(self) -> None:
        """Stop watching and clean up resources."""

    @abstractmethod
    def on_event(self, callback: Callable[[Event], None]) -> None:
        """
        Register a callback to be invoked with each Event.
        The Event dataclass carries path, event_type, timestamp.
        """
