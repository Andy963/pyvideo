#!/usr/bin/python
# coding:utf-8
import os


def list_file(src_path='audio'):
    """列出所有的文件"""
    fs = []
    print(f"开始遍历文件：")
    for i, file in enumerate(os.listdir(src_path), start=1):
        print(f"{i}. {file}")
        fs.append(os.path.join(src_path, file))
    print(f"共找到{len(fs)}个文件.")
    return fs
