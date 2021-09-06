# -*- coding: UTF-8 -*-


"""
@描述：时间校验模块
@作者：garrett
@版本：V1.0
@创建时间：2021-08-11
"""
import json
import time
from datetime import datetime as dt
import re
import linecache
import datetime
from Message_wechat import run_alarm_wechat
from send_order import send_order
from threading import Thread
from DB_sentence import get_full_devlist, insert_full_dev,create_recordtable
from send_order import send_order
# from DB_sentence import insert_log
import configparser

mqtt_config = configparser.ConfigParser()
mqtt_config.read("./config/mqtt_config.ini")
#sub_topic_0 = mqtt_config["subscribe"]['sub_topic_0']
sub_topic_1 = mqtt_config["subscribe"]['sub_topic_1']
pub_topic_0 = mqtt_config["publish"]['pub_topic_0']
pub_topic_1 = mqtt_config["publish"]['pub_topic_1']

f_dev_list = []
print_inval_cache = ''
timestamp_cache = ''
stampdic_cache = {}
dev_now_invaldic_cache = {}
dev_sta_invaldic_cache = {}


def judge_timestamp(timestamp, device):
    """

    :param timestamp:
    :param device:
    :return:
    """
    global stampdic_cache, dev_sta_invaldic_cache, dev_now_invaldic_cache, dev_inval, timestamp_cache, dev_now_inval, print_inval_cache
    # 判断回传数据报文两次间隔
    now_time = dt.now()
    n_timestamp = dt.strptime(timestamp, "%Y-%m-%d %H:%M:%S")

    if timestamp_cache != '':
        # l_timestamp = datetime.strptime(timestamp_cache, "%Y-%m-%d %H:%M:%S")
        judge_inval = (n_timestamp - timestamp_cache).seconds
    else:
        judge_inval = 300
    timestamp_cache = n_timestamp
    # print(judge_inval)


    if device in stampdic_cache:
        if n_timestamp >= now_time:
            dev_now_inval = (n_timestamp - now_time).seconds
        else:
            dev_now_inval = (now_time - n_timestamp).seconds
        if stampdic_cache[device] >= n_timestamp:
            dev_inval = (stampdic_cache[device] - n_timestamp).seconds
        else:
            dev_inval = (n_timestamp - stampdic_cache[device]).seconds
        # print(dev_inval)
        if dev_inval > 3 and dev_now_inval < 60:
            dev_now_invaldic_cache[device] = dev_now_inval
            dev_sta_invaldic_cache[device] = dev_inval
            stampdic_cache[device] = n_timestamp
    else:
        stampdic_cache[device] = n_timestamp


    # if dev_sta_invaldic_cache and dev_now_invaldic_cache and dev_inval > 5:
    if dev_sta_invaldic_cache and dev_now_invaldic_cache and dev_inval > 3 and judge_inval > 3 and dev_now_inval < 60:
        time.sleep(4)
        print_now = dt.now()
        if print_inval_cache != '':
            print_inval = (print_now - print_inval_cache).seconds
            # print(print_inval)3
            if print_inval > 7:
                try:
                    with open("./config/back_del_cache.dat","r+") as bdc:
                        for b_dev in bdc.readlines():
                            # print(f"shebei {b_dev}")
                            del stampdic_cache[b_dev.replace("\n", "")]
                            del dev_now_invaldic_cache[b_dev.replace("\n", "")]
                            del dev_sta_invaldic_cache[b_dev.replace("\n", "")]
                        bdc.truncate(0)
                except Exception as e:
                    print(e)
                # print(stampdic_cache)
                # print(dev_sta_invaldic_cache) # 某一设备当前上传的时间戳与它上一条传的
                # print(dev_now_invaldic_cache)
                with open ("./config/stamp_cache.dat","w") as e:
                    e.write(str(stampdic_cache)+"\r"+str(dev_sta_invaldic_cache)+"\r"+str(dev_now_invaldic_cache))
                print_inval_cache = print_now

        else:
            try:
                with open("./config/back_del_cache.dat", "w+") as bdc:
                    for b_dev in bdc.readlines():
                        del stampdic_cache[b_dev.replace("\n", "")]
                    bdc.truncate(0)
            except Exception as e:
                print(e)

            # print(device, dev_inval, judge_inval, dev_now_inval)
            # print(stampdic_cache)
            # print(dev_sta_invaldic_cache)
            # print(dev_now_invaldic_cache)

            with open("./config/stamp_cache.dat", "w") as e:
                e.write(str(stampdic_cache) + "\r" + str(dev_sta_invaldic_cache) + "\r" + str(dev_now_invaldic_cache))
            print_inval_cache = print_now


def judge_order(rec_order):
    """

    :param rec_order:
    :return:
    """
    try:
        for ord in rec_order:
            if ord == "#get dev":
                device_lis = get_full_devlist()
                for dev_info in device_lis:
                    send_order("CLI/MSG/DEV", f"[dev_info]:{str(dev_info)}")
                    time.sleep(0.1)
                send_order("CLI/MSG/DEV", f"[end_info]")
            elif re.match("^#cre dev.+", ord):
                lis = eval(ord[9:])
                for dic in lis:
                    insert_full_dev(dic['na'], dic['lo'], dic['co'], dic['in'], dic['se'], dic['re'])
                    create_recordtable(dic['na'])
    except Exception as e:
        print(f"[RECEICE ERR] {e} ")
        send_order("CLI/MSG/ERR", f"[ERR]:order {e}")


