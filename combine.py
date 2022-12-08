#!/usr/bin/python
# coding:utf-8
import os
import time
from functools import wraps

from moviepy.editor import VideoFileClip, concatenate_videoclips

CPU_COUNT = os.cpu_count()


def combine_2_video(v1_path,
                    v2_path,
                    out_path,
                    v1_start=0,
                    v1_end=0,
                    v2_start=0,
                    v2_end=0):
    """
    合并两个不同视频
    :param v1_path: 视频1路径
    :param v2_path: 视频2路径
    :param out_path: 输出路径
    :param v1_start: 视频1开始时间
    :param v1_end: 视频1结束时间
    :param v2_start: 视频2开始时间
    :param v2_end: 视频2结束时间
    """
    v1 = VideoFileClip(v1_path)
    if v1_start:
        v1 = v1.subclip(v1_start, v1.duration)
    if v1_end:
        v1 = v1.subclip(0, v1_end)
    v2 = VideoFileClip(v2_path)
    if v2_start:
        v2 = v2.subclip(v2_start, v2.duration)
    if v2_end:
        v2 = v2.subclip(0, v2_end)
    final_clip = concatenate_videoclips([v1, v2])
    final_clip.write_videofile(out_path, threads=CPU_COUNT, logger=None)
    final_clip.close()


def list_video(video_path, exts=('.mp4', '.mkv')):
    """列出所有的音频"""
    for file in os.listdir(video_path):
        if file.endswith(tuple(exts)):
            yield os.path.join(video_path, file)


def timer(func):
    @wraps(func)
    def inner(*args, **kwargs):
        start = time.time()
        func(*args, **kwargs)
        end = time.time()
        print(f'耗时：{end - start:.2f}s')

    return inner


@timer
def combine_list(src_path='videos', out_path=None):
    """将src目录下的文件合并成一个"""
    final_clips = []
    print('读取文件:')
    F = True
    for file in list_video(src_path):
        print(file)
        if F and not out_path:
            name, _ = os.path.splitext(os.path.basename(file))
            out_path = f"{name}_合集"
            F = False
        final_clips.append(VideoFileClip(file))
    print(f'读取完成，共{len(final_clips)}个文件，开始合成:')
    final_video = concatenate_videoclips(final_clips)
    out_path = f'./merged/{out_path}.mp4'
    final_video.write_videofile(out_path, preset='ultrafast', threads=CPU_COUNT, logger=None)


if __name__ == '__main__':
    combine_list(out_path='')
