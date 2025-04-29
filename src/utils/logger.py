import logging
import os
import sys
from pathlib import Path

from pythonjsonlogger import jsonlogger

from src.utils.path_manager import PathManager


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    """Custom JSON formatter for logging."""
    
    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        log_record['level'] = record.levelname
        log_record['logger'] = record.name

def setup_logger(name: str = 'app') -> logging.Logger:
    """
    Set up a logger with both file and console handlers.
    
    Args:
        name (str): Name of the logger
        
    Returns:
        logging.Logger: Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Clear any existing handlers
    logger.handlers = []
    
    # Create formatters
    json_formatter = CustomJsonFormatter('%(asctime)s %(levelname)s %(name)s %(message)s')
    console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    
    # File handler
    path_manager = PathManager()
    log_file = os.path.join(path_manager.log_dir, f'{name}.log')
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(json_formatter)
    logger.addHandler(file_handler)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    return logger

# Create default logger instance
logger = setup_logger() 