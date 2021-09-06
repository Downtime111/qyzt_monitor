import time
from paho.mqtt import client as mqtt_client
from paho.mqtt import publish
import configparser

mqtt_config = configparser.ConfigParser()
mqtt_config.read("./mqtt_config.ini")

#from Sentinel.Sentinel import client_id, broker, topic, port
broker = mqtt_config["subscribe"]['broker']
port = int(mqtt_config["subscribe"]['port'])
topic = mqtt_config["subscribe"]['topic']
client_id = mqtt_config["subscribe"]['client_id']
'''
broker = '39.106.189.252'
port = 1883
topic = "/pub"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 100)}'
'''

def thr_send_message(msg, send_topic, hostname, portp, qosp):
    #print("发送donehello 消息。。。")
    # print(client)
    #print("子线程id：" + str(threading.current_thread().ident))
    #time.sleep(0)
    # client.publish("donehello", "donehello") #
    result = publish.single(send_topic, msg, hostname=hostname, port=portp, qos=qosp)
    # client.on_message 和 client.publish 不再共用同一个client
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
    client.subscribe(topic, int(mqtt_config["subscribe"]["rec_qos"]))
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
    #thr_send_message("msg")
    pass
