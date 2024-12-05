import logging

def setup_logger(name, log_file, level_log=logging.INFO):

    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    logger = logging.Logger(name)
    logger.setLevel(level_log)

    handlers = [logging.FileHandler(log_file), logging.StreamHandler]

    for handler in handlers:

        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger

default_logger = setup_logger(name="Challenge 3", log_file="default.log")