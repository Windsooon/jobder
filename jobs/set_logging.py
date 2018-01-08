import json
import logging


def setup_logging(
    default_path='logging.json',
    default_level=logging.DEBUG,
):
    """Setup logging configuration
    """
    with open(default_path) as data_file:
        data = json.loads(data_file.read())
    logging.config.dictConfig(data)
    return logging
