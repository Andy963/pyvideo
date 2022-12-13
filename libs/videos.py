#!/usr/bin/python
# coding:utf-8
import os

from moviepy.video.VideoClip import ImageClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.video.compositing.concatenate import concatenate_videoclips
from moviepy.video.io.VideoFileClip import VideoFileClip

from libs import timer, LOG, CPU_COUNT, cal_sec
from libs.files import list_file


def rm_audio_from_video(v_path: str, output_path: str = './'):
    """
    去除视频中的音频
    :param v_path: 源视频路径
    :param output_path: 输入视频路径，默认当前目录
    """
    try:
        cmd = f'ffmpeg -i {v_path} -vcodec copy -an {output_path}'
        os.system(cmd)
    except Exception as e:
        print(e)
        v = VideoFileClip(v_path)
        v_ = v.without_audio()
        v_.write_videofile(output_path, preset='ultrafast', logger=LOG)
        v.close()
        v_.close()


def split_video(v_path, out_path=None, start=0, end=0, eq2=False):
    """将视频切片
    :param v_path: 源视频地址
    :param start: 视频开始时间
    :param eq2 : 是否2等分
    :param end  : 视频结束时间
    :param out_path: 输出视频地址
    :param eq2 : 是否2等分
    """
    if start and isinstance(start, str):
        start = cal_sec(start)
    if end and isinstance(end, str):
        end = cal_sec(end)
    v = VideoFileClip(v_path)
    if start and not end:
        v = v.subclip(start, v.duration)
    elif end and not start:
        if end > v.duration:
            end = v.duration
        v = v.subclip(0, end)
    elif start and end:
        if end > v.duration:
            end = v.duration
        v = v.subclip(start, end)
    if eq2:
        v1 = v.subclip(0, v.duration / 2)
        v2 = v.subclip(v.duration / 2, v.duration)
        v1.write_videofile(out_path + '1.mp4', threads=CPU_COUNT, preset='ultrafast')
        v2.write_videofile(out_path + '2.mp4', threads=CPU_COUNT, preset='ultrafast')
        return
    v.write_videofile(out_path + '.mp4', threads=CPU_COUNT, preset='ultrafast')
    v.close()


@timer
def split_video_by_ffmpeg(v_path, out_path=None, start=0, end=0):
    """使用ffmpeg切割视频
    ffmpeg -ss 0:1:30 -t 0:0:20 -i input.mp4 -vcodec copy -acodec copy output.mp4
    -ss 开始时间; -t 持续时间
    """
    cmd = f"ffmpeg -ss {start} -t {end} -i {v_path} -vcodec copy -acodec copy {out_path}"
    print(cmd)
    os.system(cmd)


@timer
def combine_videos(src_path='videos', out_path=None, method="compose"):
    """将src目录下的文件合并成一个"""
    final_clips = []
    print('读取文件:')
    F = True
    for file in list_file(src_path):
        print(file)
        if F and not out_path:
            name, _ = os.path.splitext(os.path.basename(file))
            out_path = f"{name}"
            F = False
        final_clips.append(VideoFileClip(file))
    print(f'读取完成，共{len(final_clips)}个文件，开始合成:')
    final_video = concatenate_videoclips(final_clips, method=method)
    if '全集' not in out_path:
        out_path = f'{out_path}全集'
    out_path = f'./merged/{out_path}.mp4'
    final_video.write_videofile(out_path, preset='ultrafast', threads=CPU_COUNT, logger=LOG)


@timer
def combine_videos_by_ffmpeg(video_path='videos', out_path='全集.mp4', cuda=False):
    files = []  # 文件列表
    for file in os.listdir(video_path):
        files.append(os.path.join(video_path, file))
    data = 'file \'' + '\'\nfile \''.join(files) + '\''
    f_name = 'list.txt'
    out_path = os.path.join('merged', out_path)
    with open(f_name, 'w', encoding='utf-8') as f:
        f.write(data)
    if cuda:
        cmd = f'ffmpeg -f concat -safe 0 -i {f_name} -shortest  -vcodec h264_nvenc  -threads 2 {out_path} -y'
    else:
        cmd = f'ffmpeg -f concat -safe 0  -i {f_name} -shortest -c copy {out_path} -y'
    print(cmd)
    os.system(cmd)
    os.remove(f_name)


def add_watermark(video_path, logo_path):
    """添加水印"""
    video = VideoFileClip(video_path)
    logo = (ImageClip(logo_path)
            .set_duration(video.duration)
            .resize(height=50)  # if you need to resize...
            .margin(right=8, top=8, opacity=0)  # (optional) logo-border padding
            .set_pos(("right", "top")))
    compos = CompositeVideoClip([video, logo])
    compos.write_videofile(video_path, preset='ultrafast', threads=CPU_COUNT, logger=LOG)
    compos.close()
