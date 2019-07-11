# coding=utf-8

from toubiao import get_up
import time
from find_error import get_error
from log import Logger

log = Logger()


if __name__ == '__main__':
    #up_get_next_page_again()
    while True:
        try:
            num = time.strftime('%H%M', time.localtime(time.time()))
            log.getlog(num[0:2]+'时'+num[2:4]+'分')
            if int(num) > 105 and int(num) < 125:
                get_up()
                log.getlog('招投标今日更新完毕等待更新')
                time.sleep(60*10)
            log.getlog('招投标等待更新')
            time.sleep(60*10)
        except KeyboardInterrupt:
            break
        finally:
            get_error()
