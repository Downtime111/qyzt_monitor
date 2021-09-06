# -*- coding: UTF-8 -*-


"""
@描述：微信发送模块
@作者：garrett
@版本：V1.0
@创建时间：2021-08-15
"""


import json
import urllib3
import os
import re
import time
import datetime
import difflib
import ctypes
import requests
import configparser
from DB_sentence import insert_log
urllib3.disable_warnings()

alarm_config = configparser.ConfigParser()

'''
errcode = int(alarm_config["wechat"]['errcode'])
errmsg = alarm_config["wechat"]['errmsg']
access_token = alarm_config["wechat"]['access_token']
expires_in = alarm_config["wechat"]['expires_in']
'''

alarm_config.read("./config/alarm_config.ini", encoding="utf-8")
Token_config = alarm_config["wechat"]['Token_config']


def GetTokenFromServer(Corpid, Secret):
    """获取access_token"""
    Url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken"
    Data = {
        "corpid": Corpid,
        "corpsecret": Secret
    }
    r = requests.get(url=Url, params=Data, verify=False)
    # print(r.json())
    if r.json()['errcode'] != 0:
        return False
    else:
        Token = r.json()['access_token']
        file = open(Token_config, 'w')
        file.write(r.text)
        file.close()
        return Token


def SendMessage(Partyid, Subject, Content):
    alarm_config.read("./config/alarm_config.ini", encoding="utf-8")
    Corpid = alarm_config["wechat"]['Corpid']
    Secret = alarm_config["wechat"]['Secret']
    Agentid = alarm_config["wechat"]['Agentid']
    try:
        file = open(Token_config, 'r')
        Token = json.load(file)['access_token']
        file.close()
    except:
        Token = GetTokenFromServer(Corpid, Secret)

    # 发送消息
    Url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=%s" % Token
    Data = {
        "toparty": Partyid,
        "msgtype": "text",
        "agentid": Agentid,
        "text": {"content": Subject + '\n' + Content},
        "safe": "0"
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
        'Referer': 'http://61.183.175.130/sunxf/gtghj/index.html',
        'X - Requested - With': 'XMLHttpRequest',
        'Accept': 'application / json, text / javascript, * / *; q = 0.01',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
    }
    r = requests.post(url=Url, data=json.dumps(Data, ensure_ascii=False).encode("utf-8"), verify=False, headers=headers)

    # 如果发送失败，将重试三次
    n = 1
    while r.json()['errcode'] != 0 and n < 4:
        n = n + 1
        Token = GetTokenFromServer(Corpid, Secret)
        if Token:
            Url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=%s" % Token
            r = requests.post(url=Url, data=json.dumps(Data, ensure_ascii=False).encode("utf-8"), verify=False,
                              headers=headers)
            # PartyidPartyidprint(r.json())
    return r.json()


def run_alarm_wechat(dev, contents):
    now = datetime.datetime.now()
    last_time = (now - datetime.timedelta(seconds=contents)).strftime("%Y-%m-%d %H:%M:%S")
    inval_min = round(contents/60,2)
    inval_hour = round(contents/3600,2)
    now_string = now.strftime("%Y-%m-%d %H:%M:%S")
    alarm_config.read("./config/alarm_config.ini", encoding="utf-8")
    Partyid = alarm_config["wechat"]['Partyid']
    Subject = f"[{dev}设备信息]"  # 通知标题
    Content = f"设备状态：DTU断电或断网\n设备地点：XXXXX\n报警时间：{now_string}\n最后更新：{last_time}\n空白时长：{inval_min}分（{inval_hour}时）"
    print(Subject)
    print(Content)
    Status = SendMessage(Partyid, Subject, Content)
    # print(Status)
    print("[告警下发] 微信信息下发成功")
    insert_log(dev, f"下发告警,差{round(contents/60,2)}分钟数据")

if __name__ == '__main__':
    run_alarm_wechat("test", 3255)

