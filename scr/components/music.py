import os
import sys
import glob
import random
import pygame

def get_random_music():
    """获取assets/sounds目录下的随机mp3文件路径"""

    # 判断是否是打包后的环境
    if getattr(sys, 'frozen', False):
        # 打包后的路径
        base_path = sys._MEIPASS
    else:
        # 开发时的路径：从当前文件向上两级到项目根目录
        current_dir = os.path.dirname(os.path.abspath(__file__))
        base_path = os.path.dirname(os.path.dirname(current_dir))  # 向上两级

    # 构建 sounds 目录路径
    sound_dir = os.path.join(base_path, 'assets', 'sounds')
    sound_dir = os.path.normpath(sound_dir)

    # 获取所有mp3文件
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





