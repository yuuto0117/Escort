import pygame, sys
from .scene import Scene
from ..ui import button
from .. import settings     # settings设置按钮位置


class EnterGameScene(Scene):
    def __init__(self):
        super().__init__()

        # 创建按钮实例
        self.button_1 = button.Button(
            settings.screen_width / 2 - 100,
            settings.screen_height / 2,
            200,
            50,
            'NEW GAME',
            (255, 255, 255),    # 按钮默认白色
            (192, 192, 192),     # 按钮悬停灰色
            self.font,
            (0, 0, 0))

        self.button_2 = button.Button(
            settings.screen_width / 2 - 100,
            settings.screen_height / 2 + 75,
            200,
            50,
            'SETTINGS',
            (255, 255, 255),  # 按钮默认白色
            (192, 192, 192),  # 按钮悬停灰色
            self.font,
            (0, 0, 0))

        self.button_3 = button.Button(
            settings.screen_width / 2 - 100,
            settings.screen_height / 2 + 150,
            200,
            50,
            'QUIT GAME',
            (255, 255, 255),  # 按钮默认白色
            (192, 192, 192),  # 按钮悬停灰色
            self.font,
            (0, 0, 0))



    def handle_events(self, events):
        for event in events:
            # 进入游戏界面
            if self.button_1.handle_events(event):
                from .game_scene import GameScene
                self.next_scene = GameScene()
            # 按下Esc进入菜单界面
            elif self.button_2.handle_events(event):
                from .menu_scene import MenuScene
                self.next_scene = MenuScene()
            # 退出游戏按钮
            elif self.button_3.handle_events(event):
                pygame.quit()
                sys.exit()



    def draw(self, screen):
        # 屏幕绿色
        screen.fill((255, 255, 255))
        # 绘制按钮
        self.button_1.draw(screen)
        self.button_2.draw(screen)
        self.button_3.draw(screen)

