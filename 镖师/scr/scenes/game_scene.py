import pygame
from .scene import Scene
from .. import settings
from ..entitles import player


class GameScene(Scene):
    def __init__(self):
        super().__init__()
        # 创建玩家精灵组
        self.player_group = pygame.sprite.Group()       # 创建组
        self.player = player.Player(settings.screen_width / 2, 750-184)       # 创建玩家
        self.player_group.add(self.player)              # 添加玩家进组


    def handle_events(self, events):
        for event in events:
            # 判断按键事件
            if event.type == pygame.KEYDOWN:
                # 按下Esc键，返回菜单
                if event.key == pygame.K_ESCAPE:
                    from .menu_scene import MenuScene
                    self.next_scene = MenuScene()

        # 更新玩家
        self.player_group.update(events)


    def draw(self, screen):
        # 背景白色
        screen.fill((255, 255, 255))
        # 文本黑色
        text = self.font.render('Game Scene, Press Esc to back to Menu', True, (0, 0, 0))
        screen.blit(text, (200, 250))

        # 简单绘制地面
        pygame.draw.line(screen, (0, 0, 0), (0, 750), (settings.screen_width, 750))

        # 绘制玩家
        self.player_group.draw(screen)


