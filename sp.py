#!/usr/bin/python
# coding:utf-8
from moviepy.editor import VideoFileClip


def split_video(v_path, start=0, end=0, out_path=None, eq2=False):
    """将视频切片
    :param v_path: 源视频地址
    :param start: 视频开始时间
    :param eq2 : 是否2等分
    :param end  : 视频结束时间
    :param out_path: 输出视频地址
    :param eq2 : 是否2等分
    """
    v = VideoFileClip(v_path)
    if start:
        v = v.subclip(start, v.duration)
    if end:
        v = v.subclip(0, end)
    if eq2:
        v1 = v.subclip(0, v.duration / 2)
        v2 = v.subclip(v.duration / 2, v.duration)
        v1.write_videofile(out_path + '1.mp4')
        v2.write_videofile(out_path + '2.mp4')
        return
    v.write_videofile(out_path + '.mp4')


if __name__ == '__main__':
    split_video('d:/4k/Autumn forest 2k 20221130.mp4', out_path='d:/4k/Autumn_forrest', eq2=True)