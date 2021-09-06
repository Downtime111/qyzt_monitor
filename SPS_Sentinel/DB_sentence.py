# -*- coding: UTF-8 -*-


"""
@描述：数据库查询语句模块
@作者：garrett
@版本：V1.0
@创建时间：2021-08-11
"""
import time

from DB_pool import *
from datetime import datetime
from datetime import timedelta
import re
from threading import Thread
from send_order import send_order
import configparser

mqtt_config = configparser.ConfigParser()
mqtt_config.read("./config/mqtt_config.ini")
#sub_topic_0 = mqtt_config["subscribe"]['sub_topic_0']
sub_topic_1 = mqtt_config["subscribe"]['sub_topic_1']

def create_devtable():
    """

    :return:
    """
    try:
        sql = "CREATE TABLE `device_list` (" \
              "`id` int(11) unsigned NOT NULL AUTO_INCREMENT," \
              "`device_name` varchar(100) NOT NULL," \
              "`location` varchar(200) NOT NULL," \
              "`coordinates` varchar(200) NOT NULL," \
              "`inval_time` int(20) unsigned DEFAULT NULL," \
              "`last_time` varchar(100) DEFAULT NULL," \
              "`send_topic` varchar(100) DEFAULT NULL," \
              "`remark` varchar(200) NOT NULL," \
              "PRIMARY KEY (`id`,`device_name`)," \
              "UNIQUE KEY `device_name` (`device_name`)" \
              ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;"
        result = execute(sql)
        if len(result) == 0:
            print(f"[SQL] Create table 'device_list' is OK.")
    except Exception as e:
        print(e)


def create_recordtable(dev_name):
    """

    :param dev_name:
    :return:
    """
    try:
        sql = f"CREATE TABLE `record_{dev_name}` (" \
              "`record` int(11) unsigned NOT NULL AUTO_INCREMENT," \
              "`datetime` datetime NOT NULL," \
              "`data1` float," \
              "`data2` float," \
              "`data3` float," \
              "`data4` float," \
              "`data5` float," \
              "`data6` float," \
              "`flag` varchar(100)," \
              "PRIMARY KEY (`datetime`)," \
              "UNIQUE KEY `record` (`record`)" \
              ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;"
        result = execute(sql)
        if len(result) == 0:
            print(f"[SQL] Create table record_{dev_name} is OK.")
    except Exception as e:
        print(e)


def insert_dev(dev_name, s_topic):
    """

    :param dev_name:
    :param s_topic:
    :return:
    """
    try:
        msg = [dev_name, s_topic]
        sql = f"INSERT IGNORE INTO device_list" \
              f"(device_name,send_topic) " \
              f"VALUE " \
              f"(%s,%s)"
        # result = insert_one(sql, str(msg.payload.decode()).split(","))
        result = insert_one(sql, msg)
        if int(result) == 0:
            print(f"insert \'{dev_name}\' info successd")
    except Exception as e:
        print(e)


def insert_full_dev(dev_name, location, coordinates, inval_time, send_topic, remark):
    """

    :param dev_name:
    :param location:
    :param coordinates:
    :param inval_time:
    :param send_topic:
    :param remark:
    :return:
    """
    try:
        msg = [dev_name, location, coordinates, inval_time, send_topic, remark]
        sql = f"REPLACE INTO device_list" \
              f"(device_name,location,coordinates,inval_time,send_topic,remark) " \
              f"VALUE " \
              f"(%s,%s,%s,%s,%s,%s)"
        # result = insert_one(sql, str(msg.payload.decode()).split(","))
        result = insert_one(sql, msg)
        if int(result) == 2:
            content = f"insert \'{dev_name}\' info successd"
            print(content)
            send_order("CLI/MSG/BAC", f"[create]:{content}")
    except Exception as e:
        print(e)


def insert_log(dev_name, content):
    """

    :param dev_name:
    :param content:
    "return:
    """
    log_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        msg = [log_time, dev_name, content]
        sql = f"INSERT INTO option_log" \
              f"(option_time,device_name,content) " \
              f"VALUE " \
              f"(%s,%s,%s)"
        # result = insert_one(sql, str(msg.payload.decode()).split(","))
        result = insert_one(sql, msg)
        if int(result) == 0:
            print(f"insert \'{dev_name}\' info successd")
    except Exception as e:
        print(e)


def judge_devexist(dev_name):
    """

    :param dev_name:
    :return:
    """
    global bool
    try:
        sql = f"SELECT  IF ( EXISTS (" \
              f"SELECT device_name " \
              f"FROM device_list " \
              f"WHERE device_name = '{dev_name}'),1,0)"
        result = execute(sql)
        for lis in result:
            for key in lis:
                bool = lis[key]
        # if bool == 1:
        #    print(f"设备\"{dev_name}\"存在")
        # else:
        #    print(f"设备\"{dev_name}\"不存在")
        return bool
    except Exception as e:
        print(e)


