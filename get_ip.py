# -*- coding: UTF-8 -*-


import requests
import time

ips = []


def get_ip(api_url):
    global ips
    while True:
        time.sleep(5)
        # 获取IP列表
        res = requests.get(api_url).text.strip("\n")
        # 按照\n分割获取到的IP
        ips = res.split("\n")
        # 利用每一个IP
        for proxyip in ips:
            # print(proxyip)
            return proxyip


def proxy1():
    # 这里填写无忧代理IP提供的API订单号（请到用户中心获取）
    order = "cc5c662abc34e2b67da41a340d66e2e1"
    # 获取IP的API接口
    api_url = "http://api.ip.data5u.com/dynamic/get.html?order=" + order
    # 开始自动获取IP
    ip = 'http://' + get_ip(api_url)
    return ip


def proxy():
    ip = proxy1()
    if ip == 'http://too many requests' or 'msg' in ip:
        return proxy()
    if ip != 'http://too many requests' or 'msg' not in ip:
        return ip


if __name__ == '__main__':
    print(proxy())
