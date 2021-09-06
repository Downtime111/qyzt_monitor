"""
@Description:哨兵系统
@Version:1.0
@Author:Garrett

@TODO：
    1. 读取本地测量表字段的EXCEL，并上传LCL形成FLUX语句
    2. 联网自动更新设备信息列表
    3. 将FLUX语句生成放到LCL端
    4. 适配不同数据结构
"""
import random
import time
from uuid import uuid4
import re
import detect_filechange
from mqtt_transfer_sen import *
from multiprocessing import Process
import multiprocessing
import configparser

"""
@ Get mqtt config
"""
mqtt_config = configparser.ConfigParser()
mqtt_config.read("./mqtt_config.ini")

'''
broker = '39.106.189.252'
port = 1883
topic = "/pub"
client_id = f'python-mqtt-{random.randint(0, 100)}'
'''
pub_hostname = mqtt_config["publish"]['pub_hostname']
pub_port = int(mqtt_config["publish"]['pub_port'])
pub_qos = int(mqtt_config["publish"]['pub_qos'])
pub_client_id = mqtt_config["publish"]['pub_client_id']
pub_topic = mqtt_config["publish"]['pub_topic']


def publish_records(path, stations, devices, sns, zones):
    """

    :param path:
    :param stations:
    :param devices:
    :param sns:
    :param zones:
    :return:
    """
    while True:
        try:
            for pub_msg in detect_filechange.get_content(path, stations, devices, sns, zones):
                # print("1")
                if pub_msg != "":
                    thr_send_message(pub_msg, pub_topic, pub_hostname, pub_port, pub_qos)
                    # gevent.sleep(2)  # 协程遇到耗时操作后会自动切换其他协程运行
            time.sleep(random.randint(10, 15))
        except Exception as e1:
            print(f"INFO:[Cannot find data! Please check the path.]")
            print(e1)
            time.sleep(5)
            # break
        except TimeoutError:
            time.sleep(1)
            print("超时")


def publish_pg_str22_records(path, stations, devices, sns, zones):
    """

    :param path:
    :param stations:
    :param devices:
    :param sns:
    :param zones:
    :return:
    """
    while True:
        try:
            str22_path = path + "\_STR22_Min.dat"
            for pub_msg in detect_filechange.get_content(str22_path, stations, devices, sns, zones):
                # print("1")
                if pub_msg != "":
                    thr_send_message(pub_msg, pub_topic, pub_hostname, pub_port, pub_qos)
                    # gevent.sleep(2)  # 协程遇到耗时操作后会自动切换其他协程运行
            time.sleep(15)
        except Exception as e1:
            print(f"INFO:[Cannot find data! Please check the path.]")
            print(e1)
            time.sleep(5)
            # break
        except TimeoutError:
            time.sleep(1)
            print("超时")


def publish_hts_ott_records(path, stations, devices, sns, zones):
    """

    :param path:
    :param stations:
    :param devices:
    :param sns:
    :param zones:
    :return:
    """
    while True:
        try:
            str22_path = path + "_STR22_Min.dat"
            for pub_msg in detect_filechange.get_content(str22_path, stations, devices, sns, zones):
                # print("1")
                if pub_msg != "":
                    thr_send_message(pub_msg, pub_topic, pub_hostname, pub_port, pub_qos)
                    # gevent.sleep(2)  # 协程遇到耗时操作后会自动切换其他协程运行
            time.sleep(15)
        except Exception as e1:
            print(f"INFO:[Cannot find data! Please check the path.]")
            print(e1)
            time.sleep(5)
            # break
        except TimeoutError:
            time.sleep(1)
            print("超时")


def subscribe_data():
    """

    :return:
    """
    while True:
        run_subscribe()
        # gevent.sleep(1)


