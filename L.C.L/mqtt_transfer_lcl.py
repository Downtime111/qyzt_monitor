import time
import random
from paho.mqtt import client as mqtt_client
from paho.mqtt import publish
from InfluxDB_pool import *
#from DB_pool import insert_one
# L.C.L import client_id, broker, topic, port
import configparser

mqtt_config = configparser.ConfigParser()
mqtt_config.read("./mqtt_config.ini")

# generate client ID with pub prefix randomly
broker = mqtt_config["subscribe"]['broker']
port = int(mqtt_config["subscribe"]['port'])
topic = mqtt_config["subscribe"]['topic']
client_id = mqtt_config["subscribe"]['client_id']

"""pub_hostname = mqtt_config["publish"]['pub_hostname']
pub_port = int(mqtt_config["publish"]['pub_port'])
pub_qos = int(mqtt_config["publish"]['pub_qos'])
pub_client_id = mqtt_config["publish"]['pub_client_id']
pub_topic = mqtt_config["publish"]['pub_topic']"""

def thr_send_message(msg, send_topic, hostname, portp, qosp):
    #print("发送donehello 消息。。。")
    # print(client)
    #print("子线程id：" + str(threading.current_thread().ident))
    #time.sleep(0)
    # client.publish("donehello", "donehello") #这种方式下的client.on_message 和 client.publish 共用唯一一个client 实例，会造成无法同时收发问题。
    result = publish.single(send_topic, msg, hostname=hostname, port=portp, qos=qosp)
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
    client.subscribe(topic, int(mqtt_config["subscribe"]["rec_qos"]))
    client.on_message = on_message
    client.loop_forever()

"""
[bucket]
stations > 设备所在站点

[measurement]
devices > 设备型号

[tag]
sns > 设备编号
zones > 设备所在地区

[field]
records 传感器参数
"""

def on_message(client, userdata, msg):
    # print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    contents = str((msg.payload.decode()).split(","))
    '''
    # contents[<station>,<device>,<sn>,<zone>,<logger_times><sensor1><sensor2>...] #
    '''
    station = contents[0]
    device = contents[1]
    sn = contents[2]
    zone = contents[3]
    logger_time = contents[4]
    utc_time = "{datetime}".format(datetime=(datetime.strptime(logger_time, "%Y-%m-%d %H:%M:%S") - timedelta(hours=8)).isoformat("T"))

    try:
        if device == "STR22":
            insert_str22_record(station, device, sn, zone, utc_time, contents)
        elif device == "OTT":
            pass
        elif device == "2DVD":
            pass
        elif device == "CAWS":
            pass
        elif device == "Hyvis":
            pass
        elif device == "VAISALA":
            pass
    except Exception as e:
        print(e)
        print("Insert record ERR!")
    """
    ## insert DB by MySQL
    
    sql = "insert into str22(LOCATION,DATETIME,RECORD,batt_volt_Min,Ptemp,GHI_Avg," \
          "GHI_Min,GHI_Max,GHI_Std,DHI_Avg,DHI_Min,DHI_Max,DHI_Std,DNI_Avg,DNI_Min," \
          "DNI_Max,DNI_Std,SRDown_Avg,SRDown_Min,SRDown_Max,SRDown_Std,IRDown_Avg," \
          "IRDown_Min,IRDown_Max,IRDown_Std,IRDownTK_Avg,IRDownCo_Avg,IRUP_Avg," \
          "IRUP_Min,IRUP_Max,IRUP_Std,IRUPTK_Avg,IRUpCo_Avg,UVA_Avg,UVA_Min,UVA_Max," \
          "UVA_Std,UVB_Avg,UVB_Min,UVB_Max,UVB_Std,Temp_Volt_Avg,PAR_Avg,PAR_Min," \
          "PAR_Max,PAR_Std) " \
          "VALUES " \
          "(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s," \
          "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"  # 增加 
    res = insert_one(sql, str(msg.payload.decode()).split(","))
    print(res)
   """


def run_subscribe():
    try:
        client = connect_mqtt()
        subscribe(client)
        #client.loop_forever()
    except Exception as e:
        print(e)
        time.sleep(5)


if __name__ == "__main__":
    #run_subscribe()
   """ pub_msg = "commend"
    pub_topic = "/lcl/commend"
    pub_hostname = "39.106.198.252"
    pub_port = 1883
    pub_qos = 2

    thr_send_message(pub_msg, pub_topic, pub_hostname, pub_port, pub_qos)"""