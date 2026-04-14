import pygame
from . import component
from .. import settings

class Physics(component.Component):
    def __init__(self, owner, rect, gravity=2, jump_power=-37, speed=5):
        super().__init__(owner)

        # 获取owner的位置属性
        self.rect = rect
        # 移动速度
        self.vx = 0
        self.speed = speed
        # 跳跃相关属性
        self.vy = 0
        self.gravity = gravity
        self.jump_power = jump_power
        self.on_ground = False




    def apply_gravity(self):
        '''应用重力'''
        self.vy += self.gravity


    def update_position(self):
        '''更新垂直位置，地面检测'''
        self.rect.y += self.vy

        # 设地面750
        if self.rect.bottom >= 750:
            self.rect.bottom = 750
            self.vy = 0
            self.on_ground = True
        else:
            self.on_ground = False


    def jump(self):
        '''执行跳跃'''
        if self.on_ground:
            self.vy = self.jump_power
            self.on_ground = False


    def move(self, direction):
        '''水平移动'''
        self.vx = direction * self.speed
        self.rect.x += self.vx
        # 限制在屏幕内
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > settings.screen_width:
            self.rect.right = settings.screen_width











