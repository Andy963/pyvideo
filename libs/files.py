#!/usr/bin/python
# coding:utf-8
import os
import random


def list_file(src_path='audio'):
    """列出所有的文件"""
    fs = []
    for file in os.listdir(src_path):
        fs.append(os.path.join(src_path, file))
    print(f"共找到{len(fs)}个文件")
    return fs


def save_filelist(src_path):
    """保存文件列表"""
    files = []  # 文件列表
    for file in os.listdir(src_path):
        files.append(os.path.join(src_path, file))
    data = 'file \'' + '\'\nfile \''.join(files) + '\''
    f_name = 'list.txt'
    with open(f_name, 'w', encoding='utf-8') as f:
        f.write(data)
    return files


def random_mask(face_path='mask'):
    """随机选择一张封面"""
    files = list_file(face_path)
    rs = random.choice(files)
    print('随机选择的封面为：', rs)
    return rs
