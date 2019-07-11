# coding=utf-8
from toubiao import get_page, get_next_page_again
from log import Logger
from find_error import get_error

log = Logger()


if __name__ == '__main__':
    try:
        get_page()
    except:
        get_next_page_again()
    finally:
        get_error()

