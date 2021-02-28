import logging


def __get_logger():
    """
    :return: Logger instance
    """

    __logger = logging.getLogger('logger')

    # Logging format
    formatter = logging.Formatter(
        '[%(levelname)s] %(asctime)s => BACKEND@%(filename)s:%(lineno)s >> %(message)s')
    # Stream handler
    stream_handler = logging.StreamHandler()
    # Format for each handler
    stream_handler.setFormatter(formatter)
    # Inserting handler to logger instance
    __logger.addHandler(stream_handler)

    # LOGGING LEVEL
    __logger.setLevel(logging.DEBUG)

    return __logger
