#!/usr/bin/python
# coding:utf-8
from moviepy.video.io.VideoFileClip import VideoFileClip


def rm_audio(v_path: str, output_path: str = './'):
    """
    去除视频中的音频
    :param v_path: 源视频路径
    :param output_path: 输入视频路径，默认当前目录
    """
    v = VideoFileClip(v_path)
    v_ = v.without_audio()
    v_.write_videofile(output_path)

def get_audio(v_path, out_path):
    """
    获取视频中的音频
    :param v_path: 源视频路径
    :param out_path: 输出音频路径
    """
    v = VideoFileClip(v_path)
    audio = v.audio
    v.audio.write_audiofile(out_path)

if __name__ == '__main__':
    # rm_audio('./63.mkv','./63.mp4')
    get_audio('./63.mkv', './63.mp3')