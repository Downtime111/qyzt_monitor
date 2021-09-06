import datetime
import random


def create_file(date,filename, end_time):
    with open (f"./data/{filename}-0.txt", "a+", encoding="GBK") as data:
        data.write("\"TOPFLAG\",\"版本V1.0\"\n")
        data.write("\"日期时间\",\"温度0\",\"温度1\",\"辐射0\",\"辐射1\",\"总辐射0\",\"总辐射1\"\n")
        data.write("\"YYYY-MM-DD hh:mn\",\"℃\",\"℃\",\"W/m^2\",\"W/m^2\",\"MJ/m^2\",\"MJ/m^2\"\n")
        start_time = datetime.datetime.strptime(f"{date} 00:00:00", "%Y-%m-%d %H:%M:%S")
        end = datetime.datetime.strptime(f"{date} {end_time}", "%Y-%m-%d %H:%M:%S")
        while True:
            if start_time <= end:
                data.write(f"\"{start_time},{random.randint(0, 9)}.{random.randint(0, 50)},{random.randint(0, 9)}.{random.randint(0, 50)},{random.randint(0, 9)}.{random.randint(0, 1000)},0.{random.randint(0, 50)},{random.randint(0, 2)}.{random.randint(0, 50)},{random.randint(0, 20)}.{random.randint(0, 100)},0x0{random.randint(0, 9)}\"\n")
                start_time += datetime.timedelta(minutes=5)
            else:
                break
        #data.write(f"endexport {filename}\r")


if __name__ == "__main__":
    print("SD卡测试数据生成工具")
    date = "2021-08-20"
    end_time = "23:59:59"
    filename = date[:4]+date[5:7]+date[8:10]
    create_file(date, filename, end_time)
