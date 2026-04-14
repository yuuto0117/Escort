import pygame
from .scene import Scene
from .. import settings
from ..entitles import player1, player2
from ..ui import button



class PrePVPScene(Scene):
    def __init__(self):
        super().__init__()
        # 创建玩家1精灵组
        self.player1_group = pygame.sprite.Group()       # 创建组
        self.player1 = player1.Player1(settings.screen_width / 5, 750-184)       # 创建玩家
        self.player1_group.add(self.player1)              # 添加玩家进组

        # 创建玩家2精灵组
        self.player2_group = pygame.sprite.Group()  # 创建组
        self.player2 = player2.Player2(settings.screen_width / 5 * 4, 750 - 184)  # 创建玩家
        self.player2_group.add(self.player2)

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
                from .PVP_scene import PVPScene
                self.next_scene = PVPScene()
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
        self.player1_group.update(events)
        self.player2_group.update(events)


    def draw(self, screen):
        # 覆盖、绘制背景
        screen.fill((88, 76, 76))
        Instructions = pygame.image.load('assets/images/screen2.png')
        screen.blit(Instructions, (0, 0))

        # 文本
        text = self.font.render('switch to English input method', True, (0, 0, 0))
        screen.blit(text, (settings.screen_width / 5 * 3, settings.screen_height / 4 + 180))

        # 简单绘制地面
        pygame.draw.line(screen, (0, 0, 0), (0, 750), (settings.screen_width, 750))

        # 绘制按钮
        self.button_1.draw(screen)
        self.button_2.draw(screen)

        # 绘制玩家
        self.player1_group.draw(screen)
        self.player1.strike_group.draw(screen)

        self.player2_group.draw(screen)
        self.player2.strike_group.draw(screen)

        # 玩家1名称
        text1 = self.font.render(self.player1.name, True, 'red')
        # 绘制于玩家头顶
        screen.blit(text1, (self.player1.rect.x, self.player1.rect.y - 50))

        # 玩家2名称
        text2 = self.font.render(self.player2.name, True, 'blue')
        # 绘制于玩家头顶
        screen.blit(text2, (self.player2.rect.x, self.player2.rect.y - 50))





