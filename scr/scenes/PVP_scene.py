import pygame
from .scene import Scene
from .. import settings
from ..entitles import player1, player2
from ..ui import button



class PVPScene(Scene):
    def __init__(self):
        super().__init__()
        # 创建玩家1精灵组
        self.player1_group = pygame.sprite.Group()  # 创建组
        self.player1 = player1.Player1(settings.screen_width / 5, 750 - 184)  # 创建玩家
        self.player1_group.add(self.player1)  # 添加玩家进组

        # 创建玩家2精灵组
        self.player2_group = pygame.sprite.Group()  # 创建组
        self.player2 = player2.Player2(settings.screen_width / 5 * 4, 750 - 184)  # 创建玩家
        self.player2_group.add(self.player2)

        # 创建again、back按钮
        self.button_1 = button.Button(
            settings.screen_width / 5 * 4,
            settings.screen_height / 4,
            200,
            50,
            'AGAIN',
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
            # 按钮
            if self.button_1.handle_events(event):
                self.next_scene = PVPScene()
            if self.button_2.handle_events(event):
                from .enter_scene import EnterGameScene
                self.next_scene = EnterGameScene()

            # 判断按键事件
            if event.type == pygame.KEYDOWN:
                # 按下Esc键，返回上一级
                if event.key == pygame.K_ESCAPE:
                    from .pre_PVP_scene import PrePVPScene
                    self.next_scene = PrePVPScene()


    def P1_check_combat_collision(self):
        '''
        检测玩家1挥砍与敌人碰撞
        '''
        # 碰撞检测返回字典
        hits = pygame.sprite.groupcollide(self.player1.strike_group, self.player2_group, False, False)

        for strike_sprite, hit_p2_list in hits.items():
            for p2_sprite in hit_p2_list:
                if strike_sprite.register_hit(p2_sprite):
                    p2_sprite.check_take_damage()

    def P2_check_combat_collision(self):
        '''
        检测玩家2挥砍与敌人碰撞
        '''
        # 碰撞检测返回字典
        hits = pygame.sprite.groupcollide(self.player2.strike_group, self.player1_group, False, False)

        for strike_sprite, hit_p1_list in hits.items():
            for p1_sprite in hit_p1_list:
                if strike_sprite.register_hit(p1_sprite):
                    p1_sprite.check_take_damage()





    def update(self, events):
        # 更新玩家
        self.player1_group.update(events)
        self.player2_group.update(events)

        # 检测战斗碰撞
        self.P1_check_combat_collision()
        self.P2_check_combat_collision()



    def draw(self, screen):
        # 覆盖背景
        screen.fill((88, 76, 76))

        # 简单绘制地面
        pygame.draw.line(screen, (0, 0, 0), (0, 750), (settings.screen_width, 750))


        # 绘制玩家
        self.player1_group.draw(screen)
        self.player2_group.draw(screen)
        # 绘制玩家挥砍特效
        self.player1.strike_group.draw(screen)
        self.player2.strike_group.draw(screen)

        # 绘制玩家1生命值、体力、名字
        if self.player1.health.alive:
            pygame.draw.rect(screen, 'red', (100, 100, self.player1.health.health * 2, 20))
            pygame.draw.rect(screen, 'green', (100, 130, self.player1.health.thoughness * 5, 20))

            # 玩家1名称
            text1 = self.font.render(self.player1.name, True, 'red')
            # 绘制于玩家头顶
            screen.blit(text1, (self.player1.rect.x, self.player1.rect.y - 50))


        # 绘制玩家2生命值、体力、名字
        if self.player2.health.alive:
            pygame.draw.rect(screen, 'red', (1400, 100, self.player2.health.health * 2, 20))
            pygame.draw.rect(screen, 'green', (1400, 130, self.player2.health.thoughness * 5, 20))

            # 玩家2名称
            text2 = self.font.render(self.player2.name, True, 'blue')
            # 绘制于玩家头顶
            screen.blit(text2, (self.player2.rect.x, self.player2.rect.y - 50))


        # 玩家死亡时绘制按钮
        if not self.player1.health.alive or not self.player2.health.alive:
            self.button_1.draw(screen)
            self.button_2.draw(screen)




