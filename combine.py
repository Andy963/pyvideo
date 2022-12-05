#!/usr/bin/python
# coding:utf-8
import os

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


def list_video(video_path, exts=('.mp4', '.mkv')):
    """列出所有的音频"""
    for file in os.listdir(video_path):
        if file.endswith(tuple(exts)):
            yield os.path.join(video_path, file)


def combine_list(src_path, out_path):
    """将src目录下的文件合并成一个"""
    final_clips = []
    n = 0
    for file in list_video(src_path):
        print(file)
        final_clips.append(VideoFileClip(file))
    final_video = concatenate_videoclips(final_clips)
    out_path = f'./merged/{out_path}.mp4'
    final_video.write_videofile(out_path)


if __name__ == '__main__':
    combine_list('./videos', '蒋勋《美的沉思》中国文学史从唐诗到元曲')