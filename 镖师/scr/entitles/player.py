import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        # 加载图片
        self.image = pygame.image.load('assets/images/Player/STAND.png').convert_alpha()
        # 获取位置
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # 延迟播放图片
        self.delay = 7
        self.delay_count = 0
        self.index = 0

        # 初始状态
        self.current_state = 'STAND'
        self.image_list = []

        # 加载初始状态的图片
        self.change_state(self.current_state)

        # 移速
        self.speed = 15
        # 跳跃相关属性
        self.vy = 0
        self.gravity = 4
        self.jump_power = -50
        self.on_ground = False


    def change_state(self, new_state):
        # 切换状态并重新加载对应的图片帧
        if new_state == self.current_state:
            return

        # 保存当前坐标
        old_x = self.rect.x
        old_y = self.rect.y

        self.current_state = new_state
        filename = new_state + '.png'
        path = 'assets/images/Player/' + filename
        sprite_sheet = pygame.image.load(path).convert_alpha()

        # 切换状态
        if new_state == 'STAND':
            self.image_list = [sprite_sheet]
        elif new_state == 'R_WALK':
            self.image_list = [sprite_sheet.subsurface(112 * (i + 2), 0, 112, 184) for i in range(8)]
        else:
            self.image_list = [sprite_sheet]

        # 重置索引和图片
        self.index = 0
        self.image = self.image_list[self.index]

        # 更新矩形大小以匹配新图片
        self.rect = self.image.get_rect()
        self.rect.x = old_x
        self.rect.y = old_y


    def update(self, events):
        # 延迟动画帧，只有当帧数大于 1 时才进行动画播放逻辑
        if len(self.image_list) > 1:
            self.delay_count += 1
            if self.delay_count >= self.delay:
                self.index += 1
                if self.index >= len(self.image_list):
                    self.index = 0
                self.image = self.image_list[self.index]
                self.delay_count = 0

        # 获取按住按键事件
        keys = pygame.key.get_pressed()

        # 判断是否移动中
        is_moving = False

        # 按下A键向左移动
        if keys[pygame.K_a]:
            is_moving = True
            self.rect.x -= self.speed
            if self.rect.x < 0:
                self.rect.x = 0
        # 按下D键向右移动
        if keys[pygame.K_d]:
            is_moving = True
            self.change_state('R_WALK')
            self.rect.x += self.speed
            if self.rect.x > 1707 - self.rect.width:
                self.rect.x = 1707 - self.rect.width

        if not is_moving and self.current_state != 'STAND':
            self.change_state('STAND')



        # 跳跃输入
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and self.on_ground:
                    self.vy = self.jump_power
                    self.on_ground = False


        # 应用重力
        self.vy += self.gravity
        self.rect.y += self.vy

        # 检测是否在地面
        if self.rect.bottom >= 750:
            self.rect.bottom = 750
            self.vy = 0
            self.on_ground = True
        else:
            self.on_ground = False



    def draw(self, screen):
        screen.blit(self.image, self.rect)



