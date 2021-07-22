import random
from mqtt_transfer_mon import *
from multiprocessing import Process
import multiprocessing


#'''
broker = '39.106.189.252'
port = 1883
topic = "/sub"
client_id = f'python-mqtt-{random.randint(0, 100)}'
#'''
pub_topic = "/pub"
pub_hostname = "39.106.189.252"
pub_port = 1883

def publish_order():
    while True:
        try:
            if 0:
                pub_msg = "commend"
                thr_send_message(pub_msg,pub_topic,pub_hostname,pub_port)
            #time.sleep(10)

        except TimeoutError:
            time.sleep(1)
            print("超时")
        except OSError:
            time.sleep(1)
            print("主机错误")

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