def get_dev_pubtopic(dev_name):
    """

    :param dev_name:
    :return:
    """
    try:
        sql = f"SELECT send_topic " \
              f"FROM device_list " \
              f"WHERE device_name='{dev_name}'"
        result = execute(sql)
        for lis in result:
            print(lis['send_topic'])
    except Exception as e:
        print(e)


def get_devlist():
    """

    :return:
    """
    try:
        dev_liscahce = []
        sql = "SELECT device_name " \
              "FROM device_list"
        result = execute(sql)
        for lis in result:
            #print(lis['device_name'])
            dev_liscahce.append(lis['device_name'])
        # 写入本地
        #with open ("device_list.dat", "w") as devl:
        #    devl.write(str(dev_liscahce))
        return dev_liscahce
    except Exception as e:
        print(e)


def get_full_devlist():
    """

    :return:
    """
    try:
        dev_liscahce = []
        sql = "SELECT device_name,location,coordinates,inval_time,send_topic,remark " \
              "FROM device_list"
        result = execute(sql)

        # 写入本地
        #with open ("device_list.dat", "w") as devl:
        #    devl.write(str(dev_liscahce))
        return result
    except Exception as e:
        print(e)


def get_day_count(dev, scan_date):
    global count
    try:
        sql = f"SELECT COUNT(datetime) " \
              f"FROM record_{dev} " \
              f"WHERE datetime " \
              f"BETWEEN '{scan_date} 00:00:00' " \
              f"and '{scan_date} 23:59:59'"
        result = execute(sql)
        for dic in result:
            count = dic['COUNT(datetime)']
        return count
    except Exception as e:
        print(e)


def get_inval_time(dev_name):
    """

    :param dev_name:
    :return:
    """
    try:
        sql = f"SELECT inval_time " \
              f"FROM device_list " \
              f"WHERE device_name='{dev_name}'"
        result = execute(sql)
        for lis in result:
            for key in lis:
                inval = lis[key]
                return inval
    except Exception as e:
        print(e)


def get_timelist(dev_name, beg_time, end_time):
    """

    :param dev_name:
    :param beg_time:
    :param end_time:
    :return:
    """
    try:
        time_liscache = []
        sql = f"SELECT datetime FROM record_{dev_name} " \
              f"WHERE datetime " \
              f"BETWEEN '{beg_time}' " \
              f"AND '{end_time}' " \
              f"ORDER BY datetime"
        result = execute(sql)
        # print(result)
        for lis in result:
            time_liscache.append(lis["datetime"])
        # print(time_liscache)
        return time_liscache
    except Exception as e:
        print(e)


def find_maxtime(dev_name):
    """

    :param dev_name:
    :return:
    """
    global rece_time
    try:
        sql = f"SELECT max(datetime) " \
              f"FROM record_{dev_name}"
        result = execute(sql)
        for lis in result:
            for key in lis:
                rece_time = lis[key]
        print(rece_time)
    except Exception as e:
        print(e)


def insert_record(dev_name, timestamp, msg):
    """

    :param dev_name:
    :param timestamp:
    :param msg:
    :return:
    """
    try:
       sql = f"INSERT IGNORE INTO record_{dev_name}" \
             f"(datetime,data1,data2,data3,data4,data5,data6,flag) " \
             f"VALUE " \
             f"(%s,%s,%s,%s,%s,%s,%s,%s)"
       # result = insert_one(sql, str(msg.payload.decode()).split(","))
       result = insert_one(sql, msg)
       if int(result) == 1:
           print(f"insert 【{dev_name}】 [{timestamp}] record successd")
    except Exception as e:
        print(e)


def insert_manyrecords(dev_name, msg):
    """

    :param dev_name:
    :param msg:
    :return:
    """
    try:
        sql = f"INSERT IGNORE INTO record_{dev_name}" \
              f"(datetime,data1,data2,data3,data4,data5,data6,flag) " \
              f"VALUES " \
              f"(%s,%s,%s,%s,%s,%s,%s,%s)"
        result = insert_many(sql,msg)
        if str(result) == "0":
            print(f"<数据回传> \'{dev_name}\': Discard duplicate data")
        else:
            print(f"<数据回传> insert \'{dev_name}\' {result} record successd")
    except Exception as e:
        print(e)


def first_insert(device, topic, timestamp, line_cache):
    create_recordtable(device)
    insert_dev(device, "".join(topic))
    time.sleep(0.5)
    insert_record(device, timestamp, line_cache)


def child_insert_record(contents,topic):

    """

    :param contents:
    :param topic:
    :return:
    """
    line_cache = []
    global device, clean_record, timestamp
    try:
        device = "".join(re.findall(f"{sub_topic_1}/(.+)$", topic))
        for content_line in contents.split("\r\n"):
            clean_record = content_line.strip("\"").split(",")
            clean_record_tuple = tuple(content_line.strip("\"").split(","))
            if re.match("\"\\d{4}-\\d{2}-\\d{2}.+\"", content_line):
                timestamp = clean_record[0]
                # print(device, clean_record)
                line_cache.append(clean_record_tuple)
        # print(len(line_cache),line_cache)
        if len(line_cache) == 1:
            #print(device, clean_record)
            """if judge_devexist(device):
                insert_record(device, timestamp, line_cache[0])
            else:
                fir_inser = Thread(target=first_insert, args=(device, topic, timestamp, line_cache[0]))
                fir_inser.start()"""
            insert_record(device, timestamp, line_cache[0])
        elif len(line_cache) > 1:
            # print(clean_record)
            # print(line_cache)
            insert_manyrecords(device,line_cache)
        else:
            pass
        line_cache.clear()
    except Exception as e:
        print(e)


