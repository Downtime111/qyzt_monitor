# -*- coding: UTF-8 -*-


"""
@描述：数据库配置文件
@作者：garrett
@版本：V1.0
@创建时间：2021-08-11
"""


import pymysql
from dbutils.pooled_db import PooledDB


try:
    POOL = PooledDB(
        creator=pymysql,    # 使用链接数据库的模块
        maxconnections=100,  # 连接池允许的最大连接数，0和None表示不限制连接数
        mincached=10,   # 初始化时，链接池中至少创建的空闲的链接，0表示不创建
        maxcached=30,   # 链接池中最多闲置的链接，0和None不限制
        maxshared=0,   # 链接池中最多共享的链接数量，0和None表示全部共享。
                        # PS: 无用，因为pymysql和MySQLdb等模块的 threadsafety都为1，所有值无论设置为多少，_maxcached永远为0，所以永远是所有链接都共享。
        blocking=True,  # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
        maxusage=None,  # 一个链接最多被重复使用的次数，None表示无限制
        setsession=[],  # 开始会话前执行的命令列表。如：["set datestyle to ...", "set time zone ..."]
        ping=0,
        # ping MySQL服务端，检查是否服务可用。
        # 如：0 = None = never,
        # 1 = default = whenever it is requested,
        # 2 = when a cursor is created,
        # 4 = when a query is executed,
        # 7 = always
        #host='192.168.24.5',
        #port=3306,
        host='39.106.189.252',
        port=3306,
        user='qiyun',
        password='QIYUN888',
        #database='scan',
        database='test2',
        charset='utf8'
    )
except Exception as e:
    print(e)


    '''
    # TEST数据库信息
    DB_TEST_HOST = "192.168.24.5"
    DB_TEST_PORT = 3306
    DB_TEST_DBNAME = "scan"
    DB_TEST_USER = "db"
    DB_TEST_PASSWORD = "jason491147784"
    
    # 数据库连接编码
    DB_CHARSET = "utf8"
    
    # mincached : 启动时开启的闲置连接数量(缺省值 0 以为着开始时不创建连接)
    DB_MIN_CACHED = 10
    
    # maxcached : 连接池中允许的闲置的最多连接数量(缺省值 0 代表不闲置连接池大小)
    DB_MAX_CACHED = 10
    
    # maxshared : 共享连接数允许的最大数量(缺省值 0 代表所有连接都是专用的)如果达到了最大数量,被请求为共享的连接将会被共享使用
    DB_MAX_SHARED = 20
    
    # maxconnecyions : 创建连接池的最大数量(缺省值 0 代表不限制)
    DB_MAX_CONNECYIONS = 100
    
    # blocking : 设置在连接池达到最大数量时的行为(缺省值 0 或 False 代表返回一个错误<toMany......>; 其他代表阻塞直到连接数减少,连接被分配)
    DB_BLOCKING = True
    
    # maxusage : 单个连接的最大允许复用次数(缺省值 0 或 False 代表不限制的复用).当达到最大数时,连接会自动重新连接(关闭和重新打开)
    DB_MAX_USAGE = 0
    
    # setsession : 一个可选的SQL命令列表用于准备每个会话，如["set datestyle to german", ...]
    DB_SET_SESSION = None
    '''
