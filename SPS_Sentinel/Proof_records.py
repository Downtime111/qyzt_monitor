# -*- coding: UTF-8 -*-


"""
@描述：数据校验模块
@作者：garrett
@版本：V1.0
@创建时间：2021-08-11
"""


import random
import time
from threading import Thread
from DB_sentence import get_inval_time, get_timelist, get_devlist, insert_log, get_day_count
from datetime import datetime
from datetime import timedelta
from send_order import send_order
from Message_email import run_alarm_email
import configparser

mqtt_config = configparser.ConfigParser()
mqtt_config.read("./config/mqtt_config.ini")
#sub_topic_0 = mqtt_config["subscribe"]['sub_topic_0']
#sub_topic_1 = mqtt_config["subscribe"]['sub_topic_1']
pub_topic_0 = mqtt_config["publish"]['pub_topic_0']
pub_topic_1 = mqtt_config["publish"]['pub_topic_1']

def get_no_time(dev_name, beg_time, end_time):
    """

    :param dev_name:
    :param beg_time:
    :param end_time:
    :return:
    """
    global inner
    inner0 = get_inval_time(dev_name)
    scan_list = get_timelist(dev_name, beg_time, end_time)
    count = len(scan_list)
    try:
        if inner0 is not None:
            inner = inner0
        else:
            if scan_list:
                inner1 = scan_list[1] - scan_list[0]
                inner2 = scan_list[2] - scan_list[1]
                inner3 = scan_list[3] - scan_list[2]
                if inner1 == inner2:
                    inner = inner1.seconds
                elif inner2 == inner3:
                    inner = inner2.seconds
            else:
                inner = 300
        begin = datetime.strptime(beg_time, "%Y-%m-%d %H:%M:%S")
        end = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")

        # if beg_time[-2:] == "00" and end_time[-2:] == "00":
        if inner >= 60:
            no_list_min = []
            while True:
                no_list_min.append(begin.strftime("%Y-%m-%d %H:%M") + ":00")
                begin += timedelta(minutes=inner / 60)
                if begin > end:
                    # no_list_min.append(begin.strftime("%Y-%m-%d %H:%M")+":00")
                    break
            for time_rec in scan_list:
                # print(time_rec)
                tim_todel = time_rec.strftime("%Y-%m-%d %H:%M") + ":00"
                if tim_todel in no_list_min:
                    no_list_min.remove(tim_todel)
            # print(no_list_min)
            return no_list_min, count
        else:
            no_list_sec = []
            while True:
                no_list_sec.append(begin.strftime("%Y-%m-%d %H:%M:%S"))
                begin += timedelta(seconds=inner)
                if begin > end:
                    # no_list_sec.append(begin.strftime("%Y-%m-%d %H:%M:%S"))
                    break
            for time_rec in scan_list:
                tim_todel = time_rec.strftime("%Y-%m-%d %H:%M:%S")
                if tim_todel in no_list_sec:
                    no_list_sec.remove(tim_todel)
            # print(no_list_sec)
            return no_list_sec, count
    except Exception as e:
        print("[ERR] Can't get lack of time：", e)


def get_last_day(dev_name):
    """

    :param dev_name:
    :return:
    """
    try:
        lastday = datetime.now() - timedelta(days=1)
        last_day = lastday.strftime("%Y-%m-%d")
        #last_day_flag = lastday.strftime("%Y%m%d")
        last_d_begin = f"{last_day} 00:00:00"
        last_d_end = f"{last_day} 23:59:59"
        inval_d_list, count = get_no_time(dev_name, last_d_begin, last_d_end)
        print(f"[整天校验] 设备{dev_name} {last_day}一天的条数是{count},,缺{len(inval_d_list)}条数据")
        if len(inval_d_list) == 0:
            # insert_log(dev_name, f"{last_day}数据完整，共{count}条数据")
            pass
        else:
            # 按时间区间获取

            min_record = min(inval_d_list)
            max_record = max(inval_d_list)
            send_order(f"{pub_topic_0}/{pub_topic_1}/{dev_name}",
                       f"export 0 {min_record[0:4]+min_record[5:7]+min_record[8:10]+min_record[11:13]} "
                       f"{max_record[0:4]+max_record[5:7]+max_record[8:10]+max_record[11:13]}")

            # 按天获取
            """
            send_order(f"{pub_topic_0}/{pub_topic_1}/{dev_name}", f"export 0 {last_day_flag} {last_day_flag}")
            """
            # 二次
            time.sleep(random.randint(50, 60))
            two_inval_d_list, two_count = get_no_time(dev_name, last_d_begin, last_d_end)
            if len(two_inval_d_list) == 0:
                # insert_log(dev_name, f"{last_day}数据完整，共{two_count}条数据")
                pass
            else:
                two_min_record = min(two_inval_d_list)
                two_max_record = max(two_inval_d_list)
                send_order(f"{pub_topic_0}/{pub_topic_1}/{dev_name}",
                           f"export 0 {two_min_record[0:4] + two_min_record[5:7] + two_min_record[8:10] + two_min_record[11:13]} "
                           f"{two_max_record[0:4] + two_max_record[5:7] + two_max_record[8:10] + two_max_record[11:13]}")
                insert_log(dev_name, f"[整天校验]已下发第二次拉取，当前{last_day}数据缺失{len(two_inval_d_list)}条")
    except Exception as e:
        print(f"[ERR] get err: {e}")


