import pygame
from scr import settings
from .scenes import enter_scene




class Game:
    def __init__(self):
        pygame.init()
        # 实例化屏幕
        self.screen = settings.SCREEN
        # 创建时钟对象
        self.clock = pygame.time.Clock()
        # 开始界面为进入游戏界面
        self.scene = enter_scene.EnterGameScene()
        # 运行游戏
        self.running = True



    def run(self):
        # 屏幕刷新
        while self.running:
            # 获取事件
            events = pygame.event.get()
            # 监听事件 (只处理输入和退出)
            for event in events:
                # 关闭游戏
                if event.type == pygame.QUIT:
                    self.running = False


            # 处理场景事件
            self.scene.handle_events(events)

            # 检查是否需要切换场景
            if self.scene.next_scene:
                self.scene = self.scene.next_scene

            # 更新场景逻辑
            self.scene.update()

            # 绘制当前场景
            self.scene.draw(self.screen)

            # 屏幕刷新
            pygame.display.flip()
            self.clock.tick(settings.FPS)
