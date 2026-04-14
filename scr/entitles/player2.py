import pygame
from ..components import physics
from ..components import animation
from ..components import health
from ..components import music
from . import weapon
from .. import settings


class State:
    def __init__(self, player, facing):
        self.player = player
        self.facing = facing
        self.animation = None
        self.music = music.play_music()


    def enter(self):
        '''进入游戏时调用，用于初始化动画或重置变量'''
        pass

    def exit(self):
        '''退出状态时调用'''
        pass

    def handle_input(self, keys):
        '''处理按键事件'''
        if keys[pygame.K_l] and not keys[pygame.K_QUOTE]:
            if self.facing != 'L':
                self.facing = 'L'
                self.animation.change_facing(self.facing)
        if keys[pygame.K_QUOTE] and not keys[pygame.K_l]:
            if self.facing != 'R':
                self.facing = 'R'
                self.animation.change_facing(self.facing)

    def update(self):
        '''每帧更新逻辑，物理与动画帧等'''
        if self.animation:
            self.animation.update()





class Player2(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        # 加载图片、初始状态
        self.image = pygame.image.load('assets/images/Player/STAND.png').convert_alpha()
        # 获取位置
        self.rect = self.image.get_rect()       # midbottom=(x, y)
        self.rect.x = x
        self.rect.y = y

        # 实例化物理组件
        self.physics = physics.Physics(None, self.rect)
        # 实例化健康值组件
        self.health = health.Health(self, 100, 40, 5)

        # 初始动作状态（待机）
        self.state = IdleState(self, 'L')
        # 记录上一帧朝向
        self.last_facing = 'L'

        # 是否奔跑
        self.is_running = False

        # 连击相关变量
        self.in_combo_window = False  # 是否处于连击窗口期
        self.combo_window_timer = 0  # 连击窗口计时器
        self.COMBO_WINDOW_DURATION = 20  # 连击窗口持续时间（帧）

        # 强制状态
        self.forced_state = (Attack1State, Attack2State, DodgeState, HurtState, DeathState)

        # 添加挥砍精灵组
        self.strike_group = pygame.sprite.Group()

        # 玩家像素级碰撞mask
        self.mask = None

        # 玩家名字
        self.name = 'Player2'



    def change_state(self, new_state):
        '''切换状态'''
        # 判断是否为当前状态
        if isinstance(self.state, new_state):
            return

        current_facing = self.state.facing if hasattr(self.state, 'facing') else self.last_facing
        self.state = new_state(self, current_facing)


    def toggle_run_walk(self, events):
        # 切换奔跑状态
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RALT:
                    self.is_running = not self.is_running
        if self.is_running:
            self.physics.speed = 13
        else:
            self.physics.speed = 5


    def add_strike(self, stage):
        '''添加精灵进组'''
        strike = weapon.Strike(0, 0, stage, self.last_facing, self.rect)
        self.strike_group.add(strike)


    def check_take_damage(self):
        if self.health.hurt or self.health.is_defence_invincible:
            return

        # 受伤、死亡与闪避状态，不受攻击
        if isinstance(self.state, (HurtState, DeathState, DodgeState)):
            return

        # 防御状态韧性值检测
        if isinstance(self.state, DefendState):
            self.health.defended(10)

            if self.health.hurt:
                self.change_state(HurtState)
            return

        # 除以上状态外则受击
        self.health.take_damage(10)
        self.change_state(HurtState)




    def judge_state(self, events):
        keys = pygame.key.get_pressed()

        # 死亡
        if not self.health.alive:
            self.change_state(DeathState)
            return

        # 判断强制状态，若动画尚未播放完毕则不进行切换，即return
        if isinstance(self.state, self.forced_state):
            if not self.state.animation.finished:
                return

            # 攻击
            if isinstance(self.state, Attack1State):
                if not self.in_combo_window:
                    self.in_combo_window = True
                    self.combo_window_timer = 0

        # 处理连击窗口期逻辑
        if self.in_combo_window:
            self.combo_window_timer += 1
            # 超时退出窗口期
            if self.combo_window_timer > self.COMBO_WINDOW_DURATION:
                self.in_combo_window = False

        # 防御
        if isinstance(self.state, DefendState):
            if keys[pygame.K_DOWN]:
                return

        # 判断是否移动
        is_moving = (keys[pygame.K_l] and not keys[pygame.K_QUOTE]) or (keys[pygame.K_QUOTE] and not keys[pygame.K_l])
        # 切换奔跑状态
        self.toggle_run_walk(events)

        if self.physics.on_ground:
            if is_moving:
                if self.is_running:
                    self.change_state(RunState)
                else:
                    self.change_state(WalkState)
            else:
                self.change_state(IdleState)
        else:
            self.change_state(JumpState)


    def update(self, events):
        '''更新角色'''
        # 应用物理更新
        self.physics.apply_gravity()
        self.physics.update_position()
        # 健康值更新
        self.health.update()

        # 处理输入
        self.handle_input(events)

        # 判断切换动作状态
        self.judge_state(events)

        # 更新状态动画帧
        self.state.update()
        self.image = self.state.animation.IMAGE

        # 玩家像素级碰撞
        self.mask = pygame.mask.from_surface(self.image)

        # 更新挥砍
        self.strike_group.update()



    def handle_input(self, events):
        '''处理角色物理动作'''

        # 获取按键按住行为
        keys = pygame.key.get_pressed()

        # ================移动逻辑============

        # 非在地面的强制状态下 (即空中的强制状态亦可)
        if not (self.physics.on_ground and isinstance(self.state, (self.forced_state, DefendState))):
            if keys[pygame.K_l]:
                self.physics.move(-1)
                self.last_facing = 'L'
            if keys[pygame.K_QUOTE]:
                self.physics.move(1)
                self.last_facing = 'R'

            # 跳跃
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.physics.jump()
                        self.health.consume(10)

        # ============行为逻辑==============

        # 防御
        if keys[pygame.K_DOWN]:
            if not isinstance(self.state, self.forced_state):
                self.change_state(DefendState)

        for event in events:
            if event.type == pygame.KEYDOWN:
                # 攻击
                if event.key == pygame.K_LEFT:
                    # 如果当前不在强制状态与连击状态，发起第一段攻击
                    if not isinstance(self.state, self.forced_state) and not self.in_combo_window:
                        self.change_state(Attack1State)
                        # 添加挥砍精灵进组
                        self.add_strike(1)


                    # 如果当前处于连击窗口且非强制状态，允许发起第二段攻击
                    elif not isinstance(self.state, self.forced_state) and self.in_combo_window:
                        self.in_combo_window = False
                        self.change_state(Attack2State)
                        # 添加挥砍精灵进组
                        self.add_strike(2)

                # 翻滚
                if event.key == pygame.K_SEMICOLON:
                    if not isinstance(self.state, self.forced_state) and self.physics.on_ground:
                        self.change_state(DodgeState)
                        self.health.consume(10)



        # 处理状态输入
        self.state.handle_input(keys)




class IdleState(State):
    def __init__(self, player,  facing):
        super().__init__(player, facing)

        self.image = pygame.image.load('assets/images/Player/IDLE.png').convert_alpha()
        self.animation = animation.Animation(None, self.image, 8, self.facing)


    def update(self):
        self.animation.update()



class WalkState(State):
    def __init__(self, player, facing):
        super().__init__(player, facing)

        self.image = pygame.image.load('assets/images/Player/WALK.png').convert_alpha()
        self.animation = animation.Animation(None, self.image, 8, self.facing)


    def update(self):
        self.animation.update()



class JumpState(State):
    def __init__(self, player, facing):
        super().__init__(player, facing)

        self.image = pygame.image.load('assets/images/Player/JUMP.png').convert_alpha()
        self.animation = animation.Animation(None, self.image, 2, self.facing)


    def update(self):
        if self.player.physics.vy < 0:
            target_index = 0
        else:
            target_index = 1

        if self.animation.index != target_index:
            self.animation.index = target_index
            self.animation.IMAGE = self.animation.image_list[target_index]



class RunState(State):
    def __init__(self, player, facing):
        super().__init__(player, facing)

        self.image = pygame.image.load('assets/images/Player/RUN.png').convert_alpha()
        self.animation = animation.Animation(None, self.image, 6, self.facing)


    def update(self):
        self.animation.update()



class Attack1State(State):
    def __init__(self, player, facing):
        super().__init__(player, facing)

        self.image = pygame.image.load('assets/images/Player/ATTACK1.png').convert_alpha()
        self.animation = animation.Animation(None, self.image, 5, self.facing, loop=False)


    def handle_input(self, keys):
        pass


    def update(self):
        self.animation.update()



class Attack2State(State):
    def __init__(self, player, facing):
        super().__init__(player, facing)

        self.image = pygame.image.load('assets/images/Player/ATTACK2.png').convert_alpha()
        self.animation = animation.Animation(None, self.image, 5, self.facing, loop=False)

    def handle_input(self, keys):
        pass


    def update(self):
        self.animation.update()



class DefendState(State):
    def __init__(self, player, facing):
        super().__init__(player, facing)

        self.image = pygame.image.load('assets/images/Player/DEFEND.png').convert_alpha()
        self.animation = animation.Animation(None, self.image, 1, self.facing)

    def update(self):
        self.animation.update()



class DodgeState(State):
    def __init__(self, player, facing):
        super().__init__(player, facing)

        self.image = pygame.image.load('assets/images/Player/DODGE.png').convert_alpha()
        # loop=False 确保动画只播放一次
        self.animation = animation.Animation(None, self.image, 6, self.facing, loop=False)

        # 闪避相关参数
        self.dodge_speed = 10  # 恒定闪避速度，可根据手感调整

        # 记录初始朝向用于移动方向: L为-1, R为1
        self.move_direction = -1 if facing == 'L' else 1


    def handle_input(self, keys):
        pass


    def update(self):
        # 1. 更新动画
        self.animation.update()

        # 处理位移
        if not self.animation.finished:
            self.player.rect.x += self.dodge_speed * self.move_direction
            # 2. 边界检测
            if self.player.rect.left < 0:
                self.player.rect.left = 0
            if self.player.rect.right > settings.screen_width:
                self.player.rect.right = settings.screen_width



class HurtState(State):
    def __init__(self, player, facing):
        super().__init__(player, facing)

        self.image = pygame.image.load('assets/images/Player/HURT.png').convert_alpha()
        self.animation = animation.Animation(None, self.image, 4, self.facing, loop=False)


    def handle_input(self, keys):
        pass


    def update(self):
        self.animation.update()

        # 保存原速度
        original_speed = self.player.physics.speed
        # 受伤速度
        current_speed = 8
        self.player.physics.speed = current_speed
        # 根据面朝向向后退
        self.player.physics.move(1 if self.player.last_facing == 'L' else -1)
        # 恢复原速度
        self.player.physics.speed = original_speed
        # 删除挥砍精灵
        self.player.strike_group.empty()



class DeathState(State):
    def __init__(self, player, facing):
        super().__init__(player, facing)

        self.image = pygame.image.load('assets/images/Player/DIE.png').convert_alpha()
        self.animation = animation.Animation(None, self.image, 10, self.facing, loop=False)

    def handle_input(self, keys):
        pass

    def update(self):
        self.animation.update()





