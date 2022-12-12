#!/usr/bin/python
# coding:utf-8
import os


def list_file(src_path='audio'):
    """列出所有的文件"""
    fs = []
    print(f"开始遍历文件：")
    for file in os.listdir(src_path):
        fs.append(os.path.join(src_path, file))
    print(f"共找到{len(fs)}个文件.顺序为：")
    for i, f in enumerate(fs, start=1):
        print(f"{i}. {f}")
    return fs
