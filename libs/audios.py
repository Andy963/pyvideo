#!/usr/bin/python
# coding:utf-8
import os

from moviepy.audio.AudioClip import CompositeAudioClip, concatenate_audioclips
from moviepy.audio.fx.all import audio_loop
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.VideoClip import ImageClip
from moviepy.video.io.VideoFileClip import VideoFileClip

from libs import LOG, timer, CPU_COUNT, cal_sec
from libs.files import save_filelist, random_mask


def transcode_audio(src_path, dst_ext='mp3'):
    """
    转码音频
    """
    if src_path.endswith('.mp3'):
        print('已经是mp3格式，无需转码')
        return
    a = AudioFileClip(src_path)
    p, src_ext = os.path.splitext(src_path)
    dst_path = f"{p}.{dst_ext}"
    dst_path = dst_path.replace(' ', '')
    dst_path = dst_path.replace('-', '')
    print(f'{src_path} ==> {dst_path}')
    a.write_audiofile(dst_path, logger=LOG)
    a.close()


def get_audio_from_video(v_path, a_path=None):
    """获取视频的音频"""
    v = VideoFileClip(v_path)
    if not a_path:
        name = os.path.splitext(v_path)[0]
        f_name = f"{name}.wav"
        a_path = os.path.join(os.path.dirname(v_path), f_name)
    v.audio.write_audiofile(a_path, logger=LOG)
    v.close


def combine_audios(src_path, out_path):
    """
    合并音频
    """
    files = save_filelist(src_path)
    # try:
    #     cmd = f'ffmpeg -f concat -safe 0 -i list.txt -c copy {out_path}'
    #     os.system(cmd)
    # except Exception as e:
    av = []
    for a in files:
        av.append(AudioFileClip(a))
    fvs = concatenate_audioclips(av)
    fvs.write_audiofile(out_path, logger=LOG)


def add_bgm(
        v_path, ms_path,
        out_path=None,
        v_start=0,
        v_end=None,
        ms_start=0,
        ms_end=None,
        v_has_ms=False,
        loop=True):
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
    :param loop: 是否循环背景音乐
    """
    video = VideoFileClip(v_path)
    for i in [v_start, v_end, ms_start, ms_end]:
        if isinstance(i, str):
            i = cal_sec(i)
    if v_start:
        video = video.subclip(v_start, video.duration)
    if v_end:
        video = video.subclip(0, v_end)
    bgm = AudioFileClip(ms_path)
    if ms_start:
        bgm = bgm.subclip(ms_start, bgm.duration)
    if ms_end:
        bgm = bgm.subclip(0, ms_end)
    # 视频本身无背景音乐，直接设置背景音乐
    if loop:
        bgm = audio_loop(bgm, duration=video.duration)
    if not v_has_ms:
        video = video.set_audio(bgm)
    # 视频本身是有音乐背景的，则合并两者
    else:
        com_audio = CompositeAudioClip([video.audio, bgm])
        video.set_audio(com_audio)
    if not out_path:
        name, ext = os.path.splitext(v_path)
        out_path = f"{name}_bgm{ext}"
    video.write_videofile(out_path)
    video.close()


@timer
def add_static_image_to_audio(audio_path, output_path, image_path=None, ffmpeg_params=None):
    """Create and save a video file to `output_path` after
    combining a static image that is located in `image_path`
    with an audio file in `audio_path`"""
    # create the audio clip object
    audio_clip = AudioFileClip(audio_path)
    # create the image clip object
    if not image_path:
        image_path = random_mask()
    image_clip = ImageClip(image_path)
    # use set_audio method from image clip to combine the audio with the image
    video_clip = image_clip.set_audio(audio_clip)
    # specify the duration of the new clip to be the duration of the audio clip
    video_clip.duration = audio_clip.duration
    # set the FPS to 1
    video_clip.fps = 1
    # write the resuling video clip
    video_clip.write_videofile(output_path, preset='ultrafast', threads=CPU_COUNT, logger=LOG,
                               ffmpeg_params=ffmpeg_params)
    video_clip.close()


def split_audio(src_path, dst_path, start=None, end=None):
    """
    分割音频
    """
    try:
        cmd = f'ffmpeg -i "{src_path}" -acodec copy -ss {start} -to {end} {dst_path}'
        os.system(cmd)
    except Exception as e:
        print(e)
        a = AudioFileClip(src_path)
        if start:
            start = cal_sec(start)
        if end:
            end = cal_sec(end)
        if start and not end:
            a = a.subclip(start, a.duration)
        if end and not start:
            if end > a.duration:
                end = a.duration
            a = a.subclip(0, end)
        if start and end:
            a = a.subclip(start, end)
        a.write_audiofile(dst_path, logger=LOG)
        a.close()
