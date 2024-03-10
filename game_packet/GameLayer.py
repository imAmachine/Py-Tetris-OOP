from . import pygame, IGame


class GameLayer(IGame):
    def __init__(self, game) -> None:
        self.game = game

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.game.fg_move_left = True
                elif event.key == pygame.K_RIGHT:
                    self.game.fg_move_right = True
                elif event.key == pygame.K_z:
                    self.game.rotate_fg(False)
                elif event.key == pygame.K_x:
                    self.game.rotate_fg(True)
                elif event.key == pygame.K_SPACE:
                    self.game.drop_fg()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.game.fg_move_left = False
                elif event.key == pygame.K_RIGHT:
                    self.game.fg_move_right = False
        return True

    def game_loop(self):
        while self.game.running:
            self.game.running = self.process_events()
            self.game.update_state()
            self.game.drawing_engine.draw()
        pygame.quit()