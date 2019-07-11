# coding=utf-8

import requests
import time
from datetime import date, timedelta
from fake_useragent import UserAgent
from toubiao_info import get_info_tuobiao, get_total
from log import Logger

log = Logger()
ua = UserAgent()
session = requests.session()


def get_up():  # 每日更新
    try:
        today = (date.today() + timedelta(days=-1)).strftime("%Y:%m:%d")
        headers = {
            'User-Agent': ua.random,
            'Connection': 'close'
        }
        params = {
            'searchtype': 1,
            'page_index': 1,
            'bidSort': 0,
            'buyerName': '',
            'projectId': '',
            'pinMu': 0,
            'bidType': 0,
            'dbselect': 'bidx',
            'kw': '',
            'start_time': today,
            'end_time': today,
            'timeType': 6,
            'displayZone': '',
            'zoneId': '',
           # 'pppStatus': 0,
            'agentName': ''
        }
        url = 'http://search.ccgp.gov.cn/bxsearch?'
        log.getlog('访问网址')
        # time.sleep(random.randint(10, 15))
        web_data = session.get(url, headers=headers, params=params, timeout=20)
        web_data.encoding = web_data.apparent_encoding
        log.getlog(web_data.status_code)
        if web_data.status_code == 200:
            total_num = get_total(web_data.text)
            with open('up_total_num.txt', 'wb') as f:
                f.write(bytes(str(total_num), encoding='utf-8'))
                f.close()
            txt = get_info_tuobiao(web_data.text)
            up_get_next_page(int(total_num))
            if txt == '获取完毕':
                return '获取完毕'
        if web_data.status_code != 200:
            log.getlog('访问网址出错(状态码):{}'.format(web_data.status_code))
            log.getlog('重新请求')
            for num in range(5):
                txt = get_up_again()
                if txt == '获取完毕':
                    return '获取完毕'
    except requests.exceptions.ReadTimeout:
        log.getlog('重新查找')
        for num in range(5):
            txt = get_up_again()
            if txt == '获取完毕':
                return '获取完毕'
    except requests.exceptions.ConnectionError:
        log.getlog('重新查找')
        for num in range(5):
            txt = get_up_again()
            if txt == '获取完毕':
                return '获取完毕'
    return get_up


def get_up_again():  # 重新获取更新
    try:
        today = (date.today() + timedelta(days=-1)).strftime("%Y:%m:%d")
        headers = {
            'User-Agent': ua.random,
            'Connection': 'close'
        }
        params = {
            'searchtype': 1,
            'page_index': 1,
            'bidSort': 0,
            'buyerName': '',
            'projectId': '',
            'pinMu': 0,
            'bidType': 0,
            'dbselect': 'bidx',
            'kw': '',
            'start_time': today,
            'end_time': today,
            'timeType': 6,
            'displayZone': '',
            'zoneId': '',
            # 'pppStatus': 0,
            'agentName': ''
        }
        url = 'http://search.ccgp.gov.cn/bxsearch?'
        log.getlog('重新访问网址')
        # time.sleep(random.randint(10, 15))
        web_data = session.get(url, headers=headers, params=params, timeout=20)
        web_data.encoding = web_data.apparent_encoding
        if web_data.status_code == 200:
            total_num = get_total(web_data.text)
            with open('up_total_num.txt', 'wb') as f:
                f.write(bytes(str(total_num), encoding='utf-8'))
                f.close()
            txt = get_info_tuobiao(web_data.text)
            up_get_next_page(int(total_num))
            if txt == '获取完毕':
                return '获取完毕'
        if web_data.status_code != 200:
            log.getlog('访问网址出错(状态码):{}'.format(web_data.status_code))
            return web_data.status_code
    except requests.exceptions.ReadTimeout:
        return ''
    except requests.exceptions.ConnectionError:
        return ''


def up_get_next_page(total_num):  # 获取下一页
    for num in range(2, total_num):
        try:
            with open('up_toubiao_num.txt', 'wb') as f:
                f.write(bytes(str(num), encoding='utf-8'))
                f.close()
            up_get_web_data(num)
        except requests.exceptions.ReadTimeout:
            up_get_next_page_again()
        except requests.exceptions.ConnectionError:
            up_get_next_page_again()
    return ''


def up_get_next_page_again():  # 更新获取页码错误时自动继续获取
    with open('up_toubiao_num.txt', 'rb') as f:
        nums = f.read()
        f.close()
        nums = nums.decode('utf-8')
    with open('up_total_num.txt', 'rb') as f:
        total_nums = f.read()
        f.close()
        total_num = total_nums.decode('utf-8')
    for num in range(int(nums), int(total_num)):
        with open('up_toubiao_num.txt', 'wb') as f:
            f.write(bytes(str(num), encoding='utf-8'))
            f.close()
        try:
            up_get_web_data(num)
        except requests.exceptions.ReadTimeout:
            up_get_web_data(num)
        except requests.exceptions.ConnectionError:
            up_get_web_data(num)
    return up_get_next_page_again


