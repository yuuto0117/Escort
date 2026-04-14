import pygame
from .scene import Scene
from .. import settings
from ..entitles import player
from ..ui import button



class PreGameScene(Scene):
    def __init__(self):
        super().__init__()
        # 创建玩家精灵组
        self.player_group = pygame.sprite.Group()       # 创建组
        self.player = player.Player(settings.screen_width / 5, 750-184)       # 创建玩家
        self.player_group.add(self.player)              # 添加玩家进组

        # 创建按钮实例
        self.button_1 = button.Button(
            settings.screen_width / 5 * 4,
            settings.screen_height / 4,
            200,
            50,
            'FIGHT',
            (255, 255, 255),  # 按钮默认白色
            (192, 192, 192),  # 按钮悬停灰色
            self.font,
            (0, 0, 0))

        self.button_2 = button.Button(
            settings.screen_width / 5 * 4,
            settings.screen_height / 4 + 75,
            200,
            50,
            'BACK',
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
            if self.button_2.handle_events(event):
                from .enter_scene import EnterGameScene
                self.next_scene = EnterGameScene()

            if event.type == pygame.KEYDOWN:
                # 按下Esc键，返回初始界面
                if event.key == pygame.K_ESCAPE:
                    from .enter_scene import EnterGameScene
                    self.next_scene = EnterGameScene()


    def update(self, events):
        # 更新玩家
        self.player_group.update(events)


    def draw(self, screen):
        # 覆盖、绘制背景
        screen.fill((88, 76, 76))
        Instructions = pygame.image.load('assets/images/screen.png')
        screen.blit(Instructions, (0, 0))

        # 文本
        text = self.font.render('switch to English input method', True, (0, 0, 0))
        screen.blit(text, (settings.screen_width / 5 * 3, settings.screen_height / 4 + 150))

        # 简单绘制地面
        pygame.draw.line(screen, (0, 0, 0), (0, 750), (settings.screen_width, 750))

        # 绘制按钮
        self.button_1.draw(screen)
        self.button_2.draw(screen)

        # 绘制玩家
        self.player_group.draw(screen)
        self.player.strike_group.draw(screen)

















