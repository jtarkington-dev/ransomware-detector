from dataclasses import dataclass, field
import time

@dataclass
class Event:
    path: str
    event_type: str
    timestamp: float = field(default_factory=time.time)
    # optional: add fields like entropy, size, etc., later