def up_get_web_data(num):  # 重复请求网页
    try:
        today = (date.today() + timedelta(days=-1)).strftime("%Y:%m:%d")
        headers = {
            'User-Agent': ua.random,
            'Connection': 'close'
        }
        params = {
            'searchtype': 1,
            'page_index': num,
            'bidSort': 0,
            'buyerName': '',
            'projectId': '',
            'pinMu': 0,
            'bidType': 0,
            'dbselect': 'bidx',
            'kw': '',
            'start_time': today,
            'end_time': today,
            'timeType': 6,
            'displayZone': '',
            'zoneId': '',
            # 'pppStatus': 0,
            'agentName': ''
        }
        # time.sleep(random.randint(10, 15))
        url = 'http://search.ccgp.gov.cn/bxsearch?'
        log.getlog('第' + str(num) + '页')
        web_data = session.get(url, headers=headers, params=params, timeout=20)
        web_data.encoding = web_data.apparent_encoding
        if web_data.status_code == 200:
            txt = get_info_tuobiao(web_data.text)
            if txt == '获取完毕':
                return '获取完毕'
        if web_data.status_code != 200:
            log.getlog('访问网址出错(状态码):{}'.format(web_data.status_code))
            log.getlog('重新请求第' + str(num) + '页')
            for nums in range(5):
                txt = up_get_web_data_again(num)
                if txt == '获取完毕':
                    return '获取完毕'
    except requests.exceptions.ReadTimeout:
        log.getlog('重复请求网页再次请求第' + str(num) + '页')
        for nums in range(5):
            txt = up_get_web_data_again(num)
            if txt == '获取完毕':
                return '获取完毕'
    except requests.exceptions.ConnectionError:
        log.getlog('重复请求网页再次请求第' + str(num) + '页')
        for nums in range(5):
            txt = up_get_web_data_again(num)
            if txt == '获取完毕':
                return '获取完毕'
    return up_get_web_data


def up_get_web_data_again(num):  # 请求直至获取数据
    try:
        today = (date.today() + timedelta(days=-1)).strftime("%Y:%m:%d")
        headers = {
            'User-Agent': ua.random,
            'Connection': 'close'
        }
        params = {
            'searchtype': 1,
            'page_index': num,
            'bidSort': 0,
            'buyerName': '',
            'projectId': '',
            'pinMu': 0,
            'bidType': 0,
            'dbselect': 'bidx',
            'kw': '',
            'start_time': today,
            'end_time': today,
            'timeType': 6,
            'displayZone': '',
            'zoneId': '',
            # 'pppStatus': 0,
            'agentName': ''
        }
        # time.sleep(random.randint(10, 15))
        url = 'http://search.ccgp.gov.cn/bxsearch?'
        log.getlog('第' + str(num) + '页')
        web_data = session.get(url, headers=headers, params=params, timeout=20)
        web_data.encoding = web_data.apparent_encoding
        if web_data.status_code == 200:
            txt = get_info_tuobiao(web_data.text)
            if txt == '获取完毕':
                return '获取完毕'
        if web_data.status_code != 200:
            log.getlog('访问网址出错(状态码):{}'.format(web_data.status_code))
            return web_data.status_code
    except requests.exceptions.ReadTimeout:
        return ''
    except requests.exceptions.ConnectionError:
        return ''


def get_page():  # 获取第一页
    try:
        headers = {
            'User-Agent': ua.random,
            'Connection': 'close'
        }
        params = {
            'searchtype': 1,
            'page_index': 1,
            'bidSort': 0,
            'buyerName': '',
            'projectId': '',
            'pinMu': 0,
            'bidType': 0,
            'dbselect': 'bidx',
            'kw': '',
            'start_time': '2019:05:02',
            'end_time': '2019:05:04',
            'timeType': 6,
            'displayZone': '',
            'zoneId': '',
            # 'pppStatus': 0,
            'agentName': ''
        }
        log.getlog('访问网址')
        # time.sleep(random.randint(10, 15))
        url = 'http://search.ccgp.gov.cn/bxsearch?'
        web_data = session.get(url, headers=headers, params=params, timeout=20)
        web_data.encoding = web_data.apparent_encoding
        if web_data.status_code == 200:
            txt = get_info_tuobiao(web_data.text)
            total_num = get_total(web_data.text)
            with open('total_num.txt', 'wb') as f:
                f.write(bytes(str(total_num), encoding='utf-8'))
                f.close()
            get_next_page(int(total_num))
            if txt == '获取完毕':
                return '获取完毕'
        if web_data.status_code != 200:
            log.getlog('访问网址出错(状态码):{}'.format(web_data.status_code))
            log.getlog('重新请求')
            for num in range(5):
                txt = get_page()
                if txt == '获取完毕':
                    return '获取完毕'
    except requests.exceptions.ReadTimeout:
        for num in range(5):
            log.getlog('重新访问')
            txt = get_page()
            if txt == '获取完毕':
                return '获取完毕'
    except requests.exceptions.ConnectionError:
        for num in range(5):
            log.getlog('重新访问')
            txt = get_page()
            if txt == '获取完毕':
                return '获取完毕'
    return get_page


