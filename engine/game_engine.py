import copy
import random
import time
from engine.game_objects import Tetromino
from game_packet.GameLayer import GameLayer


class TetrisGame:
    def __init__(self, drawing_engine, game_field):
        self.running = False
        self.last_drop_time = time.time()
        self.drop_interval = 0.5  # Фигура будет падать каждую секунду
        self.last_move_time = time.time()
        self.move_interval = 0.1

        # Основные модули
        self.drawing_engine = drawing_engine
        self.game_layer = GameLayer(self)

        # Инициализация игрового поля
        self.field = game_field
        self.field.initialize_field()

        # Инициализация игровой фигуры
        self.current_fg = None
        self.next_fg = self.create_random_fg()
        self.fg_move_left = False
        self.fg_move_right = False

    def check_gameOver(self):
        if self.check_collision(self.current_fg):
            self.running = False
            print("Game Over")

    def start_game(self):
        self.running = True
        self.drawing_engine.add_object(self.field)
        self.start_new_fg()
        self.game_layer.game_loop()

    def create_random_fg(self):
        choice = random.choice(list(Tetromino.SHAPES.keys()))
        fg = Tetromino(0, 0, choice)
        return fg

    def fieldBlocks_shift(self, to_idx):
        for idx in range(len(self.field)):
            self.field[idx - to_idx] = self.field[idx - 1 - to_idx]

    def delete_full_rows(self):
        for idx, row in enumerate(self.field[::-1]):
            if all(block.isFixed for block in row):
                self.fieldBlocks_shift(idx)

    def start_new_fg(self):
        if self.current_fg:
            self.drawing_engine.remove_object(self.current_fg)
        # Установка значений новой фигуры
        self.current_fg = self.next_fg
        self.current_fg.x = self.field.width // 2 - len(self.current_fg.shape[0]) // 2  # Установка начального положения фигуры
        self.current_fg.y = 0
        self.current_fg.blocks = self.fg_to_fieldBlocks(self.current_fg)

        self.drawing_engine.add_object(self.current_fg)
        self.next_fg = self.create_random_fg()
        self.delete_full_rows()
        self.check_gameOver()

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
        blocks = []
        for y, row in enumerate(fg.shape):
            for x, cell in enumerate(row):
                if cell:
                    block = self.field[y + fg.y][x + fg.x]
                    blocks.append(block)
        return blocks

    def update_state(self):
        # таймер на вертикальное движение фигуры
        if time.time() - self.last_drop_time >= self.drop_interval:
            if self.current_fg is None:
                self.start_new_fg()
            else:
                if not self.check_collision(self.current_fg, (0, 1)):
                    self.move_fg(0, 1)
                    self.last_drop_time = time.time()
                else:
                    self.current_fg.fix()
                    self.start_new_fg()

        # таймер на горизонтальное движение фигуры
        if time.time() - self.last_move_time >= self.move_interval:
            if self.fg_move_left:
                self.move_fg(-1, 0)
            if self.fg_move_right:
                self.move_fg(1, 0)
            self.last_move_time = time.time()