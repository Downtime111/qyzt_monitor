"""
@Description:InfluxDB连接
@Version:1.0
@Author:Garrett
"""
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime,timezone,timedelta

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


def insert_pg_str22_record(stations, devices, sns, zones, utc_times, sensors):
    try:
        client = InfluxDBClient.from_config_file("influxdb_config.ini")
        # client = InfluxDBClient(url=url, token=token, org=org)
        write_api = client.write_api(write_options=SYNCHRONOUS)
        p = Point(devices) \
            .tag("SN", sns) \
            .tag("ZONE", zones) \
            .field("RECORD", float(sensors[5])) \
            .field("batt_volt_Min", float(sensors[6])) \
            .field("Ptemp", float(sensors[7])) \
            .field("GHI_Avg", float(sensors[8])) \
            .field("GHI_Min", float(sensors[9])) \
            .field("GHI_Max", float(sensors[10])) \
            .field("GHI_Std", float(sensors[11])) \
            .field("DHI_Avg", float(sensors[12])) \
            .field("DHI_Min", float(sensors[13])) \
            .field("DHI_Max", float(sensors[14])) \
            .field("DHI_Std", float(sensors[15])) \
            .field("DNI_Avg", float(sensors[16])) \
            .field("DNI_Min", float(sensors[17])) \
            .field("DNI_Max", float(sensors[18])) \
            .field("DNI_Std", float(sensors[19])) \
            .field("SRDown_Avg", float(sensors[20])) \
            .field("SRDown_Min", float(sensors[21])) \
            .field("SRDown_Max", float(sensors[22])) \
            .field("SRDown_Std", float(sensors[23])) \
            .field("IRDown_Avg", float(sensors[24])) \
            .field("IRDown_Min", float(sensors[25])) \
            .field("IRDown_Max", float(sensors[26])) \
            .field("IRDown_Std", float(sensors[27])) \
            .field("IRDownTK_Avg", float(sensors[28])) \
            .field("IRDownCo_Avg", float(sensors[29])) \
            .field("IRUP_Avg", float(sensors[30])) \
            .field("IRUP_Min", float(sensors[31])) \
            .field("IRUP_Max", float(sensors[32])) \
            .field("IRUP_Std", float(sensors[33])) \
            .field("IRUPTK_Avg", float(sensors[34])) \
            .field("IRUpCo_Avg", float(sensors[35])) \
            .field("UVA_Avg", float(sensors[36])) \
            .field("UVA_Min", float(sensors[37])) \
            .field("UVA_Max", float(sensors[38])) \
            .field("UVA_Std", float(sensors[39])) \
            .field("UVB_Avg", float(sensors[40])) \
            .field("UVB_Min", float(sensors[41])) \
            .field("UVB_Max", float(sensors[42])) \
            .field("UVB_Std", float(sensors[43])) \
            .field("Temp_Volt_Avg", float(sensors[44])) \
            .field("PAR_Avg", float(sensors[45])) \
            .field("PAR_Min", float(sensors[46])) \
            .field("PAR_Max", float(sensors[47])) \
            .field("PAR_Std", float(sensors[48])) \
            .time(utc_times)
            #.time(logger_date+"T"+"05:14:00")
            #.time("2021-07-26T03:11:00.000")
            #.time(datetime.strptime("2021-07-26 03:01","%Y-%m-%d %H:%M").isoformat("T"))
            #.time(datetime.utcnow().isoformat("T"))
        write_api.write(bucket=stations, record=p)

    except Exception as e:
        print(e)
        print("Insert record ERR!")

"""    
def insert_pg_ott_record(sns, zones, stations, devices, logger_times,sensors):

        client = InfluxDBClient.from_config_file("influxdb_config.ini")
        # client = InfluxDBClient(url=url, token=token, org=org)
        write_api = client.write_api(write_options=SYNCHRONOUS)
        utc_time ="{datetime}".format(datetime=(datetime.strptime(logger_times, "%Y-%m-%d %H:%M:%S")-timedelta(hours=8)).isoformat("T"))
         p = Point(devices) \
            .tag("SN", sns) \
            .tag("ZONE", zones) \
            .field("temperature", float(sensors[0])) \
            .field("humi", float(sensors[1])) \
            .time(utc_time)
        p = {"measurement": devices,"tags": {"SN": sns,"ZONE": zones},"fields":{"temperature": float(sensors[0]),"humi": float(sensors[1]),"time": utc_time}}
        write_api.write(bucket=stations, record=p)
        
    except Exception as e:
        print(e)
        print("Insert record ERR!")
"""


if __name__ == "__main__":
    """
    sn = "b01"
    zone = "beijing"
    station = "pinggu"
    device = "str22"
    sensor = ["20333", "3"]
    logger_time = "2021-07-26 15:08:30"
    insert_pg_str22_record(sn, zone, station, device, logger_time, sensor)
    """
