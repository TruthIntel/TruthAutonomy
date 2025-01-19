import logging


def setup_logger(name: str) -> logging.Logger:
    """
    Sets up a logger for the given name.

    Args:
        name (str): The name of the logger. Typically the module name.

    Returns:
        logging.Logger: The configured logger.
    """
    # Create a logger
    logger = logging.getLogger(name)

    # Set the logging level (you can change this to DEBUG, ERROR, etc. based on needs)
    logger.setLevel(logging.INFO)

    # Create a console handler and set the log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    # Create a formatter and set it for the handler
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    ch.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(ch)

    return logger


# Create a default logger
logger = setup_logger(__name__)
