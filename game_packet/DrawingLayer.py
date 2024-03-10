from . import pygame, IDraw


class DrawingLayer(IDraw):
    def draw_block(self, surface, color, x, y, width, height, border=0):
        rect = pygame.Rect(x, y, width, height)
        current_color = color if color else (255, 255, 255)
        pygame.draw.rect(surface, current_color, rect)
        if border > 0:
            pygame.draw.rect(surface, (155, 155, 155), rect, border)

    def draw_text(self, surface, text, font, color):
        text_surface = font.render(text, True, color)
        surface.blit(text_surface, (0, 0))

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