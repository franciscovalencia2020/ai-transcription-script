import logging
import os
import sys


def setup_logger(log_path: str = "logs/transcription.log") -> logging.Logger:
    """
    Sets up a logger that writes logs to both a file and the console (UTF-8 compatible).

    Args:
        log_path: Path to the log file.

    Returns:
        A configured logger instance.
    """
    try:
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
    except Exception as e:
        print(f"⚠️ Failed to create log directory: {e}")

    logger = logging.getLogger("TranscriptionLogger")
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        file_handler = logging.FileHandler(log_path, encoding='utf-8')
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(logging.Formatter('%(levelname)s - %(message)s'))

        try:
            stream_handler.stream.reconfigure(encoding='utf-8')
        except AttributeError:
            pass

        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)

    return logger
