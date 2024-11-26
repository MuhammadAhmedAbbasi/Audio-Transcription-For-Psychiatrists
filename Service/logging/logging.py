import logging
from logging.handlers import RotatingFileHandler
import os
from datetime import datetime

# Directory for log files
LOG_DIR = "Service/logging/log_data"
os.makedirs(LOG_DIR, exist_ok=True)

# Create a custom logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)  # Set the logging level

# Create a unique log filename based on the current timestamp
log_filename = os.path.join(LOG_DIR, f"app_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

# Create a rotating file handler with UTF-8 encoding
handler = RotatingFileHandler(log_filename, maxBytes=1000000, backupCount=3, encoding='utf-8')
handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)

def get_logger():
    return logger
