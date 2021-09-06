# -*- coding: UTF-8 -*-


"""
@描述：数据接收模块
@作者：garrett
@版本：V1.0
@创建时间：2021-08-11
"""


import time
# import random
from threading import Thread
from DB_sentence import child_insert_record
from paho.mqtt import client as mqtt_client
# from paho.mqtt import publish
# import mutithread_insert_sql
import configparser

mqtt_config = configparser.ConfigParser()
mqtt_config.read("./config/mqtt_config.ini")
#mqtt_config.read("./MQTT/config/mqtt_config.ini")

broker = mqtt_config["subscribe"]['broker']
port = int(mqtt_config["subscribe"]['port'])
topic = mqtt_config["subscribe"]['topic']
client_id = mqtt_config["subscribe"]['client_id']
username = mqtt_config["subscribe"]['username']
passwd = mqtt_config["subscribe"]['passwd']

"""pub_hostname = mqtt_config["publish"]['pub_hostname']
pub_port = int(mqtt_config["publish"]['pub_port'])
pub_qos = int(mqtt_config["publish"]['pub_qos'])
pub_client_id = mqtt_config["publish"]['pub_client_id']
pub_topic = mqtt_config["publish"]['pub_topic']"""


# 匿名方式发送函数
"""
def thr_send_message(msg, send_topic, hostname, portp, qosp):
    # print("发送donehello 消息。。。")
    # print(client)
    # print("子线程id：" + str(threading.current_thread().ident))
    # time.sleep(0)
    # client.publish("donehello", "donehello") #这种方式下的client.on_message 和 client.publish 共用唯一一个client 实例，会造成无法同时收发问题。
    result = publish.single(send_topic, msg, hostname=hostname, port=portp, qos=qosp)
    # 通过该方式使client.on_message 和 client.publish 不再共用同一个client，解决了收发无法同时的问题。
    if result == None:
        # print(f"Send `{msg}` to topic `{topic}`")
        print(f"Send `{msg}` to topic")
    else:
        print(f"Failed to send message to topic")
"""


def connect_mqtt() -> mqtt_client:
    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password=passwd)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def on_connect(client, userdata, flags, rc):
    """
        rc: 连接状况
        – 0：连接成功
        – 1：连接拒绝 - 不正确的协议版本
        – 2：连接拒绝 - 无效客户标识符
        – 3：连接拒绝 - 服务器不可用
        – 4：连接拒绝 - 错误用户名或密码
        – 5：连接拒绝 - 未授权
        – 6 - 255：当前未使用。
    """
    if rc == 0:
        print("[subscribe] Connected to MQTT Broker!\r")
    else:
        print(f"[subscribe] Failed to connect, return code {rc}\n")


def subscribe(client: mqtt_client):
    client.subscribe(topic, qos=int(mqtt_config["subscribe"]["rec_qos"]))
    client.on_message = on_message
    client.loop_forever()


# 累加列表初始值
"""
s = io.StringIO()
s.seek(0, 0)
bulkpayload = []
s.write(str(datetime.now())[0:19])
"""


def on_message(client, userdata, msg):
    try:
        # contents = eval(str((msg.payload.decode()).split(",")))
        contents = str(msg.payload.decode('GBK')) # .strip('\r\n')
        # print("topic",msg.topic)
        inse_reco = Thread(target=child_insert_record, args=(contents, msg.topic))  # 建子线程处理新来的任务请求
        inse_reco.start() # 开启子线程
    except Exception as e:
        print(e)

    # 方法二：累加列表
    """
    i_time = float(str(datetime.now() - datetime.strptime(s.getvalue(), "%Y-%m-%d %H:%M:%S"))[5:10])
    # print(i_time)
    if i_time >= 1:
        if len(bulkpayload) == 0:
            print(contents)
            s.seek(0, 0)
            s.write(str(datetime.now())[0:19])
        else:
            bulkpayload.append(contents)
            s.seek(0, 0)
            s.write(str(datetime.now())[0:19])
    else:
        bulkpayload.append(contents)
        s.seek(0, 0)
        s.write(str(datetime.now())[0:19])
    if i_time > 1 and len(bulkpayload) >= 1:
        print(bulkpayload)
        #mutithread_insert_sql.run_mutithread(bulkpayload)
        bulkpayload = []
        s.seek(0, 0)
        s.write(str(datetime.now())[0:19])
    """


def receive_process():
    try:
        client = connect_mqtt()
        subscribe(client)
    except Exception as e:
        print(e)
        time.sleep(5)


if __name__ == "__main__":
    receive_process()
