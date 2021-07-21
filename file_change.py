import os
import re
import datetime
import difflib


def read_file():
    with open ("./data/_STR22_Min.dat","r") as data:
        time_list = []
        find_list = []
        full_list = []
        corr_dict = {}

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

        print(len(full_list))
        #print(corr_dict)
        recent_time = max(time_list)
        recent_flag = str(recent_time.strftime("%Y-%m-%d %H:%M:%S"))
        print(recent_flag)

        with open ("./STR22_Count.log","w+") as log:
            log.write("{{{tim},{le}}}".format(tim = recent_flag,le = len(full_list)))
        recent_content = corr_dict[recent_flag]
        find_list.append(recent_content)
        print(find_list)
        #return line


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
        print(filename + ' not found!')
        return None

#def
if __name__ == "__main__":
    #read_file()
    print(__get_last_line("STR22_Count.log"))