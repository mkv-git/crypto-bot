import sys
import logging
import logging.config


extra = {"orderName": sys.argv[1] if len(sys.argv) > 1 else ''}
print(sys.argv, extra)

def get_logger(filename, logger_name):
    logging.config.fileConfig(filename)
    logger = logging.getLogger(logger_name)
    if logger_name == "cryptobot":
        logger = logging.LoggerAdapter(logger, extra)
    return logger


log = get_logger("config/logging.conf", "cryptobot")
