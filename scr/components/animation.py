from . import component
import pygame



class Animation(component.Component):
    def __init__(self, owner, image, frames, facing, loop=True):
        super().__init__(owner)

        # 获取图片
        self.original_image = image
        # 图片方向
        self.facing = facing
        # 图片帧数
        self.frames = frames

        # 动画是否循环
        self.loop = loop

        # 延迟播放图片
        self.delay = 7
        self.delay_count = 0
        self.index = 0

        # 动画是否结束（攻击等一次性动作）
        self.finished = False

        # 初始化帧列表
        self.generate_frames()


    def generate_frames(self):
        W = self.original_image.get_width() / self.frames
        H = self.original_image.get_height()

        # 创建图片帧列表
        self.image_list = []

        for i in range(self.frames):
            frame = self.original_image.subsurface(W * i , 0, W, H)

            if self.facing == 'L':
                processed_frame = pygame.transform.flip(frame, True, False)
                self.image_list.append(processed_frame)
            else:
                self.image_list.append(frame)

        if self.image_list:
            self.IMAGE = self.image_list[self.index]
            self.finished = False   # 翻转时重置动画结束状态



    def change_facing(self, facing):
        if self.facing != facing:
            self.facing = facing
            self.index = 0
            self.generate_frames()



    def update(self):
        '''延迟更新动画'''
        if self.finished:
            return

        self.delay_count += 1
        if self.delay_count >= self.delay:
            self.index += 1
            if self.index >= self.frames:
                if self.loop:
                    self.index = 0
                else:
                    self.index = self.frames - 1   # 最后一帧
                    self.finished = True        # 停留
            else:
                self.delay_count = 0

            self.IMAGE = self.image_list[self.index]