def short_uuid():
    """

    :return:
    """
    uuidChars = ("a", "b", "c", "d", "e", "f",
                 "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s",
                 "t", "u", "v", "w", "x", "y", "z", "0", "1", "2", "3", "4", "5",
                 "6", "7", "8", "9", "A", "B", "C", "D", "E", "F", "G", "H", "I",
                 "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V",
                 "W", "X", "Y", "Z")
    uuid = str(uuid4()).replace('-', '')
    result = ''
    for i in range(0, 8):
        sub = uuid[i * 4: i * 4 + 4]
        x = int(sub, 16)
        result += uuidChars[x % 0x3E]
    return result


def get_info(uuids):
    """

    :param uuids:
    :return:
    """
    while True:
        """
        @ Get station
        """
        while True:
            print(">>[1/3] Please select the station.")
            sta = input("(ENTER NUM):")
            c1 = re.match('^[0-9]+?$', sta)
            global station
            if c1:
                if int(sta) == 1:
                    station = "PingGu"
                    break
                elif int(sta) == 2:
                    station = "HaiTuoShan"
                    break
                else:
                    print("[Tips] Please select the RIGHT station.")
            else:
                print("[Tips] Please enter (1-10)")

        """
        @ Get zone
        """
        while True:
            print(">>[2/3] Please select the zone")
            zon = input("(ENTER NUM):")
            c2 = re.match('^[0-9]+?$', sta)
            if c2:
                if int(zon) == 1:
                    zone = "BeiJing"
                    break
                elif int(zon) == 2:
                    zone = "HeBei"
                    break
                elif int(zon) == 3:
                    zone = "JiangSu"
                    break
                elif int(zon) == 4:
                    zone = "NeiMemg"
                    break
                elif int(zon) == 5:
                    zone = "ZheJiang"
                    break
                else:
                    print("[Tips] Please select the RIGHT zone.")
            else:
                print("[Tips] Please enter (1-10)")

        """
        @ Get devices
        """
        dev_list = []
        dev_path = {}
        global dev
        print(">>[3/3] Please select the device.")
        dev = input("(ENTER NUM):")
        while True:
            c3 = re.match('^[0-9]+?$', dev)
            global device
            if c3:
                if int(dev) == 1:
                    device = "pg_STR22"
                    if device not in dev_list:
                        dev_list.append(device)
                        print(f">>Please enter the {device} DATA path")
                        print("[Tips] The path format is similar to \'E:\zt_monitor\Sentinel\'")
                        path = input("Path:")
                        dev_path[device] = path
                    print(">>[3/3] Please select other device.")
                    print("[CHOOSEN DEVICES] : {list}".format(list=", ".join(dev_list)))
                    dev = input("(Enter NUM,\'q\' to finish):")
                    if str.lower(dev) == "q":
                        break
                elif int(dev) == 2:
                    device = "hts_OTT"
                    if device not in dev_list:
                        dev_list.append(device)
                        print(f">>Please enter the {device} DATA path")
                        print("[Tips] The path format is similar to \'E:\zt_monitor\Sentinel\'")
                        path = input("Path:")
                        dev_path[device] = path
                    print(">>[3/3] Please select other device.")
                    print("[CHOOSEN DEVICES] : {list}".format(list=", ".join(dev_list)))
                    dev = input("(Enter NUM,\'q\' to finish):")
                    if str.lower(dev) == "q":
                        break
                elif int(dev) == 3:
                    device = "hts_2DVD"
                    if device not in dev_list:
                        dev_list.append(device)
                        print(f">>Please enter the {device} DATA path")
                        print("[Tips] The path format is similar to \'E:\zt_monitor\Sentinel\'")
                        path = input("Path:")
                        dev_path[device] = path
                    print(">>[3/3] Please select other device.")
                    print("[CHOOSEN DEVICES] : {list}".format(list=", ".join(dev_list)))
                    dev = input("(Enter NUM,\'q\' to finish):")
                    if str.lower(dev) == "q":
                        break
                else:
                    print(">>[3/3] Please select RIGHT device.")
                    dev = input("(Enter NUM,\'q\' to finish):")
                    if str.lower(dev) == "q":
                        break
            else:
                print(">>[3/3] Please select right device.")
                dev = input("(Enter NUM,\'q\' to finish):")
                if str.lower(dev) == "q":
                    break

        """
        @ Get sn
        """

        capitals = [i for i in station if i.isupper()]

        d_num = len(dev_list)
        dev_sn = {}
        for i in range(1, d_num + 1):
            sn = ''.join([i for i in station if i.isupper()]) + str(i) + "-" + uuids[:2]
            dev_sn[dev_list[i - 1]] = sn
        # print(dic_dev)
        print(" ")
        print(f'[Station]:{station}')
        print(f'[Zone]:{zone}')
        print("[Device]:{list}".format(list=", ".join(dev_list)))
        print("[Path]:")
        for dev_key in dev_path:
            print(dev_key + ' ' + "\"" + dev_path[dev_key] + "\"")
        print(" ")
        print("Are you SURE of the above choice?")
        while True:
            sure = input("(Enter [y/n]):")
            if str.lower(sure) == "y":
                break
            elif str.lower(sure) == "n":
                break
            else:
                pass
        if str.lower(sure) == "y":
            break
        else:
            pass
    return station, zone, dev_list, dev_path, dev_sn


