import glob
import os
import random
import pygame


def get_random_music():
    """
    获取 assets/sounds 目录下的随机 mp3 文件路径
    """
    # 获取当前脚本所在的目录 (scr/components/)
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # 向上两级找到项目根目录，然后进入 assets/sounds

    project_root = os.path.join(current_dir, '..', '..')
    sound_dir = os.path.join(project_root, 'assets', 'sounds')

    # 规范化路径
    sound_dir = os.path.normpath(sound_dir)

    # 获取所有 mp3 文件
    mp3_files = glob.glob(os.path.join(sound_dir, '*.mp3'))

    if not mp3_files:
        raise FileNotFoundError(f"在目录 {sound_dir} 中未找到任何 .mp3 文件")

    # 随机选择一个
    selected_music = random.choice(mp3_files)
    return selected_music


def play_music():
    pygame.init()
    a = get_random_music()
    sound = pygame.mixer.Sound(a)
    sound.play()





