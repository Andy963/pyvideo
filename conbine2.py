#!/usr/bin/python
# coding:utf-8

from moviepy.editor import VideoFileClip, concatenate_videoclips


def combine_2_video(v1_path, v2_path, out_path, v1_start=0, v1_end=0, v2_start=0, v2_end=0):
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
    final_clip.write_videofile(out_path)
