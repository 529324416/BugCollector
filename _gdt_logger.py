import logging
import time
import os

class _GDTLoggerUtils:
    '''utility class for logger'''

    @staticmethod
    def create_dir_if_not_exist(dirpath:str) -> bool:
        '''create a new directory if not exist'''

        if not os.path.exists(dirpath):
            os.makedirs(dirpath)
            return True
        return False

    @staticmethod
    def create_logger(filepath:str) -> logging.Logger:
        '''create a new logger object'''

        logging.basicConfig(filename=filepath, level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s', filemode="w")
        logger = logging.getLogger()
        return logger


class GDTLogger:
    '''logger class for GDT server'''

    def __init__(self, folder):
        '''initialize logger object'''

        self.__folder = folder
        _GDTLoggerUtils.create_dir_if_not_exist(folder)
        self.__current_day_info, self.__logger = self.__get_today_logger()

    def __get_today_logger(self) -> logging.Logger:
        '''get logger for today'''

        _today = time.strftime("%Y-%m-%d", time.localtime())
        _filepath = os.path.join(self.__folder, _today + ".log")
        return _today, _GDTLoggerUtils.create_logger(_filepath)
    
    def __check_logger(self):
        '''check if we need a new logger'''

        _today = time.strftime("%Y-%m-%d", time.localtime())
        if _today != self.__current_day_info:
            self.__current_day_info, self.__logger = self.__get_today_logger()

    def debug(self, msg:object):
        '''if day has changed, then we create a new log file'''

        self.__check_logger()
        self.__logger.debug(msg)

    def error(self, msg:object):
        '''if day has changed, then we create a new log file'''

        self.__check_logger()
        self.__logger.error(msg)

    def info(self, msg:object):
        '''if day has changed, then we create a new log file'''

        self.__check_logger()
        self.__logger.info(msg)

    def warning(self, msg:object):

        self.__check_logger()
        self.__logger.warning(msg)


if __name__ == '__main__':

    logger = GDTLogger("./server_logs")
    logger.debug("hello world")
    logger.error("some bad happened..")
    logger.warning("be careful")