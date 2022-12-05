#!/usr/bin/python
# coding:utf-8

from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip


def add_bg_ms(v_path, ms_path, out_path, v_start=0, v_end=None, ms_start=0, ms_end=None, v_has_ms=False):
    """
    给视频添加背景音乐
    :param v_path: 视频路径
    :param ms_path: 背景音乐路径
    :param out_path: 输入路径
    :param v_start: 视频开始时间
    :param v_end: 视频结束时间
    :param ms_start: 背景音乐开始时间
    :param ms_end: 背景音乐结束时间
    :param v_has_ms: 视频是否有背景音乐
    """
    video = VideoFileClip(v_path)
    if v_start:
        video = video.subclip(v_start, video.duration)
    if v_end:
        video = video.subclip(0, v_end)
    bg_ms = AudioFileClip(ms_path)
    if ms_start:
        bg_ms = bg_ms.subclip(ms_start, bg_ms.duration)
    if ms_end:
        bg_ms = bg_ms.subclip(0, ms_end)
    # 视频本身无背景音乐，直接设置背景音乐
    if not v_has_ms:
        video = video.set_audio(bg_ms)
    # 视频本身是有音乐背景的，则合并两者
    else:
        com_audio = CompositeAudioClip([video.audio, bg_ms])
        video.set_audio(com_audio)
    video.write_videofile(out_path)


if __name__ == '__main__':
    add_bg_ms('./62.mp4', './64.wav', './65.mp4')