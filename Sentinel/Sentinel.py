import random
import time

import detect_filechange
from mqtt_transfer_sen import *
from multiprocessing import Process
import multiprocessing
import configparser

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


def publish_order():
    while True:
        try:
            for pub_msg in detect_filechange.get_content():
                #print("1")
                if pub_msg != "":
                    thr_send_message(pub_msg, pub_topic, pub_hostname, pub_port, pub_qos)       #gevent.sleep(2)  # 协程遇到耗时操作后会自动切换其他协程运行
            time.sleep(15)
        except Exception as e1:
            print(f"INFO:[Cannot find data! Please check the path.]")
            print(e1)
            time.sleep(5)
            #break
        except TimeoutError:
            time.sleep(1)
            print("超时")


def subscribe_data():
    while True:
        run_subscribe()
    #gevent.sleep(1)


if __name__ == "__main__":
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
    pub_msg = '"2021-07-20 22:36:00",81969,12.04,32.99,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-3.241173,-3.296,-2.825,0.151,299.8331,455.0078,-39.01622,-39.67,-39.01,0.085,299.5479,417.4913,0,0,0,0,0,0,0,0,98.07195,0,0,0,0'
    thr_send_message(pub_msg, pub_topic, pub_hostname, pub_port)
    '''