#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
import time
from multiprocessing import Queue as multiQueue
from multiprocessing import Process
import json


class Msg(object):
    def __init__(self, num):
        self.num = num

def producer(msg_queue):
    for i in range(5):
        m = Msg(i)
        msg_queue.put(m)
        print('Producer is processing ==> {}'.format(str(i)))
        time.sleep(0.5)

def consumer1(q, send_q):
    msg = q.get()

    def func1(n):
        return n ** 2

    msg_2 = func1(msg.num)
    print("{} is processed to {} by consumer1".format(msg, msg_2))

    send_q.put(msg_2)

def consumer2(send_q):
    msg = send_q.get()

    def func2(n):
        return n - 1

    msg_2 = func2(msg)
    print("{} is processed to {} by consumer2".format(msg, msg_2))

if __name__ == '__main__':

    msg_queue = multiQueue()
    send_msg_queue = multiQueue()

    producer_process_list = []
    consumer1_process_list = []
    consumer2_process_list = []
    for i in range(2):
        producer_process_list.append(Process(target=producer, args=(msg_queue,)))

    for i in range(10):
        consumer1_process_list.append(Process(target=consumer1, args=(msg_queue, send_msg_queue)))

    for i in range(10):
        consumer2_process_list.append(Process(target=consumer2, args=(send_msg_queue,)))

    for producer_process in producer_process_list:
        producer_process.start()
    for consumer1_process in consumer1_process_list:
        consumer1_process.start()
    for consumer2_process in consumer2_process_list:
        consumer2_process.start()

    for producer_process in producer_process_list:
        producer_process.join()
    for consumer1_process in consumer1_process_list:
        consumer1_process.join()
    for consumer2_process in consumer2_process_list:
        consumer2_process.join()

