import pygame
from ..settings import font_path

class Scene:

    def __init__(self):
        self.next_scene = None
        # 各场景通用字体测试
        self.font = pygame.font.Font(font_path, 36)

    def handle_events(self, events):
        pass

    def update(self, events):
        pass

    def draw(self, screen):
        pass