def get_last_hour(dev_name):
    """

    :param dev_name:
    :return:
    """
    try:
        now_hour = datetime.now()
        l_h = now_hour - timedelta(hours=1)
        last_hour = l_h.strftime("%Y-%m-%d %H")
        format_last_hour = l_h.strftime("%Y%m%d%H")
        last_h_begin = f"{last_hour}:00:00"
        last_h_end = f"{last_hour}:59:59"
        inval_h_list, count = get_no_time(dev_name, last_h_begin, last_h_end)
        print(f"[小时校验] 设备{dev_name}:{last_hour}时的条数是{count},缺{len(inval_h_list)}条数据")
        if len(inval_h_list) == 0:
            pass
        else:
            # 按时间区间获取
            send_order(f"{pub_topic_0}/{pub_topic_1}/{dev_name}", f"export 0 {format_last_hour} {format_last_hour}")
            # 按天获取
            """
            send_order(f"{pub_topic_0}/{pub_topic_1}/{dev_name}", f"export 0 {today} {today}")
            """
            # 二次
            time.sleep(random.randint(50, 60))
            two_inval_h_list, two_count = get_no_time(dev_name, last_h_begin, last_h_end)
            if len(two_inval_h_list) == 0:
                pass
            else:
                """
                send_order(f"{pub_topic_0}/{pub_topic_1}/{dev_name}", f"export 0 {today} {today}")
                """
                send_order(f"{pub_topic_0}/{pub_topic_1}/{dev_name}", f"export 0 {format_last_hour} {format_last_hour}")
    except Exception as e:
        print(f"[ERR] get err: {e}")


isrun_1 = 0
isrun_2 = 0


def proofrec_proc():
    global isrun_1, isrun_2
    try:
        while True:
            last_day = (datetime.now()-timedelta(days=1)).strftime("%Y-%m-%d")
            #current_day = datetime.now().day
            current_hour = datetime.now().hour
            current_min = datetime.now().minute
            """
            @每小时11分0秒触发上一小时校验
            """
            if current_min == 11 and isrun_1 == 0:
                dev_list = get_devlist()
                try:
                    l = len(dev_list)
                    ps = []
                    for i in range(0, l):
                        # print(list[i])
                        p = Thread(target=get_last_hour, args=(dev_list[i],))
                        ps.append(p)
                    # print(ps)
                    for i in range(0, l):
                        ps[i].start()
                        time.sleep(0.5)
                    isrun_1 = 1
                except Exception as e:
                    print(e)
                    print("[ERR] 无法启动小时校验线程")
            else:
                isrun_1 = 0
            """
            @每天8点56分触发整天校验
            """
            if current_hour == 8 and current_min == 56 and isrun_2 == 0:
                dev_list = get_devlist()
                try:
                    l = len(dev_list)
                    ps = []
                    for i in range(0, l):
                        # print(list[i])
                        p = Thread(target=get_last_day, args=(dev_list[i],))
                        ps.append(p)
                    # print(ps)
                    for i in range(0, l):
                        ps[i].start()
                        ps[i].join()
                        time.sleep(0.5)
                    """
                    @ 每日日报下发
                    """
                    count_dic = {}
                    for dev in dev_list:
                        count_dic[dev] = get_day_count(dev, last_day)
                    print(count_dic)
                    run_alarm_email(f"{last_day}数据回传日报", count_dic)
                    isrun_2 = 1
                except Exception as e:
                    print(e)
                    print("[ERR] 无法启动整天校验线程or日报")
            else:
                isrun_2 = 0
            # print(current_day,current_hour,current_min)
            time.sleep(60)
    except Exception as e:
        print(f"[ERR] proof record process err: {e}")


if __name__ == "__main__":
    #proofrec_proc()
    get_last_day("test")
    #get_last_hour("test")
