import pygame
from .scene import Scene
from ..ui import button
from .. import settings



class MenuScene(Scene):
    def __init__(self):
        super().__init__()

        # 创建按钮实例
        self.button_1 = button.Button(
            settings.screen_width / 4 ,
            settings.screen_height / 2,
            300,
            50,
            'BACK TO TITLE',
            (255, 255, 255),  # 按钮默认白色
            (192, 192, 192),  # 按钮悬停灰色
            self.font,
            (0, 0, 0))



    def handle_events(self, events):
        for event in events:
            # 按键事件
            if event.type == pygame.KEYDOWN:
                # 再次按Esc键，返回游戏界面
                if event.key == pygame.K_ESCAPE:
                    from .game_scene import GameScene
                    self.next_scene = GameScene()
            # 按钮事件
            # 返回标题界面
            elif self.button_1.handle_events(event):
                from .enter_scene import EnterGameScene
                self.next_scene = EnterGameScene()




    def draw(self, screen):
        # 修改为 RGB 元组 (白色)
        screen.fill((255, 255, 255))
        # 修改为 RGB 元组 (白色)
        text = self.font.render('Menu, Press Esc back to Game', True, (0, 0, 0))
        screen.blit(text, (200, 250))
        # 绘制按钮
        self.button_1.draw(screen)



