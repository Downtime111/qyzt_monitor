import time
import datetime
import random
from paho.mqtt import client as mqtt_client
from paho.mqtt import publish

#from collector import client_id, broker, topic, port

#'''
broker = '39.106.189.252'
port = 1883
topic = "DTU/ORD/test"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 100)}'
username = 'mqttx'
passwd = 'mqttx'
#'''

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("[publish] Connected to MQTT Broker!")
        else:
            print(f"[publish] Failed to connect, return code {rc}\n")

    client2 = mqtt_client.Client(client_id)
    client2.username_pw_set("test2", "test2")
    client2.on_connect = on_connect
    client2.connect(broker, port)
    return client2


def publish(client2,content):
    """
    msg_count = 0
    while True:
        time.sleep(1)
        msg = f"messages: {msg_count}"
        result = client2.publish(topic, msg, qos=2)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        msg_count += 1
        """

    i = 0
    client2.publish(topic, content, qos=2)
    print(topic,content)
    """
    while True:
        client2.publish(topic, i, qos=2)
        print(i,topic)
        i += 1

        if 20 > i > 5:
            time.sleep(0.2)
        elif 40 >= i >= 20:
            time.sleep(0.1)
        else:
            time.sleep(1)"""


def run_publish(content):
    client2 = connect_mqtt()
    #client2.loop_start()
    publish(client2,content)



if __name__ == "__main__":
    # run_subscribe()
    #run_publish(str(datetime.datetime.now()))
    run_publish("setfreq   3 600")
