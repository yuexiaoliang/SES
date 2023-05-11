import logging
import os


class Logger:
    def __init__(self, log_file=None, log_level=logging.ERROR):
        log_format = '%(asctime)s - %(levelname)s - %(message)s'

        if log_file:
            os.makedirs(os.path.dirname(log_file), exist_ok=True)

            file_handler = logging.FileHandler(
                log_file, mode='w', encoding='utf-8')
            formatter = logging.Formatter(log_format)
            file_handler.setFormatter(formatter)

            logger = logging.getLogger()
            logger.setLevel(log_level)
            logger.addHandler(file_handler)
        else:
            logging.basicConfig(level=log_level, format=log_format)

    def debug(self, message):
        logging.debug(message)

    def info(self, message):
        logging.info(message)

    def warning(self, message):
        logging.warning(message)

    def error(self, message):
        logging.error(message)

    def critical(self, message):
        logging.critical(message)


# 使用示例
if __name__ == "__main__":
    logger = Logger(log_file='logs/logger_test_file.log')

    logger.debug("这是一条 debug 日志")
    logger.info("这是一条 info 日志")
    logger.warning("这是一条 warning 日志")
    logger.error("这是一条 error 日志")
    logger.critical("这是一条 critical 日志")
