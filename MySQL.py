# coding=utf-8

import pymysql


def get_table():  # 建表函数  host='192.168.10.230'
    # 连接数据库
    connect = pymysql.connect(host='172.16.10.11',
                              port=3306,
                              user='root',
                              passwd='root',
                              db='zhonghonginfo',
                              charset="utf8",
                              use_unicode=True
                              )
    # 创建游标
    cursor = connect.cursor()
    # 创建数据表
    student = '''
            create table toubiao(
            Id varchar(200),
            Title varchar(200) not null,
            Date varchar(200),
            Purchaser varchar(200),
            Agency varchar(200),
            Type varchar(200),
            Area varchar(200),
            Url varchar(200) not null,
            primary key(Title,Url))
    '''
    # 设置多主键 primary key(RegistrationMark,ApplicationDate,Classification)
    cursor.execute(student)
    # 关闭游标
    cursor.close()
    # 提交事物
    connect.commit()
    # 关闭数据库连接
    connect.close()
    print('建表完成')
    return get_table

# 插入、修改、删除、查询数据


def get_info(data):  # 插入数据库
    # 连接数据库
    connect = pymysql.connect(host='172.16.10.11',
                              port=3306,
                              user='root',
                              passwd='root',
                              db='zhonghonginfo',
                              charset="utf8",
                              use_unicode=True
                              )
    # 创建游标
    cursor = connect.cursor()
    insert_sql = """
                INSERT into toubiao(Id, Title, Date, Purchaser, Agency, Type, Area, Url)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
    try:
        cursor.execute(insert_sql, (data["id"], data["标题"], data["时间"], data["采购人"], data["代理机构"], data["类型"], data["地区"], data["连接"]))
    except:
        pass
    finally:
        # 关闭游标
        cursor.close()
        # 提交事物
        connect.commit()
        # 关闭数据库连接
        connect.close()
    return ''


    # # 更细查询条件的数据
    # cursor.execute("update student set name='' where name = ''")
    #
    # # 删除查询条件的数据
    # cursor.execute("delete from student where 姓名='22'")
    #
    # # 查询
    # cursor.execute("SELECT * FROM student")
    #
    # for r in cursor.fetchall():
    #     print(r)


if __name__ == '__main__':
    get_table()
    # for num in range(1, 41):
    #     data = {'学号': num, '姓名': '22', '年级': '3 year 1 class', '年龄': '3'}
    #     get_info(data)
