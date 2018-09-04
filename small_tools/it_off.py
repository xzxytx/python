#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
name： 				自动关机
create_time：     	2018/09/04
modify_time：     	2018/09/04
email:				time.yu@foxmail.com
"""
import os
import time


BIG_HOURS_STR = "18"  # 几点之后自动关机 注意：必须两位数字
BIG_DELAY_INT = 60  # 关机之前的延时， int类型

EQUAL_HOURS_STR = "08"  # 等于几点时关机
EQUAL_DELAY_INT = 3600  # 等于之前的延时


def t(m=60):
    for i in range(m+1):
        time.sleep(1)
        print("\r{}{}_{}秒后关机".format(' '*i, '>'*(m-i), m-i), end='')


def off_run():
	now_h = time.strftime("%H", time.localtime()) 
	count = None

	if now_h >= BIG_HOURS_STR:
		count = BIG_DELAY_INT
	elif EQUAL_HOURS_STR == now_h:
		count = EQUAL_DELAY_INT

	if count:
		t(count)
		#windowsϵͳ
		os.system("shutdown -s -t 0")  # 0秒之后关机
		#linuxϵͳ
		# os.system("poweroff")
	print(">>> 不符合条件不关机 4秒后结束")
	time.sleep(4)

if __name__ == '__main__':
	off_run()