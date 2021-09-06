# -*- coding: UTF-8 -*-


"""
@描述：校验数据接收模块
@作者：garrett
@版本：V1.0
@创建时间：2021-08-11
"""

import time
from threading import Thread
from Proof_time import child_proof_timestamp
from paho.mqtt import client as mqtt_client
import configparser

proof_config = configparser.ConfigParser()
proof_config.read("./config/mqtt_config.ini")
# proof_config.read("./MQTT/config/mqtt_config.ini")


broker = proof_config["proof"]['broker']
port = int(proof_config["proof"]['port'])
topic = proof_config["proof"]['topic']
client_id = proof_config["proof"]['client_id']
username = proof_config["proof"]['username']
passwd = proof_config["proof"]['passwd']


def connect_mqtt() -> mqtt_client:
    client3 = mqtt_client.Client(client_id)
    client3.username_pw_set(username, password=passwd)
    client3.on_connect = on_connect
    client3.connect(broker, port)
    return client3


def on_connect(client3, userdata, flags, rc):
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
        time.sleep(1)
        print("[Receive_proof] Connected to MQTT Broker!\r")
    elif rc == 1:
        print(f"[Receive_proof] 连接拒绝 - 不正确的协议版本\n")
    elif rc == 2:
        print(f"[Receive_proof] 连接拒绝 - 无效客户标识符\n")
    elif rc == 3:
        print(f"[Receive_proof] 连接拒绝 - 服务器不可用\n")
    elif rc == 4:
        print(f"[Receive_proof] 连接拒绝 - 错误用户名或密码\n")
    elif rc == 5:
        print(f"[Receive_proof] 连接拒绝 - 未授权\n")
    elif rc == 6:
        print(f"[Receive_proof] 255：当前未使用\n")


def subscribe(client3: mqtt_client):
    client3.subscribe(topic, qos=int(proof_config["proof"]["rec_qos"]))
    client3.on_message = on_message
    client3.loop_forever()


def on_message(client3, userdata, msg):
    try:
        contents = str(msg.payload.decode('GBK'))
        inse_reco = Thread(target=child_proof_timestamp, args=(contents, msg.topic))  # 建子线程处理新来的任务请求
        inse_reco.start()  # 开启子线程
    except Exception as e:
        print(e)


def receive_proof_process():
    try:
        client3 = connect_mqtt()
        subscribe(client3)
    except Exception as e:
        print(e)
        time.sleep(20)


if __name__ == "__main__":
    receive_proof_process()
