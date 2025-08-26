import logging
import sys

def setup_logging():
    """
    Configures the logging system to write error messages to a file.
    """
    logging.basicConfig(
        level=logging.ERROR,
        format='%(asctime)s - %(levelname)s - %(message)s',
        filename='file_errors.log',
        filemode='a'
    )