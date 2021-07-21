import random
from mqtt_transfer import *
from multiprocessing import Process

broker = '39.106.189.252'
port = 1883
topic = "/pub"
client_id = f'python-mqtt-{random.randint(0, 100)}'

pub_topic = "/sub"
pub_hostname = "39.106.189.252"
pub_port = 1883

def publish_order():
    i = 1
    while True:
        try:
            pub_msg = i
            thr_send_message(pub_msg,pub_topic,pub_hostname,pub_port)        #gevent.sleep(2)  # 协程遇到耗时操作后会自动切换其他协程运行
            time.sleep(1)
            i = i + 1
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
