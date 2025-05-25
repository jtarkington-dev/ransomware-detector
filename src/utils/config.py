import os

class Config:
    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE = os.getenv("LOG_FILE", "logs/detector.log")

    # Detection thresholds
    ENTROPY_THRESHOLD = float(os.getenv("ENTROPY_THRESHOLD", 7.5))
    FILE_CHANGE_RATE = int(os.getenv("FILE_CHANGE_RATE", 100))

    # Actions to take when ransomware is detected
    ISOLATION_ACTIONS = [
        action.strip()
        for action in os.getenv("ISOLATION_ACTIONS", "").split(",")
        if action.strip()
    ]

    # Alerting & sandbox
    ALERT_EMAIL = os.getenv("ALERT_EMAIL", "")
    SANDBOX_DIR = os.getenv("SANDBOX_DIR", "")

    # Force OS (overrides detection)
    OS_OVERRIDE = os.getenv("OS_OVERRIDE", "").lower()

# Single shared config object
config = Config()
