# -*- coding: utf-8 -*-
import logging


# 开发一个日志系统， 既要把日志输出到控制台， 还要写入日志文件
class Logger(object):
    '''
       指定保存日志的文件路径，日志级别，以及调用文件
       将日志存入到指定的文件中
    '''
    # 创建一个logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # 创建一个handler，用于写入日志文件
    fh = logging.FileHandler('log.txt')
    fh.setLevel(logging.INFO)

    # 再创建一个handler，用于输出到控制台
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    # 定义handler的输出格式
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # 给logger添加handler
    logger.addHandler(fh)
    logger.addHandler(ch)

    def getlog(self, message):
        logging.info(message)
        return ''


if __name__ == '__main__':
    logger = Logger().getlog('123')


