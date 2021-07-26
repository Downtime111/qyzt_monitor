import random
import time

from mqtt_transfer_lcl import *
from multiprocessing import Process
import multiprocessing
import configparser

mqtt_config = configparser.ConfigParser()
mqtt_config.read("./mqtt_config.ini")

from paho.mqtt import client as mqtt_client
#from DB_pool import insert_one

pub_hostname = mqtt_config["publish"]['pub_hostname']
pub_port = int(mqtt_config["publish"]['pub_port'])
pub_qos = int(mqtt_config["publish"]['pub_qos'])
pub_client_id = mqtt_config["publish"]['pub_client_id']
pub_topic = mqtt_config["publish"]['pub_topic']



def publish_order():
    while True:
        try:
            if 0:
                pub_msg = "commend"
                thr_send_message(pub_msg, pub_topic, pub_hostname, pub_port, pub_qos)
            time.sleep(5)

        except TimeoutError:
            time.sleep(1)
            print("超时")
        except OSError:
            time.sleep(1)
            print("主机错误")

def subscribe_data():
    while True:
        run_subscribe()
        time.sleep(1)


if __name__ == "__main__":
    multiprocessing.freeze_support()
    try:
        t1 = Process(target=subscribe_data)
        t2 = Process(target=publish_order)
        t1.start()
        t2.start()
        t1.join()
        t2.join()
    except Exception as e:
        print(e)
        print("Error: 无法启动线程")