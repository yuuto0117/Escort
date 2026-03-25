import pygame


class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, font, font_color):
        # 按钮大小位置
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text        # 按钮文本
        self.color = color      # 按钮默认颜色
        self.hover_color = hover_color      # 按钮悬停颜色
        self.font = font        # 按钮字体
        self.font_color = font_color    # 按钮字体颜色
        self.is_hovered = False     # 鼠标是否悬停在按钮上
        self.is_pressed_inside = False      # 鼠标是否在按钮内按下

    def draw(self, screen):
        '''绘制按钮'''
        # 判断按钮颜色
        current_color = self.hover_color if self.is_hovered else self.color
        # 绘制按钮的矩形
        pygame.draw.rect(screen, current_color, self.rect)

        '''绘制文本'''
        # 创建文本
        text_surface = self.font.render(self.text, True, self.font_color)
        # 文本位置
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)    # 绘制文本

    def handle_events(self, event):
        # 鼠标移动时，判断是否悬停在按钮上
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)

        # 鼠标点击时
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:   # 鼠标左键
                self.is_pressed_inside = self.rect.collidepoint(event.pos)      # 返回T or F

        # 鼠标松开时
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if self.is_pressed_inside and self.rect.collidepoint(event.pos):
                    self.is_pressed_inside = False
                    return True
                else:
                    self.is_pressed_inside = False
        return False