def get_no_time(dev_name, beg_time, end_time):
    """
    替换为Proof_records中的函数
    :param dev_name:
    :param beg_time:
    :param end_time:
    :return:
    """
    global inner
    inner0 = get_inval_time(dev_name)
    scan_list = get_timelist(dev_name, beg_time, end_time)
    try:
        if inner0 is not None:
            inner = inner0
        else:
            inner1 = scan_list[1] - scan_list[0]
            inner2 = scan_list[2] - scan_list[1]
            inner3 = scan_list[3] - scan_list[2]
            if inner1 == inner2:
                inner = inner1.seconds
            elif inner2 == inner3:
                inner = inner2.seconds
        begin = datetime.strptime(beg_time, "%Y-%m-%d %H:%M:%S")
        end = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")

        # if beg_time[-2:] == "00" and end_time[-2:] == "00":
        if inner >= 60:
            no_list_min = []
            while True:
                no_list_min.append(begin.strftime("%Y-%m-%d %H:%M")+":00")
                begin += timedelta(minutes=inner / 60)
                if begin > end:
                    no_list_min.append(begin.strftime("%Y-%m-%d %H:%M")+":00")
                    break
            for time_rec in scan_list:
                print(time_rec)
                tim_todel = time_rec.strftime("%Y-%m-%d %H:%M")+":00"
                if tim_todel in no_list_min:
                    no_list_min.remove(tim_todel)
            print(no_list_min)
            return no_list_min
        else:
            no_list_sec = []
            while True:
                no_list_sec.append(begin.strftime("%Y-%m-%d %H:%M:%S"))
                begin += timedelta(seconds=inner)
                if begin > end:
                    no_list_sec.append(begin.strftime("%Y-%m-%d %H:%M:%S"))
                    break
            for time_rec in scan_list:
                tim_todel = time_rec.strftime("%Y-%m-%d %H:%M:%S")
                if tim_todel in no_list_sec:
                    no_list_sec.remove(tim_todel)
            print(no_list_sec)

            # 方法二：直接比较（无法获取队尾中没有的时间）
            """
            if beg_time[-2:] == "00" and end_time[-2:] == "00":
            no_list_min = []
            while True:
                for time_rec in scan_list:
                    if time_rec.strftime("%Y-%m-%d %H:%M") == begin.strftime("%Y-%m-%d %H:%M"):
                        begin += timedelta(minutes=inner/60)
                    else:
                        no_list_min.append(begin.strftime("%Y-%m-%d %H:%M:%S"))
                        begin += timedelta(minutes=inner/60)
                        while True:
                            if time_rec.strftime("%Y-%m-%d %H:%M") == begin.strftime("%Y-%m-%d %H:%M"):
                                begin += timedelta(minutes=inner / 60)
                                break
                            else:
                                no_list_min.append(begin.strftime("%Y-%m-%d %H:%M:%S"))
                                begin += timedelta(minutes=inner / 60)
                    if time_rec.strftime("%Y-%m-%d %H:%M") == end.strftime("%Y-%m-%d %H:%M"):
                        #print(time_rec.strftime("%Y-%m-%d %H:%M"))
                        break
                break
            print(no_list_min)
            return no_list_min
        else:
            no_list_sec = []
            while True:
                for time_rec in scan_list:
                    if time_rec.strftime("%Y-%m-%d %H:%M:%S") == begin.strftime("%Y-%m-%d %H:%M:%S"):
                        begin += timedelta(seconds=inner)
                    else:
                        no_list_sec.append(begin.strftime("%Y-%m-%d %H:%M:%S"))
                        begin += timedelta(seconds=inner)
                    if time_rec.strftime("%Y-%m-%d %H:%M:%S") == end.strftime("%Y-%m-%d %H:%M:%S"):
                        break
                break
            print(no_list_sec)
            return no_list_sec
            """
            return no_list_sec
    except Exception as e:
        print("[ERR] Can't get lack of time：", e)


if __name__ == "__main__":
    #create_devtable("test12")
    #print(judge_devexist("test11"))
    #find_maxtime("test1")
    #insert_record("test1", [5, "2021-08-09 22:50:00", 1, 1])
    #get_devlist()
    get_full_devlist()
    #get_timelist("test1","2021-08-09 22:40:00","2021-08-09 22:52:00")
    #get_no_time("test","2021-08-10 15:50:10","2021-08-10 16:15:00")
    #get_inval_time("test")
    #get_dev_pubtopic("test")
    #print(get_day_count('test', "2021-08-21"))