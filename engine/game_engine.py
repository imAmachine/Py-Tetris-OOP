import copy
import time
from engine.game_objects import Tetromino
from game_packet.GameLayer import GameLayer


class TetrisGame:
    def __init__(self, drawing_engine, game_field):
        # Таймеры
        self.last_drop_time = time.time()
        self.drop_interval = 0.5
        self.last_move_time = time.time()
        self.move_interval = 0.1

        # Основные модули
        self.drawing_engine = drawing_engine
        self.game_layer = GameLayer(self)

        # Инициализация игрового поля
        self.field = game_field
        self.field.initialize_field()
        self.field_center = self.field.width // 2

        # Инициализация игровой фигуры
        self.current_fg, self.next_fg = None, None
        self.switch_figures()
        self.fg_moving_left = False
        self.fg_moving_right = False

        # Игровые переменные
        self.running = False
        self.paused = True

    def start_game(self):
        self.running = True
        self.drawing_engine.add_object(self.field)
        self.switch_figures()
        self.game_layer.game_loop()

    def switch_figures(self):
        self.drawing_engine.remove_object(self.current_fg) # удаление из отрисовки предыдущей фигуры
        self.drawing_engine.add_object(self.next_fg) # добавление на отрисовку следующей фигуры
        self.current_fg = self.next_fg
        if self.current_fg:
            self.current_fg.blocks = self.fg_to_fieldBlocks(self.current_fg)
        self.next_fg = Tetromino.get_random_tetromino()
        self.next_fg.set_pos(self.field_center - len(self.next_fg.shape[0]) // 2, 0)

    def move_fg(self, dx, dy):
        if not self.check_collision(self.current_fg, (dx, dy)):
            self.current_fg.move(dx, dy)
            self.current_fg.blocks = self.fg_to_fieldBlocks(self.current_fg)

    def rotate_fg(self, to_right=True):
        test_fg = copy.deepcopy(self.current_fg)
        test_fg.rotate(to_right)
        if not self.check_collision(test_fg):
            self.current_fg.rotate(to_right)
            self.current_fg.blocks = self.fg_to_fieldBlocks(self.current_fg)

    def drop_fg(self):
        while not self.check_collision(self.current_fg, (0, 1)):
            self.current_fg.move(0, 1)
        self.current_fg.blocks = self.fg_to_fieldBlocks(self.current_fg)

    def check_collision(self, fg, offset=(0, 0)):
        for y, row in enumerate(fg.shape):
            for x, cell in enumerate(row):
                if cell and not self.is_valid_position((fg.x + x + offset[0], fg.y + y + offset[1])):
                    return True
        return False

    def is_valid_position(self, pos):
        x, y = pos
        return 0 <= x < self.field.width and 0 <= y < self.field.height and not self.field[y][x].isFixed

    def fg_to_fieldBlocks(self, fg):
        """метод для получения объектов активной фигуры с игрового поля"""
        blocks = []
        for y, row in enumerate(fg.shape):
            for x, cell in enumerate(row):
                if cell:
                    block = self.field[y + fg.y][x + fg.x]
                    blocks.append(block)
        return blocks

    def check_lines(self):
        from_y, height = self.current_fg.y, len(self.current_fg.shape)
        lines_count = self.field.check_lines(from_y, height)
        return lines_count

    def update_state(self):
        if not self.paused:
            # таймер на вертикальное движение фигуры
            if time.time() - self.last_drop_time >= self.drop_interval:
                if not self.check_collision(self.current_fg, (0, 1)):
                    self.last_drop_time = time.time()
                    self.move_fg(0, 1)
                else:
                    self.last_drop_time = time.time()
                    self.current_fg.fix() # зафиксировать фигуру на поле
                    lines_count = self.check_lines() # проверить и убрать полные линии
                    self.switch_figures() # активировать следующую фигуру

            # таймер на горизонтальное движение фигуры
            if time.time() - self.last_move_time >= self.move_interval:
                if self.fg_moving_left:
                    self.move_fg(-1, 0)
                    self.last_move_time = time.time()
                elif self.fg_moving_right:
                    self.move_fg(1, 0)
                    self.last_move_time = time.time()