import logging

COLORS = {
    'DEBUG': '\033[94m',    # Blue
    'INFO': '\033[92m',     # Green
    'WARNING': '\033[93m',  # Yellow
    'ERROR': '\033[38;5;208m',  # Orange (256-color code)
    'CRITICAL': '\033[91m', # Red
}
RESET = '\033[0m'

class ColorFormatter(logging.Formatter):
    def format(self, record):
        levelname = record.levelname
        color = COLORS.get(levelname, RESET)
        record.levelname = f"{color}[{levelname}]{RESET}"
        return super().format(record)

def get_logger(log_level):
    logger = logging.getLogger("my_app")
    logger.setLevel(log_level)

    # Handler for console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(ColorFormatter('%(levelname)s %(message)s'))

    logger.addHandler(console_handler)
    return logger