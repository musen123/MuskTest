# Author:柠檬班-木森
# E-mail:musen_nmb@qq.com
import os
import datetime
import logging
from logging.handlers import TimedRotatingFileHandler, BaseRotatingHandler
import colorama

colorama.init()


class Logger:
    __instance = None
    sh = logging.StreamHandler()

    def __new__(cls, path=None, level='DEBUG', RotatingFileHandler: BaseRotatingHandler = None):
        """
        :param path: report path
        :param args:
        :param kwargs:
        :return:
        """
        if not cls.__instance:
            cls.__instance = super().__new__(cls)
            log = logging.getLogger('apin')
            log.setLevel(level)
            if path:
                if not os.path.isdir(path):
                    os.mkdir(path)

                if RotatingFileHandler and isinstance(RotatingFileHandler, BaseRotatingHandler):
                    fh = RotatingFileHandler
                else:
                    fh = TimedRotatingFileHandler(os.path.join(path, 'logging.log'), when='d',
                                                  interval=1, backupCount=7,
                                                  encoding="utf-8")
                fh.setLevel(level)
                log.addHandler(fh)
                # 定义handler的输出格式
                formatter = logging.Formatter("%(asctime)s | 【%(levelname)s】 | : %(message)s")
                fh.setFormatter(formatter)
            cls.__instance.log = log

        return cls.__instance

    def debug(self, message):
        self.fontColor('\033[0;34m{}\033[0;34m{}\033[0;34m{}')
        self.log.debug(message)

    def info(self, message):
        self.fontColor('\033[0;32m{}\033[0;32m{}\033[0;32m{}')
        self.log.info(message)

    def warning(self, message):
        self.fontColor('\033[0;33m{}\033[0;43m{}\033[0;33m{}')
        self.log.warning(message)

    def error(self, message):
        self.fontColor('\033[0;31m{}\033[0;41m{}\033[0;31m{}')
        self.log.error(message)

    def exception(self, message):
        self.fontColor('\033[0;31m{}\033[0;41m{}\033[0;31m{}')
        self.log.exception(message)

    def critical(self, message):
        self.fontColor('\033[0;35m{}\033[0;45m{}\033[0;35m{}')
        self.log.critical(message)

    def fontColor(self, color):
        # 不同的日志输出不同的颜色
        formatter = logging.Formatter(color.format("%(asctime)s| ", "【%(levelname)s】", " | : %(message)s"))
        self.sh.setFormatter(formatter)
        self.log.addHandler(self.sh)


class CaseLog:
    log = Logger()

    def save_log(self, message, level):
        if not hasattr(self, 'log_data'):
            setattr(self, 'log_data', [])
        info = "【{}】| {} |: {}".format(level, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'), message)
        getattr(self, 'log_data').append((level, info))

    def save_error(self, message):
        if not hasattr(self, 'error_info'):
            setattr(self, 'error_info', [])
        getattr(self, 'error_info').append("【ERROR】:{} ".format(message))

    def debug_log(self, message):
        self.save_log(message, 'DEBUG')
        self.log.debug(message)

    def info_log(self, message):
        self.save_log(message, 'INFO')
        self.log.info(message)

    def warning_log(self, message):
        self.save_log(message, 'WARNING')
        self.log.warning(message)

    def error_log(self, message):
        self.save_log(message, 'ERROR')
        self.save_error(message)
        self.log.error(message)

    def exception_log(self, message):
        self.save_log(message, 'ERROR')
        self.save_error(message)
        self.log.exception(message)

    def critical_log(self, message):
        self.save_log(message, 'CRITICAL')
        self.save_error(message)
        self.log.critical(message)


def print_info(msg):
    print('\033[0;32m{}'.format(msg))


def print_waring(msg):
    print('\033[0;33m{}'.format(msg))


def print_error(msg):
    print('\033[0;31m{}'.format(msg))


if __name__ == '__main__':
    logger = Logger()
    logger.debug('debu等级日志')
    logger.info('info日志')
    logger.warning('warning日志')
    logger.error('error日志')
    logger.critical('CRITICAL日志')
    print_info('12323')
    print_waring('12323')
    print_error('12323')