if __name__ == "__main__":
    try:
        station_config = configparser.ConfigParser()
        station_config.read("./station_config.ini")
        station = station_config["station"]['station']
        zone = station_config["station"]['zone']
        dev_list = eval(station_config["station"]['dev_list'])
        dev_path = eval(station_config["station"]['dev_path'])
        dev_sn = eval(station_config["station"]['dev_sn'])
    except Exception as e:
        # print(e)
        uuid = short_uuid()
        station, zone, dev_list, dev_path, dev_sn = get_info(uuid)
        station_config = configparser.ConfigParser()
        station_config.add_section("station")
        station_config.set("station", "station", station)
        station_config.set("station", "zone", zone)
        station_config.set("station", "dev_list", str(dev_list))
        station_config.set("station", "dev_path", str(dev_path))
        station_config.set("station", "dev_sn", str(dev_sn))
        station_config.write(open("./station_config.ini", "w+"))
        time.sleep(1)
        mqtt_config = configparser.ConfigParser()
        mqtt_config.read("./mqtt_config.ini")
        mqtt_config.set("publish", 'pub_client_id', zone + "-" + station)
        mqtt_config.write(open("./mqtt_config.ini", "w+"))
    print(station, zone, dev_list, dev_path, dev_sn)
    # '''

    multiprocessing.freeze_support()
    try:
        l = len(dev_list)
        ps = []
        for i in range(0, l):
            # print(list[i])
            p = Process(target=publish_records, name="process" + str(i),
                        args=(dev_path[dev_list[i]], station, dev_list[i], dev_sn[dev_list[i]], zone))
            ps.append(p)
        # print(ps)
        for i in range(0, l):
            ps[i].start()
        for i in range(0, l):
            ps[i].join()
    except Exception as e:
        print(e)
        print("Error: 无法启动进程")
    # '''
    '''
    multiprocessing.freeze_support()
    try:
        t1 = Process(target=publish_order)
        t2 = Process(target=subscribe_data)
        t1.start()
        t2.start()
        t1.join()
        t2.join()
    except Exception as e:
        print(e)
        print("Error: 无法启动线程")
    '''
    '''
    pub_msg = '"2021-07-20 22:36:00",81969,12.04,32.99,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-3.241173,-3.296,-2.825,0.151,299.8331,455.0078,-39.01622,-39.67,-39.01,0.085,299.5479,417.4913,0,0,0,0,0,0,0,0,98.07195,0,0,0,0'
    thr_send_message(pub_msg, pub_topic, pub_hostname, pub_port)
    '''
