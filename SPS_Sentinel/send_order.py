# -*- coding: UTF-8 -*-


"""
@描述：指令下发模块
@作者：garrett
@版本：V1.0
@创建时间：2021-08-11
"""


import random
from paho.mqtt import client as mqtt_client
import configparser


mqtt_config = configparser.ConfigParser()
mqtt_config.read("./config/mqtt_config.ini")

pub_hostname = mqtt_config["publish"]['pub_hostname']
pub_port = int(mqtt_config["publish"]['pub_port'])
pub_qos = int(mqtt_config["publish"]['pub_qos'])
pub_client_id = mqtt_config["publish"]['pub_client_id']
#pub_topic = mqtt_config["publish"]['pub_topic']


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
    client2.username_pw_set(mqtt_config["publish"]['username'], mqtt_config["publish"]['passwd'])
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
    send_order("test","setfreq   10 600")