def child_proof_timestamp(contents, topic):
    """

    :param contents:
    :param topic:
    :return:
    """
    line_p_cache = []
    rec_order = []
    global content_line
    try:

        device = "".join(re.findall(f"{sub_topic_1}/(.+)$", topic))
        for content_line in contents.split("\r\n"):
            if re.match("\".+\"", content_line):
                line_p_cache.append(content_line)
            if re.match("^#.+",content_line):
                rec_order.append(content_line)
        # print(len(line_p_cache))
        #print("receive")
        if len(line_p_cache) == 1:
            clean_record = line_p_cache[0].strip("\"").split(",")
            timestamp = clean_record[0]
            # print(device, clean_record)
            judge_timestamp(timestamp, device)
        else:
            # print("duohangpaichu")
            pass
        if rec_order:
            run_ord = Thread(target=judge_order, args=(rec_order,))  # 建子线程处理新来的任务请求
            run_ord.start()  # 开启子线程
        line_p_cache.clear()
        rec_order.clear()
    except Exception as e:
        print(e)


def send_time_order(dev_name=None):
    """

    :param dev_name:
    :return:
    """
    time.sleep(2)
    RTC = (dt.now() + datetime.timedelta(seconds=3)).strftime("%Y-%m-%d %H:%M:%S")
    # print(dt.now())
    time_proof_order = f"settime {RTC}"
    send_order(f"{pub_topic_0}/{pub_topic_1}/{dev_name}", time_proof_order)
    # print(time_proof_order)


isrun_alarm = 0
isrun_settime = 0
alarm_cache = {}
wait_cache = []


def prooftim_process():
    """

    :return:
    """
    global isrun_alarm, alarm_cache, isrun_settime, wait_cache
    while True:
        try:
            nt = dt.now()
            # day = nt.day
            hour = nt.hour
            min = nt.minute
            sec = nt.second
            # print(f"isrun {isrun_alarm}")
            linecache.updatecache("./config/stamp_cache.dat")
            stampdic_out = eval(linecache.getline("./config/stamp_cache.dat", 1).replace("\n", ""))
            # dev_sta_invaldic_out = eval(linecache.getline("./config/stamp_cache.dat", 2).replace("\n", ""))
            dev_now_invaldic_out = eval(linecache.getline("./config/stamp_cache.dat", 3).replace("\n", ""))
            # print(day, hour, min, sec)

            # if sec % 30 == 0 and isrun_alarm == 0:
            """
            @每5分钟触发一次超时校验
            """
            if min % 5 == 0 and sec == 10 and isrun_alarm == 0:
                # print(stampdic_out)
                # print(dev_sta_invaldic_out)
                # print(dev_now_invaldic_out)

                for dev in stampdic_out:
                    alarm_cache[dev] = 1
                    dev_time = stampdic_out[dev]
                    if nt >= dev_time:
                        ala_inval = (nt - dev_time).total_seconds()
                    else:
                        ala_inval = (dev_time - nt).total_seconds()
                    print(f"  ********** <超时校验>{dev}据上次更新{round(ala_inval-10,2)}s **********")
                    if dev in stampdic_out:
                        if alarm_cache[dev] == 1:
                            alarm_cache[dev] = 0
                    else:
                        pass
                    with open("./config/back_del_cache.dat", "r+") as bdc:
                        for b_dev in bdc.readlines():
                            if b_dev:
                                wait_cache.append(b_dev.replace("\n", ""))
                    if ala_inval-10 > 100 and dev not in wait_cache:
                        # print(wait_cache)
                        if alarm_cache[dev] == 0:
                            """
                            @触发超时报警
                            """
                            run_a = Thread(target=run_alarm_wechat, args=(dev, round(ala_inval-10, 2)))  # 建子线程处理新来的任务请求
                            run_a.start()  # 开启子线程
                            # print("baojing")
                            alarm_cache[dev] = 1
                        with open("./config/back_del_cache.dat", "a") as bdc:
                            bdc.write(dev+"\r")
                    wait_cache = []
                isrun_alarm = 1
            else:
                isrun_alarm = 0

            # if sec % 60 == 0 and isrun_settime == 0:
            """
            @每天08点06分10秒触发第一次RTC校验
            """
            if hour == 8 and min == 6 and sec == 10 and isrun_settime == 0:
                for t_dev in dev_now_invaldic_out:
                    if dev_now_invaldic_out[t_dev] > 2:
                        print(f"  *********** <RTC异常> {t_dev}时间差值{dev_now_invaldic_out[t_dev]}  ***********")
                        send_t = Thread(target=send_time_order, args=(t_dev,))  # 建子线程处理新来的任务请求
                        send_t.start()  # 开启子线程
                    else:
                        print(f"  *********** <RTC正常> {t_dev}时间差值{dev_now_invaldic_out[t_dev]}  ***********")
                isrun_settime = 1
            else:
                isrun_settime = 0

            """
            @每天08点26分10秒触发第二次RTC校验
            """
            if hour == 8 and min == 26 and sec == 10 and isrun_settime == 0:
                for t_dev in dev_now_invaldic_out:
                    if dev_now_invaldic_out[t_dev] > 4:
                        print(f"  *********** <RTC异常> {t_dev}时间差值{dev_now_invaldic_out[t_dev]}  ***********")
                        send_t = Thread(target=send_time_order, args=(t_dev,))  # 建子线程处理新来的任务请求
                        send_t.start()  # 开启子线程
                    else:
                        print(f"  *********** <RTC正常> {t_dev}时间差值{dev_now_invaldic_out[t_dev]}  ***********")
                isrun_settime = 1
            else:
                isrun_settime = 0

            time.sleep(1)

        except Exception as e:
            time.sleep(10)
            # print(f"<等待时间校验>：{e}")


if __name__ == '__main__':
    prooftim_process()
    # send_time_order("test6")
