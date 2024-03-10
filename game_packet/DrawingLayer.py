from . import pygame, IDraw


class DrawingLayer(IDraw):
    def draw_block(self, surface, color, x, y, width, height, border=0):
        rect = pygame.Rect(x, y, width, height)
        current_color = color if color else (255, 255, 255)
        pygame.draw.rect(surface, current_color, rect)
        if border > 0:
            pygame.draw.rect(surface, (155, 155, 155), rect, border)

    def draw_text(self, surface, text, x, y, width, height, color, font_name):
        font_size = 100  # начальный размер шрифта
        font = pygame.font.Font(font_name, font_size)
        text_surface = font.render(text, True, color)
        text_width, text_height = text_surface.get_size()

        # уменьшаем размер шрифта, пока текст не влезет в заданный блок
        while text_width > width or text_height > height:
            font_size -= 1
            font = pygame.font.Font(font_name, font_size)
            text_surface = font.render(text, True, color)
            text_width, text_height = text_surface.get_size()

        # рисуем текст по центру заданного блока
        text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
        pygame.draw.rect(surface, (0, 255, 0), text_rect)
        surface.blit(text_surface, text_rect)

    def fill_screen(self, screen, color):
         screen.fill(color)

    def init_window(self, window_title, window_size):
        pygame.init()
        pygame.display.set_caption(window_title)
        surf = pygame.display.set_mode(window_size)
        return surf

    def display_update(self, rect=None):
        if rect:
            pygame.display.update(rect)
        else:
            pygame.display.flip()