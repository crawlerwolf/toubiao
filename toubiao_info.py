# coding=utf-8

from bs4 import BeautifulSoup
import re
import pymysql
import time
from log import Logger

log = Logger()


def get_info_tuobiao(web_data):
    soup = BeautifulSoup(web_data, 'lxml')
    info = soup.select('ul.vT-srch-result-list-bid  li')
    if info != []:
        time.sleep(0.05)
        for li in info:
            try:
                pattern = re.compile('.*?<span>(.*?)<br/>', re.S)
                text = re.search(pattern, str(li)).group(1)
                infos = text.split('|')
                time.sleep(0.0001)
                data = {
                    'id': int(time.time()*1000000),
                    '标题': li.select('a')[0].text.replace('\n', '').replace('\r', '').strip(),
                    '时间': infos[0].replace('.', '-').replace('\n', '').replace('\r', '').strip(),
                    '采购人': infos[1].replace('\n', '').replace('\r', '').strip()[4:],
                    '代理机构': infos[2].replace('\n', '').replace('\r', '').strip()[5:],
                    '类型': li.select('span  strong')[0].text.replace('\n', '').replace('\r', '').strip(),
                    '地区': li.select('span  a')[0].text.replace('\n', '').replace('\r', '').strip(),
                    '连接': li.select('a')[0].get('href'),
                        }
                to_mysql(data)
                log.getlog(data)
            except UnicodeEncodeError as U:
                log.getlog(U)
                pass
        return '获取完毕'
    if info == []:
        return '获取完毕'


def to_mysql(date):
    while True:
        try:
            get_data(date)
            return
        except pymysql.err.OperationalError:
            log.getlog('等待连接Mysql数据库')
            time.sleep(30)


def get_data(data):  # 插入数据库
    # 连接数据库
    connect = pymysql.connect(host='localhost',
                              port=3306,
                              user='root',
                              passwd='root',
                              db='test',
                              charset='utf8',
                              use_unicode=True
                              )
    # 创建游标
    cursor = connect.cursor()
    insert_sql = """
                   insert into toubiao(Id, Title, Date, Purchaser, Agency, Type, Area, Url)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
               """
    try:
        cursor.execute(insert_sql, (
        data["id"], data["标题"], data["时间"], data["采购人"], data["代理机构"], data["类型"], data["地区"], data["连接"]))
    except pymysql.err.IntegrityError:
        pass
    # 关闭游标
    cursor.close()
    # 提交事物
    connect.commit()
    # 关闭数据库连接
    connect.close()


def get_total(web_data):
    soup = BeautifulSoup(web_data, 'lxml')
    info = soup.select('p.pager  script')[0]
    num = re.search('.*?size: (.*?),', str(info)).group(1)
    # log.getlog(num)
    if num == 1:
        return 2
    if num != 1:
        return int(num) + 1


if __name__ == '__main__':
    with open('web.html', 'rb') as f:
        web_data = str(f.read(), encoding='utf-8')
        f.close()
    # get_info_tuobiao(web_data)
    log.getlog(get_total(web_data))
