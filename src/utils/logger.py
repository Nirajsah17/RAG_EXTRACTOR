import logging
import os
from logging.handlers import RotatingFileHandler


# -----------------------------
# Config
# -----------------------------
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_DIR = os.getenv("LOG_DIR", "logs")
LOG_FILE = os.path.join(LOG_DIR, "app.log")


# -----------------------------
# Ensure log directory exists
# -----------------------------
os.makedirs(LOG_DIR, exist_ok=True)


# -----------------------------
# Custom Formatter (better readability)
# -----------------------------
class CustomFormatter(logging.Formatter):
    def format(self, record):
        return (
            f"[{self.formatTime(record)}] "
            f"[{record.levelname}] "
            f"[{record.name}] "
            f"{record.getMessage()}"
        )


# -----------------------------
# Logger Factory
# -----------------------------
def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)

    # Prevent duplicate handlers
    if logger.handlers:
        return logger

    logger.setLevel(LOG_LEVEL)

    # -----------------------------
    # Console Handler
    # -----------------------------
    console_handler = logging.StreamHandler()
    console_handler.setLevel(LOG_LEVEL)
    console_handler.setFormatter(CustomFormatter())

    # -----------------------------
    # File Handler (with rotation)
    # -----------------------------
    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=5 * 1024 * 1024,  # 5 MB
        backupCount=3
    )
    file_handler.setLevel(LOG_LEVEL)
    file_handler.setFormatter(CustomFormatter())

    # -----------------------------
    # Attach handlers
    # -----------------------------
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    # Avoid propagating to root logger
    logger.propagate = False

    return logger