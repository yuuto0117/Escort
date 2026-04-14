import pygame
from ..components import physics
from ..components import animation
from ..components import health
from ..components import music
import random




# 状态持续时间
IDLE_DURATION_MIN = 120
IDLE_DURATION_MAX = 180
RUSH_DURATION = 90



class State:
    def __init__(self, enemy, facing):
        self.enemy = enemy
        self.facing = facing
        self.animation = None
        self.music = music.play_music()


    def enter(self):
        '''进入游戏时调用，用于初始化动画或重置变量'''
        pass

    def exit(self):
        '''退出状态时调用'''
        pass


    def update(self):
        '''每帧更新逻辑，物理与动画帧等'''
        if self.animation:
            self.animation.update()



class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, player=None):
        super().__init__()
        # 初始化图片
        self.image = pygame.image.load('assets/images/Enemy/IDLE.png').convert_alpha()

        # 朝向
        self.facing = 'L'

        # 初始状态
        self.state = IdleState(self, 'L')
        # 加载动画、位置、大小
        self.image = self.state.animation.IMAGE
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # 实例化物理组件
        self.physics = physics.Physics(None, self.rect, gravity=1.5, jump_power=-40)
        # 实例化健康值组件
        self.health = health.Health(self, 200)

        # 状态计时器
        self.state_timer = 0
        # 状态持续时间
        self.state_duration = random.randint(IDLE_DURATION_MIN, IDLE_DURATION_MAX)
        # 小计时器
        self.timer = 0

        # 传入玩家
        self.player = player

        # 像素碰撞mask
        self.mask = None


    def take_damage(self):
        self.health.take_damage(10)
        if not self.health.alive:
            self.change_state(DeathState)


    def update_facing(self):
        if not self.player:
            return

        # 判断玩家位置
        P_x = self.player.rect.x

        # 确定新朝向
        new_facing = 'R' if P_x > self.rect.x else 'L'

        if self.facing != new_facing:
            self.facing = new_facing
            self.state.facing = self.facing

            self.state.animation.change_facing(self.facing)


    def fight(self):
        self.state_timer += 1

        # 待机状态切换攻击状态
        if isinstance(self.state, IdleState):
            if self.state_timer >= self.state_duration:
                # 随即状态选择
                random_state = random.choice([RushState, JumpState])
                self.change_state(random_state)

        # 攻击状态切换待机
        if isinstance(self.state, (RushState, JumpState)):
            if self.state_timer >= self.state_duration:
                self.change_state(IdleState)


    def change_state(self, state):
        if isinstance(self.state, state):
            return
        # 切换状态
        self.state = state(self, self.state.facing)

        # 重置计时器
        self.state_timer = 0
        self.timer = 0
        if isinstance(self.state, IdleState):
            self.state_duration = random.randint(IDLE_DURATION_MIN, IDLE_DURATION_MAX)
        if isinstance(self.state, RushState):
            self.state_duration = RUSH_DURATION


    def update(self):
        # 应用物理更新
        self.physics.apply_gravity()
        self.physics.update_position()
        # 健康值更新
        self.health.update()

        # 如果死亡则跳过朝向更新和AI逻辑，只更新死亡动画
        if not self.health.alive:
            if not isinstance(self.state, DeathState):
                self.change_state(DeathState)
            # 只更新死亡状态的动画
            self.state.update()
            self.image = self.state.animation.IMAGE
            return

        # 更新朝向
        self.update_facing()
        # 战斗AI
        self.fight()
        # 更新状态动画
        self.state.update()
        self.image = self.state.animation.IMAGE

        # 创建像素碰撞mask
        self.mask = pygame.mask.from_surface(self.image)



class IdleState(State):
    def __init__(self, enemy, facing):
        super().__init__(enemy, facing)

        self.image = pygame.image.load('assets/images/Enemy/IDLE.png').convert_alpha()
        self.animation = animation.Animation(None, self.image, 8, self.facing)

    def update(self):
        self.animation.update()



class RushState(State):
    def __init__(self, enemy, facing):
        super().__init__(enemy, facing)

        self.image = pygame.image.load('assets/images/Enemy/RUSH.png').convert_alpha()
        self.animation = animation.Animation(None, self.image, 6, self.facing, loop=False)
        # 冲刺朝向
        self.rush_dir = 1 if facing == 'R' else -1

    def update(self):
        self.animation.update()
        self.enemy.timer += 1
        if self.enemy.timer >= 35:
            # 根据facing决定冲刺方向
            v = 30
            self.enemy.rect.x += v * self.rush_dir
            # 边界检测
            if self.enemy.rect.x < 0:
                self.enemy.rect.x = 0
            if self.enemy.rect.x > 1500:
                self.enemy.rect.x = 1500



class JumpState(State):
    def __init__(self, enemy, facing):
        super().__init__(enemy, facing)

        self.image = pygame.image.load('assets/images/Enemy/JUMP.png').convert_alpha()
        self.animation = animation.Animation(None, self.image, 2, self.facing)

    def update(self):
        # 跳跃
        self.enemy.physics.jump()

        # 移动速度
        v = 30
        # 获取玩家位置
        P_x = self.enemy.player.rect.x
        # 上升时移动
        if self.enemy.physics.vy < 0:
            # 判断玩家位置
            if P_x > self.enemy.rect.x:
                self.enemy.rect.x += v
            if P_x < self.enemy.rect.x:
                self.enemy.rect.x -= v

        # 根据跳跃阶段切换动画
        if self.enemy.physics.vy < 0:
            target_index = 0
        else:
            target_index = 1

        if self.animation.index != target_index:
            self.animation.index = target_index
            self.animation.IMAGE = self.animation.image_list[target_index]



class DeathState(State):
    def __init__(self, enemy, facing):
        super().__init__(enemy, facing)

        self.image = pygame.image.load('assets/images/Enemy/DIE.png').convert_alpha()
        self.animation = animation.Animation(None, self.image, 1, self.facing, loop=False)

    def update(self):
        self.animation.update()



