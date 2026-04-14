import pygame
from .scene import Scene
from .. import settings
from ..entitles import player
from ..entitles import enemy
from ..ui import button



class GameScene(Scene):
    def __init__(self):
        super().__init__()
        # 创建玩家精灵组
        self.player_group = pygame.sprite.Group()       # 创建组
        self.player = player.Player(settings.screen_width / 5, 750-184)       # 创建玩家
        self.player_group.add(self.player)              # 添加玩家进组

        # 创建敌人精灵组
        self.enemy_group = pygame.sprite.Group()
        self.enemy = enemy.Enemy(settings.screen_width / 5 * 4, 750-184, self.player)
        self.enemy_group.add(self.enemy)

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
                self.next_scene = GameScene()
            if self.button_2.handle_events(event):
                from .enter_scene import EnterGameScene
                self.next_scene = EnterGameScene()

            # 判断按键事件
            if event.type == pygame.KEYDOWN:
                # 按下Esc键，返回上一级
                if event.key == pygame.K_ESCAPE:
                    from .pre_game_scene import PreGameScene
                    self.next_scene = PreGameScene()


    def check_combat_collision(self):
        '''
        检测玩家挥砍与敌人碰撞
        '''
        # 碰撞检测返回字典
        hits = pygame.sprite.groupcollide(self.player.strike_group, self.enemy_group, False, False)

        for strike_sprite, hit_enemy_list in hits.items():
            for enemy_sprite in hit_enemy_list:
                if strike_sprite.register_hit(enemy_sprite):
                    enemy_sprite.take_damage()


    def check_collision(self):
        '''
        检测玩家与敌人碰撞
        '''
        if self.enemy.health.alive:

            # 像素级检测
            for enemy_sprite in self.enemy_group:
                if not hasattr(enemy_sprite, 'mask') or enemy_sprite.mask is None:
                    continue

                for player_sprite in self.player_group:
                    if not hasattr(player_sprite, 'mask') or player_sprite.mask is None:
                        continue

                    # 使用 collide_mask
                    if pygame.sprite.collide_mask(enemy_sprite, player_sprite):
                        player_sprite.check_take_damage()

            # 矩形检测
            # hits = pygame.sprite.groupcollide(self.enemy_group, self.player_group, False, False)
            #
            # for enemy_sprite, hit_player_list in hits.items():
            #     for player_sprite in hit_player_list:
            #         player_sprite.check_take_damage()


    def update(self, events):
        # 更新玩家
        self.player_group.update(events)
        self.enemy_group.update()
        # 检测战斗碰撞
        self.check_combat_collision()
        # 检测玩家与敌人碰撞
        self.check_collision()


    def draw(self, screen):
        # 覆盖背景
        screen.fill((88, 76, 76))

        # 简单绘制地面
        pygame.draw.line(screen, (0, 0, 0), (0, 750), (settings.screen_width, 750))


        '''
        # === 调试代码开始 ===
        # 绘制敌人碰撞框 (绿色)
        for enemy in self.enemy_group:
            pygame.draw.rect(screen, (0, 255, 0), enemy.rect, 2)

        # 绘制玩家碰撞框 (蓝色)
        for player in self.player_group:
            pygame.draw.rect(screen, (0, 0, 255), player.rect, 2)

        # 绘制挥砍碰撞框 (红色) - 这就是你可能看到的“残留”
        for strike in self.player.strike_group:
            pygame.draw.rect(screen, (255, 0, 0), strike.rect, 2)
        # === 调试代码结束 ===
        '''


        # 绘制玩家、敌人
        self.enemy_group.draw(screen)
        self.player_group.draw(screen)
        # 绘制玩家挥砍特效
        self.player.strike_group.draw(screen)

        # 绘制玩家生命值、体力
        if self.player.health.alive:
            pygame.draw.rect(screen, 'red', (100, 100, self.player.health.health * 2, 20))
            pygame.draw.rect(screen, 'green', (100, 130, self.player.health.thoughness * 5, 20))

        # 绘制敌人生命值
        pygame.draw.rect(screen, 'red', (settings.screen_width / 4, 900, self.enemy.health.health * 4, 20))

        # 玩家或敌人死亡时绘制按钮
        if not self.player.health.alive or not self.enemy.health.alive:
            self.button_1.draw(screen)
            self.button_2.draw(screen)

