import pygame

class Component:
    def __init__(self, onwer):
        self.owner = onwer
        self.enabled = True

    def start(self):
        '''所有组件更新时调用'''
        pass

    def update(self):
        '''每帧更新'''
        pass

    def destroy(self):
        '''组件销毁时调用'''
        pass



