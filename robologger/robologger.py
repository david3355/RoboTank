import logging


def get_logger(logger_name):
    log = logging.getLogger(logger_name)
    log_format = '%(asctime)s %(name)-12s %(levelname)8s\t%(message)s'
    logging.basicConfig(level=logging.DEBUG, format=log_format)
    return log
