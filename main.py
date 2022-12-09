#!/usr/bin/python
# coding:utf-8
import argparse
import os

from libs.audios import split_audio, add_static_image_to_audio, get_audio_from_video

base_dir = os.path.dirname(os.path.abspath(__file__))
default_face_path = os.path.join(base_dir, 'face', 'face.jpg')
default_audio_path = os.path.join(base_dir, 'audio')
default_video_path = os.path.join(base_dir, 'videos')
default_logo_path = os.path.join(base_dir, 'face', 'logo.png')


def main():
    # 从视频提取音频
    src_path = './绝代双骄第12话.mp4'
    out_path = './绝代双骄第12话.wav'
    start = '3:08'
    end = '17:42'

    # get_audio_from_video(src_path, out_path)
    # # 分割音频
    name, ext = os.path.splitext(out_path)
    out_path_ = f'{name}_1{ext}'
    # split_audio(out_path, out_path_, start=start, end=end)
    v_path = f'绝代双骄第12话.mp4'
    mask_path = '12.jpg'
    human_voice = '绝代双骄第12话_1_Vocals.wav'
    add_static_image_to_audio(mask_path, human_voice, v_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="将图片和音频生成视频")
    parser.add_argument("-image", help="The image path，default is ./face.jpg", nargs='?', const=1,
                        default=default_face_path)
    parser.add_argument("-audio", help="The audio path, default is ./audio", nargs='?', const=1,
                        default=default_audio_path)
    parser.add_argument("-video", help="The output video file path, default is ./videos", nargs='?', const=1,
                        default=default_video_path)
    args = parser.parse_args()
    main()
