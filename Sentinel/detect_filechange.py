"""
@Description:分析并获取采集数据
@Version:2.0
@Author:Garrett
"""

import os
import re
import datetime

"""
@
"""

def read_file(path):
    #with open ("./data/_STR22_Min.dat","r") as data:
    with open(path, "r") as data:
        time_list = []  # device time list

        full_list = []  # basic full content list
        corr_dict = {}  # time:content

        # 对可迭代对象进行迭代遍历,会自动地使用缓冲IO（buffered IO）以及内存管理
        for line in data:
            time = "".join(re.findall("^\"([0-9]+-[0-9]+-[0-9]+ [0-9]+:[0-9]+:[0-9]+)\"",line))
            other = "".join(re.findall("\",(.*)$", line))
            #print(other)
            if time != "":
                full_list.append(line)
                format_time = datetime.datetime.strptime(time,"%Y-%m-%d %H:%M:%S")
                time_list.append(format_time)
                corr_dict[format_time.strftime("%Y-%m-%d %H:%M:%S")] = other
        #print(full_list)
        #print(len(full_list))
        #print(corr_dict)
        return time_list, full_list, corr_dict

"""
@
"""


def get_content(path, stations, devices, sns, zones):
    """
    TODO:
        1. 根据devices 清洗数据

    :param path:
    :param stations:
    :param devices:
    :param sns:
    :param zones:
    :return:
    """
    global last_len
    find_list = []  # finded full content list
    time_list, full_list, corr_dict = read_file(path)
    recent_time = max(time_list)
    recent_flag = str(recent_time.strftime("%Y-%m-%d %H:%M:%S"))
    #print(recent_flag)
    try:
        shang = eval(__get_last_line("./"+devices+"_Count.log"))
        for t in shang.keys():
            last_len = shang[t]
        num =  int(len(full_list)) - int(last_len)
        #num = 1
        #print(num)
        # 当前条数大于日志记录条数
        if num >= 0:
            if num == 1:
                # 一次增加一条
                recent_content = corr_dict[recent_flag]
                find_list.append(stations+","+devices+","+sns+","+zones+","+recent_flag+","+recent_content)
            else:
                # 一次增加多条
                for i in range(0, num, 1):
                    min = datetime.timedelta(minutes=i)
                    tim_flag = (recent_time - min).strftime("%Y-%m-%d %H:%M:%S")
                    recent_content = corr_dict[tim_flag]
                    find_list.append(stations+","+devices+","+sns+","+zones+","+recent_flag+","+recent_content)
            #日志写入
            with open("./"+devices+"_Count.log", "w+") as log:
                log.write("{{\'{tim}\':\'{le}\'}}".format(tim=recent_flag, le=len(full_list)))
        # 当前条数小于日志记录条数
        else:
            # 新一天更新
            if len(full_list) == 1:
                recent_content = corr_dict[recent_flag]
                find_list.append(stations+","+devices+","+sns+","+zones+","+recent_flag+","+recent_content)
                with open("./"+devices+"_Count.log", "w+") as log:
                    log.write("{{\'{tim}\':\'{le}\'}}".format(tim=recent_flag, le=1))
            else:
                with open("./"+devices+"_Count.log", "w+") as log:
                    log.write("{{\'{tim}\':\'{le}\'}}".format(tim=recent_flag, le=0))
    except Exception as e:
        #(e)
        # 没有找到日志获取当前条数
        with open("./"+devices+"_Count.log", "w+") as log:
            log.write("{{\'{tim}\':\'{le}\'}}".format(tim=recent_flag, le=len(full_list)))
        print("INFO:[Add log file successful]")
    #for i in find_list:
    #    print(i)
    #print(find_list)
    return find_list


def __get_last_line(filename):
    try:
        filesize = os.path.getsize(filename)
        if filesize == 0:
            return None
        else:
            with open(filename, 'rb') as fp: # to use seek from end, must use mode 'rb'
                offset = -8                 # initialize offset
                while -offset < filesize:   # offset cannot exceed file size
                    fp.seek(offset, 2)      # read # offset chars from eof(represent by number '2')
                    lines = fp.readlines()  # read from fp to eof
                    if len(lines) >= 2:     # if contains at least 2 lines
                        return str(lines[-1], encoding="utf8")    # then last line is totally included
                    else:
                        offset *= 2         # enlarge offset
                fp.seek(0)
                lines = fp.readlines()
                return str(lines[-1], encoding="utf8")
    except FileNotFoundError:
        print("INFO:["+filename + ' not found!]')
        return None

#def
if __name__ == "__main__":


    #get_content()
    read_file('E:\zt_monitor\Sentinel\_STR22_Min.dat')

    # read_file()
    #last = eval(__get_last_line("STR22_Count.log"))
    #print(last)
    #print(last['2021-07-20 22:22:00'])


