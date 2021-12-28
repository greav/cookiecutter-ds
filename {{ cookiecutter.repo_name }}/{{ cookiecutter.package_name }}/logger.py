import logging

LOG_LEVELS = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
}

DEFAULT_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"


def _get_library_name():

    return __name__.split(".")[0]


def configure_root_logger(log_level="INFO", fmt=DEFAULT_FORMAT):
    stream_handler = logging.StreamHandler()
    formatter = logging.Formatter(fmt)
    stream_handler.setFormatter(formatter)
    root_logger = logging.getLogger(_get_library_name())
    root_logger.addHandler(stream_handler)
    root_logger.setLevel(LOG_LEVELS.get(log_level, logging.WARNING))
    return root_logger
