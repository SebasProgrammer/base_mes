from .instances import config

import sys
import logging

# Use Lima, Peru timezone for datetime in logs
# Source: https://stackoverflow.com/a/62265324
from pytz import timezone
from datetime import datetime
logging.Formatter.converter = lambda *args: datetime.now(tz = timezone('America/Lima')).timetuple()


def get_logger():
  logging_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  logging_date_format = "%Y/%m/%d %H:%M:%S %p"
  
  if config['profile'] == 'local':
    logger = logging.getLogger(__name__)
    logging.basicConfig(
      handlers = [
        logging.FileHandler(
          filename = "status.log", 
          encoding = 'utf-8', 
          mode = 'w',
          delay = True
        )
      ],
      format = logging_format,
      datefmt = logging_date_format,
      level = logging.INFO
    )
    return logger

  if config['profile'] == 'production':
    logger = logging.getLogger()
    
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(
      logging.Formatter(logging_format, logging_date_format)
    )

    logger.addHandler(console_handler)
    logger.setLevel(logging.INFO)
    return logger