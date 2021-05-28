"""
Author:柠檬班-木森
Time:2020/8/4   21:31
E-mail:3247119728@qq.com
"""
import os
import logging
from logging.handlers import TimedRotatingFileHandler
from apin.core.parsersetting import settings
import colorama

colorama.init()


class Logger:
    __instance = None
    sh = logging.StreamHandler()

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super().__new__(cls)
            if not os.path.isdir(settings.LOG_FILE_PATH):
                os.mkdir(settings.LOG_FILE_PATH)
            level = 'DEBUG' if getattr(settings, 'DEBUG') else "INFO"
            log = logging.getLogger('musen')
            log.setLevel(level)
            # 创建一个handler,用于写入日志文件
            fh = TimedRotatingFileHandler(os.path.join(settings.LOG_FILE_PATH, 'logging.log'), when='d',
                                          interval=1, backupCount=7,
                                          encoding="utf-8")
            fh.setLevel(level)
            # 定义handler的输出格式
            formatter = logging.Formatter("%(levelname)s %(asctime)s | 【】 | : %(message)s")
            fh.setFormatter(formatter)
            log.addHandler(fh)
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
