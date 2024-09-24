import logging
import os


def setup_logger(log_file='application.log', log_level=logging.INFO):
    # Create a custom logger
    logger = logging.getLogger(__name__)

    # Check if logger already has handlers, avoid adding multiple handlers
    if not logger.hasHandlers():
        # Set the log level
        logger.setLevel(log_level)

        # Create a file handler to log messages to a file
        log_directory = os.path.dirname(log_file)
        if log_directory and not os.path.exists(log_directory):
            os.makedirs(log_directory)

        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(log_level)

        # Create a console handler to log messages to the console (optional)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)

        # Create a logging format
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Add the handlers to the logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger
