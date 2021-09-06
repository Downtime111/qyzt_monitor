# -*- coding: UTF-8 -*-


"""
@描述：主进程
@作者：garrett
@版本：V1.0
@创建时间：2021-08-11
"""


print("程序正在启动中...\r")


import time
from receive_data import receive_process
from receive_proof import receive_proof_process
from Proof_time import prooftim_process
from multiprocessing import Process
from Proof_records import proofrec_proc
import multiprocessing


def receive_datas():
    receive_process()


def receive_proof():
    receive_proof_process()


def time_proofread():
    prooftim_process()


def records_proofread():
    proofrec_proc()


if __name__ == "__main__":
    with open("./config/back_del_cache.dat", "r+") as bdc:
        bdc.truncate(0)
    with open("./config/stamp_cache.dat", "r+") as sc:
        sc.truncate(0)

    multiprocessing.freeze_support()
    try:
        # 枚举多进程
        t1 = Process(target=receive_datas)
        t2 = Process(target=receive_proof)
        t3 = Process(target=time_proofread)
        t4 = Process(target=records_proofread)
        # 开启多进程
        t1.start()
        t2.start()
        t3.start()
        t4.start()
        # 等待子线程
        t1.join()
        t2.join()
        t3.join()
        t4.join()
    except Exception as e:
        print(e)
        print("Error: 无法启动进程")
