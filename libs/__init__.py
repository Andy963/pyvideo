#!/usr/bin/python
# coding:utf-8
import os
import subprocess
import time
from functools import wraps

from proglog import default_bar_logger

CPU_COUNT =  2
LOG = default_bar_logger('bar', bars=None, ignored_bars=None, logged_bars='all',
                         min_time_interval=5, ignore_bars_under=0)


def timer(func):
    @wraps(func)
    def inner(*args, **kwargs):
        start = time.time()
        func(*args, **kwargs)
        end = time.time()
        print(f'耗时：{end - start:.2f}s')

    return inner


def cal_sec(t_str: str):
    """将时间字符串转换为秒数
    :param t_str: 时间字符串，格式为：00:00:00.000
    """
    h, m, s = 0, 0, 0
    try:
        h, m, s = t_str.split(':')
    except ValueError:
        m, s = t_str.split(':')
    return int(h) * 3600 + int(m) * 60 + float(s)

def get_duration(input_video):
    cmd = ["ffprobe", "-i", input_video, "-show_entries", "format=duration",
           "-v", "quiet", "-sexagesimal", "-of", "csv=p=0"]
    return subprocess.check_output(cmd).decode("utf-8").strip()