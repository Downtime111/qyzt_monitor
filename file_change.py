import os
import re
import datetime



def read_file():
    #with open ("./data/_STR22_Min.dat","r") as data:
    with open("./_STR22_Min.dat", "r") as data:
        time_list = []  # device time list

        full_list = []  # basic full content list
        corr_dict = {}  # time:content

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


def get_content():
    global last_len
    find_list = []  # finded full content list
    time_list, full_list, corr_dict = read_file()
    recent_time = max(time_list)
    recent_flag = str(recent_time.strftime("%Y-%m-%d %H:%M:%S"))
    #print(recent_flag)
    try:
        shang = eval(__get_last_line("./STR22_Count.log"))
        for t in shang.keys():
            last_len = shang[t]
        num =  int(len(full_list)) - int(last_len)
        #num = 1
        #print(num)
        if num >= 0:
            if num == 1:
                recent_content = corr_dict[recent_flag]
                find_list.append(recent_flag+","+recent_content)
            else:
                for i in range(0, num, 1):
                    min = datetime.timedelta(minutes=i)
                    tim_flag = (recent_time - min).strftime("%Y-%m-%d %H:%M:%S")
                    recent_content = corr_dict[tim_flag]
                    find_list.append(tim_flag + "," + recent_content)
        else:
            recent_content = corr_dict[recent_flag]
            find_list.append(recent_flag + "," + recent_content)
            with open("./STR22_Count.log", "w+") as log:
                log.write("{{\'{tim}\':\'{le}\'}}".format(tim=recent_flag, le=1))
    except Exception as e:
        print(e)
        print("INFO:[Add log file successful]")
    #for i in find_list:
    #    print(i)
    with open ("./STR22_Count.log","w+") as log:
        log.write("{{\'{tim}\':\'{le}\'}}".format(tim = recent_flag,le = len(full_list)))
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
    #read_file()
    get_content()
    #last = eval(__get_last_line("STR22_Count.log"))
    #print(last)
    #print(last['2021-07-20 22:22:00'])


