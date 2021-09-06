# -*- coding: UTF-8 -*-


"""
@描述：数据库连接池管理模块
@作者：garrett
@版本：V1.0
@创建时间：2021-08-11
"""


try:
    from DB_config import POOL
except Exception as e:
    print("[ERR] Connect to DB error")
import pymysql


"""
@FUN:创建连接
"""
def create_conn():
    """
    @创建连接池连接
    """
    try:
        conn = POOL.connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        return conn, cursor
    except Exception as e:
        print(e)


def close_conn(conn, cursor):
    """
    @关闭连接池连接
    """
    try:
        conn.close()
        cursor.close()
    except Exception as e:
        print(e)


def select_one(sql, args):
    """
    @查询一条
    :param sql:sql语句
    :param args:条件
    :return:返回执行状态
    """
    conn, cur = create_conn()
    cur.execute(sql, args)
    result = cur.fetchone()
    close_conn(conn, cur)
    return result


def select_all(sql, args):
    """
    @查询多条
    :param sql:sql语句
    :param args:条件
    :return:返回执行状态
    """
    conn, cur = create_conn()
    cur.execute(sql, args)
    result = cur.fetchall()
    close_conn(conn, cur)
    return result


def execute(sql, args=None):
    """
    @执行sql语句
    :param sql:sql语句
    :param args:条件
    :return:返回执行状态
    """
    conn, cur = create_conn()
    cur.execute(sql, args)
    result = cur.fetchall()
    close_conn(conn, cur)
    return result


def insert_one(sql, args):
    """
    @插入一条记录
    :param sql:sql语句
    :param args:条件
    :return:返回执行状态
    """
    conn, cur = create_conn()
    result = cur.execute(sql, args)
    conn.commit()
    close_conn(conn, cur)
    return result


def insert_many(sql, args):
    """
    @插入多条记录
    :param sql:sql语句
    :param args:条件
    :return:返回执行状态
    """
    conn, cur = create_conn()
    result = cur.executemany(sql, args)
    conn.commit()
    close_conn(conn, cur)
    return result


def delete_one(sql, args):
    """
    @删除一条记录
    :param sql:sql语句
    :param args:条件
    :return:返回执行状态
    """
    conn, cur = create_conn()
    result = cur.execute(sql, args)
    conn.commit()
    close_conn(conn, cur)
    return result


def update_one(sql, args):
    """
    @更新一条记录
    :param sql:sql语句
    :param args:条件
    :return:返回执行状态
    """
    conn, cur = create_conn()
    result = cur.execute(sql, args)
    conn.commit()
    close_conn(conn, cur)
    return result


'''
import pymysql
from dbutils.pooled_db import PooledDB

import DB_config as Config

'''
#@功能：PT数据库连接池
'''
class PTConnectionPool(object):
    __pool = None
    def __enter__(self):
        self.conn = self.getConn()
        self.cursor = self.conn.cursor()
        self.commit = self.conn.commit()
        #print("PT数据库创建con和cursor")
        return self

    def getConn(self):
        if self.__pool is None:
            self.__pool = PooledDB(creator=pymysql, mincached=Config.DB_MIN_CACHED , maxcached=Config.DB_MAX_CACHED,
                                   maxshared=Config.DB_MAX_SHARED, maxconnections=Config.DB_MAX_CONNECYIONS,
                                   blocking=Config.DB_BLOCKING, maxusage=Config.DB_MAX_USAGE,
                                   setsession=Config.DB_SET_SESSION,
                                   host=Config.DB_TEST_HOST , port=Config.DB_TEST_PORT ,
                                   user=Config.DB_TEST_USER , passwd=Config.DB_TEST_PASSWORD ,
                                   db=Config.DB_TEST_DBNAME , use_unicode=False, charset=Config.DB_CHARSET)

        return self.__pool.connection()

    """
    @summary: 释放连接池资源
    """
    def __exit__(self, type, value, trace):
        self.cursor.close()
        self.conn.close()
        #print("PT连接池释放con和cursor")

'''
#@功能：获取PT数据库连接
'''
def getPTConnection():
    return PTConnectionPool()
'''