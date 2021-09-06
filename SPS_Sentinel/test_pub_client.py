# -*- coding: UTF-8 -*-


"""
@描述：MQTT虚拟DTU测试模块
@作者：garrett
@版本：V1.0
@创建时间：2021-08-11
"""


import datetime
import random
import time

from paho.mqtt import client as mqtt_client
import configparser
from uuid import uuid4

mqtt_config = configparser.ConfigParser()
mqtt_config.read("./config/mqtt_config.ini")

pub_hostname = mqtt_config["publish"]['pub_hostname']
pub_port = int(mqtt_config["publish"]['pub_port'])
pub_qos = int(mqtt_config["publish"]['pub_qos'])

#pub_topic = mqtt_config["publish"]['pub_topic']

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

def connect_mqtt():
    """

    :return:
    """
    def on_connect(client, userdata, flags, rc):
        """

        :param client:
        :param userdata:
        :param flags:
        :param rc:
        :return:
        """
        if rc == 0:
            print("[publish] Connected to MQTT Broker!")
        else:
            print(f"[publish] Failed to connect, return code {rc}\n")

    client2 = mqtt_client.Client(pub_client_id)
    client2.username_pw_set("test2", "test2")
    client2.on_connect = on_connect
    client2.connect(pub_hostname, pub_port)
    return client2


def publish(client2, content, pub_topic):
    """

    :param client2:
    :param content:
    :param pub_topic:
    :return:
    """
    client2.publish(pub_topic, content, qos=2)
    print(f"[指令下发] <{pub_topic}>: {content}")


def send_order(pub_topic, content):
    """

    :param pub_topic:
    :param content:
    :return:
    """
    client2 = connect_mqtt()
    # client2.loop_start()
    publish(client2, content, pub_topic)


if __name__ == "__main__":
    print("MQTT虚拟DTU测试程序")
    inval = int(input("间隔(60s以上):"))
    dev_num = int(input("测试设备数量:"))
    pub_client_id = f"test{short_uuid()}"
    topic_0 = 'DTU'
    topic_1 = 'MSG2'

    #print(min,sec)
    if inval >= 60:
        #print(min, sec)
        while True:
            min = datetime.datetime.now().minute
            sec = datetime.datetime.now().second
            if min % (inval / 60) == 0 and sec == 0:

                    for i in range(1, dev_num+1):
                        now = datetime.datetime.now().strftime("%Y-%m-%d %H")+f":{min}:00"
                        msg = f"\"{now},{random.randint(0, 9)}.{random.randint(0, 50)}," \
                              f"{random.randint(0, 9)}.{random.randint(0, 50)}," \
                              f"{random.randint(0, 9)}.{random.randint(0, 1000)}," \
                              f"0.{random.randint(0, 50)},{random.randint(0, 2)}.{random.randint(0, 50)}," \
                              f"{random.randint(0, 20)}.{random.randint(0, 100)},0x0{random.randint(0, 9)}\""
                        send_order(f"{topic_0}/{topic_1}/test{i}", msg)
                        #print(i, msg)
                        time.sleep(0.1)
            else:
                time.sleep(1)
                #print(min, sec)
    else:
        while True:
            min = datetime.datetime.now().minute
            sec = datetime.datetime.now().second
            if sec % inval == 0:

                for i in range(1, dev_num + 1):
                    if sec < 10:
                        sec_out = f"0{sec}"
                    else:
                        sec_out = sec
                    now = datetime.datetime.now().strftime("%Y-%m-%d %H") + f":{min}:{sec_out}"
                    msg = f"\"{now},{random.randint(0, 9)}.{random.randint(0, 50)}," \
                          f"{random.randint(0, 9)}.{random.randint(0, 50)}," \
                          f"{random.randint(0, 9)}.{random.randint(0, 1000)}," \
                          f"0.{random.randint(0, 50)},{random.randint(0, 2)}.{random.randint(0, 50)}," \
                          f" {random.randint(0, 20)}.{random.randint(0, 100)},0x0{random.randint(0, 9)}\""
                    send_order(f"{topic_0}/{topic_1}/test{i}", msg)
                    #print(i, msg)
                    time.sleep(0.1)
                time.sleep(1)
            else:
                time.sleep(1)
                #print(min, sec)