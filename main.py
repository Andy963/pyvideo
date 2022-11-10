#!/usr/bin/python
# coding:utf-8
import argparse
import os

from moviepy.editor import AudioFileClip, ImageClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.video.io.VideoFileClip import VideoFileClip

base_dir = os.path.dirname(os.path.abspath(__file__))
default_face_path = os.path.join(base_dir, 'face', 'face.jpg')
default_audio_path = os.path.join(base_dir, 'audio')
default_video_path = os.path.join(base_dir, 'video')
default_logo_path = os.path.join(base_dir, 'face', 'logo.png')


def add_static_image_to_audio(image_path, audio_path, output_path):
    """Create and save a video file to `output_path` after
    combining a static image that is located in `image_path`
    with an audio file in `audio_path`"""
    # create the audio clip object
    audio_clip = AudioFileClip(audio_path)
    # create the image clip object
    image_clip = ImageClip(image_path)
    # use set_audio method from image clip to combine the audio with the image
    video_clip = image_clip.set_audio(audio_clip)
    # specify the duration of the new clip to be the duration of the audio clip
    video_clip.duration = audio_clip.duration
    # set the FPS to 1
    video_clip.fps = 1
    # write the resuling video clip
    video_clip.write_videofile(output_path)


def list_audio(audio_path, exts=('.mp3', '.wav', '.wma', 'm4a')):
    """列出所有的音频"""
    for file in os.listdir(audio_path):
        if file.endswith(tuple(exts)):
            yield os.path.join(audio_path, file)


def get_file_name(path):
    """获取文件名"""
    return os.path.splitext(os.path.basename(path))


def get_output_name(name, ext='mp4'):
    """获取输出文件名"""
    return name + '.' + ext


def add_watermark(video_path, logo_path=default_logo_path):
    """添加水印"""
    video = VideoFileClip(video_path)
    logo = (ImageClip(logo_path)
            .set_duration(video.duration)
            .resize(height=50)  # if you need to resize...
            .margin(right=8, top=8, opacity=0)  # (optional) logo-border padding
            .set_pos(("right", "top")))
    compos = CompositeVideoClip([video, logo])
    compos.write_videofile(video_path)


def main(args):
    """主要流程"""
    for audio_path in list_audio(args.audio):
        name, _ = get_file_name(audio_path)
        output_path = os.path.join(args.video, get_output_name(name))
        add_static_image_to_audio(args.image, audio_path, output_path)
    print("finish")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="将图片和音频生成视频")
    parser.add_argument("-image", help="The image path，default is ./face.jpg", nargs='?', const=1,
                        default=default_face_path)
    parser.add_argument("-audio", help="The audio path, default is ./audio", nargs='?', const=1,
                        default=default_audio_path)
    parser.add_argument("-video", help="The output video file path, default is ./video", nargs='?', const=1,
                        default=default_video_path)
    args = parser.parse_args()
    main(args)
