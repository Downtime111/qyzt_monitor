import time
import random
from paho.mqtt import client as mqtt_client
from paho.mqtt import publish

from collector import client_id, broker, topic, port

'''
broker = '39.106.189.252'
port = 1883
topic = "/pub"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 100)}'
'''

def thr_send_message(msg,send_topic,hostname,port):
    #print("发送donehello 消息。。。")
    # print(client)
    #print("子线程id：" + str(threading.current_thread().ident))
    #time.sleep(0)
    # client.publish("donehello", "donehello") #这种方式下的client.on_message 和 client.publish 共用唯一一个client 实例，会造成无法同时收发问题。
    result = publish.single(send_topic, msg, hostname="39.106.189.252",
                   port=1883, qos=2)
    # 通过该方式使client.on_message 和 client.publish 不再共用同一个client，解决了收发无法同时的问题。
    if result == None:
        #print(f"Send `{msg}` to topic `{topic}`")
        print(f"Send `{msg}` to topic")
    else:
        print(f"Failed to send message to topic")


def connect_mqtt() -> mqtt_client:
    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print("Failed to connect, return code %d\n", rc)


def subscribe(client: mqtt_client):
    client.subscribe(topic, 2)
    client.on_message = on_message
    client.loop_forever()


def on_message(client, userdata, msg):
    print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")


def run_subscribe():
    try:
        client = connect_mqtt()
        subscribe(client)
        client.loop_forever()
    except Exception as e:
        print(e)
        time.sleep(5)


if __name__ == "__main__":
    # run_subscribe()
    thr_send_message("msg")