def get_next_page(total_num):  # 获取下一页
    for num in range(2, total_num):
        try:
            with open('toubiao_num.txt', 'wb') as f:
                f.write(bytes(str(num), encoding='utf-8'))
                f.close()
            get_web_data(num)
        except requests.exceptions.ReadTimeout:
            get_next_page_again()
        except requests.exceptions.ConnectionError:
            get_next_page_again()
    return get_next_page


def get_next_page_again():  # 获取页码错误时自动继续获取
    with open('toubiao_num.txt', 'rb') as f:
        nums = f.read()
        f.close()
        nums = nums.decode('utf-8')
    with open('total_num.txt', 'rb') as f:
        total_nums = f.read()
        f.close()
        total_num = total_nums.decode('utf-8')
    for num in range(int(nums), int(total_num)):
        tnum = time.strftime('%H%M', time.localtime(time.time()))
        if int(tnum) > 2010 and int(tnum) < 2301:
            log.getlog(tnum[0:2]+'时'+tnum[2:4]+'分')
            log.getlog('等待更新程序完成')
            time.sleep(60*200)
        else:
            with open('toubiao_num.txt', 'wb') as f:
                f.write(bytes(str(num), encoding='utf-8'))
                f.close()
            try:
                get_web_data(num)
            except requests.exceptions.ReadTimeout:
                get_web_data(num)
            except requests.exceptions.ConnectionError:
                get_web_data(num)
    return get_next_page_again


def get_web_data(num):  # 重复请求网页
    try:
        headers = {
            'User-Agent': ua.random,
            'Connection': 'close'
        }
        params = {
            'searchtype': 1,
            'page_index': num,
            'bidSort': 0,
            'buyerName': '',
            'projectId': '',
            'pinMu': 0,
            'bidType': 0,
            'dbselect': 'bidx',
            'kw': '',
            'start_time': '2019:05:02',
            'end_time': '2019:05:04',
            'timeType': 6,
            'displayZone': '',
            'zoneId': '',
            # 'pppStatus': 0,
            'agentName': ''
        }
        # time.sleep(random.randint(10, 15))
        url = 'http://search.ccgp.gov.cn/bxsearch?'
        log.getlog('第' + str(num) + '页')
        web_data = session.get(url, headers=headers, params=params, timeout=20)
        web_data.encoding = web_data.apparent_encoding
        if web_data.status_code == 200:
            txt = get_info_tuobiao(web_data.text)
            if txt == '获取完毕':
                return '获取完毕'
        if web_data.status_code != 200:
            log.getlog('访问网址出错(状态码):{}'.format(web_data.status_code))
            for nums in range(5):
                txt = get_web_data_again(num)
                if txt == '获取完毕':
                    return '获取完毕'
    except requests.exceptions.ReadTimeout:
        for nums in range(5):
            txt = get_web_data_again(num)
            if txt == '获取完毕':
                return '获取完毕'
    except requests.exceptions.ConnectionError:
        for nums in range(5):
            txt = get_web_data_again(num)
            if txt == '获取完毕':
                return '获取完毕'
    return get_web_data


def get_web_data_again(num):  # 请求直至获取数据
    try:
        headers = {
            'User-Agent': ua.random,
            'Connection': 'close'
        }
        params = {
            'searchtype': 1,
            'page_index': num,
            'bidSort': 0,
            'buyerName': '',
            'projectId': '',
            'pinMu': 0,
            'bidType': 0,
            'dbselect': 'bidx',
            'kw': '',
            'start_time': '2019:05:02',
            'end_time': '2019:05:04',
            'timeType': 0,
            'displayZone': '',
            'zoneId': '',
            # 'pppStatus': 0,
            'agentName': ''
        }
        # time.sleep(random.randint(10, 15))
        url = 'http://search.ccgp.gov.cn/bxsearch?'
        log.getlog('重复请求第' + str(num) + '页')
        web_data = session.get(url, headers=headers, params=params, timeout=20)
        web_data.encoding = web_data.apparent_encoding
        if web_data.status_code == 200:
            txt = get_info_tuobiao(web_data.text)
            if txt == '获取完毕':
                return '获取完毕'
        if web_data.status_code != 200:
            log.getlog('访问网址出错(状态码):{}'.format(web_data.status_code))
            return web_data.status_code
    except requests.exceptions.ReadTimeout:
        return ''
    except requests.exceptions.ConnectionError:
        return ''


if __name__ == '__main__':
    get_page()
    # get_up()
