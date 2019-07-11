# -*- coding: utf-8 -*-
import sys
import socket
import time
import traceback


def get_error():
    '''
    1.使用sys.exc_info接受返回的数组包含异常的对象类型，异常的值以及一个traceback对象，对象中包含出错的行数、位置等数据
    2.使用traceback模块提供的extract_tb函数来更加详细的解释traceback对象所包含的数据，数据包含异常文件名，异常的函数名，异常所在行，异常的报错点
    :return:
    '''

    # ip = socket.gethostbyname(socket.gethostname())
    times = time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time()))
    text = ""
    ex_type, ex_val, ex_stack = sys.exc_info()

    for filename, linenum, funcname, source in traceback.extract_tb(ex_stack):
        txt="{times} '{filename}', line{linenum}, in {funcname}\n\t{source}\n".format(times=times, filename=filename, linenum=linenum, source=source, funcname=funcname)
        text += txt

    if text:
        text += "{ErrorType}:{Value}\n".format(ErrorType=ex_type, Value=ex_val)

        with open('logging', 'ab+') as f:
            f.write(text.encode('utf8'))
            f.close()
    return ''
