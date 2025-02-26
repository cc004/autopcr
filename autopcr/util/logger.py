import logging
import os
from logging.handlers import TimedRotatingFileHandler
from ..constants import LOG_PATH, LOG_LEVEL

class Logger:
    def __init__(self, log_dir: str, log_name: str, log_level: int = logging.DEBUG):
        self.log_dir = log_dir
        self.log_name = log_name
        self._setup_logger(log_level)

    def _setup_logger(self, log_level: int):
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
        
        log_path = os.path.join(self.log_dir, self.log_name)
        
        self.logger = logging.getLogger(self.log_name)
        self.logger.setLevel(log_level)

        handler = TimedRotatingFileHandler(
            log_path, when="midnight", interval=1, backupCount=7, encoding="utf-8"
        )
        handler.suffix = "%Y-%m-%d.log"
        
        formatter = logging.Formatter('%(asctime)s - [%(levelname)s]: %(message)s')
        handler.setFormatter(formatter)

        self.logger.addHandler(handler)

    def get_logger(self):
        return self.logger

instance = Logger(LOG_PATH, 'autopcr.log', LOG_LEVEL).get_logger()
