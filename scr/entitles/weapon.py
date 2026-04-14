import pygame
from ..components import animation


class Strike(pygame.sprite.Sprite):
    def __init__(self, x, y, stage, facing, player_rect):
        super().__init__()
        # 加载图片
        self.image1 = pygame.image.load('assets/images/Player/STRIKE1.png').convert_alpha()
        self.image2 = pygame.image.load('assets/images/Player/STRIKE2.png').convert_alpha()
        # 选择图片
        self.current_image = self.image1 if stage == 1 else self.image2
        # 添加动画
        self.animation = animation.Animation(None, self.current_image, 5, facing, loop=False)
        self.image = self.animation.IMAGE
        # 图片位置
        self.rect = self.image.get_rect()
        # 缩小碰撞区域
        self.rect = self.rect.inflate(-10, -10)
        # 保存玩家rect
        self.player_rect = player_rect
        # 记录是否击中敌人
        self.hit_enemy = set()


    def register_hit(self, enemy):
        '''
        注册一个被击中的敌人
        如果是第一次击中返回True
        否则返回False
        '''
        if enemy not in self.hit_enemy:
            self.hit_enemy.add(enemy)
            return True
        return False


    def update(self):
        # 获取角色、挥砍宽度
        if self.player_rect:
            P_W = self.player_rect.width
            S_W = self.rect.width

            # 根据角色位置，更新位置
            if self.animation.facing == 'R':
                self.rect.x = self.player_rect.x + P_W
            else:
                self.rect.x = self.player_rect.x - S_W
            self.rect.y = self.player_rect.y

        # 更新动画
        self.animation.update()
        # 同步图像
        self.image = self.animation.IMAGE
        # 动画结束从组中删除自己
        if self.animation.finished:
            self.kill()



