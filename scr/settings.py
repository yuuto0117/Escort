import pygame
pygame.init()



# ==========================游戏窗口==========================

# 获取显示器信息
info = pygame.display.Info()
screen_width = info.current_w
screen_height = info.current_h

taskbar_height = 50  # 任务栏预估高度
titlebar_height = 30  # 窗口标题栏预估高度

# 设置窗口大小
window_width = screen_width
window_height = screen_height - taskbar_height - titlebar_height
# window_ratio = window_width / window_height
# print(window_width, window_height)

# 创建窗口
SCREEN = pygame.display.set_mode((2560, 1600), pygame.FULLSCREEN)
# (2560, 1600), pygame.FULLSCREEN       (window_width, window_height), pygame.RESIZABLE
# ==========================帧率==========================

FPS = 60

# ==========================字体==========================

# 黑体常规
font_path = './assets/fonts/simhei.ttf'

# ==========================XX==========================





